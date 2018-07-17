from django.conf.urls import url
from . import views
from . import operate
from . import facial

app_name = 'face_tech'
urlpatterns = [
    # url path, function name, shortcut name

    # ---------------------- views.py -----------------------
    url(r'^$', views.index, name='index'),
    url(r'^getstart', views.get_start, name='get_start'),
    url(r'^apis', views.apis, name='apis'),

    url(r'^imageform', views.image_form, name='image_form'),
    url(r'^projectform', views.project_form, name='project_form'),
    url(r'^loginproject', views.login_project, name='login_project'),
    url(r'^changepassword', views.change_password_form, name='change_password_form'),
    url(r'^projectinfo', views.project_info, name='project_info'),

    url(r'^groupform', views.group_form, name='group_form'),
    url(r'^deletegroupform', views.delete_group_form, name='delete_group_form'),

    url(r'^personform', views.person_form, name='person_form'),
    url(r'^deletepersonform', views.delete_person_form, name='delete_person_form'),
    url(r'^getpersonbygroupform', views.get_person_by_group_form, name='get_person_by_group_form'),
    url(r'^getpersonbyprojectform', views.get_person_by_project_form, name='get_person_by_project_form'),

    url(r'^persontogroupform', views.person_to_group_form, name='person_to_group_form'),
    url(r'^deletepersonfromgroupform', views.delete_person_group_form, name='delete_person_group_form'),

    url(r'^enrollmentform', views.enrollment_form, name='enrollment_form'),
    url(r'^verificationform', views.verification_form, name='verification_form'),

    # ---------------------- operate.py -----------------------
    url(r'^create_project', operate.create_project, name='create_project'),
    url(r'^change_psw', operate.change_password, name='change_password'),
    url(r'^authentication', operate.authentication, name='authentication'),
    url(r'^logout_project', operate.logout_project, name='logout_project'),

    url(r'^create_group', operate.create_group, name='create_group'),
    url(r'^get_groups_by_name', operate.get_groups_by_name, name='get_groups_by_name'),
    url(r'^delete_group', operate.delete_group, name='delete_group'),

    url(r'^create_person', operate.create_person, name='create_person'),
    url(r'^create_json_person', operate.create_json_person, name='create_json_person'),
    url(r'^delete_person', operate.delete_person, name='delete_person'),
    url(r'^get_persons_by_group', operate.get_persons_by_group, name='get_persons_by_group'),
    url(r'^get_all_persons', operate.get_all_persons, name='get_all_persons'),

    url(r'^person_to_group', operate.relate_person_to_group, name='relate_person_to_group'),
    url(r'^remove_person_from_group', operate.delete_person_from_group, name='delete_person_from_group'),

    # ---------------------- facial.py -----------------------
    url(r'^detect', facial.detect, name='detect'),
    url(r'^landmark', facial.landmark, name='landmark'),
    url(r'^occluder', facial.occluder, name='occluder'),

    url(r'^check_quality', facial.check_quality, name='check_quality'),
    url(r'^enrollment_faces', facial.enrollment, name='enrollment'),
    url(r'^verification_faces', facial.verification, name='verification'),
]
