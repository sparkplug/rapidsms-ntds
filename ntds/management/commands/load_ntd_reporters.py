#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from rapidsms_xforms.models import *
from ntds.utils import validate_number
from rapidsms.contrib.locations.models import Location
from django.utils.safestring import mark_safe
from ntds.models import Reporter
import operator
from django.db.models import Q
import re
from rapidsms_httprouter.models import Message, Connection
from django.contrib.auth.models import User,Group
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from uganda_common.utils import assign_backend
from healthmodels.models.HealthProvider import HealthProvider
from rapidsms.models import Connection, Contact
from optparse import make_option
import django
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-f', '--file', dest='file'),)


    def handle(self, **options):
        apo=Location.objects.get(name="Yumbe",type="district").get_descendants().filter(type="sub_county",name="Apo")[0]
        yeta=Location.objects.create(name="Yeta",type="parish")
        yeta.parent=apo
        yeta.save()
        ariinga=Location.objects.create(name="Ariinga",type="parish")
        ariinga.parent=apo
        ariinga.save()
        a=Location.objects.get(name="Yumbe",type="district").get_descendants().filter(type="parish").filter(name__icontains="ariya")[0]
        a.name="aria"
        a.save()
        file = options['file']
        wb = load_workbook(filename=file)
        ws=wb.get_sheet_by_name("Community and Schools")
        for row in ws.rows[1:]:
            try:
                role, _ = Group.objects.get_or_create(name='Ntds')
                mobile_is_valid,cleaned_mobile=validate_number("0"+str(row[10].value))
                msisdn, backend = assign_backend(cleaned_mobile)
                connection, created = Connection.objects.get_or_create(identity=cleaned_mobile, backend=backend)
                district=Location.objects.filter(type="district",name__icontains= row[2].value.strip())[0]
                try:
                    pr=row[8].value.strip()
                    if pr=="Aria":
                        pr="Ariya"
                    parish=district.get_descendants().filter(type="parish",name__icontains=row[8].value.strip())[0]
                except IndexError:
                    parish=None
                    print "index error  %s"%row[8].value

                provider = HealthProvider.objects.create(name=row[8].value.strip(), location=parish)

                provider.groups.add(role)
                connection.contact = provider
                connection.save()
                rep = Reporter(healthprovider_ptr=provider)
                rep.__dict__.update(provider.__dict__)

                rep.community=row[11].value.strip()
                rep.id_number=str(row[0].value)
                rep.county=row[3].value.strip()
                rep.subcounty_supervisor=row[6].value.strip()
                _,s_mobile=validate_number(str(row[7].value))
                rep.subcounty_supervisor_mobile=s_mobile
                rep.region=row[1].value.strip()
                rep.health_subcounty=row[4].value.strip()
                rep.subcounty_name = row[2].value.strip()
                rep.parish_name = row[8].value.strip()
                rep.save()
            except (django.core.exceptions.MultipleObjectsReturned,ValidationError):
                print row[8].value
