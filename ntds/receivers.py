
from django.dispatch import receiver

from settings import NTD_KEYWORDS
from rapidsms_xforms.models import xform_received
import datetime
from django.contrib.auth.models import  Group
from django.db.models import F



def handle_parish(xform, submission, health_provider):
    from .utils import parse_location
    from .models import Reporter,ReportProgress,NTDReport
    p_eav=submission.eav.get_values()[0].value
    reporter=Reporter.objects.get(healthprovider_ptr=health_provider)
    parish=parse_location(p_eav,"parish")
    if not parish :
        submission.response = 'You are attempting to report for parish "{0}" which does not exist.'.format(p_eav)
        submission.has_errors = True
        submission.save()
    elif parish not in reporter.subcounty.children.all():
        submission.response = 'The parish "{0}" is not in your subcounty'.format(p_eav)
        submission.has_errors = True
        submission.save()
    else:
        invalid_d=datetime.datetime.now()-datetime.timedelta(days=365)
        prog=ReportProgress.objects.filter(parish=parish,updated__gt=invalid_d).order_by("-updated")

        if not prog:
            rep=NTDReport.objects.create(parish=parish)
            ReportProgress.objects.create(reporter=reporter,report=report,parish=parish,status=1)

        else:
            #force updated date change
            prog=prog[0]
            prog.save()



    return True




def update_report(report,xform):
    pass

def generate_report(xform, submission, health_provider):
    reporter=Reporter.objects.get(health_provider_ptr=health_provider)
    report=NTDReport.objects.get_or_create(reporter=reporter)

    return True

def default_constraint(xform, submission, health_provider):
    return True





def handle_villages_targeted(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.total_villages = int(values['Vilages in Parish'])
    report.villages_targeted = int(values['Vilages Targeted'])
    report.villages_treated = int(values['Vilages Treated'])
    report.villages_incomplete = int(values['Vilages Incomplete'] )
    report.save()
    return True

def handle_schools_targeted(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.total_schools = int(values['Schools in Parish'])
    report.schools_targeted = int(values['Schools Targeted'])
    report.schools_treated = int(values['Schools Treated'])
    report.schools_incomplete = int(values['Schools Incomplete'] )
    report.save()


    return True

def handle_treated(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.treated_lt_6_male = int(values['Treated Less Than 6 Months male'])
    report.treated_lt_6_female = int(values['Treated Less Than 6 Months female'])
    report.treated_6_to_4_male = int(values['Treated 6 Months to 4 years male'])
    report.treated_6_to_4_female = int(values['Treated 6 Months to 4 years female'])
    report.treated_4_to_14_male = int(values['Treated 5 to 14 male'])
    report.treated_4_to_14_female = int(values['Treated 5 to 14 female'])
    report.treated_gt_14_male = int(values['Treated greater than 15 male'])
    report.treated_gt_14_female = int(values['Treated greater than 15 female'])
    report.save()
    return True


def  handle_pop(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.pop_lt_6_male = int(values['Pop Less Than 6 Months male'])
    report.pop_lt_6_female = int(values['Pop Less Than 6 Months female'])
    report.pop_6_to_4_male = int(values['Pop 6 Months to 4 years male'])
    report.pop_6_to_4_female = int(values['Pop 6 Months to 4 years female'])
    report.pop_4_to_14_male = int(values['Pop 5 to 14 male'])
    report.pop_4_to_14_female = int(values['Pop 5 to 14 female'])
    report.pop_gt_14_male = int(values['Pop greater than 15 male'])
    report.pop_gt_14_female = int(values['Pop greater than 15 female'])
    report.save()
    return True



def handle_alb(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.alb = int(values["Alb Usage"])
    report.save()


    return True
def handle_ivm(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.ivm = int(values["Ivm Usage"])
    report.save()
    return True
def handle_pzq(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.pzq = int(values["PZQ Usage"])
    report.save()
    return True
def handle_mbd(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.mbd = int(values["MBD Usage"])
    report.save()
    return True
def handle_zitht(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.ttr = int(values["Tet Usage"])
    report.save()
    return True
def handle_ziths(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.ziths = int(values["Zith Syrup usage"])
    report.save()
    return True
def handle_tetra(xform, submission, reporter):
    from .models import ReportProgress
    values=submission.submission_values().values("attribute__name","value_text")
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.zitht = int(values["zith Tab Usage"])
    report.save()
    return True


keyword_handlers={

    "par":handle_parish,
"vlg":handle_villages_targeted,
"sch":handle_schools_targeted,
"agg":handle_treated,
"pop":handle_pop,
"alb":handle_alb,
"ivm":handle_ivm,
"pzq":handle_pzq,
"mbd":handle_mbd,
"ziths":handle_ziths,
"zitht":handle_zitht,
    "ttr":handle_tetra






}




@receiver(xform_received)
def handle_submission(sender, **kwargs):
    from rapidsms_xforms.models import xform_received,XFormReport
    from .models import ReportProgress,Reporter,NTDReport
    xform = kwargs['xform']
    if not xform.keyword in NTD_KEYWORDS:
        return

    submission = kwargs['submission']
    role=Group.objects.get(name="Ntds")
    # manually check restrict to



    if submission.has_errors:
        return

    try:

        health_provider = submission.connection.contact.healthproviderbase.healthprovider
        reporter = Reporter.objects.get(healthprovider_ptr=health_provider)
        if not role in reporter.groups.all():
            submission.response = "You must be a reporter for NTDS"
            submission.has_errors = True
            submission.save()


    except:

        submission.response = "You must be a reporter for NTDS"
        submission.has_errors = True
        submission.save()
        return



    if xform.keyword in ['par']:
        return handle_parish(xform, submission, health_provider)


    else:
        report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-created")[0]
        if not report_in_progress.exists():
            submission.response = "Please tell us what POW you are reporting for before submitting data."
            submission.has_errors = True
            submission.save()
            return





    if xform.keyword in  NTD_KEYWORDS:
        keyword_handlers["xform.keyword"](xform, submission, health_provider)

        value_list = []

        for v in submission.eav.get_values().order_by('attribute__xformfield__order'):
            value_list.append("%s %s" % (v.attribute.name, v.value))
        if len(value_list) > 1:
            value_list[len(value_list) - 1] = " and %s" % value_list[len(value_list) - 1]
        health_provider.last_reporting_date = datetime.datetime.now().date()
        health_provider.save()

        submission.response = "You reported %s.If there is an error,please resend." % ','.join(value_list)
        submission.save()
        return
