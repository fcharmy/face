import os
import json
import requests
from requests_toolbelt import MultipartEncoder


_APIs = [
    'create_person',        # name, (optional: email, first_name, last_name, note, group)
    'create_json_person',   # data, group (optional)
    'create_group',         # name, desc (optional)
    'get_groups_by_name',   # name
    'person_to_group',      # person, group
    'get_persons_by_group', # group
    'get_all_persons',      # no param
    'delete_person',        # person
    'delete_group',         # group
    'remove_person_from_group',  # person, group
    'detect',               # image
    'landmark',             # image
    'occluder',             # image
    'check_quality',        # image, data (optional)
    'enrollment_faces',     # data, (optional: image, group)
    'verification_faces'    # image, group (optional)
]


class FaceAPI(object):
    project = None
    security_key = None
    timeout = None
    server = 'http://nusface-i.comp.nus.edu.sg/'  # Server url face_tech/

    def __init__(self, project, seckey, timeout=60, server=None):
        self.project = project
        self.security_key = seckey
        self.timeout = timeout
        if server:
            self.server = server

        for a in _APIs:
            setattr(self, a, _APICall(self, a))


class _APICall(object):
    def __init__(self, api, url):
        self.api = api
        self.url = self.api.server + url

    def __call__(self, *args, **kwargs):
        if len(args):
            raise TypeError('Only keyword arguments are allowed')

        data = {'project': self.api.project, 'seckey': self.api.security_key}
        for (k, v) in kwargs.items():
            if type(v) is tuple or type(v) is str:
                data[k] = v
            elif type(v) is list and True not in [type(i) is dict for i in v]:
                data[k] = ';'.join([str(i) for i in v])
            else:
                data[k] = json.dumps(v)

        m = MultipartEncoder(fields=data)
        response = requests.post(self.url, m, timeout=self.api.timeout,
                                 headers={'Content-Type': m.content_type})

        if response.status_code == 200:
            return json.loads(response.text).get('data')
        else:
            # print error message, raise ValueError(response.text)
            print(response.text)
            raise ValueError(response.text)


def file(image):
    if type(image) is str:
        if os.path.getsize(image) > 2 * 1024 * 1024:
            raise OverflowError('{}: File size too large which exceed 2M.'.format(image))

        if not os.path.isfile(image):
            raise IOError('{}: Not a file, please provide a valid file path.'.format(image))

        return os.path.basename(image), open(image, 'rb')
    else:
        try:
            return image.name, image.file
        except:
            raise IOError('Not valid file, please provide a valid path or file content.')
