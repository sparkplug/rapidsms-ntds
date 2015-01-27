
from django.dispatch import receiver

from settings import NTD_KEYWORDS
from rapidsms_xforms.models import xform_received
import datetime








def handle_parish(xform, submission, health_provider):
    from .utils import parse_location
    if (xform.keyword != 'par') or submission.has_errors:
        return

    p_eav=submission.eav.ntd_parish
    reporter=Reporter.objects.get(healthprovider_ptr=health_provider)
    parish=parse_location(p_eav,"parish")
    if not parish :
        submission.response = 'You are attempting to report for parish "{0}" which does not exist.'.format(submission.eav.ntd_parish)
        submission.has_errors = True
        submission.save()
    elif parish not in reporter.subcounty.get_children():
        submission.response = 'The parish "{0}" is not in your subcounty'.format(submission.eav.ntd_parish)
        submission.has_errors = True
        submission.save()



def update_report(report,xform):
    pass

def generate_report(xform, submission, health_provider):
    reporter=Reporter.objects.get(health_provider_ptr=health_provider)
    report=NTDReport.objects.get_or_create(reporter=reporter)

    return True

def default_constraint(xform, submission, health_provider):
    return True



def handle_parish(xform, submission, reporter):
    return True

def handle_villages_targeted(xform, submission, reporter):
    return True

def handle_schools_targeted(xform, submission, reporter):
    return True

def handle_treated(xform, submission, reporter):
    return True


def  handle_pop(xform, submission, reporter):
    return True


def  handle_drugs_used(xform, submission, reporter):
    return True


def handle_drugs_left(xform, submission, reporter):
    return True

xform_constraints={

    "ntd_parish":handle_parish,
"ntd_villages_targeted":handle_villages_targeted,
"ntd_schools_targeted":handle_schools_targeted,
"ntd_treated_by_age":handle_treated,
"ntd_village_pop_by_age":handle_pop,
"ntd_drugs_used":handle_drugs_used,
"ntd_drugs_left":handle_drugs_left


}


@receiver(xform_received)
def handle_submission(sender, **kwargs):
    from rapidsms_xforms.models import xform_received,XFormReport
    from .models import ReportProgress,Reporter,NTDReport
    xform = kwargs['xform']
    if not xform.keyword in NTD_KEYWORDS:
        return

    submission = kwargs['submission']
    if submission.has_errors:
        return

    try:

        health_provider = submission.connection.contact.healthproviderbase.healthprovider
    except:
        if xform.keyword in NTD_KEYWORDS:
            submission.response = "You must be a reporter for NTDS. Please register first before sending any information"
            submission.has_errors = True
            submission.save()
        return

    if not xform.keyword in ['par']:
        report_in_progress = ReportProgress.objects.filter(provider=health_provider,status=1)
        if not report_in_progress.exists():
            submission.response = "Please tell us what POW you are reporting for before submitting data."
            submission.has_errors = True
            submission.save()
            return

    if xform.keyword in  NTD_KEYWORDS and not (xform.keyword in ['par']):

        value_list = []
        for v in submission.eav.get_values().order_by('attribute__xformfield__order'):
            value_list.append("%s %d" % (v.attribute.name, v.value_int))
        if len(value_list) > 1:
            value_list[len(value_list) - 1] = " and %s" % value_list[len(value_list) - 1]
        health_provider.last_reporting_date = datetime.datetime.now().date()
        health_provider.save()
        try:
            health_provider.facility.last_reporting_date = datetime.datetime.now().date()
            health_provider.facility.save()
        except:
            pass
        submission.response = "You reported %s.If there is an error,please resend." % ','.join(value_list)
        submission.save()

    if not xform.keyword in ['par']:
        report_in_progress.xform_report.submissions.add(submission)
        report_in_progress.xform_report.save()  # i may not need this
        submission.save()
    else:
        ## 4. -> process constraints from the DB (pow handler)

        for c in XFormReport.objects.get(name='NTDs').constraints:
            # WARNING: I'm (intentionally) not catching KeyError exceptions so all constraints must exist
            xform_constraints.get(xform.keyword,default_constraint)(xform, submission, health_provider)

