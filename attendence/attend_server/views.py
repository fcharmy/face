from . import models
from shutil import copyfile
from .face_tech import file
from django.shortcuts import render
from .apps import api, error_response
from django.contrib.auth import logout
import logging, traceback, json, os, time
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from . import forms, ivle_views, attend_views
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.forms import UserCreationForm

log = logging.getLogger(__name__)


def index(request):
    message = ""
    if 'message' in request.GET:
        message = request.GET['message']

    return render(request, 'attend/index.html', {'url': 'attend:sign_in', 'message': message})


def create_user_form(request):
    form = UserCreationForm()
    return render(request, 'attend/form_csrf.html', {'url': 'attend:sign_in', 'title': 'Sign in Form', 'form': form})


def login_form(request):
    form = forms.LoginForm()
    return render(request, 'attend/form_csrf.html', {'url': 'attend:user_index', 'title': 'Login Form', 'form': form})


def update_module_form(request):
    form = forms.DataForm()
    return render(request, 'attend/form.html', {'url': 'attend:update_module', 'title': 'update_module Form', 'form': form})


def detection(request):
    form = forms.ImgForm()
    return render(request, 'attend/form.html', {'url': 'attend:detect', 'title': 'Img Form', 'form': form})


def sign_in(request):
    form = UserCreationForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('attend:user_index'))

    return render(request, 'attend/form_csrf.html', {'url': 'attend:sign_in', 'title': 'Sign in Form', 'form': form})


def user_index(request):
    if (request.user.is_authenticated() or 'ivle_user' in request.session) and 'Modules' in request.session:
        return render(request, 'attend/user.html', {'html': 'attend/profile.html', 'modules': request.session['Modules'],
                                             'message': request.GET['message'] if 'message' in request.GET else ''})

    else:
        form = forms.LoginForm(request.POST)
        message = 'please login.'

        if form.is_valid():
            response = None
            option = form.cleaned_data['option']

            if option == 'default':
                response = attend_views.log_in(request)
            elif option == 'ivle':
                response = ivle_views.log_in(request)

            # if response is valid show user index
            if response and response.status_code == 200:
                response = get_content(response)

                if option == 'ivle':
                    request.session['ivle_user'] = {'username': response['Name'],
                                                    'authToken': response['authToken']}
                elif option == 'default':
                    login(request, authenticate(username=form.cleaned_data['username'],
                                                password=form.cleaned_data['password']))

                request.session['Modules'] = response['Modules']
                return redirect_index('Login Success')
            else:
                message = response.content.decode("utf-8")

        return render(request, 'attend/form_csrf.html', {'url': 'attend:user_index', 'title': 'Login Form',
                                                  'message': message, 'form': form})


def user_logout(request):
    print("logging out")
    if request.user.is_authenticated():
        logout(request)
    return JsonResponse({'data': 'success'})

def log_out(request):
    if request.user.is_authenticated():
        logout(request)

    if 'ivle_user' in request.session:
        del request.session['ivle_user']

    return redirect_index('Log out')


def module_form(request):
    form = forms.ModuleForm()
    return render(request, 'attend/form_csrf.html', {'url': 'attend:create_module', 'title': 'Create Module', 'form': form})

def create_module(request):
    form = forms.ModuleForm(request.POST)

    if form.is_valid() and request.user.is_authenticated():
        print("login");
        try:
            code = form.cleaned_data['code']
            group = api.get_groups_by_name(name=code)

            # avoid duplicate group name
            while group:
                code = form.cleaned_data['code'] + models.get_suffix()
                group = api.get_groups_by_name(name=code)

            group_id = api.create_group(name=code, desc=form.cleaned_data['name'])

            m = models.Modules(code=code, group_id=group_id, name=form.cleaned_data['name'],
                               academic_year=form.cleaned_data['year'], semester=form.cleaned_data['semester'])
            m.save()
            
            ump, is_exist = models.User_Module_Permission.objects.get_or_create(user=request.user, module=m, permission='F')

            m = m.to_dict()
            m['Permission'] = ump.permission
            request.session['Modules'].append(m)

            return HttpResponseRedirect(reverse('attend:user_index'))
        except:
            log.error(traceback.format_exc())

    return render(request, 'attend/form_csrf.html', {'url': 'attend:create_module', 'title': 'Create Module', 'form': form})

