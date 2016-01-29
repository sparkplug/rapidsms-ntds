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
from multiprocessing import Process

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-s', '--start', dest='start'),)


    def fakeIncoming(self, message, connection=None):

        msg=self.router.handle_incoming(connection.backend.name, connection.identity, message)
        return msg


    def process(self, message):
        print message.pk
        start=options['start']
        router=get_router()
        txt=message.text.lower()
        print txt
        msg=txt.split("ntd")[1].strip()
        try:
            keyword,rest=msg.replace(" ",".").split(".",1)
            rest=rest.strip().replace("o","0").replace(" ",".").replace("i","1").replace("t06969","").replace("0v","ov").replace("..",".").replace("to6969","")
            msg=keyword+"."+rest
            word_list=msg.split(".")
            if len(word_list)==9:
                word_list.insert(1,"1")
                msg=".".join(word_list)


            router.handle_incoming(message.connection.backend.name, message.connection.identity, msg)
            lastest=Message.objects.order_by("-pk")[0]
            message.application=lastest.pk
            message.save()
            print "...............................",msg
        except ValueError:
            print "Error................................................ ,",msg

    def handle(self, **options):
        from multiprocessing import Pool
        messages = list(Message.objects.filter(text__istartswith="ntd").filter(direction="I").filter(pk__gt=int(start)).order_by("pk"))
        map(self.process, messages)








