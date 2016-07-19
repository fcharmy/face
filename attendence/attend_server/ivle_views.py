from shutil import copyfile
from django.conf import settings
import base64, logging, traceback, json, os
from . import views, forms, pyivle, models, apps
from .face_tech import FaceAPI, file
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage, FileSystemStorage

project_key = '2'
security_key = 'SWQ9HjVM'
api = FaceAPI(project_key, security_key)

log = logging.getLogger(__name__)


@csrf_exempt
def login(request):
    """ Login with ivle username and password """
    form = forms.LoginForm(request.POST)

    if form.is_valid():
        try:
            # Authenticate for IVLE
            data, modules = login_ivle(form.cleaned_data['name'], form.cleaned_data['password'])
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
    return views.error_response(2)


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

                student_ids = [i.get('UserID').lower() for i in new_list]
                student_ids.sort()

                # iterate to match with each other
                new_p, old_p = 0, 0
                new, old = [False]*len(student_ids), [False]*len(exist_list)

                while old_p < len(exist_list) and new_p < len(student_ids):
                    if student_ids[new_p] == exist_list[old_p].get('name'):
                        new[new_p] = True
                        old[old_p] = True
                        new_p += 1
                    elif student_ids[new_p] < exist_list[old_p].get('name'):
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
                data['attendance'] = get_records(data.get('ID'))

                return JsonResponse({'data': data})

            else:
                return views.error_response(5)
        except:
            log.error(traceback.format_exc())

    return views.error_response(1, name='update_module')


@csrf_exempt
def face_detection(request):
    """ Send img to detect face and check quality """
    form = forms.ImgForm(request.POST, request.FILES)

    if form.is_valid():
        try:
            img = form.cleaned_data['image']
            data = api.check_quality(image=file(img))
            data['image'] = default_storage.save(img.name, ContentFile(img.read()))

            return JsonResponse({'data': data})
        except:
            log.error(traceback.format_exc())

    return views.error_response(1, name='face_detection')


@csrf_exempt
def verify(request):
    """ verify faces with person ids"""
    form = forms.ImgForm(request.POST, request.FILES)

    if form.is_valid():
        try:
            # data = json.loads(form.cleaned_data['data'])
            img = form.cleaned_data['image']
            group = int(form.cleaned_data['group'])

            response_data = api.verification_faces(image=file(img), group=group)

            data = {"faces": response_data, "image": default_storage.save(img.name, ContentFile(img.read()))}
            return JsonResponse({'data': data})
        except:
            log.error(traceback.format_exc())

    return views.error_response(1, name='verify')


@csrf_exempt
def enrollment(request):
    """ enroll faces with person ids"""
    form = forms.DataForm(request.POST)

    if form.is_valid():
        try:
            data = json.loads(form.cleaned_data['data'])
            img = default_storage.path(data.get('image'))
            group = form.cleaned_data['group']
            response_data = api.enrollment_faces(data=data, group=group, image=file(img))

            # # get attendance info
            # time_id = models.get_time()
            # module = form.cleaned_data['module']
            # # lt = form.cleaned_data['lt']
            #
            # # copy tmp file to uploaded folder and delete tmp file
            # img_path = models.get_image_path(module, time_id)
            # if copyimg(img, img_path):
            #
            #     # create a new image record
            #     img = models.new_image(img_path, time_id, data.get('faces'))
            #     attendance = models.Attendance(module_id=module, group_id=group, owner=form.cleaned_data['owner'],
            #                                    time=time_id, lecture_or_tutorial=True)
            #     attendance.save()
            #     if img:
            #         aids = []
            #         for face in data.get('faces'):
            #             if face.get('id'):
            #                 a, is_new = models.Attend_Recodes.objects.get_or_create(attendance=attendance,
            #                                                                         person_id=face.get('id'))
            #                 aids.append(a.id)
            #
            #         return JsonResponse({'data': response_data, 'attend': aids})

            return JsonResponse({'data': response_data})
        except:
            log.error(traceback.format_exc())

    return views.error_response(1, name='enrollment')


@csrf_exempt
def attend(request):
    """ add attend records"""
    form = forms.DataForm(request.POST)

    if form.is_valid():
        if True:
            data = json.loads(form.cleaned_data['data'])
            group = form.cleaned_data['group']
            module = form.cleaned_data['module']
            lt = form.cleaned_data['lt']

            img = default_storage.path(data.get('image'))
            response_data = data.get('faces')
            time_id = form.cleaned_data['time_id'] if form.cleaned_data['time_id'] else models.get_time()

            # copy tmp file to uploaded folder and delete tmp file
            img_path = models.get_image_path(module, time_id)

            if copyimg(img, img_path):
                # create a new image record
                data = []
                for face in response_data:
                    if face.get('id'):
                        data.append({"id": face.get('id'), "coordinates": face.get('coordinates')})

                img = models.new_image(img_path, time_id, data)

                # get or create a attendance by time_id, then create attend record for each person
                attendance, is_new = models.Attendance.objects.get_or_create(module_id=module, group_id=group,
                                                                             owner=form.cleaned_data['owner'],
                                                                             time=time_id, lecture_or_tutorial=lt)
                if img and attendance:
                    aids = []
                    for face in data:
                        a, is_new = models.Attend_Recodes.objects.get_or_create(attendance=attendance,
                                                                                person_id=face.get('id'))
                        aids.append(a.id)

                    return JsonResponse({'data': response_data, 'attend': aids})

        else:
            log.error(traceback.format_exc())

    return views.error_response(1, name='attend')


# ----------------Private Functions-------------------

API_KEY = "f14zzwlfh5fxiXWS2U3hU"


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
        if m.get('Permission') in ['O', 'F', 'M', 'R', 'S']:
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

    return p.guest_roster(module_id).get('Results')


def copyimg(tmp_img, img_path):
    # copy tmp file to uploaded folder and delete tmp file
    try:
        if not os.path.exists(os.path.dirname(img_path)):
            os.makedirs(os.path.dirname(img_path))

        copyfile(tmp_img, img_path)
        default_storage.delete(tmp_img)

        return True
    except:
        return False


def get_records(module):
    """ return list of attendance records with students ids and other info by providing module id"""
    try:
        classes = models.Attendance.objects.filter(module_id=module).order_by('-time')

        data = []
        for c in classes:
            attend = {"time_id": c.time, "lt": c.lecture_or_tutorial, "owner": c.owner,
                      "students": [p.person_id for p in models.Attend_Recodes.objects.filter(attendance=c)],
                      "images": [{"url": settings.MEDIA_URL + apps.AttendServerConfig.IMG_FOLDER_NAME + img.path.name,
                                  "data": img.data} for img in models.Images.objects.filter(time=c.time)]
                      }
            data.append(attend)

        return data
    except:
        return None


