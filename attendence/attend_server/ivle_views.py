from .apps import API_KEY, api
from .apps import error_response
from . import forms, pyivle, models
from django.http import JsonResponse
import base64, logging, traceback, json
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger(__name__)


@csrf_exempt
def log_in(request):
    """ Login with ivle username and password """
    form = forms.LoginForm(request.POST)

    if form.is_valid():
        try:
            # Authenticate for IVLE
            data, modules = login_ivle(form.cleaned_data['username'], form.cleaned_data['password'])
            data['Modules'] = []

            for m in modules:
                m_data = m
                group = api.get_groups_by_name(name=m.get('ID'))

                if group:
                    m_data['face_group_id'] = group[0].get('id')
                else:
                    # Initial new modules, create group in face
                    group_id = api.create_group(name=m.get('ID'),
                                                desc=' '.join([m.get('CourseCode'), m.get('CourseName')]))
                    m_data['face_group_id'] = group_id

                data['Modules'].append(m_data)

            return JsonResponse({'data': data})
        except:
            log.error(traceback.format_exc())
    return error_response(2)


@csrf_exempt
def update_module(request):
    """ When choose one module, provide module profile and AuthToken
        to update student list from ivle to face server
    """
    form = forms.DataForm(request.POST)

    if form.is_valid():
        try:
            data = json.loads(form.cleaned_data['data'])

            # return person profile order by person name
            exist_list = api.get_persons_by_group(group=data.get('face_group_id'))
            new_list = get_students(form.cleaned_data['token'], data.get('ID'))

            # Relationship with data between face and ivle:
            # face: name -> IVLE: UserID - A0123456
            # face: first_name -> IVLE: Name - James Smith
            # face: note -> IVLE: UserGuid - xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

            if data and new_list:
                # if has no persons in face, initial with a empty list
                exist_list = exist_list if exist_list else []

                # Sort new_list by UserID
                new_list = [(dict_['UserID'], dict_) for dict_ in new_list]
                new_list.sort()
                new_list = [dict_ for (key, dict_) in new_list]

                # iterate to match with each other
                new_p, old_p = 0, 0
                new, old = [False]*len(new_list), [False]*len(exist_list)

                while old_p < len(exist_list) and new_p < len(new_list):
                    if new_list[new_p].get('UserID') == exist_list[old_p].get('name'):
                        new[new_p] = True
                        old[old_p] = True
                        new_p += 1
                    elif new_list[new_p].get('UserID') < exist_list[old_p].get('name'):
                        new_p += 1
                        old_p -= 1

                    old_p += 1

                # Add new item to face database
                updated_list, add_list = [], []

                for i in range(len(new)):
                    if new[i] is False:
                        # todo if need more fields
                        add_list.append({'name': new_list[i].get('UserID'),
                                         'email': new_list[i].get('Email'),
                                         'first_name': new_list[i].get('Name'),
                                         'note': new_list[i].get('UserGuid')})

                if add_list:
                    new_persons_id = api.create_json_person(data=add_list, group=data.get('face_group_id'))

                    if new_persons_id:
                        if None in new_persons_id:
                            data['error_add'] = []

                        for i in range(len(new_persons_id)):
                            if new_persons_id[i] is None:
                                data['error_add'].append(dict(add_list[i]))

                            else:
                                updated_list.append(dict(add_list[i]))
                                updated_list[-1]['id'] = int(new_persons_id[i])
                    else:
                        data['error_add'] = add_list

                for i in range(len(old)):
                    if old[i] is True:
                        updated_list.append(dict(exist_list[i]))

                # Delete relation of item to group, not delete items
                for i in [j for j in range(len(old)) if old[j] is True][::-1]:
                    del exist_list[i]

                if exist_list:
                    delete_result = api.remove_person_from_group(person=[i.get('id') for i in exist_list],
                                                                 group=data.get('face_group_id'))

                    if delete_result:
                        if False in [list(d.values())[0] for d in delete_result]:
                            data['error_delete'] = []

                            for i in range(len(delete_result)):
                                data['error_delete'].append(list(delete_result[i].keys())[0])
                    else:
                        data['error_delete'] = exist_list

                del exist_list, new_list, add_list
                data['student'] = updated_list
                data['attendance'] = models.get_records(data.get('ID'))

                if data.get('CourseCode') == 'CS1231':
                    data['tutorial'] = get_tutorial_from_txt(updated_list)

            else:
                data['student'] = []
                data['attendance'] = []

            return JsonResponse({'data': data})

        except:
            log.error(traceback.format_exc())

    return error_response(1, name='update_module')


# ----------------Private Functions-------------------


def login_ivle(username, password):
    """ Get user profile and teaching modules with provided username and password"""
    # Authenticate for IVLE
    p = pyivle.Pyivle(API_KEY)
    p.login(username, password)  # base64.b64decode())

    # Get your name, user ID and profile
    profile = p.profile_view()['Results'][0]
    profile['authToken'] = p.authToken

    # List teaching modules
    modules = get_teaching_modules(p.modules())

    return profile, modules


def get_teaching_modules(modules):
    """ Filter out ivle modules has teaching permision
    :param modules: return value from modules() without namedtuple
    :return list of modules with essential attributes
    """
    result = []

    for m in modules.get('Results'):
        if m.get('Permission') in ['O', 'F', 'M', 'R']:  # , 'S']: for teseting
            needed = {}
            # filter out needed attributes of modules
            for attr in ['ID', 'CourseName', 'CourseCode',  # 'hasClassRosterItems', 'hasGuestRosterItems',
                         'CourseAcadYear', 'CourseSemester', 'Permission']:
                needed[attr] = m.get(attr)

            result.append(needed)
    return result


def get_students(token, module_id):
    """ get latest student list from ivle"""
    p = pyivle.Pyivle(API_KEY, authToken=token)

    # auth if p has permission to access module todo
    # change to class_roster after testing todo
    return p.class_roster(module_id).get('Results')


def get_tutorial_from_txt(students):
    """ from txt file extract tutorial list
        students is a sorted list
    """
    import os, ast
    from django.conf import settings
    from django.contrib.staticfiles.templatetags.staticfiles import static

    file = open(os.path.join(settings.BASE_DIR, settings.INSTALLED_APPS[0] + static('CS1231_16s1.txt')))
    data = list(ast.literal_eval(file.read()))
    file.close()
    data.sort()

    i = 0
    tutorials = {}
    for s in range(len(students)):
        if i < len(data):
            if data[i][0].lower() == students[s].get('name').lower():
                if data[i][1] not in tutorials.keys():
                    tutorials[data[i][1]] = []

                tutorials[data[i][1]].append(s)
                i += 1
            elif students[s].get('name').lower() in [d[0].lower() for d in data]:
                i = [d[0].lower() for d in data].index(students[s].get('name').lower())
                if data[i][1] not in tutorials.keys():
                    tutorials[data[i][1]] = []

                tutorials[data[i][1]].append(s)
                i += 1
            else:
                if 'None' not in tutorials.keys():
                    tutorials['None'] = []
                tutorials['None'].append(s)

    tutorial_list = []
    key = list(tutorials.keys())
    key.sort()

    for k in key:
        tutorial_list.append({k: tutorials[k]})

    return tutorial_list
