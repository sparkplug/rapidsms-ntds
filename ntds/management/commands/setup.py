#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from rapidsms_httprouter.router import get_router
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


class Command(BaseCommand):
    help = """ Loadmission sites
    """


    def handle(self, **options):

        user = User.objects.get(username='admin')
        role,_=Group.objects.get_or_create(name="Ntds")

        site = Site.objects.all()[0]

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



        treated_by_age,_ = XForm.on_site.get_or_create(name='ntd_treated_by_age', keyword='agg', owner=user, command_prefix=None, separator = '.',
                                                            site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months male', command='trd_less_6month_male', order=0)
        f1,_ = treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated Less Than 6 Months female', command='trd_less_6month_female', order=1)
        f1,_ = treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years male', command='trd_6_to_4years_male', order=2)
        f1,_ = treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 6 Months to 4 years female', command='trd_6_to_4years_female', order=3)
        f1,_ = treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 male', command='trd_5_to_14_male', order=4)
        f1,_ = treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated 5 to 14 female', command='trd_5_to_14_female', order=5)
        f1,_ = treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 male', command='trd_greater_15_male', order=6)
        f1,_ = treated_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Treated greater than 15 female', command='trd_greater_15_female', order=7)


        village_population_by_age,_ = XForm.on_site.get_or_create(name='ntd_village_pop_by_age', keyword='pop', owner=user, command_prefix=None, separator = '.',
                                                                       site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop Less Than 6 Months male', command='pop_less_6month_male', order=0)
        f1,_ = village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop Less Than 6 Months female', command='pop_less_6month_female', order=1)
        f1,_ = village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop 6 Months to 4 years male', command='pop_6_to_4years_male', order=2)
        f1,_ = village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop 6 Months to 4 years female', command='pop_6_to_4years_female', order=3)
        f1,_ = village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop 5 to 14 male', command='pop_5_to_14_male', order=4)
        f1,_ = village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop 5 to 14 female', command='pop_5_to_14_female', order=5)
        f1,_ = village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop greater than 15 male', command='pop_greater_15_male', order=6)
        f1,_ = village_population_by_age.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='Pop greater than 15 female', command='pop_greater_15_female', order=7)







        alb_usage,_ = XForm.on_site.get_or_create(name='Alb Usage', keyword='alb', owner=user, command_prefix=None, separator = '.',
                                                       site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = alb_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='alb_used', command='used', order=0)
        f1,_ = alb_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='alb_left', command='left', order=1)


        ivm_usage,_ = XForm.on_site.get_or_create(name='Ivm Usage', keyword='ivm', owner=user, command_prefix=None, separator = '.',
                                                       site=Site.objects.get_current(), response='Thanks for your report')
        f1,_ = ivm_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='ivm_used', command='used', order=0)
        f1,_ = ivm_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='ivm_left', command='left', order=1)

        pzq_usage,_ = XForm.on_site.get_or_create(name='PZQ Usage', keyword='pzq', owner=user, command_prefix=None, separator = '.',
                                                       site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = pzq_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='pzq_used', command='used', order=0)
        f1,_ = pzq_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='pzq_left', command='left', order=1)

        mbd_usage,_ = XForm.on_site.get_or_create(name='MBD Usage', keyword='mbd', owner=user, command_prefix=None, separator = '.',
                                                       site=Site.objects.get_current(), response='Thanks for your report')
        f1,_ = mbd_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='mbd_used', command='used', order=0)
        f1,_ = mbd_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='mbd_left', command='left', order=1)

        tet_usage,_ = XForm.on_site.get_or_create(name='Tet Usage', keyword='ttr', owner=user, command_prefix=None, separator = '.',
                                                       site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = tet_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='tet_used', command='used', order=0)
        f1,_ = tet_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='tet_left', command='left', order=1)


        ziths_usage,_ = XForm.on_site.get_or_create(name='Zith Syrup usage', keyword='ziths', owner=user, command_prefix=None, separator = '.',
                                                         site=Site.objects.get_current(), response='Thanks for your report')

        f1,_ = ziths_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='ziths_used', command='used', order=0)
        f1,_ = ziths_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='ziths_left', command='left', order=1)

        zitht_usage,_ = XForm.on_site.get_or_create(name='zith Tab Usage', keyword='zitht', owner=user, command_prefix=None, separator = '.',
                                                         site=Site.objects.get_current(), response='Thanks for your report')


        f1,_ = zitht_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='zitht_used', command='used', order=0)
        f1,_ = zitht_usage.fields.get_or_create(field_type=XFormField.TYPE_TEXT, name='zitht_left', command='left', order=1)





