def tutor_form(request):
    """ Create tutor form """
    if request.user.is_authenticated():
        # choice = tuple([(m.module.id, m.module.code + ' ' + m.module.name) for m in models.get_user_modules(request)])
        form = forms.TutorForm({'module':request.session['cur_module_id']})

        return render(request, 'attend/form_csrf.html', {'url': 'attend:add_tutor', 'title': 'Add Tutor', 'form': form})

    return HttpResponseRedirect(reverse('attend:user_index'))

def add_tutor(request):
    form = forms.TutorForm(request.POST)

    if form.is_valid() and request.user.is_authenticated():
        try:
            module = models.Modules.objects.filter(id=form.cleaned_data['module'])
            tutor = models.get_user(form.cleaned_data['name'])

            if module:
                if tutor:
                    ump, is_exist = models.User_Module_Permission.objects.get_or_create(user=tutor[0], module=module[0], defaults={'permission':'M'})

                    return HttpResponseRedirect(reverse('attend:view_module') + '?id=' + str(module[0].id))
                else:
                    message = 'Unknown Tutor.'
            else:
                message = 'Unknown Module.'
        except:
            log.error(traceback.format_exc())
            message = 'This student name is already exist.'

        return render(request, 'attend/form_csrf.html', {'url': 'attend:add_tutor', 'title': 'Add tutor', 'form': form,
                                                  'message': message})
    else:
        return HttpResponseRedirect(reverse('attend:user_index'))

def tutor_add_student_form(request):
    if request.user.is_authenticated():
        my_ss = [ts.student.name for ts in models.get_my_student_in_module(request.user, request.session['cur_module_id'])]
        all_ss = [s.to_dict() for s in models.get_all_students_in_module(request.session['cur_module_id'])]
        initial_val = [all_ss[i]['name'] for i in range(len(all_ss)) if all_ss[i]['name'] in my_ss]

        form = forms.TutorStudentForm({'module':request.session['cur_module_id'], 'checklist': initial_val}, student_list=all_ss)

        return render(request, 'attend/form_csrf.html', {'url': 'attend:tutor_add_student', 'title': 'Add My Students', 'form': form, 'message': 'Search name or Check name'})

def tutor_add_student(request):
    if request.user.is_authenticated():
        my_st = [st for st in models.get_my_student_in_module(request.user, request.session['cur_module_id'])]
        all_ss = [s for s in models.get_all_students_in_module(request.session['cur_module_id'])]

        form = forms.TutorStudentForm(request.POST, student_list=[s.to_dict() for s in all_ss])

        if form.is_valid():
            module = models.Modules.objects.filter(id=form.cleaned_data['module'])
            new_student_list = [s for s in models.Student.objects.filter(name=form.cleaned_data['search_name'])]
            [new_student_list.append(s) for s in models.Student.objects.filter(name__in=form.cleaned_data['checklist'])]
            
            # add the relation with minimal overhead
            # delete ones not in the new student list
            for s in new_student_list:
                st, is_new = models.Tutor_Students.objects.get_or_create(tutor=request.user, student=s, module=module[0])
                if st in my_st:
                    my_st.remove(st)
            if my_st:
                [st.delete() for st in my_st]

            return HttpResponseRedirect(reverse('attend:view_module') + '?id=' + str(module[0].id))
            
    return HttpResponseRedirect(reverse('attend:user_index'))

