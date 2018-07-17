from . import views
from . import ivle_views
from . import attend_views
from django.conf.urls import url


app_name = 'attend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^form_update_module', views.update_module_form, name='update_module'),
    url(r'^form_detect', views.detection, name='detect_form'),
    url(r'^form_new_module', views.module_form, name='module_form'),
    url(r'^form_new_tutor', views.tutor_form, name='tutor_form'),
    url(r'^form_student', views.student_form, name='student_form'),
    url(r'^signin', views.create_user_form, name='create_user_form'),
    url(r'^login', views.login_form, name='login_form'),

    url(r'^logout', views.log_out, name='log_out'),
    url(r'^register', views.sign_in, name='sign_in'),
    url(r'^user_index', views.user_index, name='user_index'),
    url(r'^detect', views.face_detection, name='detect'),
    url(r'^enrollment', views.enrollment, name='enrollment'),
    url(r'^verify', views.verify, name='verify'),
    url(r'^attendance', views.attend, name='attend'),
    url(r'^create_module', views.create_module, name='create_module'),
    url(r'^create_student', views.create_student, name='create_student'),
    url(r'^add_tutor', views.add_tutor, name='add_tutor'),
    url(r'^view', views.view_module, name='view_module'),

    url(r'^attend_login', attend_views.log_in, name='attend_login'),
    url(r'^attend_module', attend_views.update_module, name='attend_module'),

    url(r'^ivle_login', ivle_views.log_in, name='ivle_login'),
    url(r'^ivle_module', ivle_views.update_module, name='update_module'),
]
