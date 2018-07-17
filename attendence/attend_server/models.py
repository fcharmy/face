import datetime, json
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .apps import IMG_FOLDER, IMG_FOLDER_NAME
from django.core.validators import RegexValidator


class Attendance(models.Model):
    module_id = models.CharField(max_length=50)             # xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx from ivle
    group_id = models.IntegerField()                        # group id from face tech
    time = models.BigIntegerField(unique=True)                 # unique time id for each class
    lecture_or_tutorial = models.BooleanField(default=True) # 1 for lecture, 0 for tutorial
    owner = models.CharField(max_length=50)                 # user name


class Attend_Recodes(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    person_id = models.IntegerField()                       # person id from face tech
    # class_or_guest = models.BooleanField(default=1)       # 1 for class, 0 for guest


class Images(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    path = models.ImageField(blank=True, null=True)         # path for images
    data = models.CharField(max_length=5120)                # face info
    created = models.DateTimeField(auto_now=True)


class Modules(models.Model):
    group_id = models.IntegerField()                        # group id from face tech
    code = models.CharField(max_length=50, unique=True)     # module code
    name = models.CharField(max_length=100)                 # modules name
    academic_year = models.CharField(max_length=20)         # Academic Year of module
    semester = models.CharField(max_length=100)             # modules semester

    def to_dict(self):
        """ return dictionary of this object """
        return {"CourseAcadYear": self.academic_year, "CourseCode": self.code, "CourseSemester": self.semester,
                "face_group_id": self.group_id, "CourseName": self.name, "ID": self.id}


class User_Module_Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20)            # 'M' for TA

class Student(models.Model):
    name = models.CharField(max_length=50, validators=[RegexValidator(r'^[\w.@+-]+$')])
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    note = models.CharField(max_length=200, blank=True)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("name", "module"),)

    def to_dict(self):
        """ return dictionary of this object """
        _dict = {}
        for f in self._meta.fields:
            if f.name == 'created':
                _dict[f.name] = str(f.value_from_object(self))
            else:
                _dict[f.name] = f.value_from_object(self)

        return _dict

# for fast searching
class Tutor_Students(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)

    def __str__(self):
        return self.tutor.username+":"+self.student.name

def get_image_path(module_id, time):
    return '{0}/{1}/{2}_{3}.jpg'.format(IMG_FOLDER, module_id, time,
                                        datetime.datetime.now().strftime("%M%S"))

def get_suffix():
    return datetime.datetime.now().strftime("%M%S")


def get_time():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def new_image(path, attendance, data):
    """ create new image record """
    try:
        return Images.objects.get_or_create(path=path.replace(IMG_FOLDER, '', 1),
                                            attendance=attendance, data=json.dumps(data))
    except:
        return None


def get_records(module):
    """ return list of attendance records with students ids and other info by providing module id"""
    if True:
        classes = Attendance.objects.filter(module_id=module).order_by('-time')

        data = []
        for c in classes:
            attend = {"time_id": c.time, "lt": c.lecture_or_tutorial, "owner": c.owner,
                      "students": [p.person_id for p in Attend_Recodes.objects.filter(attendance=c)],
                      "images": [{"url": settings.MEDIA_URL + IMG_FOLDER_NAME + img.path.name,
                                  "data": json.loads(img.data)} for img in Images.objects.filter(attendance=c)]}
            data.append(attend)

        return data
    else:
        return None


def get_user_modules(user):
    return User_Module_Permission.objects.filter(user=user, permission__in=['O', 'F', 'M', 'R'])

def get_user(name):
    return User.objects.filter(username=name)

def get_my_student_in_module(tutor, module_id):
    if type(tutor)==type(0):
        return Tutor_Students.objects.filter(tutor__id=tutor, module__id=module_id)
    return Tutor_Students.objects.filter(tutor=tutor, module__id=module_id)

def get_all_students_in_module(module_id):
    return Student.objects.filter(module__id=module_id)

# def get_user_module_perm(user, module):
#     return User_Module_Permission.objects.filter(user=user, module__id=module.id)
