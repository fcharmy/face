// ajax request setting
var serverUrl = 'http://172.26.187.124:8000/',
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

var option = null,
    profile = {'MatriculationYear': '2013', 'FirstMajor': 'Nil', 'authToken': '89D406823E8DDDF3376EB92C9C5471B7487A515BB100B024D1664EC378C6E59D429A977902D378D375C1F042F94C9490E8B167DC8E9528C4B03912BFCF86EB3EB3A26F32F4C543362EA30703D974FA2CC09E3D3629B8D46CF4027B6BD84B1A2B441D1AA85139FFCFEA0F1E52D8A71B1923F19E98675FCA0E1E9A448D66D4B558401E661275A39DF227CA3AAFEBF13779CCDA031DB83EB4379C8C2687D3EA1BF6C7667AFD24AC52B23C0027AD5B6351D32CCCDDE80398F60078D28E0BF01BE6FCC724CF8000059379278E548C19612CED4EA43D6C8EA5F073CE93D693FC3C752F510F053DB38A4620A204E56D54592594', 'Modules': [{'ID': 'f786eceb-7861-46dc-90f2-436e8884405e', 'CourseCode': 'RI3001A', 'CourseName': 'Understanding Biometrics', 'CourseAcadYear': '2015/2016', 'face_group_id': 4, 'Permission': 'M', 'CourseSemester': 'Semester 4'}], 'Faculty': 'School of Computing', 'Email': 'a0112472@u.nus.edu', 'UserID': 'a0112472', 'Gender': 'Female', 'Name': 'LI JING', 'SecondMajor': ''}
;

