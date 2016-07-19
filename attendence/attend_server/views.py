from . import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    form = forms.LoginForm()
    return render(request, 'form.html', {'url': 'attend:ivle_login', 'message': 'Login Form', 'form': form})


def module(request):
    form = forms.DataForm()
    return render(request, 'form.html', {'url': 'attend:update_module', 'message': 'update_module Form', 'form': form})


def detection(request):
    form = forms.ImgForm()
    return render(request, 'form.html', {'url': 'attend:detect', 'message': 'Img Form', 'form': form})


# ----------------Private Functions-------------------

def error_response(error_code, name='', message=None):
    error_message = {
        0: message,
        1: '{} Error: Invalid input.'.format(name),
        2: 'Invalid user name or password.',
        # 3: 'Group does not exist or belong to your project',
        # 4: 'Persons do not exist or belong to your project',
        5: 'No student existed.',
    }

    response = HttpResponse(error_message.get(error_code))
    response.status_code = 406
    return response
