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
from rapidsms.models import Connection, Contact,Backend
from optparse import make_option
import django
from ntds.models import Reporter,Reporter,NTDReport
import csv


import sys, traceback
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-f', '--file', dest='file'),)


    def handle(self, **options):
        reports=NTDReport.objects.all()
        errors = XFormSubmission.objects.filter(has_errors=True).values("message__text","message__connection__pk","message__connection__identity","message__application")
        import pdb;pdb.set_trace()
        error_list=[]
        for e in errors:


            edic={}
            qs=Reporter.objects.filter(connection__pk=e["message__connection__pk"])
            if qs.exists():
                reporter=qs[0]
                edic["mobile"]=e["message__connection__pk"]
                edic["text"] = e["message__text"]

                edic["reporter"]=reporter.name
                edic["mobile"] = reporter.default_connection.identity
                edic["district"] =reporter.district.name
                edic["parish"]= reporter.parish_name
                error_list.append(edic)
            else:
                edic["mobile"]=e["message__connection__pk"]
                edic["text"] = e["message__text"]

                edic["reporter"]=""
                edic["mobile"] = ""
                edic["district"] =""
                edic["parish"]= ""
                error_list.append(edic)





        with open('media/error_messages.csv', 'w') as csvfile:
            fieldnames = ['mobile', 'text', 'parish', 'district', 'reporter']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in error_list:
                writer.writerow(row)



        reps=[]
        for r in reports:
            dic={}
            dic["message"]=r.message
            dic.update(eval(r.raw))
            dic["reporter"]=r.reporter.name
            dic["mobile"] = r.reporter.default_connection.identity
            dic["district"] =r.reporter.district.name
            dic["parish"]= r.reporter.parish_name
            dic["disease"]=r.disease
            reps.append(dic)


        with open('media/raw_messages.csv', 'w') as csvfile:
            fieldnames = ['Treated 5 to 14 female', 'Treated greater than 15 female', 'No of communities and schools', 'Treated 5 to 14 male', 'mobile', 'parish', 'reporter', 'Treated Less Than 6 Months male', 'Treated 6 Months to 4 years female', 'district', 'Treated 6 Months to 4 years male', 'message', 'Treated greater than 15 male', 'Treated Less Than 6 Months female',"disease"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reps:
                writer.writerow(row)
