from django.conf.urls.defaults import *
try:
    from mtrack.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required
from generic.views import *
from .views import view_submissions,dashboard,view_messages,new_reporter,view_districts,view_diseases,upload_reporters,manage_reporters,get_all_parishes,get_all_subcounties


urlpatterns = patterns('',

    url(r'^ntds/dashboard$', login_required(dashboard), name='ndts-dashboard'),
    url(r'^ntds/messages/?$', login_required(view_messages), name='messages'),
    url(r'^ntds/(?P<reporter_id>\d+)/submissions/$', login_required(view_submissions), name='ntd-submissions'),
    url(r'^ntds/reporters/?$', login_required(manage_reporters), name='messages'),
    url(r'^ntds/reporters/new/?$', login_required(new_reporter), name='messages'),
    url(r'^ntds/reporters/upload/?$', login_required(upload_reporters), name='messages'),
    url(r'^ntds/submissions/?$', login_required(view_submissions), name='submissions'),
    url(r'^ntds/submissions/(?P<reporter_id>\d+)/?$', login_required(view_submissions), name='submissions'),
    url(r'^ntds/messages/?$', login_required(view_messages), name='messages'),
    url(r'^ntds/districts/report/?$', login_required(view_districts), name='analytics'),
    url(r'^ntds/diseases/report/?$', login_required(view_diseases), name='analytics'),
    url(r'^ntds/messages/(?P<reporter_id>\d+)/?$', login_required(view_messages), name='messages'),
    url(r'^ntds/get_parishes/', login_required(get_all_parishes), name='parishes'),
    url(r'^ntds/get_subcounties/', login_required(get_all_subcounties), name="subcounties"),


)
