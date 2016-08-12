import json
from . import views
from . import forms
from . import models
from . import fac_pravite
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def detect(request):
    """ Face detection
    :param: POST request, param: image=image file
    :return: Faces coordinates array
    """
    form = forms.MultiPurposeForm(request.POST, request.FILES)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        if project:
            image, path = fac_pravite.get_numpy_image(form.cleaned_data['image'])
            coordinates = fac_pravite.detect_faces(image)

            # Show Result#
            # import cv2
            # for (y, h, x, w) in faces:
            #     cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
            #     tem_face = image[y:h, x:w]
            # cv2.imshow("Faces found", image)
            # cv2.waitKey(0)

            if coordinates:
                return JsonResponse({'data': coordinates})
        else:
            return views.error_response(2)

    return views.error_response(1, name=detect.__name__, message=form.errors)


@csrf_exempt
def landmark(request):
    """ Face landmarks detection
    :param: POST request, param: image=image file
    :return: json
    """
    form = forms.MultiPurposeForm(request.POST, request.FILES)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        if project:
            image, path = fac_pravite.get_numpy_image(form.cleaned_data['image'])
            coordinates = fac_pravite.detect_faces(image)
            data = []

            if coordinates:
                for c in coordinates:
                    landmarks = fac_pravite.detect_landmark(image, c)
                    data.append({'coordinates': c, 'landmarks': landmarks})

                return JsonResponse({'data': data})
        else:
            return views.error_response(2)

    return views.error_response(1, name=landmark.__name__, message=form.errors)


@csrf_exempt
def occluder(request):
    """ Face occluder detection
    :param: POST request, param: image=image file
    :return: json
    """
    form = forms.MultiPurposeForm(request.POST, request.FILES)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        if project:
            image, path = fac_pravite.get_numpy_image(form.cleaned_data['image'])
            coordinates = fac_pravite.detect_faces(image)
            data = []

            if coordinates:
                for c in coordinates:
                    occlude = fac_pravite.is_occluded(image[c[0]:c[1], c[2]:c[3]])
                    data.append({'coordinates':c, 'occlude': occlude})

                return JsonResponse({'data': data})
        else:
            return views.error_response(2)

    return views.error_response(1, name=occluder.__name__, message=form.errors)


@csrf_exempt
def check_quality(request):
    """ Check faces for occluder, motion blur and lighting
    :param: POST request, param: image=image file, data=True or False (save image to server)
    :return: json
    """
    form = forms.MultiPurposeForm(request.POST, request.FILES)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        if project:
            save = form.cleaned_data['data'] in ('true', 'True', '1')
            image, filename = fac_pravite.get_numpy_image(form.cleaned_data['image'], save=save)
            result = {}
            data = []

            coords = fac_pravite.detect_faces(image)
            if coords:
                for c in coords:
                    face = image[c[0]:c[1], c[2]:c[3]]
                    # landmarks = fac_pravite.detect_landmark(image, c)
                    illuminate = fac_pravite.check_illumination(face)
                    occluder = fac_pravite.is_occluded(face)
                    size = fac_pravite.check_resolution(face)
                    # todo check more facts

                    data.append({'coordinates': c, 'landmarks': None,
                                 'occlude': str(False), 'illumination': illuminate, 'resolution': size})
            result['faces'] = data

            if save:
                result['filename'] = filename

            return JsonResponse({'data': result})
        else:
            return views.error_response(2)
    return views.error_response(1, name=check_quality.__name__, message=form.errors)


@csrf_exempt
def enrollment(request):
    """
    Enroll faces  in project or group with its person id to db. if no id, add new person.
    if person has no relationship with group, add one.
    :param: Project Name, seckey, (group, image)
            data = {'faces':[{'id':id, 'coordinates':[],.], ('filename': '..' or image, must have one)}
            Or {'filename': '..'} for delete saved image.
    :return: list of faces id ('enroll failed' if fails)
    """
    form = forms.EnrollmentForm(request.POST, request.FILES)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        if project:
            data = json.loads(form.cleaned_data['data'])
            image = None
            group = form.cleaned_data["group"]

            if group:
                group = models.get_group_from_project(group, project)
                if not group:
                    return views.error_response(3)

            if 'filename' in data.keys() and form.cleaned_data['image'] is None:
                filename = data.get('filename')
                # image file will delete after this, for one time use
                image, filename = fac_pravite.get_numpy_image(filename)
            elif form.cleaned_data['image'] is not None:
                image, filename = fac_pravite.get_numpy_image(form.cleaned_data['image'])

            if image is not None and 'faces' in data.keys():
                faces = data.get('faces')

                result = []
                for face in faces:
                    if 'coordinates' in face.keys() \
                            and 'id' in face.keys() and type(face.get('id')) is int:

                        coords = face.get('coordinates')
                        person_face, landmarks = \
                            fac_pravite.align_face(image, [coords[0] if coords[0] > 0 else 0,
                                                           coords[1] if coords[1] > 0 else 0,
                                                           coords[2] if coords[2] > 0 else 0,
                                                           coords[3] if coords[3] > 0 else 0])
                        pid = int(face.get('id'))
                        person = models.get_persons_from_project_by_ids(pid, project)

                        if person:
                            if group:
                                # if person not related to group, create one
                                models.Person_To_Group.objects.get_or_create(group=group, person_id=pid)

                            face_id = fac_pravite.enroll_face(person, person_face)
                            if face_id:
                                result.append((pid, face_id))
                                continue

                    result.append(False)

                return JsonResponse({'data': result})
        else:
            return views.error_response(2)
    return views.error_response(1, name=enrollment.__name__, message=form.errors)


@csrf_exempt
def verification(request):
    """
    Verification in project or group
    :param Group/project Name, seckey, image
    :return: {'data':[{'id':id, 'person_name','email'..
            'coordinates':[], 'occlude':bool..},{},.]}
    """
    form = forms.VerificationForm(request.POST, request.FILES)

    if form.is_valid():
        project = models.auth_project_seckey(form.cleaned_data['project'], form.cleaned_data['seckey'])
        group = form.cleaned_data["group"]

        if project:
            if group:
                group = models.get_group_from_project(group, project)
                if not group:
                    return views.error_response(3)

            image, filename = fac_pravite.get_numpy_image(form.cleaned_data['image'])

            coords = fac_pravite.detect_faces(image)
            data = []
            persons = None

            if project is not None and not group:
                persons = models.Person.objects.filter(project=project)
            elif group:
                persons = [ptp.person for ptp in models.Person_To_Group.objects.filter(group_id=group).distinct()]

            if coords and persons is not None:
                persons_feature_array = fac_pravite.get_feature_array(persons)

                for c in coords:
                    result = {'id': 'None'}
                    person_face, landmarks = fac_pravite.align_face(image, c)
                    p = fac_pravite.verify_face_from_feature_array(person_face, persons_feature_array)

                    if p is not False:
                        result = persons[p].to_dict()

                    result['coordinates'] = c
                    data.append(result)

                return JsonResponse({'data': data})
            else:
                return views.error_response(5)
        else:
            views.error_response(2)

    return views.error_response(1, name=verification.__name__, message=form.errors)
