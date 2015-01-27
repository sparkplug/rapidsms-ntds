import os
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.conf import settings
from rapidsms_xforms.models import XForm, XFormSubmission
from generic.views import generic
from django.contrib.auth.decorators import  user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from .models import NTDReport,Reporter
from django.db.models import Sum
from rapidsms.contrib.locations.models import Location
from skipdict import SkipDict

from generic.views import generic
from generic.sorters import SimpleSorter
from .forms import *
from rapidsms_httprouter.models import Message

def get_prevelance(reports,rep_toret,pdata,ldata):
    toret={}
    for d in reports:
        loc=Location.objects.get(pk=d.pop("reporter__district"))
        v_dict=SkipDict(d)
        toret["name"]="%s-%s"%(str(loc.name),v_dict.keys()[-1].split("__")[0])
        toret["style"]={"fill": '#007ACC',"fill-opacity": 0.8,"stroke":'rgba(29,210,175,0.3)',"stroke-width": 3}
        toret["latLng"]=[float(loc.point.latitude),float(loc.point.longitude)]
        rep_toret.append(toret)
        pdata[str(loc.name).upper()]=v_dict.values()[-1]
        ldata[str(loc.name).upper()]=v_dict.keys()[-1].split("__")[0]

def dashboard(request):



    bubbles_to_ret=[]
    pdata={}
    ldata={}
    report_q = NTDReport.objects.values("reporter__district", "trachoma", "helminthiasis", "schistosomiasis",
                                        "onchocerciasis", "filariasis", "lymphatic").annotate(Sum("lymphatic"),
                                                                                              Sum("filariasis"),
                                                                                              Sum("onchocerciasis"),
                                                                                              Sum("schistosomiasis"),
                                                                                              Sum("trachoma"),
                                                                                              Sum("helminthiasis"))


    get_prevelance(report_q,bubbles_to_ret,pdata,ldata)

    context = {

        'bubbles_to_ret':mark_safe(bubbles_to_ret),
        'pdata':mark_safe(pdata),
        'ldata':mark_safe(ldata)

     }
    return render_to_response("ntds/dashboard.html",context,context_instance=RequestContext(request))



def view_analytics(request):



    bubbles_to_ret=[]
    pdata={}
    ldata={}
    report_q = NTDReport.objects.values("reporter__district", "trachoma", "helminthiasis", "schistosomiasis",
                                        "onchocerciasis", "filariasis", "lymphatic").annotate(Sum("lymphatic"),
                                                                                              Sum("filariasis"),
                                                                                              Sum("onchocerciasis"),
                                                                                              Sum("schistosomiasis"),
                                                                                              Sum("trachoma"),
                                                                                              Sum("helminthiasis"))


    get_prevelance(report_q,bubbles_to_ret,pdata,ldata)

    context = {

        'bubbles_to_ret':mark_safe(bubbles_to_ret),
        'pdata':mark_safe(pdata),
        'ldata':mark_safe(ldata)

    }
    return render_to_response("ntds/view_analytics.html",context,context_instance=RequestContext(request))





def manage_reporters(request):
    queryset=Reporter.objects.all(),

    columns = [('Name', True, 'title', SimpleSorter()),
               ('Parish', True, 'decription', SimpleSorter()),
               ('Subcounty', True, 'decription', SimpleSorter()),
               ('District', True, 'decription', SimpleSorter()),
               ('Mobile', True, 'questions__name', SimpleSorter()),
               ('Status', True, 'enabled', SimpleSorter()),
               ('Submissions', False, '', ''),

               ]



    filter_forms = [FreeSearchForm,MultipleDistictFilterForm]
    action_forms = [DownloadForm, SendTextForm]

    if not request.POST.get("page_num") and request.method =="POST":
        return ExcelResponse(queryset)
    return generic(
        request,
        model=Reporter,
        queryset=queryset,
        filter_forms=filter_forms,
        action_forms=action_forms,
        objects_per_page=25,
        partial_row='ntds/partials/reporter_row.html',
        base_template='ntds/reporter_base.html',
        columns=columns,
        sort_column='pk',
        sort_ascending=False,
    )


def reports(request):

    columns = [('Name', True, 'title', SimpleSorter()),
               ('Parish', True, 'decription', SimpleSorter()),
               ('Mobile', True, 'questions__name', SimpleSorter()),
               ('Status', True, 'enabled', SimpleSorter()),
               ('Submissions', False, '', ''),
               ('Last Submission', False, '', ''),
               ]

    filter_forms = [FreeSearchForm,MultipleDistictFilterForm]
    action_forms = [DownloadForm, SendTextForm]

    return generic(
        request,
        model=Reporter,
        queryset=Reporter.objects.all(),
        filter_forms=filter_forms,
        action_forms=action_forms,
        objects_per_page=25,
        partial_row='ntds/partials/report_row.html',
        base_template='ntds/report_base.html',
        columns=columns,
        sort_column='pk',
        sort_ascending=False,
        )


def view_messages(request):
    context={}

    columns = [('Name', True, 'title', SimpleSorter()),
               ('Parish', True, 'decription', SimpleSorter()),
               ('Mobile', True, 'questions__name', SimpleSorter()),
               ('Status', True, 'enabled', SimpleSorter()),
               ('Submissions', False, '', ''),
               ('Last Submission', False, '', ''),
               ]

    messages=Message.objects.filter(connection__pk__in= Reporter.objects.values("connection")).order_by("-pk")

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
    context={}

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
    context={}

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




