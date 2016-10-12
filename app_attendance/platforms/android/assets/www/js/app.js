// ajax request setting
var SERVER = 'http://172.26.187.110:8000/',
    requestObj = {
      type: "POST",
      dataType: 'json',
      headers: {},
      xhrFields: {
        withCredentials: true
      }
    },
    uploadImg = function(url, imgURI, params, success, fail){
      var options = new FileUploadOptions();
      options.fileKey="image";
      options.fileName=imgURI.substr(imgURI.lastIndexOf('/')+1);
      options.mimeType="image/jpeg";

      options.params = params;
      options.chunkedMode = false;

      var ft = new FileTransfer();
      ft.upload(imgURI, url, success, fail, options);
    };

// server response data hardcoded
var notMatched = 'None'; // When face is not recognized, person id is None

var OPTION = null, // specify login type
    PROFILE = null, // user profile after login
    aMODULE = null;
// var OPTION = 'ivle',
//     PROFILE = {'FirstMajor': 'Nil', 'Email': 'e0013178@u.nus.edu', 'Gender': 'Female', 'MatriculationYear': '2015', 'Name': 'SIVASANKARAN DIVYA', 'authToken': 'D41A734885A38795EDBC371AA5C3E6B318AB563B3C161E63D742FF11D777D5C9563E9A47B373CFF2A6E7D322974D119667BFD63027E5182A28DA7740F4BC1390E105007DEC08BAB9841220A111262F5C547DB72EB6F8CD3D4DF7E5893442882F1DC4FA918A6CFDBD15BE67BA7CF3FB409C7B1E60259CFA26C19480F8552E37108A8A27F2390ABF5349FBDCD737EEDD320711F1052527556FE2CC6B6927D67CF7E909549D5951EF653F0D36B84C9B351379B57C4497DC3EBEA07711C385D640A3435B7DDCA5E6D72EBF90683FC4925366AE9C74C59EE21FD39F18792364502AF8E4207808653D0A145BE864E8EF5DFE4D', 'Modules': [{'ID': '73efbd67-772e-4de3-b743-8e4f574378c0', 'face_group_id': 5, 'CourseSemester': 'Semester 1', 'CourseAcadYear': '2016/2017', 'CourseCode': 'CS1231', 'Permission': 'M', 'CourseName': 'DISCRETE STRUCTURES'}, {'ID': '8f248169-99fd-412c-a499-9308571befc5', 'face_group_id': 6, 'CourseSemester': 'Semester 1', 'CourseAcadYear': '2016/2017', 'CourseCode': 'NM3216', 'Permission': 'R', 'CourseName': 'GAME DESIGN'}], 'SecondMajor': '', 'UserID': 'e0013178', 'Faculty': 'School of Computing', 'Photo': ''};


// Ionic attendance App
angular.module('attendance', ['ionic'])
.config(function($stateProvider, $urlRouterProvider, $ionicConfigProvider){
  $stateProvider
    .state('login',{
      url: "/login",
      templateUrl: "login-page.html",
      controller: "loginController"
    })
    .state('modules',{
      url: "/modules",
      templateUrl: "modules.html",
      controller: 'moduleController'
    })
    .state('tabs',{
      url: "/tab",
      abstract: true,
      templateUrl: "tabs.html",
      controller: 'tabController'
    })
    .state('tabs.attend', {
      url: "/attend",
      views: {
        'attend-tab': {
          templateUrl: "attend.html",
          controller: 'attendController'
        }
      }
    })
    .state('tabs.home', {
      url: "/home",
      views: {
        'home-tab': {
          templateUrl: "home.html",
          controller: 'homeController'
        }
      }
    })
    .state('tabs.about', {
      url: "/about",
      views: {
        'about-tab': {
          templateUrl: "about.html",
          controller: 'aboutController'
        }
      }
    })
    .state('enroll', {
      url: "/enroll",
      templateUrl: "enroll.html",
      cache: false,
      params: { 
        is_enroll: null,
        img: null,
        data: null,
        class: null
      },
      controller: 'enrollController'
    })    
    .state('detail', {
      url: "/detail",
      templateUrl: "detail.html",
      cache: false,
      params: { 
        data: null
      },
      controller: 'detailController'
    });

  $urlRouterProvider.otherwise("/login");
  $ionicConfigProvider.tabs.position('bottom');
  $ionicConfigProvider.navBar.alignTitle('center');

})


