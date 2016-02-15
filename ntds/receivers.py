
from django.dispatch import receiver

from settings import NTD_KEYWORDS
from rapidsms_xforms.models import xform_received
import datetime
from django.contrib.auth.models import  Group
from django.db.models import F
from .utils import parse_location
from .models import Reporter,ReportProgress,NTDReport,NtdLocation
import json
from django.db import transaction



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
            report=NTDReport.objects.create(reporter=reporter)
            ReportProgress.objects.create(reporter=reporter,report=report,parish=parish,status=1)

        else:
            #force updated date change
            prog=prog[0]
            prog.save()



    return True


def pivot_dicts(dict_list):
    toret={}
    for d in dict_list:
        dd={d["attribute__name"]:d["value_text"]}
        toret.update(dd)

    return toret

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
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
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
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
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
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
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
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
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





def  handle_pop_fil(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]



    report=report_in_progress.report
    report.pop_u_5_male_fil = int(values['Pop Under 5 male'])
    report.pop_u_5_female_fil = int(values['Pop Under 5 female'])
    report.pop_4_to_14_male_fil = int(values['Pop 5 to 14 male'])
    report.pop_4_to_14_female_fil = int(values['Pop 5 to 14 female'])
    report.pop_gt_14_male_fil = int(values['Pop greater than 15 male'])
    report.pop_gt_14_female_fil = int(values['Pop greater than 15 female'])
    report.save()
    return True





def handle_treated_fil(xform, submission, health_provider):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    reporter=Reporter.objects.get(healthprovider_ptr=health_provider)
    try:
        report=NTDReport.objects.create(reporter=reporter)
        report.message=submission.message.text
        report.raw = json.dumps(values)
        report.disease="Helminthiasis"
        report.number_of_communities_fil = int(values['No of communities and schools'])
        report.treated_lt_6_male_fil = int(values['Treated Less Than 6 Months male'])
        report.treated_lt_6_female_fil = int(values['Treated Less Than 6 Months female'])
        report.treated_6_to_4_male_fil = int(values['Treated 6 Months to 4 years male'])
        report.treated_6_to_4_female_fil = int(values['Treated 6 Months to 4 years female'])
        report.treated_4_to_14_male_fil = int(values['Treated 5 to 14 male'])
        report.treated_4_to_14_female_fil = int(values['Treated 5 to 14 female'])
        report.treated_gt_14_male_fil = int(values['Treated greater than 15 male'])
        report.treated_gt_14_female_fil = int(values['Treated greater than 15 female'])
        report.filariasis=int(values['Treated 6 Months to 4 years female'])+int(values['Treated 6 Months to 4 years male'])+int(values['Treated Less Than 6 Months male'])+int(values['Treated Less Than 6 Months female'])+int(values['Treated 5 to 14 male'])+int(values['Treated 5 to 14 female'])+int(values['Treated greater than 15 male'])+int(values['Treated greater than 15 female'])
        report.save()

    except KeyError:
        submission.response="Your report Is incomplete.Please Resubmit"
        submission.has_errors=True
        submission.save()

    return True


def  handle_pop_trac(xform, submission, health_provider):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report=NTDReport.objects.create(reporter=reporter)
    report.message=submission.message.text
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.pop_lt_6_male_trac = int(values['Pop Less Than 6 Months male'])
    report.pop_lt_6_female_trac = int(values['Pop Less Than 6 Months female'])
    report.pop_6_to_4_male_trac = int(values['Pop 6 Months to 4 years male'])
    report.pop_6_to_4_female_trac = int(values['Pop 6 Months to 4 years female'])
    report.pop_4_to_14_male_trac = int(values['Pop 5 to 14 male'])
    report.pop_4_to_14_female_trac = int(values['Pop 5 to 14 female'])
    report.pop_gt_14_male_trac = int(values['Pop greater than 15 male'])
    report.pop_gt_14_female_trac = int(values['Pop greater than 15 female'])
    report.save()
    return True