def view_submissions(request, reporter=None):


    columns = [('Name', True, 'title', SimpleSorter()),
               ('Parish', True, 'decription', SimpleSorter()),
               ('Mobile', True, 'questions__name', SimpleSorter()),
               ('Status', True, 'enabled', SimpleSorter()),
               ('Submissions', False, '', ''),
               ('Last Submission', False, '', ''),
               ]

    return generic(
        request,
        model=XFormSubmission,
        queryset=XFormSubmission.objects.all(),
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
    #missions=Mission.objects.filter(active=True)
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


@user_passes_test(lambda u: u.has_perm('accounts.can_upload_excel'))
def excel_reports(request):
    upload_form = ExcelUploadForm()
    countries = Location.objects.filter(pk__in=MissionSite.objects.values("country")).order_by("name")
    missions = Mission.objects.filter(active=True).order_by("country__name")



    if request.method == "POST" :

        upload_form = ExcelUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():


            excel = request.FILES['excel_file']
            format=request.FILES['excel_file'].name.split('.')[-1]

            if format in ["xlsx","xls"]:
                message = upload_mission_excel_xls.delay(excel.temporary_file_path(),request.POST.get("phase"),request.POST.get("mission"),request.POST.get("site"),format=format)
                #upload_mission_excel_xls.delay(excel, request.POST.get("phase"), request.POST.get("mission"),request.POST.get("site"),format=format)
                messages.add_message(request, messages.SUCCESS, 'Successfully Uploaded Excel sheet.')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid File format')
        else:
            messages.add_message(request, messages.ERROR, str(upload_form.errors))


    return render_to_response("mission/excel.html",
                              dict(upload_form=upload_form, countries=countries, missions=missions),
                              context_instance=RequestContext(request))



@csrf_exempt
@user_passes_test(lambda u: u.has_perm('accounts.can_view_patients'))
def patients(request):
    from generic.views import generic
    from generic.sorters import SimpleSorter

    filter_forms = [SearchPatientsForm, AgeFilterForm]
    action_forms = [DownloadForm, SendTextForm, SendEmailForm]
    if not request.user.is_superuser or not request.user.is_staff:
        country=request.user.get_profile().country
        title="Patient Listing For %s" %(" ".join(country.values_list("name",flat=True)))
        patients=Patient.objects.filter(mission__country__in=country.values("pk")).prefetch_related("phase1","phase2","phase3","mission")
        filter_forms.append(SiteFilterForm)
    else:
        title="All Patients"
        patients=Patient.objects.all().prefetch_related("phase1","phase2","phase3","mission")
        filter_forms.append(CountryFilterForm)
    partial_row = 'mission/partials/patient_row.html'
    base_template = 'mission/partials/patients_base.html'
    paginator_template = 'mission/partials/pagination.html'
    columns = [('Name', True, 'first_name', SimpleSorter()),
               ('Age', True, 'age', SimpleSorter()),
               ('Gender', True, 'gender', SimpleSorter()),
               ('Country', True, 'mission__country__name', SimpleSorter()),
               ('Mobile', True, 'mobile', SimpleSorter()),
               ('Email', True, 'email', SimpleSorter()),
               ('User', True, 'user', SimpleSorter()),
               ('Actions', False, '', '')]
    return generic(
        request,
        model=Patient,
        queryset=patients,
        filter_forms=filter_forms,
        action_forms=action_forms,
        objects_per_page=25,
        partial_row=partial_row,
        results_title="Patients",
        title=title,
        base_template=base_template,
        paginator_template=paginator_template,
        paginator_func=paginate,
        columns=columns,
        sort_column='pk',
        show_unfiltered=False,
        sort_ascending=False,
        )



@csrf_exempt
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def view_messages(request):


    #filter_forms = []
    #action_forms = []

    partial_row = 'mission/partials/messages_row.html'
    base_template = 'mission/partials/messages_base.html'
    paginator_template = 'mission/partials/pagination.html'
    columns = [('Message', True, 'text', SimpleSorter()),
               ('Type', True, 'type', SimpleSorter()),
               ('sender', True, 'sender__username', SimpleSorter()),
               ('Destination', True, 'identifier', SimpleSorter()),
               ('Date', True, 'created', SimpleSorter()),
               ('Status', True, 'delivered', SimpleSorter()),
               ]
    return generic(
        request,
        model=Message,
        queryset=Message.objects.all(),
        objects_per_page=25,
        partial_row=partial_row,
        results_title="Messages",
        title="All SMS and Emails",
        base_template=base_template,
        paginator_template=paginator_template,
        paginator_func=paginate,
        columns=columns,
        sort_column='pk',
        show_unfiltered=False,
        sort_ascending=False,
        )



def missions_json(request):
    feature_collection = {"type": "FeatureCollection",
                          "features": []
    }
    qdict = Patient.objects.exclude(mission__country=None).values("mission__country__name",
                                                                  "mission__country__pk").annotate(
        patients=Count("mission__country__name"), number_of_aids=Sum('aids_received')).order_by("-patients")
    features = []
    for data in qdict:
        feature = {
            "type": "Feature",
            "properties": {
                "name": "name",
                "amenity": "Mission",
                "popupContent": "popup"
            },
            "geometry": {
                "type": "Point",
                "coordinates": []
            }
        }

        feature["properties"]["name"] = data["mission__country__name"]
        feature["properties"]["popupContent"] = "<h3>%s</h3>%d hearing aids given to %d People" % (
            data["mission__country__name"], data["number_of_aids"], data["patients"])
        location = Location.objects.get(pk=data["mission__country__pk"])
        feature["geometry"]["coordinates"] = [float(location.longitude), float(location.latitude)]
        feature_collection["features"].append(feature)

    return JSONResponse(feature_collection)