.controller('loginController', function($scope, $http, $state){
  // $scope.hideList = true;
  $scope.submitDisable = false;
  $scope.loginOptions = [['ivle', "NUS Login"], ['attend', "Default"]];
  $scope.login_option = $scope.loginOptions[0];
  // ionic.Platform.isFullScreen = true;

  $scope.click_login_list = function(){
    // $scope.hideList = !$scope.hideList;
    $('#login-list').toggle(500);
  };


 $scope.choose_login = function(option){
    // $scope.hideList = true;
    $('#login-list').hide(500);
    $scope.login_option = option;
  };

  $scope.submit_loading = function(bool){
    $('#submit-button').prop( "disabled", bool );
    $('#submit-spinner').css( "display", (bool? 'block': 'none'));
  };

  $scope.login_submit = function(username, password){
    OPTION = $scope.login_option[0];

    if (OPTION != null){
      $scope.submit_loading(true);
      requestObj.url = SERVER + OPTION + '_login';
      requestObj.data = {username: username, password: password};

      requestObj.success = function(data){
        $scope.submit_loading(false);
        PROFILE = data.data;
        $state.go('modules', {data: data.data});
      };

      requestObj.error = function(xhr, status, error){
        if ('Not Acceptable' == error) {
          show_message(7, xhr.responseText);
        }
        else{
          show_message(0);
        }

        $scope.submit_loading(false);
      };

      $.ajax(requestObj);
    }
    else{
      show_message(2);
    }
  };
})

.controller('moduleController', function($scope, $state){
  $scope.modules = PROFILE.Modules;

  $scope.choose_module = function(data){
    requestObj.url = SERVER + OPTION + '_module';
    requestObj.data = {data: data, token: PROFILE.authToken};

    requestObj.success = function(data){
      if(data.data.student.length > 0) {
        aMODULE = data.data;
        $state.go('tabs.attend');
      }
      else{
        show_message(7, 'No Student.');
      }

      $('#spinner').hide();
    };

    requestObj.error = function(xhr, status, error){
      if ('Not Acceptable' == error) {
        show_message(7, xhr.responseText);
      }
      else{
        show_message(0);
      }
      $('#spinner').hide();
    };

    $('#spinner').show();
    $.ajax(requestObj);
  };
})

.controller('tabController', function($scope, $state){
  $scope.goState = function (state) {
    $state.go(state);
  };
})

.controller('homeController', function($scope, $state){
  $scope.stu_amount = aMODULE.student.length;

  // for show list in home tab
  $scope.attend_records = aMODULE.attendance? aMODULE.attendance : [];

  for (var i = 0; i < $scope.attend_records.length; i++) {
    var d = new Date(Date.UTC(parseInt($scope.attend_records[i].time_id/1e10),
        parseInt($scope.attend_records[i].time_id%1e10/1e8 - 1),
        parseInt($scope.attend_records[i].time_id%1e8/1e6),
        parseInt($scope.attend_records[i].time_id%1e6/1e4),
        parseInt($scope.attend_records[i].time_id%1e4/1e2), 0, 0));

    $scope.attend_records[i].year = d.getFullYear();
    $scope.attend_records[i].date = d.toLocaleDateString("en-us",{ month: "short", day: "numeric"});
    $scope.attend_records[i].time = d.toLocaleTimeString("en-us",{ hour: "2-digit", minute: "2-digit"});
    $scope.attend_records[i].day = d.toLocaleDateString("en-us",{ weekday: "long" });
    $scope.attend_records[i].week = d.getWeekNumber();

    if($scope.min_week == undefined || $scope.min_week > $scope.attend_records[i].week){
      $scope.min_week = $scope.attend_records[i].week;
    }
  }

  $scope.$on("$ionicView.afterEnter", function(event, data) {
    $('#spinner').hide();
    setTimeout(function () {
      for (var i = 0; i < $scope.attend_records.length; i++) {
        if(i == 0 || $scope.attend_records[i].week != $scope.attend_records[i-1].week){
          $('#'+$scope.attend_records[i].time_id).before('<li class="item item-divider">Week ' + ($scope.attend_records[i].week - $scope.min_week + 1) + '</li>');
        }
      }
    }, 0);
  });

  $scope.detail = function(index){
    $state.go('detail', {data: $scope.attend_records[index]});
  };

  $scope.range = function(len){
    var list = [];
    for (var i = 0; i < len; i++) { list.push(i); }
    return list;
  };
})