def handle_treated_trac(xform, submission, health_provider):
    from .models import ReportProgress,NtdLocation
    values_list=submission.submission_values().values("attribute__name","value_text")
    try:
        reporter=Reporter.objects.get(healthprovider_ptr=health_provider)

        values=pivot_dicts(values_list)
        reportNTDReport.objects.create(reporter=reporter)
        report.raw = json.dumps(values)
        report.disease="Trachoma"
        report.message=submission.message.text
        report.number_of_communities_trac = int(values['No of communities and schools'])
        report.treated_lt_6_male_trac = int(values['Treated Less Than 6 Months male'])
        report.treated_lt_6_female_trac = int(values['Treated Less Than 6 Months female'])
        report.treated_6_to_4_male_trac = int(values['Treated 6 Months to 4 years male'])
        report.treated_6_to_4_female_trac = int(values['Treated 6 Months to 4 years female'])
        report.treated_4_to_14_male_trac = int(values['Treated 5 to 14 male'])
        report.treated_4_to_14_female_trac = int(values['Treated 5 to 14 female'])
        report.treated_gt_14_male_trac = int(values['Treated greater than 15 male'])
        report.treated_gt_14_female_trac = int(values['Treated greater than 15 female'])
        report.trachoma=int(values['Treated 6 Months to 4 years female'])+int(values['Treated 6 Months to 4 years male'])+int(values['Treated Less Than 6 Months male'])+int(values['Treated Less Than 6 Months female'])+int(values['Treated 5 to 14 male'])+int(values['Treated 5 to 14 female'])+int(values['Treated greater than 15 male'])+int(values['Treated greater than 15 female'])
        report.save()
    except KeyError:
        submission.response="Your report Is incomplete.Please Resubmit"
        submission.has_errors=True
        submission.save()
    return True

def  handle_pop_lyf(xform, submission, health_provider):
    from .models import ReportProgress,NtdLocation
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    reporter=Reporter.objects.get(healthprovider_ptr=health_provider)
    report.pop_u_5_male_lyf = int(values['Pop Under 5 male'])
    report.pop_u_5_female_lyf = int(values['Pop Under 5 female'])
    report.pop_4_to_14_male_lyf = int(values['Pop 5 to 14 male'])
    report.pop_4_to_14_female_lyf = int(values['Pop 5 to 14 female'])
    report.pop_gt_14_male_lyf = int(values['Pop greater than 15 male'])
    report.pop_gt_14_female_lyf = int(values['Pop greater than 15 female'])
    report.save()
    return True


def handle_treated_lyf(xform, submission, health_provider):
    from .models import ReportProgress

    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    reporter=Reporter.objects.get(healthprovider_ptr=health_provider)
    try:
        report=NTDReport.objects.create(reporter=reporter)
        report.message=submission.message.text
        report.raw = json.dumps(values)
        report.disease="Lympatic"
        report.number_of_communities_lyf = int(values['No of communities and schools'])
        report.treated_lt_6_male_lyf = int(values['Treated Less Than 6 Months male'])
        report.treated_lt_6_female_lyf = int(values['Treated Less Than 6 Months female'])
        report.treated_6_to_4_male_lyf = int(values['Treated 6 Months to 4 years male'])
        report.treated_6_to_4_female_lyf = int(values['Treated 6 Months to 4 years female'])
        report.treated_4_to_14_male_lyf = int(values['Treated 5 to 14 male'])
        report.treated_4_to_14_female_lyf = int(values['Treated 5 to 14 female'])
        report.treated_gt_14_male_lyf = int(values['Treated greater than 15 male'])
        report.treated_gt_14_female_lyf = int(values['Treated greater than 15 female'])
        report.lymphatic=int(values['Treated 6 Months to 4 years female'])+int(values['Treated 6 Months to 4 years male'])+int(values['Treated Less Than 6 Months male'])+int(values['Treated Less Than 6 Months female'])+int(values['Treated 5 to 14 male'])+int(values['Treated 5 to 14 female'])+int(values['Treated greater than 15 male'])+int(values['Treated greater than 15 female'])
        report.save()
    except KeyError:
        submission.response="Your report Is incomplete.Please Resubmit"
        submission.has_errors=True
        submission.save()
    return True