def student_form(request):
    """ Create student form """
    if request.user.is_authenticated():
        # choice = tuple([(m.module.id, m.module.code + ' ' + m.module.name) for m in models.get_user_modules(request)])
        form = forms.StudentForm({'module': request.session['cur_module_id']})

        return render(request, 'attend/form_csrf.html', {'url': 'attend:create_student', 'title': 'Add Student', 'form': form})

    return HttpResponseRedirect(reverse('attend:user_index'))


def create_student(request):
    form = forms.StudentForm(request.POST)

    if form.is_valid() and request.user.is_authenticated():

        module = models.Modules.objects.filter(id=form.cleaned_data['module'])
        try:
            if module:
                student = models.Student(module=module[0], name=form.cleaned_data['name'],
                                         first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                         email=form.cleaned_data['email'], note=form.cleaned_data['note'], )
                student.save()

                return HttpResponseRedirect(reverse('attend:view_module') + '?id=' + str(module[0].id))
            else:
                message = 'Unknown Module.'
        except:
            log.error(traceback.format_exc())
            message = 'This student name is already exist.'

        return render(request, 'attend/form_csrf.html', {'url': 'attend:create_student', 'title': 'Add Student', 'form': form,
                                                  'message': message})
    else:
        return HttpResponseRedirect(reverse('attend:user_index'))


def view_module(request):
    if request.method == 'GET' and 'id' in request.GET and 'Modules' in request.session:
        module = [m for m in request.session['Modules'] if str(m['ID']) == request.GET['id']]

        try:
            response = None
            new_request = HttpRequest()
            new_request.POST = {'data': json.dumps(module[0])}

            if module and request.user.is_authenticated():
                new_request.POST['owner'] = request.user.id
                response = attend_views.update_module(new_request)

            elif module and 'ivle_user' in request.session:
                new_request.POST['token'] = request.session['ivle_user']['authToken']
                response = ivle_views.update_module(new_request)

            if response and response.status_code == 200:
                data = get_content(response)

                for a in data['attendance']:
                    # convert time_id to datetime and lecture_or_tutorial
                    a['lt'] = 'Lecture' if a['lt'] else 'Tutorial'

                # sort student list by student id
                sort_list = list([(str(s['name']), s) for s in data['student']])
                sort_list.sort()
                data['student'] = list([dict_ for (key, dict_) in sort_list])

                #perm = (models.get_user_module_perm(user=request.user, module=module[0]))[0].permission
                perm = module[0]['Permission']
 
                request.session['cur_module_id'] = request.GET['id']

                return render(request, 'attend/user.html', {'html': 'attend/dashboard.html', 'modules': request.session['Modules'],
                                                            'attend_records': data['attendance'], 'module': module[0],
                                                            'students': data['student'], 'tutors': data['tutors'], 'is_owner': perm=='F'})
        except:
            log.error(traceback.format_exc())

    return HttpResponseRedirect(reverse('attend:user_index') + "?message=Unknown Module.")


# ----------------Public Functions-------------------

@csrf_exempt
def face_detection(request):
    """ Send img to detect face and check quality """
    t1 = time.time()
    form = forms.ImgForm(request.POST, request.FILES)

    if form.is_valid():
        try:
            img = form.cleaned_data['image']
            file_path = default_storage.save(img.name, ContentFile(img.read()))
            print(file_path)

            data = api.check_quality(image=file(img))
            data['image'] = file_path

            t2 = time.time()
            log.info("face_detection: {}".format(t2 - t1))
            return JsonResponse({'data': data})
        except:
            log.error(traceback.format_exc())
            return error_response(0, message=traceback.format_exc().splitlines()[-1])

    return error_response(1, name='face_detection')


