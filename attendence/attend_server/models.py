import datetime
from .apps import AttendServerConfig
from django.db import models


class Attendance(models.Model):
    module_id = models.CharField(max_length=50)             # xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx from ivle
    group_id = models.IntegerField()                        # group id from face tech
    time = models.IntegerField()                            # unique time id for each class
    lecture_or_tutorial = models.BooleanField(default=True) # 1 for lecture, 0 for tutorial
    owner = models.CharField(max_length=50)                 # user name


class Attend_Recodes(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    person_id = models.IntegerField()                       # person id from face tech
    # class_or_guest = models.BooleanField(default=1)       # 1 for class, 0 for guest


class Images(models.Model):
    path = models.ImageField(blank=True, null=True)         # path for images
    time = models.IntegerField()                            # unique time id for each class
    data = models.CharField(max_length=5120)                # face info


def get_image_path(module_id, time):
    return '{0}/{1}/{2}_{3}.jpg'.format(AttendServerConfig.IMG_FOLDER, module_id, time,
                                        datetime.datetime.now().strftime("%M%S"))


def get_time():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def new_image(path, time, data):
    """ create new image record """
    try:
        return Images.objects.get_or_create(path=path.replace(AttendServerConfig.IMG_FOLDER, '', 1), time=time, data=data)
    except:
        return None


