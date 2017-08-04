from django.conf.urls import url
from django.views.generic import DetailView
from . import views
from core.models import Work, Comm
from core.views import WorkList, HomePage, CommList


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', HomePage.as_view()),
    url(r'^works/$', WorkList.as_view()),
    url(r'^work/(?P<pk>\d+)$', DetailView.as_view(model=Work, template_name='core/work.html')),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/success/$', views.success, name='success'),
    url(r'^blog/$', CommList.as_view()),
    url(r'^blog/(?P<pk>\d+)$', DetailView.as_view(model=Comm, template_name='core/comm.html')),
]