.controller('attendController', function($scope, $state, $ionicModal){
  $scope.$on("$ionicView.enter", function(event, data){

    // initial confirm modal and destory when hide
    $ionicModal.fromTemplateUrl('confirm.html', {
      scope: $scope,
      animation: 'slide-in-up'
    }).then(function(modal) {
      $scope.confirmModal = modal;
    });

    $scope.confirm = function() {
      // this will sperate into two conditions
      $state.go('enroll', {is_enroll: $scope.is_enroll, img: $scope.img, data: $scope.response_data});
      $scope.confirmModal.remove();
    };

    $scope.cancel = function() {
      $('#spinner').hide();
      $scope.confirmModal.hide();
    };
  });

  $scope.getPhoto = function (ev) {
    navigator.camera.getPicture(function(data){
      // take photo succeed
      $scope.newRecord(ev, data);

    },function(message){
      // take photo failed
      navigator.camera.getPicture(function (data) {
        // select photo succeed
        $scope.newRecord(ev, data);
      }, function () {
        show_message(7, message);
      }, {
        quality: 60,
        correctOrientation: true,
        destinationType: Camera.DestinationType.FILE_URI,
        sourceType: Camera.PictureSourceType.PHOTOLIBRARY
      });

    },{
      quality: 60,
      correctOrientation: true,
      encodingType: Camera.EncodingType.JPEG
    });
  };

  $scope.newRecord = function(ev, photo){
    // $scope.confirmModal.show();
    // $('#confirm-canvas').hide();
    // $('#confirm-img').show();
    $('#spinner').show();
    // $('#confirm-button').prop('disabled', true);

    $scope.is_enroll = ev;
    $scope.img = photo;
    // document.getElementById('confirm-img').src = $scope.img;

    uploadImg(SERVER + (ev? 'detect': 'verify'), photo, {group: aMODULE.face_group_id},
      function(r){
        // submit image to server succeed
        $scope.response_data = JSON.parse(r.response).data;
        highlight = null; curPointer = null;  // initial

        // $('#confirm-button').prop('disabled', false);
        // if ($scope.response_data.hasOwnProperty('faces')) {
        //       facesList = $scope.response_data.faces;
        //   drawRects('confirm-canvas', 'confirm-img', false);
        // }
        $state.go('enroll', {is_enroll: $scope.is_enroll, img: $scope.img, data: $scope.response_data});
      },
      function(error){
        show_message(6, error.code);
        // $scope.confirmModal.hide();
        $('#spinner').hide();
    });

  };

  $scope.test = function (ev) {
    $('#spinner').show();
    setTimeout(function(){
      $scope.is_enroll = ev;
      // $scope.img = "https://upload.wikimedia.org/wikipedia/commons/c/c7/Spencer_Davis_Group_1974.JPG";
      $scope.img = Math.random() < 0.5 ? "http://web.mit.edu/chemistry/jamison/images/Group%20Photos/Group%20Photo%207.3.2012.JPG"
        :"https://upload.wikimedia.org/wikipedia/commons/c/c7/Spencer_Davis_Group_1974.JPG";
      $scope.response_data = {"faces": [{'id': 13, "landmarks": null, "resolution": 1, "coordinates": [353, 427, 593, 667], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [245, 320, 842, 916], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [237, 311, 1190, 1265], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [759, 834, 1057, 1132], "occlude": "False", "illumination": 0}, {'id': 135, "landmarks": null, "resolution": 1, "coordinates": [336, 411, 1878, 1953], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [701, 776, 585, 659], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [353, 427, 1124, 1198], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [353, 427, 385, 460], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [334, 424, 124, 214], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [203, 278, 1397, 1472], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [369, 444, 767, 842], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [394, 469, 1298, 1373], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [187, 262, 452, 526], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [71, 145, 1099, 1173], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [266, 328, 1012, 1074], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [336, 411, 1655, 1729], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [759, 834, 842, 916], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [320, 394, 1489, 1563], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [394, 469, 949, 1024], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [228, 303, 651, 726], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 0, "coordinates": [38, 74, 1605, 1641], "occlude": "True", "illumination": 0}]};

      // document.getElementById('confirm-img').src = $scope.img;
      // if ($scope.response_data.hasOwnProperty('faces')) {
      //   facesList = $scope.response_data.faces;
      //   drawRects('confirm-canvas', 'confirm-img', false);
      // }
      // $('#confirm-button').prop('disabled', false);
      $state.go('enroll', {is_enroll: $scope.is_enroll, img: $scope.img, data: $scope.response_data});
    }, 1000);

  };
})

