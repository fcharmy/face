import os
from .face_tech import FaceAPI
from django.conf import settings
from django.apps import AppConfig
from django.http import HttpResponse

API_KEY = "f14zzwlfh5fxiXWS2U3hU"

project_key = '1'
security_key = 'XJ7Yx5U0'
api = FaceAPI(project_key, security_key, server='http://localhost/')

IMG_FOLDER_NAME = 'img_upload'
IMG_FOLDER = os.path.join(settings.MEDIA_ROOT, IMG_FOLDER_NAME)


class ErrorResponse(object):
    def __call__(self, error_code, name='', message=None):
        self.error_message = {
            0: message,
            1: '{} Error: Invalid input.'.format(name),
            2: 'Invalid user name or password.',
        }
        self.error_code = error_code
        response = HttpResponse(self.error_message.get(self.error_code))
        response.status_code = 406
        return response

error_response = ErrorResponse()


class AttendServerConfig(AppConfig):
    pass

