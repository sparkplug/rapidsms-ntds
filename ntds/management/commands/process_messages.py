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
from rapidsms_httprouter.router import get_router

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-f', '--file', dest='file'),)


    def fakeIncoming(self, message, connection=None):

        msg=self.router.handle_incoming(connection.backend.name, connection.identity, message)
        return msg


    def handle(self, **options):
        router=get_router()
        messages = Message.objects.filter(text__istartswith="ntd")

        for message in messages:
            txt=message.text.lower()
            print txt
            msg=txt.split("ntd")[1].strip()
            try:
                keyword,rest=msg.replace(" ",".").split(".",1)
                rest=rest.strip().replace("o","0").replace(" ",".").replace("i","1").replace("t06969","").replace("to6969","")
                msg=keyword+"."+rest
                router.handle_incoming(message.connection.backend.name, message.connection.identity, msg)
                print "...............................",msg
            except ValueError:
                print "Error................................................ ,",msg
          





