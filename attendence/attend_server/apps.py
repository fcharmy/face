import os
from django.conf import settings
from django.apps import AppConfig


class AttendServerConfig(AppConfig):
    name = 'attend_server'

    IMG_FOLDER_NAME = 'img_upload'
    IMG_FOLDER = os.path.join(settings.MEDIA_ROOT, IMG_FOLDER_NAME)