.controller('aboutController', function($scope, $state){
  $scope.$on("$ionicView.enter", function(event, data) {
    $scope.ID = aMODULE.ID;
    $scope.CourseCode = aMODULE.CourseCode;
    $scope.CourseName = aMODULE.CourseName;
    $scope.CourseAcadYear = aMODULE.CourseAcadYear;
    $scope.CourseSemester = aMODULE.CourseSemester;
    $scope.face_group_id = aMODULE.face_group_id;

    $scope.stu_amount = aMODULE.student.length;
    $scope.Permission = aMODULE.Permission;
  });

  $scope.back = function(){
    $state.go('modules');
  };

})

.controller('enrollController', function($scope, $stateParams, $state, $ionicPlatform, $ionicPopup){
  highlight = null; curPointer = null;  // initial
  $scope.img = $stateParams.img;
  $scope.data = $stateParams.data;
  $scope.student_list = $.extend(true, [], aMODULE.student);
  $scope.show_tutorial = aMODULE.tutorial != undefined;
  $scope.lt = (!$stateParams.is_enroll && $stateParams.class)? $stateParams.class.lt : null;

  $scope.$on("$ionicView.enter", function(event, data){
    $scope.orientationChange();

    if ($scope.data.hasOwnProperty('faces')) {
      facesList = $scope.data.faces;
      drawRects('img-canvas', 'enroll-img', true);
    }

    if ($scope.show_tutorial) {
        $scope.tutorial = $.extend(true, [], aMODULE.tutorial);
        for (var i = 0; i < $scope.tutorial.length; i++) {
          var k = Object.keys($scope.tutorial[i])[0];
          for (var j = 0; j < $scope.tutorial[i][k].length; j++) {
              $scope.tutorial[i][k][j] = $scope.student_list[$scope.tutorial[i][k][j]]
          }
        }
    }

    $('#spinner').hide();
  });

  $ionicPlatform.ready(function() {
    window.addEventListener("orientationchange", function(){$scope.orientationChange();}, false);
  });

  // To fix when keyboard show, rearrange orientation in css
  ionic.Platform.isFullScreen = true;
  $scope.orientationChange = function () {
    if (window.screen.orientation.type == 'portrait-primary') {
      // set image height, delay to wait for rotation
      setTimeout(function() { $('#enroll-img').height($(window).height()*0.48); }, 200);

      // add or remove class for each rotate
      $('.img-container').removeClass('img-container-landscape');
      $('.img-container').addClass('img-container-portrait');
      $('.student-list').removeClass('student-list-landscape');
      $('.student-list').addClass('student-list-portrait');
      $('.list-container').addClass('list-container-portrait');
      $('.list-container').removeClass('list-container-landscape');
    }
    else if (window.screen.orientation.type == 'landscape-primary'){
      // set image height, delay to wait for rotation
      setTimeout(function() { $('#enroll-img').height($(window).height()*0.93); }, 200);

      // add or remove class for each rotate
      $('.img-container').addClass('img-container-landscape');
      $('.img-container').removeClass('img-container-portrait');
      $('.student-list').removeClass('student-list-portrait');
      $('.student-list').addClass('student-list-landscape');
      $('.list-container').removeClass('list-container-portrait');
      $('.list-container').addClass('list-container-landscape');
    }
    else{
      console.log("Unknown orientation.");
    }
  };

  $scope.safeApply = function( fn ) {
    var phase = this.$root.$$phase;
    if(phase == '$apply' || phase == '$digest') {
        if(fn) {
            fn();
        }
    } else {
        this.$apply(fn);
    }
  };

  $scope.toggle_tutorial = function(tkey){
    for (var i = 0; i < $scope.tutorial.length; i++) {
      var k = Object.keys($scope.tutorial[i])[0];
      if(Object.keys($scope.tutorial[i])[0] == tkey){
        for(var j = 0; j < $scope.tutorial[i][k].length; j++){
          $('#' + $scope.tutorial[i][k][j].id).animate({height: 'toggle'}, 'fast');
        }
      }
    }
  };

  $scope.match_face = function(person){
    if (curPointer != null && facesList) {
      if (facesList[curPointer].hasOwnProperty('id')) {

        if (confirm('This face already match to student '
          + facesList[curPointer].first_name + ' (' + facesList[curPointer].name
          + '), are you sure to change to ' + person.first_name + ' (' + person.name + ')?')) {

          var flindex = $.map($scope.student_list, function(obj, index) { if(obj.id == facesList[curPointer].id) { return index; }})[0];
          if (flindex != undefined){
            delete $scope.student_list[flindex]['match'];
          }
        }
        else{  return ; }
      }

      var index = $.map($scope.student_list, function(obj, index) { if(obj.id == person.id) { return index; }})[0];
      if ($scope.student_list[index].hasOwnProperty('match') && $scope.student_list[index].match == 'occupied') {
        if (confirm('This student already match to a face, are you sure to delete previous one?')){
          for (var i = 0; i < facesList.length; i++) {
            if (facesList[i].hasOwnProperty('id') && facesList[i].id == person.id) {
              delete facesList[i]['id']; delete facesList[i]['name']; delete facesList[i]['first_name']; delete facesList[i]['alter'];
            }
          }
        }
        else{  return ; }
      }

      facesList[curPointer]['id'] = person.id;
      facesList[curPointer]['name'] = person.name;
      facesList[curPointer]['first_name'] = person.first_name;
      facesList[curPointer]['alter'] = true;
      $scope.student_list[index]['match'] = 'occupied';

      highlight = curPointer;
      curPointer = null;
      drawRects('img-canvas', 'enroll-img', true);
    }
    else if (curPointer == null && facesList) {
      for (var n = 0; n < facesList.length; n++) {
        if (facesList[n].hasOwnProperty('id') && facesList[n].id == person.id) {
          highlight = n;
          drawRects('img-canvas', 'enroll-img', true);
          break;
        }
      }
    }

  };

  $scope.back = function(){
    $state.go('tabs.attend');
  };

  $scope.lectureOrTutorial = function () {
    if (!$stateParams.is_enroll && !$stateParams.class) {
      $ionicPopup.show({
        title: 'Lecture or Tutorial',
        subTitle: 'Is this class a lecture or a tutorial? Please choose one to submit attendance.',
        scope: $scope,
        buttons: [
          { text: '<small>Cancel</small>',
            onTap: function(e) {
              $scope.lt = null;
            }
          },
          {
            text: '<b><small>Lecture</small></b>',
            type: 'button-positive',
            onTap: function(e) {
              $scope.lt = true;
            }
          },
          {
            text: '<b><small>Tutorial</small></b>',
            type: 'button-positive',
            onTap: function(e) {
              $scope.lt= false;
            }
          }
        ]
      }).then(function() {
        if($scope.lt != null){
          $('#spinner').show();
          $scope.submit_enroll();
        }
      });
    }else{ // or other condition, directly call submit_enroll
      $('#spinner').show();
      $scope.submit_enroll();
    }

  };

  $scope.submit_enroll = function(){
    // remove unnessesary property before send request
    var cleaned_data = [], alter_list = [];
    for (var i = 0; i < facesList.length; i++) {
      cleaned_data.push({'coordinates': facesList[i].coordinates, 'id': facesList[i].id});

      if (!$stateParams.is_enroll && facesList[i].hasOwnProperty('alter') && facesList[i].alter) {
        alter_list.push({'coordinates': facesList[i].coordinates, 'id': facesList[i].id});
      }
    }
    $scope.data.faces = cleaned_data;
    $scope.data['enroll'] = alter_list;

    // enroll or add attend students
    requestObj.url = SERVER + ($stateParams.is_enroll? 'enrollment': 'attendance');
    requestObj.data = {data: JSON.stringify($scope.data), group: aMODULE.face_group_id,
      module: aMODULE.ID, owner: PROFILE.Name, time_id: $stateParams.class? $stateParams.class.time_id: null};

    if($scope.lt != null){
      requestObj.data['lt'] =$scope.lt;
    }

    requestObj.success = function(data){
      if (data.hasOwnProperty('data')) {
        show_message(4);

        // send request to update tabs info
        requestObj.url = SERVER + OPTION + '_module';
        requestObj.data = {data: JSON.stringify(aMODULE), token: PROFILE.authToken};

        requestObj.success = function(data){
          aMODULE = data.data;
          $state.go('tabs.home');
        };

        requestObj.error = function(xhr, status, error){
          if ('Not Acceptable' == error) {
            show_message(7, xhr.responseText);
          }
          else{
            show_message(0);
          }
          $state.go('tabs.home');
        };

        $.ajax(requestObj);

      }else{
        show_message(5);
        $state.go('tabs.home');
      }
    };

    requestObj.error = function(xhr, status, error){
      $('#spinner').hide();
      if ('Not Acceptable' == error) {
        show_message(7, xhr.responseText);
      }
      else{
        show_message(0);
      }
    };

    $.ajax(requestObj);

  };

})