def  handle_pop_hel(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.pop_u_5_male_hel = int(values['Pop Under 5 male'])
    report.pop_u_5_female_hel = int(values['Pop Under 5 female'])
    report.pop_4_to_14_male_hel = int(values['Pop 5 to 14 male'])
    report.pop_4_to_14_female_hel = int(values['Pop 5 to 14 female'])
    report.pop_gt_14_male_hel = int(values['Pop greater than 15 male'])
    report.pop_gt_14_female_hel = int(values['Pop greater than 15 female'])
    report.save()
    return True

def handle_treated_hel(xform, submission, health_provider):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    reporter=Reporter.objects.get(healthprovider_ptr=health_provider)

    try:
        report.message=submission.message.text
        report=NTDReport.objects.create(reporter=reporter)
        report.raw = json.dumps(values)
        report.disease="Helminthiasis"
        report.number_of_communities_hel = int(values['No of communities and schools'])
        report.treated_lt_6_male_hel = int(values['Treated Less Than 6 Months male'])
        report.treated_lt_6_female_hel = int(values['Treated Less Than 6 Months female'])
        report.treated_6_to_4_male_hel = int(values['Treated 6 Months to 4 years male'])
        report.treated_6_to_4_female_hel = int(values['Treated 6 Months to 4 years female'])
        report.treated_4_to_14_male_hel = int(values['Treated 5 to 14 male'])
        report.treated_4_to_14_female_hel = int(values['Treated 5 to 14 female'])
        report.treated_gt_14_male_hel = int(values['Treated greater than 15 male'])
        report.treated_gt_14_female_hel = int(values['Treated greater than 15 female'])
        report.helminthiasis=int(values['Treated 6 Months to 4 years female'])+int(values['Treated 6 Months to 4 years male'])+int(values['Treated Less Than 6 Months male'])+int(values['Treated Less Than 6 Months female'])+int(values['Treated 5 to 14 male'])+int(values['Treated 5 to 14 female'])+int(values['Treated greater than 15 male'])+int(values['Treated greater than 15 female'])
        report.save()
    except KeyError:
        submission.response="Your report Is incomplete.Please Resubmit"
        submission.has_errors=True
        submission.save()

    return True

def  handle_pop_schi(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.pop_u_5_male_schi = int(values['Pop Under 5 male'])
    report.pop_u_5_female_schi = int(values['Pop Under 5 female'])
    report.pop_4_to_14_male_schi = int(values['Pop 5 to 14 male'])
    report.pop_4_to_14_female_schi = int(values['Pop 5 to 14 female'])
    report.pop_gt_14_male_schi = int(values['Pop greater than 15 male'])
    report.pop_gt_14_female_schi = int(values['Pop greater than 15 female'])

    report.save()
    return True

def handle_treated_schi(xform, submission, health_provider):

    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    reporter=Reporter.objects.get(healthprovider_ptr=health_provider)

    try:
        report=NTDReport.objects.create(reporter=reporter)
        report.raw = json.dumps(values)
        report.disease="Schistosomiasis"
        report.number_of_communities_schi = int(values['No of communities and schools'])
        report.message=submission.message.text
        report.treated_lt_6_male_schi = int(values['Treated Less Than 6 Months male'])
        report.treated_lt_6_female_schi = int(values['Treated Less Than 6 Months female'])
        report.treated_6_to_4_male_schi = int(values['Treated 6 Months to 4 years male'])
        report.treated_6_to_4_female_schi = int(values['Treated 6 Months to 4 years female'])
        report.treated_4_to_14_male_schi = int(values['Treated 5 to 14 male'])
        report.treated_4_to_14_female_schi = int(values['Treated 5 to 14 female'])
        report.treated_gt_14_male_schi = int(values['Treated greater than 15 male'])
        report.treated_gt_14_female_schi = int(values['Treated greater than 15 female'])
        report.schistosomiasis=int(values['Treated 6 Months to 4 years female'])+int(values['Treated 6 Months to 4 years male'])+int(values['Treated Less Than 6 Months male'])+int(values['Treated Less Than 6 Months female'])+int(values['Treated 5 to 14 male'])+int(values['Treated 5 to 14 female'])+int(values['Treated greater than 15 male'])+int(values['Treated greater than 15 female'])
        report.save()
    except KeyError:
        submission.response="Your report Is incomplete.Please Resubmit"
        submission.has_errors=True
        submission.save()

    return True

def  handle_pop_onch(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.pop_u_5_male_onch = int(values['Pop Under 5 male'])
    report.pop_u_5_female_onch = int(values['Pop Under 5 female'])
    report.pop_4_to_14_male_onch = int(values['Pop 5 to 14 male'])
    report.pop_4_to_14_female_onch = int(values['Pop 5 to 14 female'])
    report.pop_gt_14_male_onch = int(values['Pop greater than 15 male'])
    report.pop_gt_14_female_onch = int(values['Pop greater than 15 female'])
    report.save()
    return True


def handle_treated_onch(xform, submission, health_provider):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    reporter=Reporter.objects.get(healthprovider_ptr=health_provider)
    try:
        report=NTDReport.objects.create(reporter=reporter)
        report.message=submission.message.text
        report.raw = json.dumps(values)
        report.disease="Onchocerciasis"
        report.number_of_communities_onch = int(values['No of communities and schools'])
        report.treated_lt_6_male_onch = int(values['Treated Less Than 6 Months male'])
        report.treated_lt_6_female_onch = int(values['Treated Less Than 6 Months female'])
        report.treated_6_to_4_male_onch = int(values['Treated 6 Months to 4 years male'])
        report.treated_6_to_4_female_onch = int(values['Treated 6 Months to 4 years female'])
        report.treated_4_to_14_male_onch = int(values['Treated 5 to 14 male'])
        report.treated_4_to_14_female_onch = int(values['Treated 5 to 14 female'])
        report.treated_gt_14_male_onch = int(values['Treated greater than 15 male'])
        report.treated_gt_14_female_onch = int(values['Treated greater than 15 female'])
        report.onchocerciasis=int(values['Treated 6 Months to 4 years female'])+int(values['Treated 6 Months to 4 years male'])+int(values['Treated Less Than 6 Months male'])+int(values['Treated Less Than 6 Months female'])+int(values['Treated 5 to 14 male'])+int(values['Treated 5 to 14 female'])+int(values['Treated greater than 15 male'])+int(values['Treated greater than 15 female'])
        report.save()
        return (xform, submission, reporter,False)
    except KeyError:
        submission.response="Your report Is incomplete.Please Resubmit"
        submission.has_errors=True
        submission.save()

    return (xform, submission, reporter,False)




def handle_alb(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.alb_used = int(values["alb used"])
    report.alb_received = int(values["alb received"])
    report.alb_wasted = int(values["alb wasted"])
    report.alb_left = int(values["alb received"]) - int(values["alb wasted"]) - int(values["alb used"])
    #report.lymphatic = F('lymphatic') + int(values["alb_used"])
    report.save()
    return True

def handle_ivm(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.ivm_used = int(values["ivm used"])
    report.ivm_received = int(values["ivm received"])
    report.ivm_wasted = int(values["ivm wasted"])
    report.ivm_left = int(values["ivm received"]) - int(values["ivm wasted"]) - int(values["ivm used"])
    #report.lymphatic = F('lymphatic') + int(values["ivm_used"])
    report.save()
    return True

def handle_pzq(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.pzq_used = int(values["pzq used"])
    report.pzq_received = int(values["pzq received"])
    report.pzq_wasted = int(values["pzq wasted"])
    report.pzq_left = int(values["pzq received"]) - int(values["pzq wasted"]) - int(values["pzq used"])
    #report.schistosomiasis = int(values["pzq_used"])
    report.save()
    return True

def handle_mbd(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.mbd_used = int(values["mbd used"])
    report.mbd_received = int(values["mbd received"])
    report.mbd_wasted = int(values["mbd wasted"])
    report.mbd_left = int(values["mbd received"]) - int(values["mbd wasted"]) - int(values["mbd used"])
    report.save()
    return True

def handle_ttr(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.ttr_used = int(values["tet used"])
    report.ttr_wasted = int(values["tet wasted"])
    report.ttr_received = int(values["tet received"])
    report.ttr_left = int(values["ttr received"]) - int(values["ttr wasted"]) - int(values["ttr used"])
    #report.trachoma = F('trachoma') + int(values["tet_used"])
    report.save()
    return True

def handle_ziths(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.ziths_used = int(values["ziths used"])
    report.ziths_received = int(values["ziths received"])
    report.ziths_wasted = int(values["ziths wasted"])
    report.ziths_left = int(values["ziths received"]) - int(values["ziths wasted"]) - int(values["ziths used"])
    #report.trachoma = F('trachoma') + int(values["ziths_used"])
    report.save()
    return True

def handle_zitht(xform, submission, reporter):
    from .models import ReportProgress
    values_list=submission.submission_values().values("attribute__name","value_text")
    values=pivot_dicts(values_list)
    report_in_progress = ReportProgress.objects.filter(reporter=reporter,status=1).order_by("-updated")[0]
    report=report_in_progress.report
    report.zitht_used = int(values["zitht used"])
    report.zitht_received = int(values["zitht received"])
    report.zitht_wasted = int(values["zitht wasted"])
    report.zitht_left = int(values["zitht received"]) - int(values["zitht wasted"]) - int(values["zitht used"])
    #report.trachoma = F('trachoma') + int(values["zitht_used"])
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
            "ttr":handle_ttr,
            'st':handle_treated_fil,
            'tr':handle_treated_trac,
            'lf':handle_treated_lyf,
            'hel':handle_treated_hel,
            'sc':handle_treated_schi,
            'ov':handle_treated_onch,
            'pst':handle_pop_fil,
            'pt':handle_pop_trac,
            'plf':handle_pop_lyf,
            'phel':handle_pop_hel,
            'psc':handle_pop_schi,
            'pov':handle_pop_onch

            }




@receiver(xform_received)
def handle_submission(sender, **kwargs):

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




    if xform.keyword in  NTD_KEYWORDS:
        keyword_handlers[xform.keyword](xform, submission, health_provider)


        value_list = []
        if not submission.has_errors:
            for v in submission.eav.get_values().order_by('attribute__xformfield__order'):
                value_list.append("%s %s" % (v.attribute.name, v.value))
            if len(value_list) > 1:
                value_list[len(value_list) - 1] = " and %s" % value_list[len(value_list) - 1]
            health_provider.last_reporting_date = datetime.datetime.now().date()
            health_provider.save()

            submission.response = "You reported %s.If there is an error,please resend." % ','.join(value_list)
            submission.save()
        return
