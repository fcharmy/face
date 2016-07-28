import os
import cv2
import json
import math
import dlib
import random
import logging
import traceback
import numpy as np
import numpy.matlib
from math import exp
from . import models
from .apps import FaceTechConfig
from .detection import face_detection
from django.core.files.base import ContentFile
from scipy.spatial.distance import pdist, squareform
from django.core.files.storage import default_storage
log = logging.getLogger(__name__)


# ----------------Private Functions-------------------

def enroll_face(person, image):
    """
    Add new face to table.
    if person has identifier feature, calculate new one, update person.
    :param person: person object, image: numpy array
    :return: face_id or False
    """
    try:
        feature = json.dumps(feature_extraction(image).tolist())

        path = models.get_image_path(person)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        if cv2.imwrite(path, image):
            face = models.Face(person=person, feature=feature, image=path)
            face.save()

            person.save()

            return face.id
    except:
        log.error(traceback.format_exc())

    return False


# if person.feature:
#     faces = []
#     for f in models.Face.objects.filter(person=person):
#         if f.image:
#             faces.append(cv2.imread(f.image.path))
#         else:
#             f.delete()
#
#     # Add new feature to identifier
#     new_feature = str(feature_extraction(faces))
#     person.feature = new_feature
# else:
#     person.feature = feature


def get_feature_array(persons):
    try:
        persons_feature_array = []

        for p in persons:
            dimension = 25  # the rows of proj_lda60
            faces = models.Face.objects.filter(person=p)

            feature_array = np.array([[] for _ in range(dimension)])

            for f in faces:
                feature_array = np.concatenate((feature_array, np.array((json.loads(f.feature)))), axis=1)

            persons_feature_array.append(feature_array)

        return persons_feature_array
    except:
        log.error(traceback.format_exc())
    return None


def verify_face_from_feature_array(face, feature_array):
    """
    Return identification index from feature_array, compare one face among faces.
    :param face: numpy array, feature_array: return from get_featrue_array(persons)
    :return: person object or False
    """
    try:
        feature = feature_extraction(face)
        max_match, person_index = 0, None

        for i in range(len(feature_array)):
            if len(feature_array[i]) > 0 and feature_array[i].shape[1] > 0:
                farray = np.concatenate((feature, feature_array[i]), axis=1)
                flag, compare_score = compare(farray)

                if flag and max_match < compare_score:
                    person_index = i
                    max_match = compare_score

        if max_match > 0 and person_index is not None:
            return person_index

    except:
        log.error(traceback.format_exc())
    return False


