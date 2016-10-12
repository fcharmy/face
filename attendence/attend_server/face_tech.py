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
        if os.path.getsize(image) > 5 * 1024 * 1024:
            raise OverflowError('{}: File size too large which exceed 2M.'.format(image.split('/')[-1]))

        if not os.path.isfile(image):
            raise IOError('{}: Not a file, please provide a valid file path.'.format(image.split('/')[-1]))

        return os.path.basename(image), open(image, 'rb')
    else:
        try:
            return image.name, image.file
        except:
            raise IOError('Not valid file, please provide a valid path or file content.')


if __name__ == '__main__':
    import pyivle

    API_KEY = "f14zzwlfh5fxiXWS2U3hU"
    # p = pyivle.Pyivle(API_KEY, authToken='5BFB9302D342CA96D73654DD7A30E9D43C4FB960A9EB8D1B6FC40EBBF924E1C23732D22DE55DE4D15788E6D4DF7CD88CC53E5A4402584E87F1A2660FAAF91178EDCFBFD8F81EABC8A1E26162F3CAAC92961219DE3D7E360A3AEED8D7E375F6792C885AFB92208B101871624CFDE4D8A9C8090201B78ED44F8914DF447CB0BCD559675E147C9FB0AAC4D95FE81A44B9121DC65D800B475C8CDDA793A174AF7B0EAE87A5D5D2A3A6FF96308D0B9EE802D68E4B24DEC02EE65EFAD5C2FAED625C112BC6F89A401E3A45DD45D8B0F94A8F35EED0EFD9FCC62E224E23DE50A689A1DFE2ECEEC5BDFE4045D260317DCBC59E65')
    p = pyivle.Pyivle(API_KEY, authToken='D41A734885A38795EDBC371AA5C3E6B318AB563B3C161E63D742FF11D777D5C9563E9A47B373CFF2A6E7D322974D119667BFD63027E5182A28DA7740F4BC1390E105007DEC08BAB9841220A111262F5C547DB72EB6F8CD3D4DF7E5893442882F1DC4FA918A6CFDBD15BE67BA7CF3FB409C7B1E60259CFA26C19480F8552E37108A8A27F2390ABF5349FBDCD737EEDD320711F1052527556FE2CC6B6927D67CF7E909549D5951EF653F0D36B84C9B351379B57C4497DC3EBEA07711C385D640A3435B7DDCA5E6D72EBF90683FC4925366AE9C74C59EE21FD39F18792364502AF8E4207808653D0A145BE864E8EF5DFE4D')

    # data = p.groups_by_user_and_module(courseId='73efbd67-772e-4de3-b743-8e4f574378c0', acadYear='2016/2017', semester='Semester 1').get('Results')

    data = p.groups_by_user().get('Results')
    # data = p.module_class_groups('73efbd67-772e-4de3-b743-8e4f574378c0').get('Results')
    # data = p.module_class_group_users('00000000-0000-0000-0000-000000000000').get('Results')
    # data = p.module_official_group_users(courseId='73efbd67-772e-4de3-b743-8e4f574378c0',
    #                                      groupName='1', groupType='Tutorial').get('Results')

    print(data)

