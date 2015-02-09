from django.db import models
from rapidsms.contrib.locations.models import Location
from django.utils.translation import (ugettext, activate, deactivate)
from django.conf import settings
from healthmodels.models.HealthProvider import HealthProvider
from rapidsms_xforms.models import XForm,XFormReportSubmission
from .receivers import handle_submission

class OptinWord(models.Model):
    words = models.CharField(max_length=500)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, null=True)

    def __unicode__(self):
        return "%s(%s)" % (self.words, self.language)

class Translation(models.Model):
    field = models.TextField(db_index=True)
    language = models.CharField(max_length=5, db_index=True,
                                choices=settings.LANGUAGES)
    value = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s: %s' % (self.language, self.value)

    class Meta:
        unique_together = ('field', 'language')


class NTDReport(models.Model):
    reporter = models.ForeignKey("Reporter")
    xforms = models.ManyToManyField(XForm)
    population = models.IntegerField(max_length=10,null=True,blank=True)
    total_villages = models.IntegerField(max_length=10,null=True,blank=True)
    villages_targeted = models.IntegerField(max_length=10,null=True,blank=True)
    villages_treated = models.IntegerField(max_length=10,null=True,blank=True)
    villages_incomplete = models.IntegerField(max_length=10,null=True,blank=True)
    total_schools = models.IntegerField(max_length=10,null=True,blank=True)
    schools_targeted = models.IntegerField(max_length=10,null=True,blank=True)
    schools_treated = models.IntegerField(max_length=10,null=True,blank=True)
    schools_incomplete = models.IntegerField(max_length=10,null=True,blank=True)
    treated_lt_6_male = models.IntegerField(max_length=10,null=True,blank=True)
    treated_lt_6_female = models.IntegerField(max_length=10,null=True,blank=True)
    treated_6_to_4_male = models.IntegerField(max_length=10,null=True,blank=True)
    treated_6_to_4_female = models.IntegerField(max_length=10,null=True,blank=True)
    treated_4_to_14_male = models.IntegerField(max_length=10,null=True,blank=True)
    treated_4_to_14_female = models.IntegerField(max_length=10,null=True,blank=True)
    treated_gt_14_male = models.IntegerField(max_length=10,null=True,blank=True)
    treated_gt_14_female = models.IntegerField(max_length=10,null=True,blank=True)
    pop_lt_6_male = models.IntegerField(max_length=10,null=True,blank=True)
    pop_lt_6_female = models.IntegerField(max_length=10,null=True,blank=True)
    pop_6_to_4_male = models.IntegerField(max_length=10,null=True,blank=True)
    pop_6_to_4_female = models.IntegerField(max_length=10,null=True,blank=True)
    pop_4_to_14_male = models.IntegerField(max_length=10,null=True,blank=True)
    pop_4_to_14_female = models.IntegerField(max_length=10,null=True,blank=True)
    pop_gt_14_male = models.IntegerField(max_length=10,null=True,blank=True)
    pop_gt_14_female = models.IntegerField(max_length=10,null=True,blank=True)
    lymphatic =  models.IntegerField(max_length=10,null=True,blank=True)
    filariasis = models.IntegerField(max_length=10,null=True,blank=True)
    onchocerciasis = models.IntegerField(max_length=10,null=True,blank=True)
    schistosomiasis = models.IntegerField(max_length=10,null=True,blank=True)
    helminthiasis = models.IntegerField(max_length=10,null=True,blank=True)
    trachoma = models.IntegerField(max_length=10,null=True,blank=True)
    alb = models.IntegerField(max_length=10,null=True,blank=True)
    ivm = models.IntegerField(max_length=10,null=True,blank=True)
    pzq = models.IntegerField(max_length=10,null=True,blank=True)
    mbd = models.IntegerField(max_length=10,null=True,blank=True)
    ttr = models.IntegerField(max_length=10,null=True,blank=True)
    ziths = models.IntegerField(max_length=10,null=True,blank=True)
    zitht = models.IntegerField(max_length=10,null=True,blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ReportProgress(models.Model):
    ACTIVE=1
    COMPLETE=2
    reporter = models.ForeignKey("Reporter")
    status = models.IntegerField(max_length=2 ,choices=((ACTIVE,"inprogress"),(COMPLETE,"complete")))
    parish = models.ForeignKey(Location)
    xform_reports = models.ManyToManyField(XFormReportSubmission)
    report=models.ForeignKey(NTDReport)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class DiseaseReport(models.Model):
    district = models.ForeignKey(Location)



class Reporter(HealthProvider):
    district = models.ForeignKey(Location,related_name="districts",null=True,blank=True)
    subcounty = models.ForeignKey(Location,related_name="subcounties",null=True,blank=True)
    reporting_area=models.ManyToManyField(Location)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.district and self.location:
            self.district =self.location.get_ancestors().get(type="district")
            self.subcounty=self.location.get_ancestors().get(type="sub_county")

        super(Reporter, self).save(*args, **kwargs)

class RegistrationPhase(models.Model):
    parish=models.ForeignKey(Location)
class DispensePhase(models.Model):
    parish=models.ForeignKey(Location)

class DrugAdministration(models.Model):
    year=models.CharField(max_length=50)
    registration=models.ForeignKey(RegistrationPhase)
    admnistration=models.ForeignKey(DispensePhase)

class Disease(models.Model):
    name=models.CharField(max_length=50)

class Treatment(models.Model):
    name=models.CharField(max_length=50)
    diseases=models.ManyToManyField(Disease)

class Drug(models.Model):
    name=models.CharField(max_length=50)


def check_basic_validity(xform_type, submission, health_provider, day_range, report_in_progress):
    return



def gettext_db(field, language):
    #if name exists in po file get it else look
    if Translation.objects.filter(field=field, language=language).exists():
        return Translation.objects.filter(field=field, language=language)[0].value
    else:
        activate(language)
        lang_str = ugettext(field)
        deactivate()
        return lang_str