.controller('detailController', function($scope, $stateParams, $state){
  $scope.student_list = aMODULE.student;
  $scope.add_disabled = !($stateParams.data.owner == PROFILE.Name);
  $scope.images = $stateParams.data.images;
  $scope.serverUrl = SERVER;
  $scope.img_index = 0;
  $scope.previous_disabled = true;
  $scope.next_disabled = $scope.images.length < 2;

  // show title and subtile on detail page
  $scope.title = $stateParams.data.date +' '+ $stateParams.data.year;
  $scope.subtitle = ($stateParams.data.lt? 'Lecture': 'Tutorial') +' on '+ $stateParams.data.day +' '+ $stateParams.data.time +' by '+ $stateParams.data.owner;

  // calculate the attend and abcent student list
  $scope.student_attend = []; $scope.student_absence = [];
  for (var i = 0; i < $scope.student_list.length; i++) {
    if ($.inArray($scope.student_list[i].id, $stateParams.data.students) < 0) {
      $scope.student_absence.push($scope.student_list[i]);
    }
    else{
      $scope.student_attend.push($scope.student_list[i]);
    }
  }

  $scope.$on("$ionicView.enter", function(event, data){
    $scope.change_list(true); // show attend list when entered
    $scope.draw();  // draw rectangle on img
  });

  $scope.draw = function(){
    if ($scope.images[$scope.img_index].hasOwnProperty('data')) {
      highlight = null; curPointer = null;  // initial
      facesList = $scope.images[$scope.img_index].data;
      drawRects('detail-canvas', 'detail-img', false);
    }
  };

  $scope.match_face = function(person){
    if (facesList) {
      for (var n = 0; n < facesList.length; n++) {
        if (facesList[n].hasOwnProperty('id') && facesList[n].id == person.id) {
          highlight = n;
          drawRects('detail-canvas', 'detail-img', false);
          break;
        }
      }
    }
  };

  $scope.back = function(){
    $state.go('tabs.home');
  };

  $scope.change_list = function(flag){
    $scope.tab_flag = flag;
    $scope.student_show_list = flag? $scope.student_attend: $scope.student_absence;
  };

  $scope.previous = function(){
    $scope.img_index--;
    $scope.previous_disabled = ($scope.img_index <= 0);
    $scope.next_disabled = ($scope.img_index + 1 >= $scope.images.length);

    $scope.draw();  // draw rectangle on img
  };

  $scope.next = function(){
    $scope.img_index++;
    $scope.previous_disabled = ($scope.img_index <= 0);
    $scope.next_disabled = ($scope.img_index + 1 >= $scope.images.length);

    $scope.draw();  // draw rectangle on img
  };

  $scope.add_photo = function(){
    $('#spinner').show();
    navigator.camera.getPicture(function(data){
      // take photo succeed
      $scope.img = data;

      uploadImg(SERVER + 'verify', data, {group: aMODULE.face_group_id}, 
        function(r){
          // submit image to server succeed
          $scope.response_data = JSON.parse(r.response).data;
          $state.go('enroll', {is_enroll: false, img: $scope.img, data: $scope.response_data, class: $stateParams.data});
        }, 
        function(error){
          show_message(6, error.code);
          $('#spinner').hide();
      });

    },function(message){
      // take photo failed
      show_message(7, message);
      $('#spinner').hide();
    },{
      quality: 50, 
      correctOrientation: true, 
      encodingType: Camera.EncodingType.JPEG
    });

  };
});