@csrf_exempt
def verify(request):
    """ verify faces with person ids"""

    t1 = time.time()
    form = forms.ImgForm(request.POST, request.FILES)

    if form.is_valid():
        img = form.cleaned_data['image']
        group = int(form.cleaned_data['group'])
        owner = form.cleaned_data['owner']

        module = models.Modules.objects.filter(group_id = group)[0]
        my_students = [ts.student.id for ts in models.get_my_student_in_module(owner, module.id)]


        try:
            file_path = default_storage.save(img.name, ContentFile(img.read()))
            print(file_path)
            response_data = api.verification_faces(image=file(img), group=group, prioritized_persons={'ids':my_students})
        except:
            response_data = []
            file_path = ''

        data = {"faces": response_data, "image": file_path}

        t2 = time.time()
        log.info("verify: {}".format(t2 - t1))

        return JsonResponse({'data': data})

    return error_response(1, name='verify')


@csrf_exempt
def enrollment(request):
    """ enroll faces with person ids"""
    t1 = time.time()
    form = forms.DataForm(request.POST)

    if form.is_valid():
        try:
            data = json.loads(form.cleaned_data['data'])
            img = default_storage.path(data.get('image'))
            group = form.cleaned_data['group']
            response_data = api.enrollment_faces(data=data, group=group, image=file(img))

            # # get attendance info
            # time_id = models.get_time()
            module = form.cleaned_data['module']
            # # lt = form.cleaned_data['lt']

            # copy tmp file to uploaded folder and delete tmp file
            img_path = models.get_image_path(module, 'enroll')
            copyimg(img, img_path)

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

            t2 = time.time()
            log.info("enrollment: {}".format(t2 - t1))

            return JsonResponse({'data': response_data})
        except:
            log.error(traceback.format_exc())
            return error_response(0, message=traceback.format_exc().splitlines()[-1])

    return error_response(1, name='enrollment')


@csrf_exempt
def attend(request):
    """ add attend records"""
    t1 = time.time()
    form = forms.DataForm(request.POST)

    if form.is_valid():
        try:
            data = json.loads(form.cleaned_data['data'])
            group = form.cleaned_data['group']
            module = form.cleaned_data['module']
            lt = form.cleaned_data['lt']

            result = {}
            img = default_storage.path(data.get('image'))
            response_data = data.get('faces')
            time_id = form.cleaned_data['time_id'] if form.cleaned_data['time_id'] else models.get_time()

            # when enroll is not null, which means user correct or add new faces, enroll new faces
            if data.get('enroll'):
                enroll_data = api.enrollment_faces(data={'faces': data.get('enroll')}, group=group, image=file(img))
                result['enroll'] = enroll_data

            # copy tmp file to uploaded folder and delete tmp file
            img_path = models.get_image_path(module, time_id)

            if copyimg(img, img_path):
                # get or create a attendance by time_id, then create attend record for each person
                attendance, is_new = models.Attendance.objects.get_or_create(module_id=module, group_id=group,
                                                                             owner=form.cleaned_data['owner'],
                                                                             time=time_id, lecture_or_tutorial=lt)

                # create a new image record
                data = []
                for face in response_data:
                    if 'id' in face.keys() and face.get('id') != 'None':
                        data.append({"id": face.get('id'), "coordinates": face.get('coordinates')})

                img = models.new_image(img_path, attendance, data)

                if img and attendance:
                    aids = []
                    for face in data:
                        a, is_new = models.Attend_Recodes.objects.get_or_create(attendance=attendance,
                                                                                person_id=face.get('id'))
                        aids.append(a.id)

                    result['data'] = aids
            if result:
                t2 = time.time()
                log.info("attend: {}".format(t2 - t1))

                return JsonResponse(result)
        except:
            log.error(traceback.format_exc())
            return error_response(0, message=traceback.format_exc().splitlines()[-1])

    return error_response(1, name='attend')


# ----------------Private Functions-------------------

def redirect_index(message):
    return HttpResponseRedirect(reverse('attend:index') + '?message=' + message)


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


def get_content(http_response):
    return json.loads(http_response.content.decode("utf-8"))['data']
