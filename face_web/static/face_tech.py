import os
import json
import requests
from requests_toolbelt import MultipartEncoder


_APIs = [
    'create_person',        # name, (optional: email, first_name, last_name, note, group)
    'create_person_json',   # data, group (optional)
    'create_group',         # name, desc (optional)
    'get_groups_by_name',   # data (group name)
    'person_to_group',      # person, group
    'get_persons_by_group', # group
    'get_all_persons',      # no param
    'delete_person',        # person
    'delete_group',         # group
    'remove_person_from_group',  # person, group
    'detect',               # image
    'landmark',             # image
    'occluder',             # image
    'check_quality',        # image, save (optional)
    'enrollment_faces',     # data, (optional: image, group)
    'verification_faces'    # image, group (optional)
]


class FaceAPI(object):
    project = None
    security_key = None
    timeout = None
    server = 'http://localhost:8000/'  # Server url face_tech/

    def __init__(self, project, seckey, timeout=10, server=None):
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
            elif type(v) is list:
                data[k] = ';'.join(v)
            else:
                data[k] = json.dumps(v)

        m = MultipartEncoder(fields=data)
        response = requests.post(self.url, m, timeout=self.api.timeout,
                                 headers={'Content-Type': m.content_type})

        if response.status_code == 200:
            return json.loads(response.text).get('data')
        else:
            print(response.text)
            return False


def file(path):
    if os.path.getsize(path) > 2 * 1024 * 1024:
        raise OverflowError('{}: File size too large which exceed 2M.'.format(path))

    if not os.path.isfile(path):
        raise IOError

    f = (os.path.basename(path), open(path, 'rb'))
    return f


if __name__ == "__main__":
    project_key = '2'
    security_key = '6fFVF2gG'
    api = FaceAPI(project_key, security_key)

    new_list = [2,4,6,8,10]
    old_list = [1,3,5,7,9,10,13]

    new_p, old_p, count = 0, 0, 0
    new, old = [0]*len(new_list), [0]*len(old_list)

    while old_p < len(old_list) and new_p < len(new_list):
        if new_list[new_p] == old_list[old_p]:
            new[new_p] = 1
            old[old_p] = 1
            new_p += 1
        elif new_list[new_p] < old_list[old_p]:
            new_p += 1
            old_p -= 1

        old_p += 1
        count += 1

    print('Add item: {}'.format([new_list[i] for i in range(len(new)) if new[i] == 0]))
    print('Delete item: {}'.format([old_list[i] for i in range(len(old)) if old[i] == 0]))
    print(count)

    # # Group
    # r = api.create_group(name='file test10.@+-', desc='create by me')
    # print(r)
    #
    # if r:
    #     re = api.delete_group(group=r)
    #     print(re)
    #
    # # Person
    # r = api.create_person(name='test_00', email='test@test.com', first_name='James', last_name='Smith', note='freshman', group=27)
    # print(r)
    #
    # if r:
    #     re = api.delete_person(person=r)
    #     print(re)

    # Person to group
    # rp = api.person_to_group(person=12, group=2)
    # print(rp)
    #
    # if rp:
    #     re = api.remove_person_from_group(person=12, group=2)
    #     print(re)

    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/123.jpg'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/22x20/04000_09_11.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/22x20/04000_07_11.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/22x20/04000_05_11.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/22x20/04000_05_08.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/180x160/04000_05_11.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/180x160/04000_27_11.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/180x160/04001_09_08.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/180x160/04001_09_11.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/180x160/04001_27_11.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/180x160/04037_09_08.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/180x160/04003_09_11.bmp'
    # image = '/home/tsim/Downloads/Untitled Folder/Verification_DrSim/images/180x160/04002_27_11.bmp'
    # image = 'simple/image/sample.jpg'


    # r = api.detect(image=file(image))
    # print(r)
    #
    # re = api.landmark(image=file(image))
    # print(re)
    #
    # r = api.occluder(image=file(image))
    # print(r)
    #
    # r = api.check_quality(image=file(image), save=0)
    # print(r)
    #
    # if r:
    #     faces = []
    #     pid = 81
    #     for f in r.get('faces'):
    #         f['person_id'] = pid
    #         faces.append(f)
    #         pid += 1
    #     r['faces'] = faces
    #
    #     re = api.enrollment_faces(data=r)
    #     print(re)
    #
    # r = api.verification_faces(image=file(image))
    # print(r)
    #
    # r = api.enrollment_faces(data={"faces": [{"person_id":63, "coordinates": [78, 186, 293, 400]}]},
    #                          image=file(image), group=2)
    # print(r)

    # import cv2
    # img = cv2.imread(image)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)

