import os
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.conf import settings
from rapidsms_xforms.models import XForm, XFormSubmission
from django.http import HttpResponseRedirect
from generic.views import generic
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from ntds.models import NTDReport, Reporter
from django.db.models import Sum
from rapidsms.contrib.locations.models import Location
from skipdict import SkipDict

from generic.views import generic
from generic.sorters import SimpleSorter
from .forms import *
from rapidsms_httprouter.models import Message
from .utils import get_all_children, JSONResponse, parse_mobile, empty
from uganda_common.utils import assign_backend
from django.contrib.auth.models import Group
from healthmodels.models.HealthProvider import HealthProvider
from rapidsms.models import Connection, Contact
from openpyxl.workbook import Workbook
from openpyxl.reader.excel import load_workbook
from django.db.models import F


def get_prevelance(reports, loc_qs, pdata, ldata):
    toret = {}
    for d in reports:
        loc = Location.objects.get(pk=d.pop(loc_qs))
        v_dict = SkipDict(d)
        pdata[str(loc.name).upper()] = v_dict.values()[-1]
        ldata[str(loc.name).upper()] = v_dict.keys()[-1].split("__")[0]


def dashboard(request):
    bubbles_to_ret = []
    district_pdata = {}
    district_ldata = {}
    subcounty_pdata = {}
    subcounty_ldata = {}
    parish_pdata = {}
    parish_ldata = {}
    report_ds = NTDReport.objects.values("reporter__district", "trachoma", "helminthiasis", "schistosomiasis",
                                         "onchocerciasis", "filariasis", "lymphatic").annotate(Sum("lymphatic"),
                                                                                               Sum("filariasis"),
                                                                                               Sum("onchocerciasis"),
                                                                                               Sum("schistosomiasis"),
                                                                                               Sum("trachoma"),
                                                                                               Sum("helminthiasis"))

    report_pa = NTDReport.objects.values("reporter__location", "trachoma", "helminthiasis", "schistosomiasis",
                                         "onchocerciasis", "filariasis", "lymphatic").annotate(Sum("lymphatic"),
                                                                                               Sum("filariasis"),
                                                                                               Sum("onchocerciasis"),
                                                                                               Sum("schistosomiasis"),
                                                                                               Sum("trachoma"),
                                                                                               Sum("helminthiasis"))

    report_sub = NTDReport.objects.values("reporter__subcounty", "trachoma", "helminthiasis", "schistosomiasis",
                                          "onchocerciasis", "filariasis", "lymphatic").annotate(Sum("lymphatic"),
                                                                                                Sum("filariasis"),
                                                                                                Sum("onchocerciasis"),
                                                                                                Sum("schistosomiasis"),
                                                                                                Sum("trachoma"),
                                                                                                Sum("helminthiasis"))

    get_prevelance(report_ds, "reporter__district", district_pdata, district_ldata)
    get_prevelance(report_pa, "reporter__location", parish_pdata, parish_ldata)
    get_prevelance(report_sub, "reporter__subcounty", subcounty_pdata, subcounty_ldata)

    context = {

        'bubbles_to_ret': mark_safe(bubbles_to_ret),
        'district_pdata': mark_safe(district_pdata),
        'district_ldata': mark_safe(district_ldata),
        'parish_pdata': mark_safe(parish_pdata),
        'parish_ldata': mark_safe(parish_ldata),
        'subcounty_pdata': mark_safe(subcounty_pdata),
        'subcounty_ldata': mark_safe(subcounty_ldata),

    }
    return render_to_response("ntds/dashboard.html", context, context_instance=RequestContext(request))


