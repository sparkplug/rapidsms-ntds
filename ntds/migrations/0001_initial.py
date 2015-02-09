# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OptinWord'
        db.create_table('ntds_optinword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('words', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
        ))
        db.send_create_signal('ntds', ['OptinWord'])

        # Adding model 'Translation'
        db.create_table('ntds_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.TextField')(db_index=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('ntds', ['Translation'])

        # Adding unique constraint on 'Translation', fields ['field', 'language']
        db.create_unique('ntds_translation', ['field', 'language'])

        # Adding model 'NTDReport'
        db.create_table('ntds_ntdreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ntds.Reporter'])),
            ('population', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('total_villages', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('villages_targeted', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('villages_treated', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('villages_incomplete', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('total_schools', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('schools_targeted', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('schools_treated', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('schools_incomplete', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('treated_lt_6_male', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('treated_lt_6_female', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('treated_6_to_4_male', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('treated_6_to_4_female', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('treated_4_to_14_male', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('treated_4_to_14_female', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('treated_gt_14_male', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('treated_gt_14_female', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('lymphatic', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('filariasis', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('onchocerciasis', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('schistosomiasis', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('helminthiasis', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('trachoma', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ntds', ['NTDReport'])

        # Adding M2M table for field xforms on 'NTDReport'
        m2m_table_name = db.shorten_name('ntds_ntdreport_xforms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ntdreport', models.ForeignKey(orm['ntds.ntdreport'], null=False)),
            ('xform', models.ForeignKey(orm['rapidsms_xforms.xform'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ntdreport_id', 'xform_id'])

        # Adding model 'ReportProgress'
        db.create_table('ntds_reportprogress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ntds.Reporter'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('parish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
            ('xform_report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms_xforms.XFormReportSubmission'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ntds', ['ReportProgress'])

        # Adding model 'DiseaseReport'
        db.create_table('ntds_diseasereport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
        ))
        db.send_create_signal('ntds', ['DiseaseReport'])

        # Adding model 'Reporter'
        db.create_table('ntds_reporter', (
            ('healthprovider_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['healthmodels.HealthProvider'], unique=True, primary_key=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='districts', null=True, to=orm['locations.Location'])),
            ('subcounty', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subcounties', null=True, to=orm['locations.Location'])),
        ))
        db.send_create_signal('ntds', ['Reporter'])

        # Adding M2M table for field reporting_area on 'Reporter'
        m2m_table_name = db.shorten_name('ntds_reporter_reporting_area')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reporter', models.ForeignKey(orm['ntds.reporter'], null=False)),
            ('location', models.ForeignKey(orm['locations.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reporter_id', 'location_id'])

        # Adding model 'RegistrationPhase'
        db.create_table('ntds_registrationphase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
        ))
        db.send_create_signal('ntds', ['RegistrationPhase'])

        # Adding model 'DispensePhase'
        db.create_table('ntds_dispensephase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
        ))
        db.send_create_signal('ntds', ['DispensePhase'])

        # Adding model 'DrugAdministration'
        db.create_table('ntds_drugadministration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('registration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ntds.RegistrationPhase'])),
            ('admnistration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ntds.DispensePhase'])),
        ))
        db.send_create_signal('ntds', ['DrugAdministration'])

        # Adding model 'Disease'
        db.create_table('ntds_disease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('ntds', ['Disease'])

        # Adding model 'Treatment'
        db.create_table('ntds_treatment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('ntds', ['Treatment'])

        # Adding M2M table for field diseases on 'Treatment'
        m2m_table_name = db.shorten_name('ntds_treatment_diseases')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('treatment', models.ForeignKey(orm['ntds.treatment'], null=False)),
            ('disease', models.ForeignKey(orm['ntds.disease'], null=False))
        ))
        db.create_unique(m2m_table_name, ['treatment_id', 'disease_id'])

        # Adding model 'Drug'
        db.create_table('ntds_drug', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('ntds', ['Drug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Translation', fields ['field', 'language']
        db.delete_unique('ntds_translation', ['field', 'language'])

        # Deleting model 'OptinWord'
        db.delete_table('ntds_optinword')

        # Deleting model 'Translation'
        db.delete_table('ntds_translation')

        # Deleting model 'NTDReport'
        db.delete_table('ntds_ntdreport')

        # Removing M2M table for field xforms on 'NTDReport'
        db.delete_table(db.shorten_name('ntds_ntdreport_xforms'))

        # Deleting model 'ReportProgress'
        db.delete_table('ntds_reportprogress')

        # Deleting model 'DiseaseReport'
        db.delete_table('ntds_diseasereport')

        # Deleting model 'Reporter'
        db.delete_table('ntds_reporter')

        # Removing M2M table for field reporting_area on 'Reporter'
        db.delete_table(db.shorten_name('ntds_reporter_reporting_area'))

        # Deleting model 'RegistrationPhase'
        db.delete_table('ntds_registrationphase')

        # Deleting model 'DispensePhase'
        db.delete_table('ntds_dispensephase')

        # Deleting model 'DrugAdministration'
        db.delete_table('ntds_drugadministration')

        # Deleting model 'Disease'
        db.delete_table('ntds_disease')

        # Deleting model 'Treatment'
        db.delete_table('ntds_treatment')

        # Removing M2M table for field diseases on 'Treatment'
        db.delete_table(db.shorten_name('ntds_treatment_diseases'))

        # Deleting model 'Drug'
        db.delete_table('ntds_drug')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eav.attribute': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('site', 'slug'),)", 'object_name': 'Attribute'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'datatype': ('eav.fields.EavDatatypeField', [], {'max_length': '6'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'enum_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eav.EnumGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('eav.fields.EavSlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'eav.enumgroup': {
            'Meta': {'object_name': 'EnumGroup'},
            'enums': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eav.EnumValue']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'eav.enumvalue': {
            'Meta': {'object_name': 'EnumValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'eav.value': {
            'Meta': {'object_name': 'Value'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eav.Attribute']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'entity_ct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_entities'", 'to': "orm['contenttypes.ContentType']"}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'generic_value_ct': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'value_values'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'generic_value_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'value_enum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eav_values'", 'null': 'True', 'to': "orm['eav.EnumValue']"}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'healthmodels.healthfacility': {
            'Meta': {'object_name': 'HealthFacility', '_ormbases': ['healthmodels.HealthFacilityBase']},
            'healthfacilitybase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthFacilityBase']", 'unique': 'True', 'primary_key': 'True'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'})
        },
        'healthmodels.healthfacilitybase': {
            'Meta': {'object_name': 'HealthFacilityBase'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'authority': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'catchment_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'district': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_reporting_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Point']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'report_to_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report_to_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthFacilityType']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'healthmodels.healthfacilitytype': {
            'Meta': {'object_name': 'HealthFacilityType', '_ormbases': ['healthmodels.HealthFacilityTypeBase']},
            'healthfacilitytypebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthFacilityTypeBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'healthmodels.healthfacilitytypebase': {
            'Meta': {'object_name': 'HealthFacilityTypeBase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'healthmodels.healthprovider': {
            'Meta': {'object_name': 'HealthProvider', '_ormbases': ['healthmodels.HealthProviderBase']},
            'healthproviderbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthProviderBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'healthmodels.healthproviderbase': {
            'Meta': {'object_name': 'HealthProviderBase', '_ormbases': ['rapidsms.Contact']},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rapidsms.Contact']", 'unique': 'True', 'primary_key': 'True'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthFacility']", 'null': 'True'}),
            'last_reporting_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True'})
        },
        'locations.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Point']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': "orm['locations.LocationType']"})
        },
        'locations.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True'})
        },
        'locations.point': {
            'Meta': {'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'})
        },
        'logistics.contactrole': {
            'Meta': {'object_name': 'ContactRole'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'responsibilities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['logistics.Responsibility']", 'null': 'True', 'blank': 'True'})
        },
        'logistics.defaultmonthlyconsumption': {
            'Meta': {'unique_together': "(('supply_point_type', 'product'),)", 'object_name': 'DefaultMonthlyConsumption'},
            'default_monthly_consumption': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.Product']"}),
            'supply_point_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPointType']"})
        },
        'logistics.product': {
            'Meta': {'object_name': 'Product'},
            'average_monthly_consumption': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'emergency_order_level': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'equivalents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'equivalents_rel_+'", 'null': 'True', 'to': "orm['logistics.Product']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'product_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sms_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.ProductType']"}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'logistics.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'logistics.responsibility': {
            'Meta': {'object_name': 'Responsibility'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'logistics.supplypoint': {
            'Meta': {'object_name': 'SupplyPoint'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['logistics.SupplyPointGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_reported': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'supplied_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPointType']"})
        },
        'logistics.supplypointgroup': {
            'Meta': {'object_name': 'SupplyPointGroup'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'logistics.supplypointtype': {
            'Meta': {'object_name': 'SupplyPointType'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'default_monthly_consumptions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['logistics.Product']", 'null': 'True', 'through': "orm['logistics.DefaultMonthlyConsumption']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ntds.disease': {
            'Meta': {'object_name': 'Disease'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ntds.diseasereport': {
            'Meta': {'object_name': 'DiseaseReport'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ntds.dispensephase': {
            'Meta': {'object_name': 'DispensePhase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"})
        },
        'ntds.drug': {
            'Meta': {'object_name': 'Drug'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ntds.drugadministration': {
            'Meta': {'object_name': 'DrugAdministration'},
            'admnistration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ntds.DispensePhase']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ntds.RegistrationPhase']"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ntds.ntdreport': {
            'Meta': {'object_name': 'NTDReport'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'filariasis': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'helminthiasis': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lymphatic': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'onchocerciasis': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ntds.Reporter']"}),
            'schistosomiasis': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'schools_incomplete': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'schools_targeted': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'schools_treated': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'total_schools': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'total_villages': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'trachoma': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treated_4_to_14_female': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treated_4_to_14_male': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treated_6_to_4_female': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treated_6_to_4_male': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treated_gt_14_female': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treated_gt_14_male': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treated_lt_6_female': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treated_lt_6_male': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'villages_incomplete': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'villages_targeted': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'villages_treated': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'xforms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rapidsms_xforms.XForm']", 'symmetrical': 'False'})
        },
        'ntds.optinword': {
            'Meta': {'object_name': 'OptinWord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'words': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'ntds.registrationphase': {
            'Meta': {'object_name': 'RegistrationPhase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"})
        },
        'ntds.reporter': {
            'Meta': {'object_name': 'Reporter', '_ormbases': ['healthmodels.HealthProvider']},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'districts'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'healthprovider_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthProvider']", 'unique': 'True', 'primary_key': 'True'}),
            'reporting_area': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['locations.Location']", 'symmetrical': 'False'}),
            'subcounty': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subcounties'", 'null': 'True', 'to': "orm['locations.Location']"})
        },
        'ntds.reportprogress': {
            'Meta': {'object_name': 'ReportProgress'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ntds.Reporter']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'xform_report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_xforms.XFormReportSubmission']"})
        },
        'ntds.translation': {
            'Meta': {'unique_together': "(('field', 'language'),)", 'object_name': 'Translation'},
            'field': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'ntds.treatment': {
            'Meta': {'object_name': 'Treatment'},
            'diseases': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ntds.Disease']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'rapidsms.backend': {
            'Meta': {'object_name': 'Backend'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'rapidsms.connection': {
            'Meta': {'unique_together': "(('backend', 'identity'),)", 'object_name': 'Connection'},
            'backend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Backend']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Contact']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'commodities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'reported_by'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['logistics.Product']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'needs_reminders': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.ContactRole']", 'null': 'True', 'blank': 'True'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contact'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villagers'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'rapidsms_httprouter.message': {
            'Meta': {'object_name': 'Message'},
            'application': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'null': 'True', 'to': "orm['rapidsms_httprouter.MessageBatch']"}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['rapidsms.Connection']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_response_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'null': 'True', 'to': "orm['rapidsms_httprouter.Message']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'db_index': 'True'})
        },
        'rapidsms_httprouter.messagebatch': {
            'Meta': {'object_name': 'MessageBatch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'rapidsms_xforms.xform': {
            'Meta': {'object_name': 'XForm'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'command_prefix': ('django.db.models.fields.CharField', [], {'default': "'+'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('eav.fields.EavSlugField', [], {'max_length': '32'}),
            'keyword_prefix': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'restrict_message': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'restrict_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'separator': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'rapidsms_xforms.xformlist': {
            'Meta': {'ordering': "['priority']", 'object_name': 'XFormList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_xforms.XFormReport']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'xform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_xforms.XForm']"})
        },
        'rapidsms_xforms.xformreport': {
            'Meta': {'object_name': 'XFormReport'},
            'constraints': ('picklefield.fields.PickledObjectField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'xforms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rapidsms_xforms.XForm']", 'through': "orm['rapidsms_xforms.XFormList']", 'symmetrical': 'False'})
        },
        'rapidsms_xforms.xformreportsubmission': {
            'Meta': {'object_name': 'XFormReportSubmission'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_xforms.XFormReport']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'submissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rapidsms_xforms.XFormSubmission']", 'symmetrical': 'False'})
        },
        'rapidsms_xforms.xformsubmission': {
            'Meta': {'object_name': 'XFormSubmission'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmation_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'null': 'True', 'to': "orm['rapidsms.Connection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'has_errors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'null': 'True', 'to': "orm['rapidsms_httprouter.Message']"}),
            'raw': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'xform': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': "orm['rapidsms_xforms.XForm']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['ntds']