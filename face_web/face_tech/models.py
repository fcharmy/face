import datetime
from django.db import models
from .apps import FaceTechConfig
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[RegexValidator(r'^[\w\s.@+-]+$')])
    description = models.CharField(max_length=200, default='')
    project = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """ return dictionary of this object """
        dict = {}
        for f in self._meta.fields:
            if f.name == 'name':
                dict[f.name] = ''.join(f.value_from_object(self).split('_')[1:])
            else:
                dict[f.name] = f.value_from_object(self)

        return dict


class Person(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[RegexValidator(r'^[\w.@+-]+$')])
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    note = models.CharField(max_length=200, blank=True)
    project = models.ForeignKey(User, on_delete=models.CASCADE)
    # feature = models.CharField(max_length=5120, blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """ return dictionary of this object """
        dict = {}
        for f in self._meta.fields:
            if f.name == 'name':
                dict[f.name] = ''.join(f.value_from_object(self).split('_')[1:])
            else:
                dict[f.name] = f.value_from_object(self)

        return dict


class Person_To_Group(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Face(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    feature = models.CharField(max_length=5120)
    image = models.ImageField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)


# ----------------Private Functions-------------------

def get_real_name(name, project):
    return '{0}_{1}'.format(project.id, name)


def add_or_get_person(name, project, email='', first_name='', last_name='', note=''):
    """ add new person to database"""
    person_name = get_real_name(name, project)

    try:
        return Person.objects.get(name=person_name)
    except:
        try:
            person = Person(name=person_name, project=project, email=email,
                            first_name=first_name, last_name=last_name, note=note)
            person.save()

            return person
        except: return None


def add_or_get_group(name, project, description=''):
    """ add new person to database"""
    group_name = get_real_name(name, project)
    try:
        return Person.objects.get(name=group_name)
    except:
        try:
            group = Group(name=group_name, project=project, description=description)
            group.save()

            return group
        except:
            return None


def auth_project_seckey(id, key):
    """ Authenticate security key from project name """
    try:
        project = User.objects.get(id=id)

        if project.last_name == key:
            return project
    except: pass

    return False


def get_group_from_project(group_id, project):
    """ From project object and group id to get group ojbect
    If this group not belong to project, return None"""
    try:
        group = Group.objects.get(id=group_id, project=project)
        return group
    except:
        return None


def get_persons_from_project_by_ids(person_id, project):
    """ From project object and person id to get person ojbect
    If this person not belong to project, return None"""
    try:
        if type(person_id) is int:
            person = Person.objects.get(id=person_id, project=project)
            return person
        else:
            persons = []
            for p in person_id:
                persons.append(Person.objects.get(id=p, project=project))
            return persons
    except:
        return None


def get_image_path(person):
    return '{0}/{1}/{2}_{3}.jpg'.format(FaceTechConfig.FACE_FOLDER, person.project_id, person.id,
                                            datetime.datetime.now().strftime("%y%m%d%H%M%S"))