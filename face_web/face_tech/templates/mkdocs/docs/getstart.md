# Getting Started

## Create a project

Before you get started, click [here](index.md) to register a new project.

After sign in you will get your project and security key, it will be used for 

* Use face APIs
* Create groups or persons to your project
* Enroll faces with identification to your project
* Verify faces from your project

You can login your project to check status of groups and persons.

`Tips: Groups are belong to one project, they are used to separate persons into different groups. `
`One person may belong to several groups and enroll many times to server.`


## Download

Click [here](index.md) to download face_tech.py, no need to install, just make sure you have install the following.

	# Python3
	sudo apt-get install python3

	# Requests
	pip install requests

	# Requests toolbelt
	pip install requests-toolbelt

	
## Initial

The main object is FaceAPI, it create connection between your project and the face server. Now you can call functions to do your project.

```
from face_tech import FaceAPI
```

	project_key = 'your project key'
	security_key = 'your security key'
	
	api = FaceAPI(project_key, security_key)


## Group

Create a new group with provided group name, and you can provide optional description to specify this group. This function will return the new group’s id.

	r = api.create_group(name='new group', desc=’create by Jim’)
	print(r)

The name may contain only letters, numbers, ' ' and @/./+/-/_ characters, make sure name is unique in your project.

Pass the group id to delete_group to delete the group you just created. This will return a boolean to tell you if it is successfully deleted.

	r = api.delete_group(group=1)
	print(r)


## Person

To create a new person, use create_person and provide new names you want. If new persons belong to a group you just created, pass group id to this function, it will create the relation with new persons with group. Additional email, first name, last name and note is optional while creating new person.

	r = api.create_person(name='james', email='test@test.com', 
						  first_name='James', last_name='Smith', 
						  note='freshman', group=2)
	print(r)

This will return a list of person id if no error. The name may contain only letters, numbers and @/./+/-/_ characters, and should be unique in your project. All these fields except 'group' can be list to create multiple persons at one time.

Or use create_person_json for creating person by json format, provide json format 'data' param and additional group id.

To get all persons exist in your project or a group, use following function to retrieve, where group should be the group id.

    r = api.get_persons_by_group(group=1)

    r = api.get_all_persons()

   	print(r)

To delete a person, you only have to provide person id you get when you created it. And it will return [{‘person_id’: True or False}], where False means you do not have the permission to delete because this person does not belong to your project, or this person does not exist. 'person' can be a list of person ids to delete multiple persons at one time.

	r = api.delete_person(person=1)
	print(r)


## Person to Group

If you have several groups in your project, you probably want to relate some persons to groups. Persons do not have to belong to any group, but it is good to divide them to speed up the searching process. 

If you assign a group id when you create new persons, you do not need to related them together again as below.

	r = api.person_to_group(person=12, group=2)

This will return a list of numbers instead of False, which means the row id of this relationship in server. Make sure all person ids are valid and belong to your project. 'person' can be list to relate many persons to one group at one time.

All parameters are the same as above when delete the relation by using remove_person_from_group.


## Detect faces and landmarks

You only need provide a valid image, detect function will return a list of face coordinates, which refer to [top, bottom, left, right]. Landmark detection will return all landmark coordinates and face coordinates.
	
```
from face_tech import file
```

	img = "image/sample.jpg"
	
	r = api.detect(image=file(img))
	print(r)
	>> [[74, 173, 312, 398], [107, 198, 86, 165]]

	r = api.landmark(image=file(img))
	print(len(r))
	>> [{'landmarks': [[303, 108], [302, 121] .. , 'coordinates': [115, 205, 85, 174]}, ..]

	r = api.occluder(image=file(img))
	print(r)
	>> [{'occlude': True, 'coordinates': [78, 186, 293, 400]}, ..]

## Face recognition

Before you want to recognize faces from images, you have to enroll faces into server. Provide a json format data to specify each person id and its face coordinates, then you can verify these persons next time. Group id is optional if this person does not belong to any group.

```
# specify person_id with face coordinates
data = {"faces": [{"person_id":63, "coordinates": [78, 186, 293, 400]}]} 
```
	
	r = api.enrollment_faces(data=data, image=file(img), group=2)
	print(r)

Or you can call check_quality every time before you enroll faces, this will tell you the quality of image you provided, retake a photo to improve the result.

	r = api.check_quality(image=file(img), data=False)
	print(r)
	
If data is True, it means it will return a filename which stored in sever. Just pass the result with  person ids to enrollment_faces, you do not need to pass a whole image again.

After you enroll faces to server, it’s time to verify them from photos.

	r = api.verification_faces(image=file(img), group=2)
	print(r)

Group id is optional when verify, and it will return person id as following.
	
	>> [{'person_id': 34, 'name': Jim, 'first_name': 'Jim', 'last_name': 'Smith', 'email': 'test@test.com', 'note': 'freshman', 'coordinates': [78, 186, 293, 400]}, {'person_id': 'None', 'coordinates': [175, 264, 214, 304]}]

If there is no match identification in record, the person_id will be None.