// Ionic attendence App
angular.module('attendence', ['ionic'])
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
      cache: false,
      templateUrl: "tabs.html",
      params: { module: null }
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
        module: null,
        class: null
      },
      controller: 'enrollController'
    })    
    .state('detail', {
      url: "/detail",
      templateUrl: "detail.html",
      cache: false,
      params: { 
        data: null,
        module: null 
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
  $scope.loginOptions = [['ivle', "NUS Login"], ['attend', "Other"]];
  $scope.login_option = $scope.loginOptions[0];

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
    option = $scope.login_option[0];

    if (option != null){
      $scope.submit_loading(true);
      requestObj.url = serverUrl + option + '_login';
      requestObj.data = {username: username, password: password};

      requestObj.success = function(data){
        $scope.submit_loading(false);
        profile = data.data;
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
  $scope.modules = profile.Modules;

  $scope.choose_module = function(data){
    requestObj.url = serverUrl + option +'_module';
    requestObj.data = {data: data, token: profile.authToken};

    requestObj.success = function(data){
      $('#spinner').hide();
      $state.go('tabs.attend', {module: data.data});
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

.controller('homeController', function($scope, $stateParams, $state){
  $scope.stu_amount = $stateParams.module.student.length;

  // for show list in home tab
  $scope.attend_records = $stateParams.module.attendance? $stateParams.module.attendance : [];

  var monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  for (var i = 0; i < $scope.attend_records.length; i++) {
    $scope.attend_records[i].year = parseInt($scope.attend_records[i].time_id/1e10);
    $scope.attend_records[i].month = monthNames[parseInt($scope.attend_records[i].time_id%1e10/1e8) - 1];
    $scope.attend_records[i].date = parseInt($scope.attend_records[i].time_id%1e8/1e6);
    $scope.attend_records[i].hour = parseInt($scope.attend_records[i].time_id%1e6/1e4);
    $scope.attend_records[i].min = $scope.attend_records[i].time_id.toString().slice(10,12);

    var d = new Date($scope.attend_records[i].year, parseInt($scope.attend_records[i].time_id%1e10/1e8) - 1, $scope.attend_records[i].date);
    $scope.attend_records[i].day = dayNames[d.getDay()];
  };

  $scope.detail = function(index){
    $state.go('detail', {data: $scope.attend_records[index], module: $stateParams.module});
  }

  $scope.range = function(len){
    var list = [];
    for (var i = 0; i < len; i++) {
      list.push(i);
    };
    return list;
  };
})

.controller('attendController', function($scope, $stateParams, $state, $ionicModal, $ionicHistory){
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
      $state.go('enroll', {is_enroll: $scope.is_enroll, img: $scope.img, data: $scope.response_data, module: $stateParams.module});
      $scope.confirmModal.remove();
    };

    $scope.cancel = function() {
      $scope.confirmModal.hide();
    };
  });

  $scope.newRecord = function(ev){
    $scope.confirmModal.show();
    $('#confirm-canvas').hide();
    $('#confirm-img').show();
    $('#spinner').show();
    $('#confirm-button').prop('disabled', true);

    navigator.camera.getPicture(function(data){
      // take photo succeed
      $scope.is_enroll = ev;
      $scope.img = data;
      document.getElementById('confirm-img').src = $scope.img;

      uploadImg(serverUrl + (ev? 'detect': 'verify'), data, {group: $stateParams.module.face_group_id}, 
        function(r){
          // submit image to server succeed
          $scope.response_data = JSON.parse(r.response).data;
          highlight = null, curPointer = null;  // initial

          $('#spinner').hide();
          $('#confirm-button').prop('disabled', false);
          if ($scope.response_data.hasOwnProperty('faces')) {
                facesList = $scope.response_data.faces;
            drawRects('confirm-canvas', 'confirm-img', false);
          }; 
        }, 
        function(error){
          show_message(6, error.code);
          $scope.confirmModal.hide();
          $('#spinner').hide();
      });

    },function(message){
      // take photo failed
      show_message(7, message);
      $scope.confirmModal.hide();
      $('#spinner').hide();
    },{
      quality: 50, 
      correctOrientation: true, 
      encodingType: Camera.EncodingType.JPEG
    });
    
    // setTimeout(function(){
    //   $scope.is_enroll = ev;
    //   // $scope.img = "https://upload.wikimedia.org/wikipedia/commons/c/c7/Spencer_Davis_Group_1974.JPG";
    //   $scope.img = Math.random() < 0.5 ? "http://web.mit.edu/chemistry/jamison/images/Group%20Photos/Group%20Photo%207.3.2012.JPG"
    //     :"https://upload.wikimedia.org/wikipedia/commons/c/c7/Spencer_Davis_Group_1974.JPG";
    //   $scope.response_data = {"faces": [{'id': 134, "landmarks": null, "resolution": 1, "coordinates": [353, 427, 593, 667], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [245, 320, 842, 916], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [237, 311, 1190, 1265], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [759, 834, 1057, 1132], "occlude": "False", "illumination": 0}, {'id': 135, "landmarks": null, "resolution": 1, "coordinates": [336, 411, 1878, 1953], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [701, 776, 585, 659], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [353, 427, 1124, 1198], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [353, 427, 385, 460], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [334, 424, 124, 214], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [203, 278, 1397, 1472], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [369, 444, 767, 842], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [394, 469, 1298, 1373], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [187, 262, 452, 526], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [71, 145, 1099, 1173], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [266, 328, 1012, 1074], "occlude": "False", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [336, 411, 1655, 1729], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [759, 834, 842, 916], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [320, 394, 1489, 1563], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [394, 469, 949, 1024], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 1, "coordinates": [228, 303, 651, 726], "occlude": "True", "illumination": 0}, {"landmarks": null, "resolution": 0, "coordinates": [38, 74, 1605, 1641], "occlude": "True", "illumination": 0}]};

    //   document.getElementById('confirm-img').src = $scope.img;
    //   $('#spinner').hide();
    //   if ($scope.response_data.hasOwnProperty('faces')) {
    //     facesList = $scope.response_data.faces;
    //     drawRects('confirm-canvas', 'confirm-img', false);
    //   }
    //   $('#confirm-button').prop('disabled', false);
    // }, 1000);

  };
})

.controller('aboutController', function($scope, $stateParams, $state){
  // for about tab
  $scope.ID = $stateParams.module.ID;
  $scope.CourseCode = $stateParams.module.CourseCode;
  $scope.CourseName = $stateParams.module.CourseName;
  $scope.CourseAcadYear = $stateParams.module.CourseAcadYear;
  $scope.CourseSemester = $stateParams.module.CourseSemester;
  $scope.face_group_id = $stateParams.module.face_group_id;

  $scope.stu_amount = $stateParams.module.student.length;
  $scope.Permission = $stateParams.module.Permission;

  $scope.back = function(){
    $state.go('modules');
  };

})

.controller('enrollController', function($scope, $stateParams, $state, $ionicHistory){
  highlight = null, curPointer = null;  // initial
  $scope.img = $stateParams.img;
  $scope.student_list = $stateParams.module.student;
  $scope.data = $stateParams.data;

  if ($scope.data.hasOwnProperty('faces')) {
    facesList = $scope.data.faces;
    drawRects('img-canvas', 'enroll-img', true);
  }

  $scope.match_face = function(person){
    matching('img-canvas', 'enroll-img', person);
  };

  $scope.back = function(){
    $ionicHistory.goBack();
  };

  $scope.submit_enroll = function(){
    // remove unnessesary property before send request
    var cleaned_data = [], alter_list = [];
    for (var i = 0; i < facesList.length; i++) {
      cleaned_data.push({'coordinates': facesList[i].coordinates, 'id': facesList[i].id});

      if (!$stateParams.is_enroll && facesList[i].hasOwnProperty('alter') && facesList[i].alter) {
        alter_list.push({'coordinates': facesList[i].coordinates, 'id': facesList[i].id});
      };
    };
    $scope.data.faces = cleaned_data;
    $scope.data['enroll'] = alter_list;

    // enroll or add attend students
    requestObj.url = serverUrl + ($stateParams.is_enroll? 'enrollment': 'attendance');
    requestObj.data = {data: JSON.stringify($scope.data), group: $stateParams.module.face_group_id, 
      module: $stateParams.module.ID, owner: profile.Name, time_id: $stateParams.class? $stateParams.class.time_id: null};

    if (!$stateParams.is_enroll && !$stateParams.class) {
      if ('M' == $stateParams.module.Permission) {
        requestObj.data['lt'] = false;
      }else{  requestObj.data['lt'] = true; }
    }
    else if(!$stateParams.is_enroll && $stateParams.class){
      requestObj.data['lt'] = $stateParams.class.lt;
    }

    requestObj.success = function(data){
      $('#spinner').hide();
      if (data.hasOwnProperty('data')) {
        show_message(4);

        // send request to update tabs info
        requestObj.url = serverUrl + 'update_module';
        requestObj.data = {data: JSON.stringify($stateParams.module), token: profile.authToken};

        requestObj.success = function(data){
          $state.go('tabs.home', {module: data.data});
        };

        requestObj.error = function(xhr, status, error){
          if ('Not Acceptable' == error) {
            show_message(7, xhr.responseText);
          }
          else{
            show_message(0);
          }
          $state.go('tabs.home', {module: $stateParams.module});
        };

        $.ajax(requestObj);

      }else{
        show_message(5);
        $state.go('tabs.home', {module: $stateParams.module});
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

    $('#spinner').show();
    $.ajax(requestObj);

  };

})

.controller('detailController', function($scope, $stateParams, $state, $ionicHistory){
  $scope.student_list = $stateParams.module.student;
  $scope.add_disabled = !($stateParams.data.owner == profile.Name);
  $scope.images = $stateParams.data.images;
  $scope.serverUrl = serverUrl;
  $scope.img_index = 0;
  $scope.previous_disabled = true;
  $scope.next_disabled = $scope.images.length > 1? false : true;

  // show title and subtile on detail page
  $scope.title = $stateParams.data.date +' '+ $stateParams.data.month +' '+ $stateParams.data.year;
  $scope.subtitle = ($stateParams.data.lt? 'Lecture': 'Tutorial') +' on '+ $stateParams.data.day +' '+ $stateParams.data.hour 
    +':'+ $stateParams.data.min +' by '+ $stateParams.data.owner;

  // calculate the attend and abcent student list
  $scope.student_attend = [], $scope.student_absence = [];
  for (var i = 0; i < $scope.student_list.length; i++) {
    if ($.inArray($scope.student_list[i].id, $stateParams.data.students) < 0) {
      $scope.student_absence.push($scope.student_list[i]);
    }
    else{
      $scope.student_attend.push($scope.student_list[i]);
    }
  };

  $scope.$on("$ionicView.enter", function(event, data){
    $scope.change_list(true); // show attend list when entered
    $scope.draw();  // draw rectangle on img
  });

  $scope.draw = function(){
    if ($scope.images[$scope.img_index].hasOwnProperty('data')) {
      highlight = null, curPointer = null;  // initial
      facesList = $scope.images[$scope.img_index].data;
      drawRects('detail-canvas', 'detail-img', false);
    }
  };

  $scope.match_face = function(person){
    matching('detail-canvas', 'detail-img', person);
  };

  $scope.back = function(){
    $ionicHistory.goBack();
  };

  $scope.change_list = function(flag){
    $scope.tab_flag = flag;
    $scope.student_show_list = flag? $scope.student_attend: $scope.student_absence;
  };

  $scope.previous = function(){
    $scope.img_index--;
    $scope.previous_disabled = $scope.img_index > 0? false : true;
    $scope.next_disabled = $scope.img_index + 1 < $scope.images.length? false : true;

    $scope.draw();  // draw rectangle on img
  };

  $scope.next = function(){
    $scope.img_index++;
    $scope.previous_disabled = $scope.img_index > 0? false : true;
    $scope.next_disabled = $scope.img_index + 1 < $scope.images.length? false : true;

    $scope.draw();  // draw rectangle on img
  };

  $scope.add_photo = function(){
    $('#spinner').show();
    navigator.camera.getPicture(function(data){
      // take photo succeed
      $scope.img = data;

      uploadImg(serverUrl + 'verify', data, {group: $stateParams.module.face_group_id}, 
        function(r){
          $('#spinner').hide();
          // submit image to server succeed
          $scope.response_data = JSON.parse(r.response).data;
          $state.go('enroll', {is_enroll: false, img: $scope.img, data: $scope.response_data, 
            module: $stateParams.module, class: $stateParams.data});
        }, 
        function(error){
          $('#spinner').hide();
          show_message(6, error.code);
      });

    },function(message){
      // take photo failed
      $('#spinner').hide();
      show_message(7, message);
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
    // replace old canvas with new one to clear event lisener
    var canvas = document.getElementById(canvasId);
    var newc = canvas.cloneNode(true);
    canvas.parentNode.replaceChild(newc, canvas);

    var c = document.getElementById(canvasId),
      ctx = c.getContext("2d"),
      img = document.getElementById(imgId);

    // get actula img size which show in page
    document.getElementById(imgId).style.display = 'block';
    var actualimgWidth = img.width,
        actualimgHeight = img.height;

    // get original size of img and calculate their ratio
    document.getElementById(imgId).style.display = 'none';
    var imgWidth = img.width,
        imgHeight = img.height,
        ratio = actualimgWidth/imgWidth;

    // set canvas size and draw image in it
    c.width = actualimgWidth;
    c.height = actualimgHeight;
    ctx.drawImage(img, 0, 0, actualimgWidth, actualimgHeight);

    for (var i = 0; i < facesList.length; i++) {
      if (facesList[i].hasOwnProperty('coordinates')){
        coordinates = facesList[i].coordinates;

        var color = regular;
        if (facesList[i].hasOwnProperty('id') && facesList[i].id != 'None'){
          color = normal;
          $('#'+facesList[i].id).addClass('occupied');
        }
        else if (facesList[i].hasOwnProperty('id') && facesList[i].id == 'None'){
          color = error;
        }
        else if((facesList[i].hasOwnProperty('resolution') && facesList[i].resolution == 0) 
          || (facesList[i].hasOwnProperty('illumination') && facesList[i].illumination != 0)
          || (facesList[i].hasOwnProperty('occlude') && facesList[i].occlude == 'True')){
          color = warning;
        }

        ctx.beginPath();
        if (i == curPointer){
          ctx.rect(coordinates[2] * ratio - 5, coordinates[0] * ratio - 5, 
                  (coordinates[3] - coordinates[2]) * ratio + 10, (coordinates[1] - coordinates[0]) * ratio + 10);
          ctx.lineWidth = 8;

          // show person name under rectangle if has name
          if (facesList[i].hasOwnProperty('id') && facesList[i].id != 'None'){
            ctx.font = "15px Arial";
            ctx.fillStyle = normal;
            ctx.fillText(facesList[i].first_name, coordinates[2] * ratio - 5, coordinates[1] * ratio + 20); 
          }
        }
        else{
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
        };
      }
    }

    if (clickable) {
      c.onclick = function(e) {
        var dbclick = ($.now() - ctime < 500)? true:false;
        ctime = new Date($.now());

        for (var i = 0; i < facesList.length; i++) {
          if (e.offsetX >= facesList[i].coordinates[2]*ratio && e.offsetY >= facesList[i].coordinates[0]*ratio
            && e.offsetX <= facesList[i].coordinates[3]*ratio && e.offsetY <= facesList[i].coordinates[1]*ratio) {
            if(!dbclick){
              highlight = null;
              curPointer = i;
              drawRects(canvasId, imgId, clickable);
              return;
            }else{
              $('#'+facesList[i].id).removeClass('occupied');
              delete facesList[i]['id']; delete facesList[i]['name']; delete facesList[i]['first_name']; delete facesList[i]['alter'];
            }
          }
        };

        highlight = null;
        curPointer = null;
        drawRects(canvasId, imgId, clickable);
      };
    }

  }
  reloadRects();
  document.getElementById(canvasId).style.display = 'initial';
  document.getElementById(imgId).onload = window.onresize = reloadRects;
}


function matching(canvasId, imgId, person){
  if (curPointer != null && facesList) {
    if (facesList[curPointer].hasOwnProperty('id')) {

      if (confirm('This face already match to student ' 
        + facesList[curPointer].first_name + ' (' + facesList[curPointer].name 
        + '), are you sure to change to ' + person.first_name + ' (' + person.name + ')?')) {

        $('#'+facesList[curPointer].id).removeClass('occupied');
      }
      else{  return; }
    }

    if ($('#'+person.id).hasClass('occupied')) {
      if (confirm('This student already match to a face, are you sure to delete previous one?')){
        for (var i = 0; i < facesList.length; i++) {
          if (facesList[i].hasOwnProperty('id') && facesList[i].id == person.id) {
            delete facesList[i]['id']; delete facesList[i]['name']; delete facesList[i]['first_name']; delete facesList[i]['alter'];
          };
        }
      }
      else{  return; }
    };

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
    for (var i = 0; i < facesList.length; i++) {
      if (facesList[i].hasOwnProperty('id') && facesList[i].id == person.id) {
        highlight = i;
        drawRects(canvasId, imgId, true);
        break;
      };
    };
  };
}


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