# Introduction
 This is the APP client side of Attendance server, provide a user interface in mobile phone for user to enroll student and take attendance, also user can check module details and attendance history.   
 This APP is develop on [Phonegap](http://phonegap.com/) with [AngularJS](https://angularjs.org/) framework, it is easy to build app for Android and IOS.
 
 There are two important files [index.html][html] and [app.js][js], and [style.css][css] is used to define customized styles.

 [html]: https://github.com/fcharmy/face/blob/master/app_attendance/www/index.html
 [js]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js
 [css]: https://github.com/fcharmy/face/blob/master/app_attendance/www/css/style.css

# APP Interface
 This APP consists of below views to provide user a interface to connect to Attendance server. [View configuration][tabs] define which template and controller every view uses. Template is the html code defined in [index.html][html], and 'controller' is used to define variables and functions, 'params' is the parameters variables passed from one view to another.
 
 [tabs]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L35
 [login]: https://github.com/fcharmy/face/blob/master/app_attendance/www/index.html#L33
 [modules]: https://github.com/fcharmy/face/blob/master/app_attendance/www/index.html#L73
 [attend]: https://github.com/fcharmy/face/blob/master/app_attendance/www/index.html#L112
 [enroll]: https://github.com/fcharmy/face/blob/master/app_attendance/www/index.html#L151
 [home]: https://github.com/fcharmy/face/blob/master/app_attendance/www/index.html#L197
 [detail]: https://github.com/fcharmy/face/blob/master/app_attendance/www/index.html#L218
 [about]: https://github.com/fcharmy/face/blob/master/app_attendance/www/index.html#L262
 [login controller]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L110
 [modules controller]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L167
 [attend controller]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L253
 [about Controller]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L355
 [home controller]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L207
 [detail controller]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L624
 [lectureOrTutorial]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L515
 [match_face]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L461
 [drawRects]: https://github.com/fcharmy/face/blob/master/app_attendance/www/js/app.js#L746
 
* ## [Login View][login]
 There is a select list when login, user can choose to login by using IVLE account or regular account which created in Attendance website, this will change the url when login request submit as defined in [login controller][login controller].
 
 ![login image](https://github.com/fcharmy/face/blob/master/img/login.png =250x250)
 
* ## [Module View][modules]
 Modules view list out all available modules after login. When user click one, [modules controller][modules controller] will submit a request of update modules to server, update student list of current module, retrive and return all data will used in later views.

* ## [Attend View][attend]
 There are two button in attend view, 'Enrollment' and 'Take Attendance'. When user click one of them, [attend controller][attend controller] will open local camera to let user take a group photo. User can also choose a photo from phone Gallery, this function will be called when click 'back'.  
 
 After a photo is taken, controller will send a request with this photo to server, then switch current view to [Enrollment View][enroll].
 
* ## [Enrollment View][enroll]
 We have to mention here is that after clicking take attendance, current view will also switch to enrollment view, only difference is that the parameter is_enroll will be False, and when click submit, this will triger a dialog in [lectureOrTutorial][lectureOrTutorial]for user to choose whether it is a Lecture or a Tutorial.  
 
 [drawRects][drawRects] is a function not in any controller but it will be called in enrollment and detail view. It uses canvas tag to construct a image with rectangles on faces. When user choose a face displayed in the image, the rectangle will have thicker border, then choose a student in the list, this will call [match_face][match_face] in controller, this will match the choosen face with student info. 

* ## [Module Info view][about]
 [About Controller][about Controller] of module info view will show detail information about current module, and provide a back button for user to go back to choose another module.  

* ## [History View][home]
 When user choose a module in modules view, app retrive all history data of current module from server and display in this view. When list out attendance records, [home controller][home controller] will rearrange them into weeks. The week of first attendance record will the week 1. After clicking any attendance record, current view will switch to Detail view.
 
* ## [Detail View][detail]
 There are list of group images and two student lists in this view, attendee and absence list. Notice the owner name in the corner of this view, if the owner matches the current user, there is a '+' button on the right top. By clicking the button, just like click the 'Take Attendance' button, the only difference is that this will not create a new attendance record, instead [detail controller][detail controller] will add a new group photo into current attendance record, so there will be one more image in the images list after submission.
 
 
# Implementation
 When APP is updated, please refer [UPDATE.md](https://github.com/fcharmy/face/blob/master/app_attendance/UPDATE.md) to release a new version.
 
