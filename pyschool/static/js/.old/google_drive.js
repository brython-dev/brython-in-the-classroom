var CLIENT_ID = '811911740723-i5a32ld5q1ugfgmgkgpl3st0b831qp2g.apps.googleusercontent.com';
var SCOPES = ['https://www.googleapis.com/auth/drive', 
              'https://www.googleapis.com/auth/userinfo.profile'].join(' ');

      /**
       * Called when the client library is loaded to start the auth flow.
       */
function handleClientLoad() {
   console.log("handleClientLoad")
   //document.getElementById("login").style.display="block";
   //window.setTimeout(checkAuth, 1);
   checkAuth()
}

      /**
       * Check if the current user has authorized the application.
       */
function checkAuth() {
   var authButton = document.getElementById('authorizeButton');

   authButton.onclick= function() {
       gapi.auth.authorize(
            {'client_id': CLIENT_ID, 'scope': SCOPES, 'immediate': false},
            handleAuthResult);
       return false;
   };

   gapi.auth.authorize(
        {'client_id': CLIENT_ID, 'scope': SCOPES, 'immediate': true},
        handleAuthResult);

}

      /**
       * Called when authorization server replies.
       *
       * @param {Object} authResult Authorization result.
       */
function handleAuthResult(authResult) {
        if (authResult && !authResult.error) {
           // Access token has been successfully retrieved, requests can be sent to the API.
           $('#login').dialog({closed:true})

           gapi.client.load('plus','v1', function(){
              var request = gapi.client.plus.people.get({'userId': 'me'});
              request.execute(function(resp) {
                 document.getElementById("username").innerHTML=resp.displayName;
                 document.getElementById("userthumbnail").src=resp.image.url;
                 console.log('Retrieved profile for:' + resp.displayName);
              });
           });
        } else {
          // No access token could be retrieved, show the button to start the authorization flow.
          // show dialog asking person to login
           $('#login').dialog({closed:false})
        }
}

      /**
       * Start the file upload.
       *
       * @param {Object} evt Arguments from the file selector.
       */
function uploadFile(evt) {
        gapi.client.load('drive', 'v2', function() {
          var file = evt.target.files[0];
          insertFile(file);
        });
}

function initialize_drive() {
     gapi.client.load('drive', 'v2', function() {
        
        insertFile(file);
     });
}

function root_dir_check( ) {
  var check_for_brython_root=function(request, callback) {
     request.execute(function(resp) {
        var found=false
        for (var i=0; i < resp.items.length; i++) {
            if (resp.items[i] == 'brython') found=true 
        }

        if (!found) {  // we didn't find a brython directory, so lets create it!
           var mkdir = gapi.client.request({
                   'path': '/upload/drive/v2/files',
                   'method': 'POST',
                   'params': {'title': 'brython', 'parents': 'root',
                              'mimeType': 'application/vnd.google-apps.folder'}
           });

           mkdir.execute(function(file) { console.log(file)}); 
        }
     });
  }
  var _r=gapi.client.drive.children.list({'folderId': 'root'});
    
  check_for_brython_root(_r, []);
}

      /**
       * Insert new file.
       *
       * @param {File} fileData File object to read data from.
       * @param {Function} callback Function to call when the request is complete.
       */
function insertFile(fileData, callback) {
        const boundary = '-------314159265358979323846';
        const delimiter = "\r\n--" + boundary + "\r\n";
        const close_delim = "\r\n--" + boundary + "--";

        var reader = new FileReader();
        reader.readAsBinaryString(fileData);
        reader.onload = function(e) {
          var contentType = fileData.type || 'application/octet-stream';
          var metadata = {
            'title': fileData.name,
            'mimeType': contentType
          };

          var base64Data = btoa(reader.result);
          var multipartRequestBody =
              delimiter +
              'Content-Type: application/json\r\n\r\n' +
              JSON.stringify(metadata) +
              delimiter +
              'Content-Type: ' + contentType + '\r\n' +
              'Content-Transfer-Encoding: base64\r\n' +
              '\r\n' +
              base64Data +
              close_delim;

          var request = gapi.client.request({
              'path': '/upload/drive/v2/files',
              'method': 'POST',
              'params': {'uploadType': 'multipart'},
              'headers': {
                'Content-Type': 'multipart/mixed; boundary="' + boundary + '"'
              },
              'body': multipartRequestBody});
          if (!callback) {
            callback = function(file) {
              console.log(file)
            };
          }
          request.execute(callback);
        }
}

/*
var _s=document.createElement("script")
_s.type="text/javascript"
_s.src="https://apis.google.com/js/client.js?onload=handleClientLoad"

document.getElementsByTagName("head")[0].appendChild(_s)
*/
