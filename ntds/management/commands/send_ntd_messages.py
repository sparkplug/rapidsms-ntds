#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from rapidsms_xforms.models import *
from rapidsms_httprouter.models import Message

from django.db import transaction
from rapidsms_httprouter.models import Message
import requests
from ntds.tasks import send_message


class Command(BaseCommand):
    help = """ Send out messages
    """

    def sendall(self):

        try:
            transaction.enter_transaction_management()
            msgs= Message.objects.filter(direction='O',status__in=['Q','P'])
            for msg in msgs:
                send_message.delay(msg.text,msg.connection.identity)
            msgs.update(status='S')
        except Exception, exc:
            print exc
            transaction.rollback()

    def handle(self, **options):
        self.sendall()