/* 
  For drawing rectangles on image and specify current face
*/

var facesList = [],     // copy of face list
    highlight = null,   // highlight a face
    curPointer = null,  // point to the index of current face
    ctime = new Date(); // for save last single click time 

var normal = 'green',   // faces with identification
    regular = 'blue',   // faces detected without id
    warning = 'orange', // bad quality
    error = 'red';      // faces cannot be verfied

// Draw rectangles on image to highlight faces, 
// set facesList first before call this function
function drawRects(canvasId, imgId, clickable){
  var reloadRects = function(){
    if(document.getElementById(canvasId) != null) {
      // replace old canvas with new one to clear event lisener
      var canvas = document.getElementById(canvasId);
      var newc = canvas.cloneNode(true);
      canvas.parentNode.replaceChild(newc, canvas);

      var c = document.getElementById(canvasId),
          ctx = c.getContext("2d"),
          div = document.getElementsByClassName('card')[0];
          img = document.getElementById(imgId);

      // get actula img size which show in page
      // document.getElementById(imgId).style.display = 'block';
      var actualimgHeight = div.offsetHeight-6;

      // get original size of img and calculate their ratio
      // document.getElementById(imgId).style.display = 'none';
      var imgWidth = img.width,
          imgHeight = img.height,
          ratio = actualimgHeight / imgHeight;

      // set canvas size and draw image in it
      var actualimgWidth = actualimgHeight/imgHeight*imgWidth;
      c.width = actualimgWidth;
      c.height = actualimgHeight;
      ctx.drawImage(img, 0, 0, actualimgWidth, actualimgHeight);

      for (var i = 0; i < facesList.length; i++) {
        if (facesList[i].hasOwnProperty('coordinates')) {
          coordinates = facesList[i].coordinates;

          var color = regular;
          if (facesList[i].hasOwnProperty('id') && facesList[i].id != notMatched) {
            color = normal;

            // Find student id of current face, and mark it as occupied
            // $('#' + facesList[i].id).addClass('occupied');
            if(clickable){
              var scope = angular.element($("#"+canvasId)).scope();
              scope.safeApply(function(){
                var index = $.map(scope.student_list, function(obj, index) { if(obj.id == facesList[i].id) { return index; }})[0];
                if(index != undefined){
                  scope.student_list[index]['match'] = 'occupied';
                }
              });
            }

          }
          else if (facesList[i].hasOwnProperty('id') && facesList[i].id == notMatched) {
            color = error;
          }
          else if ((facesList[i].hasOwnProperty('resolution') && facesList[i].resolution == 0)
              || (facesList[i].hasOwnProperty('illumination') && facesList[i].illumination != 0)
              || (facesList[i].hasOwnProperty('occlude') && facesList[i].occlude == 'True')) {
            color = warning;
          }

          ctx.beginPath();
          if (i == curPointer) {
            ctx.rect(coordinates[2] * ratio - 5, coordinates[0] * ratio - 5,
                (coordinates[3] - coordinates[2]) * ratio + 10, (coordinates[1] - coordinates[0]) * ratio + 10);
            ctx.lineWidth = 8;

            // show person name under rectangle if has name
            if (facesList[i].hasOwnProperty('id') && facesList[i].id != notMatched) {
              ctx.font = "15px Arial";
              ctx.fillStyle = normal;
              ctx.fillText(facesList[i].first_name, coordinates[2] * ratio - 5, coordinates[1] * ratio + 20);
            }
          }
          else {
            ctx.rect(coordinates[2] * ratio, coordinates[0] * ratio,
                (coordinates[3] - coordinates[2]) * ratio, (coordinates[1] - coordinates[0]) * ratio);
            ctx.lineWidth = 2;
          }
          ctx.strokeStyle = color;
          ctx.stroke();

          if (i == highlight) {
            ctx.beginPath();
            ctx.rect(coordinates[2] * ratio - 3, coordinates[0] * ratio - 3,
                (coordinates[3] - coordinates[2]) * ratio + 6, (coordinates[1] - coordinates[0]) * ratio + 6);
            ctx.lineWidth = 5;
            ctx.strokeStyle = 'white';
            ctx.stroke();
          }
        }
      }

      if (clickable) {
        c.onclick = function (e) {
          var dbclick = ($.now() - ctime < 500);
          ctime = new Date($.now());

          for (var i = 0; i < facesList.length; i++) {
            if (e.offsetX >= facesList[i].coordinates[2] * ratio && e.offsetY >= facesList[i].coordinates[0] * ratio
                && e.offsetX <= facesList[i].coordinates[3] * ratio && e.offsetY <= facesList[i].coordinates[1] * ratio) {
              if (!dbclick) {
                highlight = null;
                curPointer = i;
                drawRects(canvasId, imgId, clickable);
                return;
              } else {
                // Remove corresponding occupied marker from scope student_list
                // $('#' + facesList[i].id).removeClass('occupied');
                var scope = angular.element($("#"+canvasId)).scope();
                scope.safeApply(function(){
                  var index = $.map(scope.student_list, function(obj, index) { if(obj.id == facesList[i].id) { return index; }})[0];
                  if(index != undefined){
                    delete scope.student_list[index]['match'];
                  }
                });

                delete facesList[i]['id'];
                delete facesList[i]['name'];
                delete facesList[i]['first_name'];
                delete facesList[i]['alter'];
              }
            }
          }

          highlight = null;
          curPointer = null;
          drawRects(canvasId, imgId, clickable);
        };
      }
    }
  };

  reloadRects();
  document.getElementById(canvasId).style.display = 'initial';
  document.getElementById(imgId).onload = reloadRects;//window.onresize =

  window.addEventListener("orientationchange", function(){
    setTimeout(function() {
        reloadRects();
    }, 200);
  });
}