def view_diseases(request):
    bubbles_to_ret = []
    pdata = {}
    ldata = {}
    report_q = NTDReport.objects.values("trachoma", "helminthiasis", "schistosomiasis",
                                        "onchocerciasis", "filariasis", "lymphatic").annotate(Sum("lymphatic"),
                                                                                              Sum("filariasis"),
                                                                                              Sum("onchocerciasis"),
                                                                                              Sum("schistosomiasis"),
                                                                                              Sum("trachoma"),
                                                                                              Sum("helminthiasis"))

    try:
        rep=report_q[0]
    except IndexError:
        rep={}

    context = {

        'bubbles_to_ret': mark_safe(bubbles_to_ret),
        'pdata': mark_safe(pdata),
        'ldata': mark_safe(ldata),
        'rep': rep

    }
    return render_to_response("ntds/view_analytics.html", context, context_instance=RequestContext(request))


def manage_reporters(request):
    columns = [('Name', True, 'mobile', SimpleSorter()),
               ('Parish', True, 'parish', SimpleSorter()),
               ('Subcounty', True, 'subcounty', SimpleSorter()),
               ('District', True, 'district', SimpleSorter()),
               ('Mobile', True, 'default_connection', SimpleSorter()),
               ('Active', True, 'active', SimpleSorter()),
               ('Submissions', False, '', ''),

    ]

    filter_forms = [FreeSearchForm, MultipleDistictFilterForm]
    action_forms = [DownloadForm, SendTextForm]


    return generic(
        request,
        model=Reporter,
        queryset=Reporter.objects.all(),
        filter_forms=filter_forms,
        action_forms=action_forms,
        objects_per_page=25,
        partial_row='ntds/partials/reporter_row.html',
        base_template='ntds/reporter_base.html',
        columns=columns,
        sort_column='pk',
        sort_ascending=False,
    )


def create_reporter(mobile, name, parish):
    role, _ = Group.objects.get_or_create(name='Ntds')
    msisdn, backend = assign_backend(mobile)
    connection, created = Connection.objects.get_or_create(identity=mobile, backend=backend)
    provider = HealthProvider.objects.create(name=name, location=parish)
    provider.groups.add(role)
    connection.contact = provider
    connection.save()
    rep = Reporter(healthprovider_ptr=provider)
    rep.__dict__.update(provider.__dict__)
    rep.save()
    # reporter=Reporter.objects.create(healthprovider_ptr=provider)
    return rep


def new_reporter(request):
    form = ReporterForm(request.POST or None)

    if form.is_valid():
        rep = create_reporter(form.cleaned_data["mobile"], form.cleaned_data["name"], form.cleaned_data["parish"])

        return HttpResponseRedirect("/ntds/reporters/")

    return render_to_response("ntds/new_reporter.html", dict(form=form), context_instance=RequestContext(request))


def upload_reporters(request):
    form = ExcelUploadForm(request.POST, request.FILES)
    format = request.FILES['excel_file'].name.split('.')[-1]
    if format in ["xlsx"] and form.is_valid():
        file = form.clened_data["excel_file"]
        workbook = load_workbook(file)
        if workbook:
            worksheets = workbook.get_sheet_names()
        for sheet in worksheets:
            worksheet = workbook.get_sheet_by_name(sheet)

            for index, row in enumerate(worksheet.rows):
                if not index > 0:
                    continue
                name = ""
                if not empty(row[0].value):
                    name = row[0].value

                if not empty(row[1].value):
                    district = row[1].value
                if not empty(row[2].value):
                    subcounty = row[2].value
                if not empty(row[3].value):
                    parish = row[3].value
                if not empty(row[4].value):
                    mobile = parse_mobile(row[3].value)
                if mobile:
                    create_reporter(mobile, name, parish)

        return HttpResponseRedirect("/ntds/reporters/")

    return render_to_response("ntds/upload_reporters.html", dict(form=form), context_instance=RequestContext(request))


