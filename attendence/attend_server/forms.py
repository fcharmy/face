from django import forms


class LoginForm(forms.Form):
    """ User login form: userid and encoded password"""
    name = forms.CharField(max_length=30, label='User Name')
    password = forms.CharField(widget=forms.PasswordInput())


class DataForm(forms.Form):
    """ data usually is dict, token is AuthToken fetch from IVLE """
    data = forms.CharField()
    token = forms.CharField(max_length=500, label='Auth Token', required=False)
    group = forms.IntegerField(label='Group ID', required=False)
    module = forms.CharField(label='Module ID', required=False)
    # cg = forms.BooleanField(label='class or guest', required=False)
    lt = forms.BooleanField(label='lecture or tutorial', required=False)
    owner = forms.CharField(label='Owner', required=False)
    time_id = forms.IntegerField(label='Time ID', required=False)


class ImgForm(forms.Form):
    """ Provide img with data """
    image = forms.ImageField()
    data = forms.CharField(required=False, label='Data (optional)')
    group = forms.IntegerField(label='Group ID', required=False)
    module = forms.CharField(label='Module ID', required=False)
    lt = forms.BooleanField(label='lecture or tutorial', required=False)
