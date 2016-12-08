# Instruction
 This document is for Attendance Web Server, Attendance is a application based on [Face Tech][face tech], it has its own web page, server and database, but also obtain data from Face Tech.   
 Attendance APP is the client APP in mobile, which will cover [here][app]. Currently this application is integrated with IVLE public API of NUS, which means login with NUS account will automatically create modules and students for IVLE users, but also user can create their own personal module/group in Attendance website. Attendance user interface provide statistic report for each module in real time.  
 [face tech]: https://github.com/fcharmy/face/tree/master/face_web
 [app]: https://github.com/fcharmy/face/tree/master/app_attendance
 
# Data Structure
 Attendance obtain data from Face Tech, but it also has its own database on mySQL.   
 Except the data from other web service, there are two types of tables in Attendance, data from first type will be used for every user, eg. attend_recodes, the other type of tables only used for regular users, which means user create their account/modules/students in Attendance website, this is because we need to store their information in Attendance database, unlike IVLE users, data comes from other web service database.  
 [View Code](https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py)
 [Attendance]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L9
 [Attend_Recodes]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L17
 [Images]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L23
 [Modules]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L30
 [User_Module_Permission]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L43
 [Student]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L49
 
## Tables
### [Attendance][Attendance]  
 * module_id - CharField, max length is 50. if data comes from IVLE, format will be xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
 * group_id - IntegerField, each module is a group and group id comes from Face Tech
 * time - BigIntegerField and it is unique, eg. 20161208095348
 * lecture_or_tutorial - BooleanField. True for lecture, False for tutorial, default is True
 * owner - user name, max length is 50
 
Attendance table save all the class information for each module. Every time user take attendance, there will be a new record of attendance.   
The class can be a lecture or tutorial, depends on user's choice, and owner define which user can modify current class attendance.
 
### [Attend_Recodes][Attend_Recodes]  
 * attendance - ForeignKey, id of attendance, if attendance was deleted, corresponding attend_recodes will also be deleted
 * person_id - IntegerField, student's person id from Face Tech
 
For each class attendance, there are many students who attend this class. This table store attandee's person id from Face Tech, not user id.  
 
### [Images][Images]
 * attendance - ForeignKey, if attendance was deleted, corresponding attend_recodes will also be deleted
 * path - ImageField, group image full path in server
 * data - CharField and max length is 5120. This field is faces coordinates from current image
 * created - DateTimeField, auto generated with creation time  
 
For each class attendance, there can be many group images. All these group photo are saved in server, also faces coordinates in every photo.
 
### [Modules][Modules]
 * group_id - IntegerField, group id from Face Tech
 * code - CharField, max length is 50. Module code defined by user, and it must be unique
 * name - CharField and max length is 100, modules name defined by user
 * academic_year - CharField, max length is 20, Academic Year of module defined by user
 * semester - CharField, max length is 100, modules semester defined by user

 _**Method**_ to_dict:  
  return dictionary type of current modules object

Only for regular users who creates module on Attendacne website.

### [User_Module_Permission][User_Module_Permission]
 * user - ForeignKey, User object from auth.models of Django
 * module - ForeignKey, if module was deleted, corresponding user_module_permission will also be deleted
 * permission - 'F' for module owner, 'M' for TA

Only for regular users who creates module on Attendacne website.

### [Student][Student]
 * name - CharField, max length is 50 which can only contain letters, numbers and .@+-]+
 * email -  EmailField and optional
 * first_name - CharField, max length is 30 and optional
 * last_name - CharField, max length is 30 and optional
 * note - CharField, max length is 200 and optional
 * module - ForeignKey, if module was deleted, corresponding user_module_permission will also be deleted
 * created - DateTimeField, auto generated with creation time  

 _**Method**_ to_dict:  
  return dictionary type of current student object

Name and Module is a pair of unique key for this table. 
Only for regular users who creates student on Attendacne website.


## Private Functions

# Web Pages

# APIs
