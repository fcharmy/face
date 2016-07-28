import os
import dlib
from scipy import io
from django.apps import AppConfig
from django.conf import settings


class FaceTechConfig(AppConfig):
    name = 'face_tech'
    # TMP_UPLOAD_FOLDER = settings.MEDIA_ROOT + 'tmp_upload/'
    FACE_FOLDER = os.path.join(settings.MEDIA_ROOT, 'faces_upload')
    CASCADE_CLASSIFIER_PATH = os.path.join(settings.BASE_DIR, 'face_tech/detection/haarcascade_frontalface_default.xml')
    SHAPE_PREDICTOR_PATH = os.path.join(settings.BASE_DIR, 'face_tech/detection/shape_predictor_68_face_landmarks.dat')
    LDA_MAT_PATH = os.path.join(settings.BASE_DIR, 'face_tech/detection/proj_lda60.mat')
    MODEL_MAT_PATH = os.path.join(settings.BASE_DIR, 'face_tech/detection/model.mat')

    dlib_predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
    lda_mat = io.loadmat(LDA_MAT_PATH)['proj_lda60']

    wfld = io.loadmat(MODEL_MAT_PATH)['wfld']