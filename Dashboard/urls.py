from django.conf.urls import url
from . import views
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^$', views.Landing),
    url(r'^signup/$', views.Signup),
    url(r'^login/$', views.Login),
    url(r'^logout/$', views.Logout),
    url(r'api/getTasks/$', views.getTasks),
    url(r'api/getEvents/$', views.getEvents),
    url(r'api/getAllUnits/$', views.getAllUnits),
    url(r'api/getCustomUnits/$', views.getCustomUnits),
    url(r'api/getJobs/$', views.getJobs),
    url(r'api/extensions/$', views.extensions),
    url(r'dashboard/$', views.Dashboard),
    url(r'api/extensions/$', views.Dashboard),
    url(r'settings/$', views.Settings),
]
