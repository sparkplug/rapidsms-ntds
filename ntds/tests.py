'''
Created on May 23, 2012

@author: asseym
'''
from django.test import TestCase
from django.conf import settings
import datetime
import traceback
from rapidsms_httprouter.router import get_router#, HttpRouterThread
from rapidsms_xforms.models import *
from rapidsms.messages.incoming import IncomingMessage, IncomingMessage
from rapidsms.models import Connection, Backend, Contact
from rapidsms_httprouter.models import Message
from rapidsms_httprouter.router import get_router
from django.contrib.auth.models import Group
from healthmodels.models import *
from django.db import connection
from rapidsms.contrib.locations.models import Location, LocationType

from poll.models import Poll, Response
from script.signals import *
from script.models import *
from django.contrib.sites.models import Site
from ntds.models import OptinWord
from ntds.utils import handle_progress
from script.utils.outgoing import check_progress
from django.core.management import call_command

class NTDSTests(TestCase): #pragma: no cover

    def setUp(self):


        #call_command("loaddata","locations.json")

        user, created = User.objects.get_or_create(username='admin')
        self.user=user
        site = Site.objects.get_or_create(pk=settings.SITE_ID, defaults={
            'domain':'example.com',
            })

        self.router=get_router()
        contact1,_=Contact.objects.get_or_create(name="foo")
        contact2,_=Contact.objects.get_or_create(name="foo2")
        backend,_=Backend.objects.get_or_create(name='TEST')
        self.connection1,_ = Connection.objects.get_or_create(identity='80001', backend=backend)
        self.connection2,_ = Connection.objects.get_or_create(identity='80002', backend=backend)
        self.connection3,_ = Connection.objects.get_or_create(identity='80004', backend=backend)
        self.connection4,_ = Connection.objects.get_or_create(identity='80005', backend=backend)
        self.connection5,_ = Connection.objects.get_or_create(identity='80006', backend=backend)
        self.connection6,_ = Connection.objects.get_or_create(identity='80007', backend=backend)


        script= Script.objects.get(
            slug="ntd_autoreg"


            )
        self.script = script
        script.sites.add(Site.objects.get_current())

        poll1,_=Poll.objects.get_or_create(name='ntds_parish',
                                  type=Poll.TYPE_TEXT,
                                  question='What is your Parish?',
                                  default_response='',
                                  user=user)

        poll2,_=Poll.objects.get_or_create(name='ntds_subcounty',
                          type=Poll.TYPE_TEXT,
                          question='What is your Subcounty?',
                          default_response='',
                          user=user)

        poll3,_=Poll.objects.get_or_create(name='ntds_district',
                          type=Poll.TYPE_TEXT,
                          question='What is your district?',
                          default_response='',
                          user=user)
        step1,_=ScriptStep.objects.get_or_create(
            script=script,
            message="Welcome to NTDs Mass drug administration program",
            order=0,
            rule=ScriptStep.WAIT_MOVEON,
            start_offset=0,
            giveup_offset=0,
            )


        script.steps.add(step1)

        step2,_=ScriptStep.objects.get_or_create(
            script=script,
            poll=poll1,
            order=1,
            rule=ScriptStep.WAIT_MOVEON,
            start_offset=0,
            giveup_offset=8640000,
            )

        script.steps.add(step2)

        step3,_=ScriptStep.objects.get_or_create(
            script=script,
            poll=poll2,
            order=2,
            rule=ScriptStep.WAIT_MOVEON,
            start_offset=0,
            giveup_offset=8640000,
            )

        script.steps.add(step3)
        step4,_=ScriptStep.objects.get_or_create(
            script=script,
            poll=poll3,
            order=3,
            rule=ScriptStep.WAIT_MOVEON,
            start_offset=0,
            giveup_offset=8640000,
            )
        script.steps.add(step4)

        OptinWord.objects.get_or_create(language="en",words="ntds")

        self.reg_xform,_ = XForm.on_site.get_or_create(name='ntd_parish', keyword='par', owner=self.user, command_prefix=None, separator = '.',
                                                          site=Site.objects.get_current(), response="The parish has been set to {{ parish }}. Please send the data for it")


        f1,_ = self.reg_xform.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Reporting Parish', command='parish', order=0)

        self.villages_targeted,_ = XForm.on_site.get_or_create(name='ntd_villages_targeted', keyword='vlg', owner=self.user, command_prefix=None, separator = '.',
                                                               site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = self.villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Vilages in Parish', command='vlg_no', order=0)
        f1,_ = self.villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Vilages Targeted', command='vlg_tgt', order=1)
        f1,_ = self.villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Vilages Treated', command='vlg_trd', order=2)
        f1,_ = self.villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Vilages Incomplete', command='vlg_incpt', order=3)


        self.villages_targeted,_ = XForm.on_site.get_or_create(name='ntd_schools_targeted', keyword='sch', owner=self.user, command_prefix=None, separator = '.',
                                                               site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = self.villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Schools in Parish', command='sch_no', order=0)
        f1,_ = self.villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Schools Targeted', command='sch_tgt', order=1)
        f1,_ = self.villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Schools Treated', command='sch_trd', order=2)
        f1,_ = self.villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Schools Incomplete', command='sch_incpt', order=3)



        self.treated_by_age,_ = XForm.on_site.get_or_create(name='ntd_treated_by_age', keyword='agg', owner=self.user, command_prefix=None, separator = '.',
                                                               site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = self.treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months male', command='trd_less_6month_male', order=0)
        f1,_ = self.treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months female', command='trd_less_6month_female', order=1)
        f1,_ = self.treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years male', command='trd_6_to_4years_male', order=2)
        f1,_ = self.treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years female', command='trd_6_to_4years_female', order=3)
        f1,_ = self.treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 male', command='trd_5_to_14_male', order=4)
        f1,_ = self.treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 female', command='trd_5_to_14_female', order=5)
        f1,_ = self.treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 male', command='trd_greater_15_male', order=6)
        f1,_ = self.treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 female', command='trd_greater_15_female', order=7)


        self.village_population_by_age,_ = XForm.on_site.get_or_create(name='ntd_village_pop_by_age', keyword='pop', owner=self.user, command_prefix=None, separator = '.',
                                                            site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = self.village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop Less Than 6 Months male', command='pop_less_6month_male', order=0)
        f1,_ = self.village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop Less Than 6 Months female', command='pop_less_6month_female', order=1)
        f1,_ = self.village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop 6 Months to 4 years male', command='pop_6_to_4years_male', order=2)
        f1,_ = self.village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop 6 Months to 4 years female', command='pop_6_to_4years_female', order=3)
        f1,_ = self.village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop 5 to 14 male', command='pop_5_to_14_male', order=4)
        f1,_ = self.village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop 5 to 14 female', command='pop_5_to_14_female', order=5)
        f1,_ = self.village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop greater than 15 male', command='pop_greater_15_male', order=6)
        f1,_ = self.village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop greater than 15 female', command='pop_greater_15_female', order=7)







        self.drugs_used,_ = XForm.on_site.get_or_create(name='ntd_drugs_used', keyword='dru', owner=self.user, command_prefix=None, separator = '.',
                                                                       site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = self.drugs_used.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='praziquantel', command='pzq', order=0)
        f1,_ = self.drugs_used.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='mebendazole', command='mbd', order=1)
        f1,_ = self.drugs_used.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='albendazole', command='alb', order=2)
        f1,_ = self.drugs_used.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='ivermectin', command='ivm', order=3)
        f1,_ = self.drugs_used.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='teo', command='tetracycline', order=4)
        f1,_ = self.drugs_used.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Zithromax syrup', command='zith_syr', order=5)
        f1,_ = self.drugs_used.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Zithromax tabs', command='zith_tabs', order=6)



        self.drugs_leftover,_ = XForm.on_site.get_or_create(name='ntd_drugs_left', keyword='drl', owner=self.user, command_prefix=None, separator = '.',
                                                        site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = self.drugs_leftover.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='praziquantel', command='pzq', order=0)
        f1,_ = self.drugs_leftover.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='mebendazole', command='mbd', order=1)
        f1,_ = self.drugs_leftover.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='albendazole', command='alb', order=2)
        f1,_ = self.drugs_leftover.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='ivermectin', command='ivm', order=3)
        f1,_ = self.drugs_leftover.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='teo', command='tetracycline', order=4)
        f1,_ = self.drugs_leftover.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Zithromax syrup', command='zith_syr', order=5)
        f1,_ = self.drugs_leftover.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Zithromax tabs', command='zith_tabs', order=6)





    def fakeIncoming(self, message, connection=None):
        if connection is None:
            connection = self.connection
        router = get_router()
        return router.handle_incoming(connection.backend.name, connection.identity, message)



    def test_registration(self):
        #fake english join message
        inmsg1=self.fakeIncoming('ntds',self.connection1)
        #make sure a scrpt progress was created
        #get a response
        #self.assertEquals(ScriptProgress.objects.count(), 1)
        prog1 = ScriptProgress.objects.get(connection=self.connection1)

        #0000

        self.assertEquals(prog1.script.slug, 'ntd_autoreg')
        check_progress(self.script)
        check_progress(self.script)
        self.assertEquals(ScriptProgress.objects.get(connection=self.connection1).step.order, 1)



        #Parish

        self.fakeIncoming('Gwengdiya',self.connection1)
        check_progress(self.script)
        self.assertEquals(ScriptProgress.objects.get(connection=self.connection1).step.order, 2)

        #subcounty
        self.fakeIncoming('Awach',self.connection1)

        check_progress(self.script)
        self.assertEquals(ScriptProgress.objects.get(connection=self.connection1).step.order, 3)

        #district

        self.fakeIncoming('Gulu',self.connection1)

        check_progress(self.script)
        self.assertEquals(ScriptProgress.objects.filter(connection=self.connection1).count(), 0)


    def test_troublesome_registration(self):
        #fake english join message
        inmsg2=self.fakeIncoming('ntds',self.connection2)
        #make sure a scrpt progress was created
        #get a response
        #self.assertEquals(ScriptProgress.objects.count(), 1)
        prog2 = ScriptProgress.objects.get(connection=self.connection2)

        #0000

        self.assertEquals(prog2.script.slug, 'ntd_autoreg')
        check_progress(self.script)
        check_progress(self.script)
        self.assertEquals(ScriptProgress.objects.get(connection=self.connection2).step.order, 1)



        #Parish

        self.fakeIncoming('Gwegdiya',self.connection2)
        check_progress(self.script)
        self.assertEquals(ScriptProgress.objects.get(connection=self.connection2).step.order, 2)

        #subcounty
        self.fakeIncoming('Awachi',self.connection2)

        check_progress(self.script)
        self.assertEquals(ScriptProgress.objects.get(connection=self.connection2).step.order, 3)

        #district

        self.fakeIncoming('Gul0',self.connection2)

        check_progress(self.script)
        self.assertEquals(ScriptProgress.objects.filter(connection=self.connection2).count(), 0)

    def parish_registration(self):
        self.fakeIncoming('par gwegdiya', connection=self.connection1)
        self.assertEquals(Message.objects.filter(connection=self.connection1,direction="O").order_by('-date')[0].text, 'You must be a reporter for FHDs. Please register first before sending any information')


    def villages_targeted_submission(self):
        self.fakeIncoming('vlg.80.29.10.2', connection=self.connection1)
        self.assertEquals(Message.objects.filter(connection=self.connection1,direction="O").order_by('-date')[0].text, 'You must be a reporter for FHDs. Please register first before sending any information')


    def schools_targeted_submission(self):
        self.fakeIncoming('sch.80.29.10.2', connection=self.connection1)
        self.assertEquals(Message.objects.filter(connection=self.connection1,direction="O").order_by('-date')[0].text, 'You must be a reporter for FHDs. Please register first before sending any information')

    def total_treated_submission(self):
        self.fakeIncoming('agg.23.15.12.8.6.5.6.8', connection=self.connection1)
        self.assertEquals(Message.objects.filter(connection=self.connection1,direction="O").order_by('-date')[0].text, 'You must be a reporter for FHDs. Please register first before sending any information')

    def drugs_used_submission(self):
        self.fakeIncoming('dru.26.45.32.0.71.5.6', connection=self.connection1)
        self.assertEquals(Message.objects.filter(connection=self.connection1,direction="O").order_by('-date')[0].text, 'You must be a reporter for FHDs. Please register first before sending any information')

    def village_population_submission(self):
        self.fakeIncoming('pop.23.15.12.8.6.5.6.8', connection=self.connection1)
        self.assertEquals(Message.objects.filter(connection=self.connection1,direction="O").order_by('-date')[0].text, 'You must be a reporter for FHDs. Please register first before sending any information')

    def drugs_leftOver_submission(self):
        self.fakeIncoming('drl.26.45.32.0.71.5.6', connection=self.connection1)
        self.assertEquals(Message.objects.filter(connection=self.connection1,direction="O").order_by('-date')[0].text, 'You must be a reporter for FHDs. Please register first before sending any information')

    def tearDown(self):
        ScriptProgress.objects.all().delete()









