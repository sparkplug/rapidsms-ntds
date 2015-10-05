from celery.task import Task, task
from django.conf import settings
import json
import requests
import urllib



@task
def send_message(text,mobile):
    rest=urllib.urlencode({"sms_content":text,"destinations":mobile})
    requests.get(settings.SEND_API+"&"+rest)