import random, string, logging, traceback, json
from . import views, forms, models
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
log = logging.getLogger(__name__)


def create_project(request):
    form = forms.ProjectForm(request.POST)
    message = 'Error. Please correct or complete all required fields.'

    if form.is_valid():
        sec_key = get_securitykey()
        try:
            project = User.objects.create_user(form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['password'])
            project.first_name = form.cleaned_data['owner']
            project.last_name = sec_key
            project.save()

            return views.redirect_index('Project registered successfully! Hi '
                                            + request.POST['owner']+'. Security Key is ' + sec_key
                                            + ', Your project key is ' + str(project.id))
        except:
            log.error(traceback.format_exc())
            message = 'Please try again with different information.'

    return render(request, 'face_tech/form_csrf.html',
                  {'url': 'face_tech:create_project', 'message': 'Create project form',
                   'error_message':message, 'form': form})


def authentication(request):
    form = forms.LoginProjectForm(request.POST)
    message = 'Error, please login again.'

    if form.is_valid():
        project_name, pswd = form.cleaned_data['name'], form.cleaned_data['password']

        user = authenticate(username=project_name, password=pswd)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                return views.redirect_index('Your Security Key is ' + request.user.last_name
                                            + ', project key is ' + str(request.user.id))
            else:
                message = 'The password is valid, but the account has been disabled!'
        else:
            # the authentication system was unable to verify the username and password
            message = 'The username and password were incorrect.'

    return render(request, 'face_tech/form_csrf.html',
                  {'url': 'face_tech:authentication', 'message': 'Login Project Form',
                               'error_message':message, 'form': form})


def logout_project(request):
    logout(request)
    return views.redirect_index("User log out!")


def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)

    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)

        return views.redirect_index("Your password has been changed.")

    return views.redirect_index("Please provide correct new password.")


# ---------------- API Functions -------------------

@csrf_exempt
def create_group(request):
    """
    Pass project_name and security_key to authenticate, then create new group
    """
    form = forms.GroupForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])

        if project:
            group = models.add_or_get_group(form.cleaned_data['name'], project, description=form.cleaned_data['desc'])

            return JsonResponse({'data': group.id if group else None})
        else:
            return views.error_response(2)

    return views.error_response(1, name=create_group.__name__, message=form.errors)


@csrf_exempt
def get_groups_by_name(request):
    """
    Pass project_name and security_key to authenticate, then create new group
    """
    form = forms.GroupForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])

        if project:
            try:
                group_name = models.get_real_name(form.cleaned_data['name'], project)
                gs = models.Group.objects.filter(name__contains=group_name)
                groups = []

                for g in gs:
                    groups.append(g.to_dict())

                return JsonResponse({'data': groups})
            except:
                log.error(traceback.format_exc())
        else:
            return views.error_response(2)

    return views.error_response(1, name=get_groups_by_name.__name__, message=form.errors)


@csrf_exempt
def create_person(request):
    """
    Create persons with project_name or group_name. (person names separate with ';')
    """
    form = forms.PersonForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        group = form.cleaned_data["group"]

        if project:
            if group:
                group = models.get_group_from_project(group, project)
                if not group:
                    return views.error_response(3)

            name = form.cleaned_data['name'].split(';')
            email = form.cleaned_data['email'].split(';')
            first_name = form.cleaned_data['first_name'].split(';')
            last_name = form.cleaned_data['last_name'].split(';')
            note = form.cleaned_data['note'].split(';')
            pid = []

            for n in range(len(name)):
                em = email[n] if len(email) > n else ''
                fn = first_name[n] if len(first_name) > n else ''
                ln = last_name[n] if len(last_name) > n else ''
                nt = note[n] if len(note) > n else ''

                person = models.add_or_get_person(name=name[n], project=project, email=em, first_name=fn, last_name=ln, note=nt)
                pid.append(person.id if person else None)

                if group and person:
                    models.Person_To_Group.objects.get_or_create(person=person, group=group)

            if pid:
                return JsonResponse({'data': pid})
        else:
            return views.error_response(2)

    return views.error_response(1, name=create_person.__name__, message=form.errors)


@csrf_exempt
def create_json_person(request):
    """
    Create persons with project_name or group_name. (person names separate in json format)
    """
    form = forms.MultiPurposeForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        group = form.cleaned_data["group"]

        if project:
            if group:
                group = models.get_group_from_project(group, project)
                if not group:
                    return views.error_response(3)

            try:
                # might raise error if wrong formate of json
                data = json.loads(form.cleaned_data['data'])
                pid = []

                for d in data:
                    # if None, then set to empty string
                    name = d.get('name')
                    em = d.get('email') if d.get('email') else ''
                    fn = d.get('first_name') if d.get('first_name') else ''
                    ln = d.get('last_name') if d.get('last_name') else ''
                    nt = d.get('note') if d.get('note') else ''

                    person = models.add_or_get_person(name=name, project=project, email=em, first_name=fn, last_name=ln, note=nt)

                    pid.append(person.id if person else None)

                    if group and group:
                        models.Person_To_Group.objects.get_or_create(person=person, group=group)

                if pid:
                    return JsonResponse({'data': pid})
            except:
                log.error(traceback.format_exc())
        else:
            return views.error_response(2)

    return views.error_response(1, name=create_json_person.__name__, message=form.errors)


