from django.conf.urls.defaults import *
try:
    from mtrack.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required
from generic.views import *
from .views import view_submissions,dashboard,view_messages,manage_reporters,view_analytics,reports


urlpatterns = patterns('',

    url(r'^ntds/dashboard$', login_required(dashboard), name='ndts-dashboard'),
    url(r'^ntds/messages/?$', login_required(view_messages), name='messages'),
    url(r'^ntds/(?P<reporter_id>\d+)/submissions/$', login_required(view_submissions), name='ntd-submissions'),
    url(r'^ntds/reporters/?$', login_required(manage_reporters), name='messages'),
    url(r'^ntds/submissions/?$', login_required(view_submissions), name='submissions'),
    url(r'^ntds/submissions/(?P<reporter_id>\d+)/?$', login_required(view_submissions), name='submissions'),
    url(r'^ntds/messages/?$', login_required(view_messages), name='messages'),
    url(r'^ntds/analytics/?$', login_required(view_analytics), name='analytics'),
    url(r'^ntds/reports/?$', login_required(reports), name='analytics'),
    url(r'^ntds/messages/(?P<reporter_id>\d+)/?$', login_required(view_messages), name='messages'),


)
