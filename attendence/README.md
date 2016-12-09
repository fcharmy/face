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
 [get_image_path]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L73
 [get_suffix]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L78
 [get_time]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L82
 [new_image]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L86
 [get_records]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L95
 [get_user_modules]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/models.py#L113
 
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
#### [get_image_path][get_image_path]
 * input: module_id (string), time (integer)
 * output: unique image path in server

#### [get_suffix][get_suffix]
 * output: get a string of mins and seconds of current timesamp

#### [get_time][get_time]
 * output: get current full timesamp

#### [new_image][new_image]
 * input: path (string), attendance (object), data (string)
 * output: image object of None if fail

add a new row to image table with given image path, attendance object and data.

#### [get_records][get_records]
 * input: module id (string)
 * output: retrive all attendance records of given module id in json format

#### [get_user_modules][get_user_modules]
 * input: user (object)
 * output: retrive all modules which given user has permission of 'O', 'F', 'M', 'R'

# Web Pages
 As usual, there are many regular user interface like index, sign in, login, etc, source code will be list out as following.  
 In Attendance there are pages eg. user_index, view_module which is for all the users to review/export the statistic report, and other form pages for regular user to create module/students, all the forms used in user interface are in [forms.py][forms].
 [View Code](https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py)
 [forms]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/forms.py
 [index]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py#L21
 [sign_in]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py#L49
 [login_form]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py#L34
 [LoginForm]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/forms.py#L5
 [user_index]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py#L59
 [create_module]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py#L112
 [module_form]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py#L107
 [create_student]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py#L155
 [student_form]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/views.py#L144
 [dashboard]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/templates/attend/dashboard.html
 [Chart.bundle.js]: https://github.com/fcharmy/face/blob/master/attendence/attend_server/static/Chart.bundle.js
 [static]: https://github.com/fcharmy/face/tree/master/attendence/attend_server/static
 
 * #### [Home Page][index]  
  
 * #### [Sign in][sign_in]  
 
 * #### [Login][login_form]
  Use [LoginForm][LoginForm] then submit to [user_index][user_index].
  
 * #### [user_index][user_index]  
  Need login to show all available modules.  
  
 * #### [create_module][create_module]
  Destination of [module_form][module_form], regular user can create a new module and will submit to this page. If succeed, it will redirect to user_index, otherwise go back to module_form.
  
 * #### [create_student][create_student]
  Destination of [student_form][student_form], regular user can create new students and will submit to this page. If succeed, it will redirect to view_module, otherwise go back to student_form.
  
 * #### [view_module][view_module]
  This page use [dashboard.html][dashboard] as template to display statistic reports/charts, user can click the export button to download tables which conbine all those shown in this page. Related files are in [static][static] folder.  
  Bar chart is drawn by [Chart.bundle.js][Chart.bundle.js] which comes from [Chart.js](http://chartjs.org/).
  
# APIs
