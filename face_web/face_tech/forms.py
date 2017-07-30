from django import forms
from django.core.validators import RegexValidator


class MultiPurposeForm(forms.Form):
    """ Check_quality, detect, occluder, landmark
    This form also used for create_person_json, where data is person info of json formate, image will be null.

    :param data in 'True', 'true', '1' represent save image to server when check_quality.
    """
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')
    data = forms.CharField(required=False, label='Data (optional)')
    image = forms.ImageField(required=False)
    group = forms.IntegerField(label='Group ID', required=False)


class ProjectForm(forms.Form):
    """ Create Project form """
    name = forms.CharField(max_length=30, validators=[RegexValidator(r'^[\w.@+-]+$')])
    owner = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginProjectForm(forms.Form):
    name = forms.CharField(max_length=30, label='Project Name')
    password = forms.CharField(widget=forms.PasswordInput())


class GroupForm(forms.Form):
    """ Project key and security key with new group name and description """
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')
    name = forms.CharField(max_length=50, validators=[RegexValidator(r'^[\w\s.@+-]+$')])
    desc = forms.CharField(max_length=200, required=False, label='Description (optional)')


class DeleteGroupForm(forms.Form):
    """ Project key and security key with new group name and description """
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')
    group = forms.IntegerField(label='Group ID')


class PersonForm(forms.Form):
    """ Create Person form with project key """
    name = forms.CharField(max_length=5120, validators=[RegexValidator(r'^[\w\s.@;+-]+$')])
    email = forms.CharField(max_length=5120, required=False, label='Email (optional)', validators=[RegexValidator(r'^[\w\s.@;+-]+$')])
    first_name = forms.CharField(max_length=5120, required=False, label='First Name (optional)', validators=[RegexValidator(r'^[\w\s.@;+-]+$')])
    last_name = forms.CharField(max_length=5120, required=False, label='Last Name (optional)', validators=[RegexValidator(r'^[\w\s.@;+-]+$')])
    note = forms.CharField(max_length=5120, required=False, label='Note (optional)', validators=[RegexValidator(r'^[\w\s.@;+-]+$')])
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')
    group = forms.IntegerField(label='Group ID (optional)', required=False)


class DeletePersonForm(forms.Form):
    """ Project key and security key with person id """
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')
    person = forms.CharField(label='Person IDs', validators=[RegexValidator(r'^[\d;]+$')])


class PersonByGroupForm(forms.Form):
    """ Project key and security key with person id """
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')
    group = forms.IntegerField(label='Group ID')


class PersonByProjectForm(forms.Form):
    """ Project key and security key with person id """
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')


class PersonToGroupForm(forms.Form):
    """ Relate person to group """
    person = forms.CharField(label='Person IDs', validators=[RegexValidator(r'^[\d;]+$')])
    group = forms.IntegerField(label='Group ID')
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')


class EnrollmentForm(forms.Form):
    """
    Provide group name and security key, enroll new faces, if person_name, add new person.
    data = {'faces':[{'person_id':id, 'coordinates':[], 'occlude':bool..},{},.], filename='server_file_name'}
    """
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')
    data = forms.CharField()
    image = forms.ImageField(required=False, label='Image (if optional, please provide filename in data)')
    group = forms.IntegerField(label='Group ID (optional)', required=False)


class VerificationForm(forms.Form):
    """ Verify image according to project key and security key """
    project = forms.IntegerField(label='Project Key')
    seckey = forms.CharField(max_length=30, label='Security Key')
    image = forms.ImageField()
    group = forms.IntegerField(label='Group ID (optional)', required=False)
    prioritized_persons = forms.CharField(required=False)

