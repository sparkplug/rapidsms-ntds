from celery.task import Task, task
from celery.registry import tasks
from rapidsms_httprouter.router import get_router
from django.conf import settings
import json
import requests
from requests.auth import HTTPBasicAuth
import csv
from rapidsms.models import Contact, Connection, Backend
from datetime import *; from dateutil.relativedelta import *
from django.db import transaction
import urllib
from celery.contrib import rdb



@task
def send_message(text,mobile):
    rdb.set_trace()
    rest=urllib.urlencode({"sms_content":text,"destinations":mobile})
    requests.get(settings.SEND_API+"&"+rest)