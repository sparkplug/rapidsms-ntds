'''
Created on Nov 23, 2014

@author: MosesM
'''
# -*- coding: utf-8 -*-
import rapidsms
import datetime

from rapidsms.apps.base import AppBase
from rapidsms_httprouter.models import Message,MessageBatch
from rapidsms.apps.base import AppBase
import datetime
import re
from django.conf import settings
from rapidsms_httprouter.router import get_router
from script.models import ScriptProgress,ScriptSession,Script
from ntds.models import gettext_db,OptinWord
from .utils import handle_progress
from healthmodels.models import HealthProvider
from .models import Reporter

class App(AppBase):

    def progress(self,message):

        progress = ScriptProgress.objects.filter(connection=message.connection, script__enabled=True).order_by('-time')
        if progress.count():
            progress = progress[0]
            res=handle_progress(progress,message)
            if res:
                message.respond(gettext_db(res,progress.language))
        return True

    def is_match(self,message):
        template = r"(.*\b(%s)\b.*)"
        optins = OptinWord.objects.values("language","words")
        optin_regs = { opt["language"]: re.compile(r"|".join(opt["words"].split(",")), re.IGNORECASE) for opt in optins for k, v in opt.items() }
        matched_script = Script.objects.filter(slug="ntd_autoreg",enabled=True).order_by("-pk")
        for lan,reg in optin_regs.items():
            match = reg.search(message.text.lower())
            if match:
                return (True,matched_script[0])


        return (False,None)




    def handle_keyword_match(self,message,script):
        connection=message.connection
        if not connection.contact:
            contact = HealthProvider.objects.create()
            connection.contact=contact
            rep=Reporter.objects.create(healthprovider_ptr=contact)

        prog,_ = ScriptProgress.objects.get_or_create(script=script, connection=message.connection)
        prog.time=datetime.datetime.now()
        prog.save()
        prog.language = 'en'
        ScriptSession.objects.create(script=script, connection=message.connection)
        prog.save()
        return True



    def handle (self, message):

        if not message.connection.contact:
            match,script=self.is_match(message)

            if match:
                self.handle_keyword_match(message,script)
                return True


            elif ScriptProgress.objects.filter(connection=message.connection, script__enabled=True).exists():
                self.progress(message)
                return True