/*function matching(canvasId, imgId, person){
  if (curPointer != null && facesList) {
    if (facesList[curPointer].hasOwnProperty('id')) {

      if (confirm('This face already match to student ' 
        + facesList[curPointer].first_name + ' (' + facesList[curPointer].name 
        + '), are you sure to change to ' + person.first_name + ' (' + person.name + ')?')) {

        $('#'+facesList[curPointer].id).removeClass('occupied');
      }
      else{  return ; }
    }

    if ($('#'+person.id).hasClass('occupied')) {
      if (confirm('This student already match to a face, are you sure to delete previous one?')){
        for (var i = 0; i < facesList.length; i++) {
          if (facesList[i].hasOwnProperty('id') && facesList[i].id == person.id) {
            delete facesList[i]['id']; delete facesList[i]['name']; delete facesList[i]['first_name']; delete facesList[i]['alter'];
          }
        }
      }
      else{  return ; }
    }

    facesList[curPointer]['id'] = person.id;
    facesList[curPointer]['name'] = person.name;
    facesList[curPointer]['first_name'] = person.first_name;
    facesList[curPointer]['alter'] = true;
    $('#'+person.id).addClass('occupied');

    highlight = curPointer;
    curPointer = null;
    drawRects(canvasId, imgId, true);
  }
  else if (curPointer == null && facesList) {
    for (var n = 0; n < facesList.length; n++) {
      if (facesList[n].hasOwnProperty('id') && facesList[n].id == person.id) {
        highlight = n;
        drawRects(canvasId, imgId, true);
        break;
      }
    }
  }
}*/


function show_message(){
  switch(arguments[0]){
    case 0:
      alert('Network Error'); break;
    case 1:
      alert('Invalid Username or Password'); break;
    case 2:
      alert('Not Avaliable'); break;
    case 3:
      alert('Invalid Module'); break;
    case 4:
      alert('Update Succeed'); break;
    case 5:
      alert('Update Failed'); break;
    case 6:
      alert("An error has occurred: Code = " + arguments[1]); break;
    case 7:
      alert(arguments[1]); break;
    default:
      alert('Unknown Error');
  }
}

// calculate date's week number in current year
Date.prototype.getWeekNumber = function() {
  var d = new Date(+this);
  d.setHours(0,0,0);
  d.setDate(d.getDate()+4-(d.getDay()||7));
  return Math.ceil((((d-new Date(d.getFullYear(),0,1))/8.64e7)+1)/7);
};
