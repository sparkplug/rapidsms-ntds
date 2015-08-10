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

        script,_= Script.objects.get_or_create(
            slug="ntd_autoreg",enabled=True


        )
        script = script
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

        reg_xform,_ = XForm.on_site.get_or_create(name='ntd_parish', keyword='par', owner=user, command_prefix=None, separator = '.',
                                                  site=Site.objects.get_current(), response="Please send the data for  {{ parish }} parish.")


        parish_field,_ = reg_xform.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Reporting Parish', command='parish', order=0)

        villages_targeted,_ = XForm.on_site.get_or_create(name='ntd_villages_targeted', keyword='vlg', owner=user, command_prefix=None, separator = '.',
                                                          site=Site.objects.get_current(), response='Thanks for your report')

        vlg_no_field,_ = villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Vilages in Parish', command='vlg_no', order=0)
        vlg_tgt_field,_ = villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Vilages Targeted', command='vlg_tgt', order=1)
        vlg_trd_field,_ = villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Vilages Treated', command='vlg_trd', order=2)
        vlg_incpt_field,_ = villages_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Vilages Incomplete', command='vlg_incpt', order=3)


        schools_targeted,_ = XForm.on_site.get_or_create(name='ntd_schools_targeted', keyword='sch', owner=user, command_prefix=None, separator = '.',
                                                         site=Site.objects.get_current(), response='Thanks for your report')

        sch_no_field,_ = schools_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Schools in Parish', command='sch_no', order=0)
        sch_tgt_field,_ = schools_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Schools Targeted', command='sch_tgt', order=1)
        sch_trd_field,_ = schools_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Schools Treated', command='sch_trd', order=2)
        f1,_ = schools_targeted.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Schools Incomplete', command='sch_incpt', order=3)



        onch_treated_by_age,_ = XForm.on_site.get_or_create(name='onch_treated_by_age', keyword='ov', owner=user, command_prefix=None, separator = '.',
                                                            site=Site.objects.get_current(), response='Thanks for your report')

        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Parish', command='parish_code', order=0)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='No of communities and schools', command='no_of_schools', order=1)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months male', command='trd_less_6month_male', order=2)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months female', command='trd_less_6month_female', order=3)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years male', command='trd_6_to_4years_male', order=4)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years female', command='trd_6_to_4years_female', order=5)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 male', command='trd_5_to_14_male', order=6)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 female', command='trd_5_to_14_female', order=7)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 male', command='trd_greater_15_male', order=8)
        onch,_ = onch_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 female', command='trd_greater_15_female', order=9)


        schi_treated_by_age,_ = XForm.on_site.get_or_create(name='schi_treated_by_age', keyword='st', owner=user, command_prefix=None, separator = '.',
                                                            site=Site.objects.get_current(), response='Thanks for your report')


        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Parish', command='parish_code', order=0)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='No of communities and schools', command='no_of_schools', order=1)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months male', command='trd_less_6month_male', order=2)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months female', command='trd_less_6month_female', order=3)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years male', command='trd_6_to_4years_male', order=4)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years female', command='trd_6_to_4years_female', order=5)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 male', command='trd_5_to_14_male', order=6)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 female', command='trd_5_to_14_female', order=7)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 male', command='trd_greater_15_male', order=8)
        fi,_ = schi_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 female', command='trd_greater_15_female', order=9)

        lf_treated_by_age,_ = XForm.on_site.get_or_create(name='lf_treated_by_age', keyword='lf', owner=user, command_prefix=None, separator = '.',
                                                          site=Site.objects.get_current(), response='Thanks for your report')

        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Parish', command='parish_code', order=0)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='No of communities and schools', command='no_of_schools', order=1)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months male', command='trd_less_6month_male', order=2)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months female', command='trd_less_6month_female', order=3)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years male', command='trd_6_to_4years_male', order=4)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years female', command='trd_6_to_4years_female', order=5)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 male', command='trd_5_to_14_male', order=6)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 female', command='trd_5_to_14_female', order=7)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 male', command='trd_greater_15_male', order=8)
        fi,_ = lf_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 female', command='trd_greater_15_female', order=9)


        fil_treated_by_age,_ = XForm.on_site.get_or_create(name='fil_treated_by_age', keyword='sc', owner=user, command_prefix=None, separator = '.',
                                                           site=Site.objects.get_current(), response='Thanks for your report')
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Parish', command='parish_code', order=0)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='No of communities and schools', command='no_of_schools', order=1)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months male', command='trd_less_6month_male', order=2)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months female', command='trd_less_6month_female', order=3)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years male', command='trd_6_to_4years_male', order=4)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years female', command='trd_6_to_4years_female', order=5)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 male', command='trd_5_to_14_male', order=6)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 female', command='trd_5_to_14_female', order=7)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 male', command='trd_greater_15_male', order=8)
        fi,_ = fil_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 female', command='trd_greater_15_female', order=9)


        trac_treated_by_age,_ = XForm.on_site.get_or_create(name='trac_treated_by_age', keyword='tr', owner=user, command_prefix=None, separator = '.',
                                                            site=Site.objects.get_current(), response='Thanks for your report')
        f1,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Parish', command='parish_code', order=0)
        f1,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='No of communities and schools', command='no_of_schools', order=1)
        trac,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months male', command='trd_less_6month_male', order=2)
        trac,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months female', command='trd_less_6month_female', order=3)
        trac,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years male', command='trd_6_to_4years_male', order=4)
        trac,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years female', command='trd_6_to_4years_female', order=5)
        trac,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 male', command='trd_5_to_14_male', order=6)
        trac,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 female', command='trd_5_to_14_female', order=7)
        trac,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 male', command='trd_greater_15_male', order=8)
        trac,_ = trac_treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 female', command='trd_greater_15_female', order=9)





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
        submission = self.xform.process_sms_submission(IncomingMessage(None, "survey +age 10 +name matt berg +gender male"))

        fields = self.xform.fields.all()
        self.failUnlessEqual(self.gender_field.pk, fields[0].pk)
        self.failUnlessEqual(self.field.pk, fields[1].pk)


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