@csrf_exempt
def relate_person_to_group(request):
    """
    Provide person ids and group_name to relate each other. (person ids separate with ';')
    """
    form = forms.PersonToGroupForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        group = form.cleaned_data["group"]

        if project:
            group = models.get_group_from_project(group, project)
            if group:
                person_ids = [int(person) for person in form.cleaned_data['person'].split(';')]
                persons = models.get_persons_from_project_by_ids(person_ids, project)

                if persons:
                    for p in persons:
                        models.Person_To_Group.objects.get_or_create(group=group, person=p)

                    return JsonResponse({'data': True})
                else:
                    return views.error_response(4)
            else:
                return views.error_response(3, name=project.username)
        else:
            return views.error_response(2)

    return views.error_response(1, name=relate_person_to_group.__name__, message=form.errors)


@csrf_exempt
def get_persons_by_group(request):
    """
    Return persons by group id
    """
    print("get person by group")
    form = forms.PersonByGroupForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])

        if project:
            group = models.get_group_from_project(form.cleaned_data["group"], project)

            if group:
                persons = [ptp.person for ptp in
                           models.Person_To_Group.objects.filter(group_id=group).order_by('person__name')]
                data = []

                for p in persons:
                    p_dict = p.to_dict()
                    p_dict['enrolled'] = len(models.Face.objects.filter(person=p)) > 0
                    data.append(p_dict)

                return JsonResponse({'data': data})

            else:
                return views.error_response(3, name=project.username)
        else:
            return views.error_response(2)

    return views.error_response(1, name=get_persons_by_group.__name__, message=form.errors)


@csrf_exempt
def get_all_persons(request):
    """
    Return persons by project
    """
    form = forms.PersonByProjectForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])

        if project:
            persons = models.Person.objects.filter(project=project).order_by('name').distinct()
            data = []

            for p in persons:
                data.append(p.to_dict())

            return JsonResponse({'data': data})

        else:
            return views.error_response(2)

    return views.error_response(1, name=get_all_persons.__name__, message=form.errors)


@csrf_exempt
def delete_person(request):
    """
    Delete persons with provide project key and security key
    """
    form = forms.DeletePersonForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        if project:
            person_ids = [int(person) for person in form.cleaned_data['person'].split(';')]
            data = []

            for pid in person_ids:
                person = models.get_persons_from_project_by_ids(pid, project)
                if person:
                    data.append({pid: True})
                    person.delete()
                else:
                    data.append({pid: False})

            if data:
                return JsonResponse({'data': data})
        else:
            return views.error_response(2)

    return views.error_response(1, name=get_all_persons.__name__, message=form.errors)


@csrf_exempt
def delete_group(request):
    """
    Delete one group with provide project key and security key
    """
    form = forms.DeleteGroupForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        group = form.cleaned_data["group"]

        if project:
            group = models.get_group_from_project(group, project)
            if group:
                group.delete()
                return JsonResponse({'data': True})
            else:
                return views.error_response(3, name=project.username)
        else:
            return views.error_response(2)

    return views.error_response(1, name=delete_group.__name__, message=form.errors)


@csrf_exempt
def delete_person_from_group(request):
    """
    Provide person ids and group_name to relate each other. (person ids separate with ';')
    """
    form = forms.PersonToGroupForm(request.POST)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        group = form.cleaned_data["group"]

        if project:
            group = models.get_group_from_project(group, project)

            if group:
                person_ids = [int(person) for person in form.cleaned_data['person'].split(';')]
                persons = models.get_persons_from_project_by_ids(person_ids, project)

                if persons:
                    data = []
                    for p in persons:
                        try:
                            ptp = models.Person_To_Group.objects.get(person=p, group=group)
                            data.append({p.id: True})
                            ptp.delete()
                        except:
                            log.error(traceback.format_exc())
                            data.append({p.id: False})

                    if data:
                        return JsonResponse({'data': data})
                else:
                    return views.error_response(4, name=project.username)
            else:
                return views.error_response(3, name=project.username)
        else:
            return views.error_response(2)

    return views.error_response(1, name=delete_person_from_group.__name__, message=form.errors)


def delete_project(request):
    pass


# ----------------Private Functions-------------------

def get_securitykey(size=8):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase +
                                                string.ascii_uppercase +
                                                string.digits) for _ in range(size))
