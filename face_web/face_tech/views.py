from . import forms
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    message = ""
    if 'message' in request.GET:
        message = request.GET['message']

    return render(request, 'index.html', {'message': message})


def get_start(request):
    return render(request, 'getstart.html')


def apis(request):
    return render(request, 'apis.html')


def image_form(request):
    form = forms.MultiPurposeForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:check_quality', 'message': 'Face Detection', 'form': form})


def project_form(request):
    form = forms.ProjectForm()
    return render(request, 'simple/form_csrf.html', {'url': 'face_tech:create_project',
                                                     'message': 'Create project form', 'form': form})


def login_project(request):
    form = forms.LoginProjectForm()
    return render(request, 'simple/form_csrf.html', {'url': 'face_tech:authentication',
                                                     'message': 'Login Project Form', 'form': form})


@login_required(login_url='/face_tech/loginproject')
def change_password_form(request):
    form = PasswordChangeForm(user=request.user)
    return render(request, 'simple/form_csrf.html', {'url': 'face_tech:change_password',
                                                     'message': 'Create project form', 'form': form})


@login_required(login_url='/face_tech/loginproject')
def project_info(request):
    return render(request, 'about.html', {'message': 'Project Profile'})


def group_form(request):
    form = forms.GroupForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:create_group',
                                                'message': 'Create group form', 'form': form})


def delete_group_form(request):
    form = forms.DeleteGroupForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:delete_group',
                                                'message': 'Delete group form', 'form': form})


def person_form(request):
    form = forms.PersonForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:create_person',
                                                'message': 'Create person form (only numbers, letters and .@;+- will be allowed, '
                                                           + '";" is used to separate different persons)',
                                                'form': form})


def get_person_by_group_form(request):
    form = forms.PersonByGroupForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:get_persons_by_group',
                                                'message': 'Get persons by group id', 'form': form})


def get_person_by_project_form(request):
    form = forms.PersonByProjectForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:get_all_persons',
                                                'message': 'Get persons by Project', 'form': form})


def delete_person_form(request):
    form = forms.DeletePersonForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:delete_person',
                                                'message': 'Delete person form (";" is used to separate different person ids)',
                                                'form': form})


def person_to_group_form(request):
    form = forms.PersonToGroupForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:relate_person_to_group',
                                                'message': 'Add persons to group form. '
                                                           + 'Use ";" to separate different persons.', 'form': form})


def delete_person_group_form(request):
    form = forms.PersonToGroupForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:delete_person_from_group',
                                                'message': 'Delete persons from group form. '
                                                           + 'Use ";" to separate different persons.', 'form': form})


def enrollment_form(request):
    form = forms.EnrollmentForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:enrollment',
                                                'message': 'Enrollment form.', 'form': form})


def verification_form(request):
    form = forms.VerificationForm()
    return render(request, 'simple/form.html', {'url': 'face_tech:verification',
                                                'message': 'Verification form.', 'form': form})


# ----------------Private Functions-------------------

def redirect_index(message):
    return HttpResponseRedirect(reverse('face_tech:index') + '?message=' + message)


def error_response(error_code, name='', message=''):
    error_message = {
        0: '{}: {}'.format(name, message),
        1: 'Error: {} Invalid input. {}'.format(name, message),
        2: 'Project or security key is Invalid.',
        3: 'Group does not exist or belong to your project {}'.format(name),
        4: 'Persons do not exist or belong to your project {}'.format(name),
        5: 'No face detected in image or No person exists.',
        6: 'No person exists.',
    }

    response = HttpResponse(error_message.get(error_code))
    response.status_code = 406
    return response