def view_districts(request, location_id=None):
    reports = NTDReport.objects.values("reporter__district", "reporter__district__name", "updated", "trachoma",
                                       "helminthiasis", "schistosomiasis",
                                       "onchocerciasis", "filariasis", "lymphatic").annotate(Sum("lymphatic"),
                                                                                             Sum("filariasis"),
                                                                                             Sum("onchocerciasis"),
                                                                                             Sum("schistosomiasis"),
                                                                                             Sum("trachoma"),
                                                                                             Sum("helminthiasis"))
    if location_id:
        district = get_object_or_404(Location, pk=location_id)
        district_report = NTDReport.objects.filter(reporter__district=district)
        drug_reports = district_report.values("reporter__district",
                                                                                    "reporter__district__name",
                                                                                    "updated", "trachoma",
                                                                                    "helminthiasis", "schistosomiasis",
                                                                                    "onchocerciasis", "filariasis",
                                                                                    "lymphatic", "alb_used", "ivm_used",
                                                                                    "pzq_used", "mbd_used", "ttr_used",
                                                                                    "ziths_used", "zitht_used",
                                                                                    "alb_received", "ivm_received",
                                                                                    "pzq_received", "mbd_received",
                                                                                    "ttr_received", "ziths_received",
                                                                                    "zitht_received", "alb_wasted",
                                                                                    "ivm_wasted", "pzq_wasted",
                                                                                    "mbd_wasted", "ttr_wasted",
                                                                                    "ziths_wasted",
                                                                                    "zitht_wasted").annotate(
            Sum("lymphatic"),
            Sum("filariasis"),
            Sum("onchocerciasis"),
            Sum("schistosomiasis"),
            Sum("trachoma"),
            Sum("helminthiasis"),

            Sum("alb_received"), Sum("ivm_received"), Sum("pzq_received"), Sum("mbd_received"), Sum("ttr_received"),
            Sum("ziths_received"), Sum("zitht_received"),
            Sum("alb_wasted"), Sum("ivm_wasted"), Sum("pzq_wasted"), Sum("mbd_wasted"), Sum("ttr_wasted"),
            Sum("ziths_wasted"), Sum("zitht_wasted"),
            Sum("alb_used"), Sum("ivm_used"), Sum("pzq_used"), Sum("mbd_used"), Sum("ttr_used"), Sum("ziths_used"),
            Sum("zitht_used"),
            Sum("alb_left"), Sum("ivm_left"), Sum("pzq_left"), Sum("mbd_left"), Sum("ttr_left"), Sum("ziths_left"),
            Sum("zitht_left"),


        )

        reports = district_report.values("reporter__district",
                                                                               "reporter__district__name", "updated",
                                                                               "trachoma", "helminthiasis",
                                                                               "schistosomiasis",
                                                                               "onchocerciasis", "filariasis",
                                                                               "lymphatic").annotate(Sum("lymphatic"),
                                                                                                     Sum("filariasis"),
                                                                                                     Sum(
                                                                                                         "onchocerciasis"),
                                                                                                     Sum(
                                                                                                         "schistosomiasis"),
                                                                                                     Sum("trachoma"),
                                                                                                     Sum(
                                                                                                         "helminthiasis"),
                                                                                                     Sum(
                                                                                                         "treated_u_5_male_onch"),
                                                                                                     Sum(
                                                                                                         "treated_u_5_female_onch"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_male_onch"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_female_onch"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_male_onch"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_female_onch"),
                                                                                                     Sum(
                                                                                                         "pop_u_5_male_onch"),
                                                                                                     Sum(
                                                                                                         "pop_u_5_female_onch"),
                                                                                                     Sum(
                                                                                                         "pop_4_to_14_male_onch"),
                                                                                                     Sum(
                                                                                                         "pop_4_to_14_female_onch"),
                                                                                                     Sum(
                                                                                                         "pop_gt_14_male_onch"),
                                                                                                     Sum(
                                                                                                         "pop_gt_14_female_onch"),
                                                                                                     Sum(
                                                                                                         "treated_u_5_male_schi"),
                                                                                                     Sum(
                                                                                                         "treated_u_5_female_schi"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_male_schi"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_female_schi"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_male_schi"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_female_schi"),


                                                                                                     Sum(
                                                                                                         "treated_lt_6_male"),
                                                                                                     Sum(
                                                                                                         "treated_lt_6_female"),
                                                                                                     Sum(
                                                                                                         "treated_6_to_4_male"),
                                                                                                     Sum(
                                                                                                         "treated_6_to_4_female"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_male"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_female"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_male"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_female"),

                                                                                                     Sum(
                                                                                                         "treated_lt_6_male_trac"),
                                                                                                     Sum(
                                                                                                         "treated_lt_6_female_trac"),
                                                                                                     Sum(
                                                                                                         "treated_6_to_4_male_trac"),
                                                                                                     Sum(
                                                                                                         "treated_6_to_4_female_trac"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_male_trac"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_female_trac"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_male_trac"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_female_trac"),
                                                                                                     Sum(
                                                                                                         "pop_u_5_male_lyf"),
                                                                                                     Sum(
                                                                                                         "pop_u_5_female_lyf"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_male_lyf"),
                                                                                                     Sum(
                                                                                                         "treated_4_to_14_female_lyf"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_male_lyf"),
                                                                                                     Sum(
                                                                                                         "treated_gt_14_female_lyf"),


                                                                                                     Sum(
                                                                                                         "pop_lt_6_male"),
                                                                                                     Sum(
                                                                                                         "pop_lt_6_female"),
                                                                                                     Sum(
                                                                                                         "pop_6_to_4_male"),
                                                                                                     Sum(
                                                                                                         "pop_6_to_4_female"),
                                                                                                     Sum(
                                                                                                         "pop_4_to_14_male"),
                                                                                                     Sum(
                                                                                                         "pop_4_to_14_female"),
                                                                                                     Sum(
                                                                                                         "pop_gt_14_male"),
                                                                                                     Sum(
                                                                                                         "pop_gt_14_female"))
        # 5+
        lf_eligible = reports[0].get("pop_gt_14_female__sum", 0) + reports[0].get("pop_gt_14_male__sum", 0) + reports[
            0].get("pop_4_to_14_male__sum", 0) + reports[0].get("pop_4_to_14_female__sum", 0)
        #1+
        alb_eligible = reports[0].get("pop_6_to_4_male__sum", 0) + reports[0].get("pop_6_to_4_female__sum", 0) + \
                       reports[0].get("pop_gt_14_female__sum", 0) + reports[0].get("pop_gt_14_male__sum", 0) + reports[
                           0].get("pop_4_to_14_male__sum", 0) + reports[0].get("pop_4_to_14_female__sum", 0)
        #total pop
        total_pop = reports[0].get("pop_lt_6_male__sum", 0) + reports[0].get("pop_lt_6_female__sum", 0) + reports[
            0].get("pop_6_to_4_male__sum", 0) + reports[0].get("pop_6_to_4_female__sum", 0) + reports[0].get(
            "pop_gt_14_female__sum", 0) + reports[0].get("pop_gt_14_male__sum", 0) + reports[0].get(
            "pop_4_to_14_male__sum", 0) + reports[0].get("pop_4_to_14_female__sum", 0)

        subcounty_reports = district_report.values("reporter__subcounty",
                                                                                         "reporter__subcounty__name",
                                                                                         "updated", "trachoma",
                                                                                         "helminthiasis",
                                                                                         "schistosomiasis",
                                                                                         "onchocerciasis", "filariasis",
                                                                                         "lymphatic", "alb_used",
                                                                                         "ivm_used", "pzq_used",
                                                                                         "mbd_used", "ttr_used",
                                                                                         "ziths_used", "zitht_used",
                                                                                         "alb_received", "ivm_received",
                                                                                         "pzq_received", "mbd_received",
                                                                                         "ttr_received",
                                                                                         "ziths_received",
                                                                                         "zitht_received", "alb_wasted",
                                                                                         "ivm_wasted", "pzq_wasted",
                                                                                         "mbd_wasted", "ttr_wasted",
                                                                                         "ziths_wasted",
                                                                                         "zitht_wasted").annotate(
            Sum("lymphatic"),
            Sum("filariasis"),
            Sum("onchocerciasis"),
            Sum("schistosomiasis"),
            Sum("trachoma"),
            Sum("helminthiasis"),
            Sum("alb_received"), Sum("ivm_received"), Sum("pzq_received"), Sum("mbd_received"), Sum("ttr_received"),
            Sum("ziths_received"), Sum("zitht_received"),
            Sum("alb_wasted"), Sum("ivm_wasted"), Sum("pzq_wasted"), Sum("mbd_wasted"), Sum("ttr_wasted"),
            Sum("ziths_wasted"), Sum("zitht_wasted"),
            Sum("alb_used"), Sum("ivm_used"), Sum("pzq_used"), Sum("mbd_used"), Sum("ttr_used"), Sum("ziths_used"),
            Sum("zitht_used"))

        parish_count = get_all_children(Location.objects.filter(pk=district.pk)).filter(type__name="parish").count()
        subcounty_count = get_all_children(Location.objects.filter(pk=district.pk)).filter(type__name="sub_county").count()
        village_count =  get_all_children(Location.objects.filter(pk=district.pk)).filter(type__name="village").count()
        subcounties_covered=district_report.values("reporter__subcounty").count()

        return render_to_response('ntds/report_detail.html',
                                  dict(village_count=village_count,parishes_covered=subcounties_covered,parish_count=parish_count,subcounty_count=subcounty_count,total_pop=total_pop, lf_eligible=lf_eligible, alb_eligible=alb_eligible,
                                       reports=reports, drug_report=drug_reports[0], district=district,
                                       subcounty_reports=subcounty_reports), context_instance=RequestContext(request))

    return render_to_response('ntds/report.html', dict(reports=reports), context_instance=RequestContext(request))


def view_messages(request):
    context = {}

    columns = [('Name', True, 'title', SimpleSorter()),
               ('Parish', True, 'decription', SimpleSorter()),
               ('Mobile', True, 'questions__name', SimpleSorter()),
               ('Status', True, 'enabled', SimpleSorter()),
               ('Submissions', False, '', ''),
               ('Last Submission', False, '', ''),
    ]

    messages = Message.objects.filter(connection__pk__in=Reporter.objects.values("connection")).order_by("-pk")

    return generic(
        request,
        model=Message,
        queryset=Reporter.objects.all(),
        filter_forms=[],
        action_forms=[],
        objects_per_page=25,
        partial_row='ntds/partials/reporter_row.html',
        base_template='ntds/reporter_base.html',
        columns=columns,
        sort_column='pk',
        sort_ascending=False,
        current='survey'
    )


def disease_report(request):
    context = {}

    columns = [('Name', True, 'title', SimpleSorter()),
               ('Parish', True, 'decription', SimpleSorter()),
               ('Mobile', True, 'questions__name', SimpleSorter()),
               ('Status', True, 'enabled', SimpleSorter()),
               ('Submissions', False, '', ''),
               ('Last Submission', False, '', ''),
    ]

    return generic(
        request,
        model=NTDReport,
        queryset=NTDReport.objects.all(),
        filter_forms=[],
        action_forms=[],
        objects_per_page=25,
        partial_row='ntds/partials/reporter_row.html',
        base_template='ntds/reporter_base.html',
        columns=columns,
        sort_column='pk',
        sort_ascending=False,
        current='survey'
    )


def drug_report(request):
    context = {}

    columns = [('Name', True, 'title', SimpleSorter()),
               ('Parish', True, 'decription', SimpleSorter()),
               ('Mobile', True, 'questions__name', SimpleSorter()),
               ('Status', True, 'enabled', SimpleSorter()),
               ('Submissions', False, '', ''),
               ('Last Submission', False, '', ''),
    ]

    return generic(
        request,
        model=NTDReport,
        queryset=NTDReport.objects.all(),
        filter_forms=[],
        action_forms=[],
        objects_per_page=25,
        partial_row='ntds/partials/reporter_row.html',
        base_template='ntds/reporters_base.html',
        columns=columns,
        sort_column='pk',
        sort_ascending=False,
        current='survey'
    )




def view_submissions(request, reporter_id=None):
    if reporter_id:
        reporter = get_object_or_404(Reporter, pk=reporter_id)
        health_provider = reporter.healthprovider_ptr
        submissions = XFormSubmission.objects.filter(
            connection__contact__healthproviderbase__healthprovider=health_provider)
    else:
        group, _ = Group.objects.get_or_create(name='Ntds')
        submissions = XFormSubmission.objects.filter(connection__contact__groups=group).order_by("-message__date")

    columns = [('Name', True, 'name', SimpleSorter()),
               ('Parish', True, 'connection__contact__healthproviderbase__healthprovider__location', SimpleSorter()),
               ('District', True, 'connection__contact__healthproviderbase__healthprovider__reporter__district', SimpleSorter()),
               ('Mobile', True, 'connection__identity', SimpleSorter()),
               ('Valid', True, 'enabled', SimpleSorter()),
               ('Message', False, 'message__text', SimpleSorter()),

    ]

    return generic(
        request,
        model=XFormSubmission,
        queryset=submissions,
        filter_forms=[],
        action_forms=[],
        objects_per_page=25,
        partial_row='ntds/partials/submission_row.html',
        base_template='ntds/submissions_base.html',
        columns=columns,
        sort_column='pk',
        sort_ascending=False,
        current='survey'
    )


def edit_reporter(request, pk):
    instance = Patient.objects.get(pk=pk)
    patient_form = PatientForm(instance=instance, mission=instance.mission)
    phase1_form = Phase1SessionForm(instance=instance.phase1)
    # missions=Mission.objects.filter(active=True)
    if request.method == "POST":
        patient_form = PatientForm(request.POST, instance=instance, mission=instance.mission)
        phase1_form = Phase1SessionForm(request.POST, instance=instance.phase1)
        if patient_form.is_valid() and phase1_form.is_valid():
            patient = patient_form.save()
            phase1_form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully Updated Patient %s' % patient.identifier)
            if request.POST.get("next", None):
                return HttpResponseRedirect("/patients/%d/phase2/edit/" % patient.pk)
            return HttpResponseRedirect("/patients/new/")

    return render_to_response("mission/edit_patient.html",
                              {"patient_form": patient_form, "patient": instance, "phase1_form": phase1_form,
                               'tab': 'patient', "identifier": instance.identifier, 'country': instance.country},
                              context_instance=RequestContext(request))


def view_messages(request):
    # filter_forms = []
    #action_forms = []
    group, _ = Group.objects.get_or_create(name='Ntds')
    messages = Message.objects.filter(connection__contact__groups=group).order_by("-date")

    partial_row = 'ntds/partials/message_row.html'
    columns = [('Message', True, 'text', SimpleSorter()),
               ('Mobile', True, 'identity', SimpleSorter()),
               ('Date', True, 'date', SimpleSorter()),
               ('Direction', True, 'direction', SimpleSorter()),

    ]
    return generic(
        request,
        model=Message,
        queryset=messages,
        objects_per_page=25,
        partial_row=partial_row,
        results_title="Messages",
        title="All SMS ",
        base_template="ntds/messages_base.html",
        columns=columns,
        sort_column='pk',
        show_unfiltered=False,
        sort_ascending=False,
    )


def get_all_subcounties(request):
    data_dict = dict(request.GET)
    subcounties = Location.objects.filter(type="sub_county").order_by("name")

    districts = data_dict.get("districts", None)
    if districts:
        try:

            subcounties = get_all_children(Location.objects.filter(pk__in=districts)).filter(
                type="sub_county").order_by("name")
        # handle nil pk
        except AttributeError:
            pass
    s = map(lambda x: [x.pk, x.name], subcounties)
    return JSONResponse(s)


def get_all_parishes(request):
    data_dict = dict(request.GET)
    parishes = Location.objects.filter(type="parish").order_by("name")

    subcounties = data_dict.get("subcounties", None)
    if subcounties:
        try:

            parishes = get_all_children(Location.objects.filter(pk__in=subcounties)).filter(type="parish").order_by(
                "name")
        except AttributeError:
            pass
    s = map(lambda x: [x.pk, x.name], parishes)
    return JSONResponse(s)







