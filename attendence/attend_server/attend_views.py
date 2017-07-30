from .apps import api
from . import forms, models
from .apps import error_response
from django.http import JsonResponse
import base64, logging, traceback, json
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger(__name__)


@csrf_exempt
def log_in(request):
    """ Login with username and password """
    form = forms.LoginForm(request.POST)

    if form.is_valid():
        try:
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print('username:'+form.cleaned_data['username'],'password:'+form.cleaned_data['password'])
            if user is not None:
                # the password verified for the user
                print('correct password',user.is_active)
                if user.is_active:
                    data = {"Name": user.get_username(), "UserID": user.id, "Modules": []}

                    modules = models.get_user_modules(user)
                    for m in modules:
                        dict_ = m.module.to_dict()
                        dict_['Permission'] = m.permission

                        data['Modules'].append(dict_)
                    return JsonResponse({'data': data})
        except:
            log.error(traceback.format_exc())
    print('responsing')
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
            print('owner:',form.cleaned_data['owner'])

            # return person profile order by person name
            exist_list = api.get_persons_by_group(group=data.get('face_group_id'))
            new_list = models.Student.objects.filter(module_id=data.get('ID'))
            tutors_list = [ump.user for ump in models.User_Module_Permission.objects.filter(module__id=data.get('ID'), permission='M')]
            tutored_students = [s.student.to_dict() for s in models.get_my_student_in_module(tutor=form.cleaned_data['owner'], module_id=data.get('ID'))]

            new_tutors_list = []
            for i in range(len(tutors_list)):
                myss = [ts.student.to_dict() for ts in models.get_my_student_in_module(tutors_list[i],data.get('ID'))];
                new_tutors_list.append({
                    'username': tutors_list[i].username,
                    'myss_len': len(myss)
                })

            # Relationship with data between face and ivle:
            # face: name -> IVLE: UserID - A0123456
            # face: first_name -> IVLE: Name - James Smith
            # face: note -> IVLE: UserGuid - xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

            if data and new_list :
                # if has no persons in face, initial with a empty list
                exist_list = exist_list if exist_list else []

                # Sort new_list by UserID
                new_list = [(str(s.to_dict()['id']), s.to_dict()) for s in new_list]
                new_list.sort()
                new_list = [dict_ for (key, dict_) in new_list]

                # iterate to match with each other
                new_p, old_p = 0, 0
                new, old = [False]*len(new_list), [False]*len(exist_list)

                while old_p < len(exist_list) and new_p < len(new_list):
                    if str(new_list[new_p].get('id')) == exist_list[old_p].get('name'):
                        new[new_p] = True
                        old[old_p] = True
                        new_p += 1
                    elif str(new_list[new_p].get('id')) < exist_list[old_p].get('name'):
                        new_p += 1
                        old_p -= 1

                    old_p += 1

                # Add new item to face database
                updated_list, add_list = [], []

                #print([p.get('id') for p in new_list], [p.get('name') for p in exist_list])

                for i in range(len(new)):
                    if new[i] is False:
                        add_list.append({'name': new_list[i].get('id'),
                                         'email': new_list[i].get('email'),
                                         'first_name': new_list[i].get('name'),
                                         'last_name': new_list[i].get('last_name'),
                                         'note': new_list[i].get('note')})

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
                    delete_result = api.delete_person(person=[i.get('id') for i in exist_list],
                                                      group=data.get('face_group_id'))

                    if delete_result:
                        if False in [list(d.values())[0] for d in delete_result]:
                            data['error_delete'] = []

                            for i in range(len(delete_result)):
                                data['error_delete'].append(list(delete_result[i].keys())[0])
                    else:
                        data['error_delete'] = exist_list

                del exist_list, new_list, add_list, tutors_list
                data['student'] = updated_list
                data['attendance'] = models.get_records(data.get('ID'))

            else:
                data['student'] = []
                data['attendance'] = []

            data['tutors'] = new_tutors_list
            data['tutorial'] = tutored_students
            return JsonResponse({'data': data})
        except:
            log.error(traceback.format_exc())

    return error_response(1, name='update_module')


