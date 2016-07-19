from . import ivle_views
from django.conf.urls import url

from . import views

app_name = 'attend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^module', views.module, name='module'),
    url(r'^form_detect', views.detection, name='detect_form'),

    url(r'^ivle_login', ivle_views.login, name='ivle_login'),
    url(r'^update_module', ivle_views.update_module, name='update_module'),
    url(r'^detect', ivle_views.face_detection, name='detect'),
    url(r'^enrollment', ivle_views.enrollment, name='enrollment'),
    url(r'^verify', ivle_views.verify, name='verify'),
    url(r'^attend', ivle_views.attend, name='attend'),
]