def detect_faces(image):
    """ Face detection from dlib
    :param: facial image local path or image of numpy array
    :return: faces coordinates list
    """
    try:
        # Dlib face detector
        detector = dlib.get_frontal_face_detector()
        image = cv2.equalizeHist(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

        dets = detector(image, 1)
        coordinates = [[d.top() if d.top() > 0 else 0, d.bottom() if d.bottom() > 0 else 0,
                        d.left() if d.left() > 0 else 0, d.right() if d.right() > 0 else 0] for d in dets]

        return coordinates

    except:
        log.error(traceback.format_exc())
        return False


def detect_faces_cv2(image):
    """ Face detection from opencv, 7:8
    :param: facial image local path or image of numpy array
    :return: faces coordinates list
    """
    try:
        # Opencv face detector
        detector = face_detection.FaceDetector()
        faces = detector.find_face_path(cv2.equalizeHist(image))
        coordinates = []

        for (x, y, w, h) in faces:
            face_x = int(x) + int(0.15*w)
            face_y = int(y) + int(0.1*h)
            face_w_x = int(0.7*w) + face_x
            face_h_y = int(0.8*h) + face_y
            coordinates.append([face_y, face_h_y, face_x, face_w_x])

        return coordinates

    except:
        log.error(traceback.format_exc())
        return False


def detect_landmark(image, coordinates):
    """ input: entire image Numpy array RGB
        coordinates: one face coordinates
    """
    predictor = FaceTechConfig.dlib_predictor

    # Convert coordinates list to dlib.rectangle
    b = dlib.rectangle(coordinates[2], coordinates[0], coordinates[3], coordinates[1])
    # Convert opencv RGB image to BGR then detect landmarks
    shape = predictor(cv2.cvtColor(image, cv2.COLOR_RGB2BGR), b)

    # # Show results
    # win = dlib.image_window()
    # win.clear_overlay()
    # win.set_image(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    # win.add_overlay(shape)
    # win.add_overlay(b)
    # win.wait_until_closed()

    landmarks = [[s.x, s.y] for s in shape.parts()]
    return landmarks


def align_face(image, coordinates):
    """ Face detection from dlib landmark detection
    :param: facial image local path or image of numpy array
    :return: faces coordinates list and landmarks
    """
    try:
        d = dlib.rectangle(coordinates[2], coordinates[0], coordinates[3], coordinates[1])

        # Detect landmarks
        predictor = FaceTechConfig.dlib_predictor
        shape = predictor(image, d)

        # Get left and right eye position
        l_x, l_y, n = 0, 0, 0
        for i in range(36, 42):
            l_x, l_y = l_x + shape.part(i).x, l_y + shape.part(i).y
            n += 1
        left_eye = (l_x/n, l_y/n)

        r_x, r_y, m = 0, 0, 0
        for i in range(42, 48):
            r_x, r_y = r_x + shape.part(i).x, r_y + shape.part(i).y
            m += 1
        right_eye = (r_x/m, r_y/m)

        # Calculate the distance between eyes, and the center point
        eye_dist = np.sqrt((right_eye[0] - left_eye[0])**2 + (right_eye[1] - left_eye[1])**2)
        centroid = ((left_eye[0] + right_eye[0])/2, (left_eye[1] + right_eye[1])/2)
        top = centroid[1] - eye_dist/1.6
        bottom = centroid[1] + 1.6 * eye_dist
        left = centroid[0] - eye_dist
        right = centroid[0] + eye_dist

        # Calculate the rotation matrix to rotate the image and get the rotated face
        angle = math.atan2(float(right_eye[1] - left_eye[1]), float(eye_dist))
        rotate_mat = cv2.getRotationMatrix2D(centroid, angle / math.pi * 180, 1.0)
        rotate_img = cv2.warpAffine(image, rotate_mat, (image.shape[1], image.shape[0]), flags=cv2.INTER_LINEAR)
        rotate_face = rotate_img[top if top > 0 else 0: bottom, left if left >0 else 0: right]

        landmarks = [[s.x, s.y] for s in shape.parts()]
        return rotate_face, landmarks
    except:
        log.error(traceback.format_exc())
        return False


def check_illumination(image):
    """
    Check the illumination of croped faces
    :param image: numpy array with color
    :return: -1: too dark, 0: okay, 1: too bright
    """
    try:
        hist, bins = np.histogram(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 256, [0, 256])
        count = len(hist)

        threshold = image.shape[0] * image.shape[1] * 0.72
        measure = sum(hist[:int(count / 2)]) - sum(hist[int(count / 2):])

        if measure > threshold:
            return -1   # the image is too dark
        elif measure < -threshold:
            return 1    #the image is too bright
        else:
            return 0    #the image is okay
    except:
        log.error(traceback.format_exc())
        return False


def check_resolution(image):
    """
    Check face image's resolution
    :param image: face numpy array with color
    :return: 1: good, 0: too small
    """
    try:
        x, y, c = image.shape
        if x * y < 60 * 60:
            return 0
        else:
            return 1
    except:
        log.error(traceback.format_exc())
        return False


def is_occluded(image):
    """ input: Numpy array """
    return random.choice([True, False])


def feature_extraction(image):
    """ input, output: Numpy array """

    w, h = 160, 180  # w*h is columns of proj_lda60
    wfld = FaceTechConfig.wfld

    img = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (w, h))
    array = np.reshape(cv2.equalizeHist(img), (w * h, 1))

    return np.mat(wfld['V'][0][0]) * np.mat(array - np.matlib.repmat(wfld['org'][0][0], 1, array.shape[1]))


def compare(feature):
    """
    Return the result of accept or reject.
    Feature matrix: numpy array
    """
    try:
        d = squareform(pdist(feature.T, 'cosine'))[1:, 0]

        amin = np.amin(d)
        mean = np.mean(d)

        if amin < 0.57:
            return True, exp(-amin ** 2)
        elif mean < 0.8:
            return True, exp(-mean**2)
        else:
            dd = np.max([amin, mean])
            return False, exp(-dd**2)
    except:
        log.error(traceback.format_exc())
        return False, None


def get_numpy_image(img, save=False):
    """ Store cleaned_data of request.FILE to local, read as numpy array
    read image file as numpy array if img is file path
    :param: form.cleaned_data['image'] or file path, delete if save=False
    :return: numpy array
    """
    try:
        if type(img) is str:
            img_name = img
        else:
            # Real image name, upload
            img_name = default_storage.save(img.name, ContentFile(img.read()))

        # Read as numpy array
        image = cv2.imread(default_storage.path(img_name))

        if not save:
            # Delete temp image file
            default_storage.delete(img_name)
            img_name = ''

        return image, img_name

    except:
        log.error(traceback.format_exc())
        return None, None


