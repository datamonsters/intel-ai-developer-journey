sessionId = document.getElementById('session_id').value
var totalFiles = 0

btnEnabled = false;
checkFiles = function()
{
  if (totalFiles == 5)
  {
    document.getElementById('fileSubmit').classList.remove('btn-disabled');
    btnEnabled = true;
  }
  else
    if (btnEnabled) {
      document.getElementById('fileSubmit').className += 'btn-disabled';
      btnEnabled = false;
    }

}

checkFiles();

function newDZ(num)
{
  var prevFile = null;
  var myDropzone = new Dropzone("div#droparea"+String(num), {
    url: "uploadajax/"+sessionId+"/"+String(num),
    method: "POST", // can be changed to "put" if necessary
    maxFilesize: 10, // in MB
    paramName: "file", // The name that will be used to transfer the file
    uploadMultiple: true, // This option will also trigger additional events (like processingmultiple).
    headers: {
      "My-Awesome-Header": "header value"
    },
    renameFile: function (file) {
            return file.upload.filename ="file"+String(num)+"." + file.split('.').pop();
        },
    addRemoveLinks: true, // add an <a class="dz-remove">Remove file</a> element to the file preview that will remove the file, and it will change to Cancel upload
    previewsContainer: "#previewsContainer"+String(num),
    clickable: [document.getElementById('droparea'+String(num)), document.getElementById('uploadHint'+String(num))],
    createImageThumbnails: true,
    maxThumbnailFilesize: 10, // in MB
    thumbnailWidth: 200,
    thumbnailHeight: 200,
    maxFiles: 1,
    acceptedFiles: "image/jpeg", //This is a comma separated list of mime types or file extensions.Eg.: image/*,application/pdf,.psd.
    autoProcessQueue: true, // When set to false you have to call myDropzone.processQueue() yourself in order to upload the dropped files. 
    forceFallback: false,

    init: function() {

        },
    resize: function(file) {
        var w = file.width * (this.options.thumbnailHeight / file.height);
        var h = this.options.thumbnailHeight;
        if (w > this.options.thumbnailWidth)
        {
          w = this.options.thumbnailWidth;
          h = file.height * (this.options.thumbnailWidth / file.width);
        }
        var resizeInfo = {
            srcX: 0,
            srcY: 0,
            trgX: 0,
            trgY: 0,
            srcWidth: file.width,
            srcHeight: file.height,
            trgWidth: w,
            trgHeight: h
        };

        return resizeInfo;
    }, /*
    resize: function(file) {
      console.log("resize");
      return {"srcX":0, "srcY":0, "srcWidth":300, "srcHeight":300}
  },*/
    accept: function(file, done) {
      console.log("accept");
      done();
    },
    fallback: function() {
      console.log("fallback");
    }
  });

  /*
   * Custom preview template here.
   * ex) myDropzone.options.previewTemplate = '';
   */
  myDropzone.options.previewTemplate = '\
    <div class="dz-preview dz-file-preview">\
      <div class="dz-thumbnail-container">\
        <img class="dz-thumbnail" data-dz-thumbnail />\
      </div>\
    </div>\
    <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>\
    <div class="dz-error-message"><span data-dz-errormessage></span></div>\
    </div>';


  /*
   * Available Events
   */ 

  /* receive the "event" as first parameter */
  myDropzone.on("drop", function(event){
    console.log(event.type);
    console.log(event)
  });
  myDropzone.on("dragstart", function(event){ console.log(event.type); });
  myDropzone.on("dragend", function(event){ console.log(event.type); });
  myDropzone.on("dragenter", function(event){ console.log(event.type); });
  myDropzone.on("dragover", function(event){ console.log(event.type); });
  myDropzone.on("dragremove", function(event){ console.log(event.type); });


  /* receive the "file" as first parameter */
  myDropzone.on("addedfile", function(file) {
    console.log("addedfile");
    console.log(file);
      if (prevFile !== null) {
                    myDropzone.removeFile(prevFile);
                    console.log('YYY')
                }
      prevFile = file;
  });
  myDropzone.on("removedfile", function(file) { totalFiles -= 1; checkFiles(); prevFile = null; console.log("removedfile"); });
  myDropzone.on("selectedfiles", function(file) { console.log("selectedfiles"); });
  myDropzone.on("thumbnail", function(file) { console.log("thumbnail"); });
  myDropzone.on("error", function(file) { console.log("error"); });
  myDropzone.on("processing ", function(file) { console.log("processing "); });
  myDropzone.on("uploadprogress", function(file) { console.log("uploadprogress"); });
  myDropzone.on("sending", function(file) { console.log("sending"); });
  myDropzone.on("success", function(file) { totalFiles += 1; checkFiles(); console.log("success"); });
  
  myDropzone.on("canceled", function(file) { console.log("canceled"); });
  myDropzone.on("maxfilesreached", function(file) { console.log("maxfilesreached"); });
  myDropzone.on("maxfilesexceeded", function(file) { console.log("maxfilesexceeded"); });

  /* receive a "list of files" as first parameter
   * only called if the uploadMultiple option is true:
   */
  myDropzone.on("processingmultiple", function(files) { console.log("processingmultiple") });
  myDropzone.on("sendingmultiple", function(files) { console.log("sendingmultiple") });
  myDropzone.on("successmultiple", function(files) { console.log("successmultiple") });
  myDropzone.on("completemultiple", function(files) { console.log("completemultiple") });
  myDropzone.on("canceledmultiple", function(files) { console.log("canceledmultiple") });

  /* Special events */
  myDropzone.on("totaluploadprogress", function() { console.log("totaluploadprogress") });
  myDropzone.on("reset", function() { console.log("reset") });
  return myDropzone;
}

var dzs = [];



$(function() {
  dzs.push(newDZ(1));
  dzs.push(newDZ(2));
  dzs.push(newDZ(3));
  dzs.push(newDZ(4));
  dzs.push(newDZ(5));
  
  
  $('#fileSubmit').click(function(){
      var ready = true
      var notLoaded = false
      for (var i=0; i<dzs.length; i++){
        console.log(dzs[i].files.length, i)
        if (dzs[i].files.length<=0){
            ready = false
        } else {
            if (dzs[i].files[0].status != "success") {
              notLoaded = true
            }
        }
      }
      if (ready && !notLoaded)
      {
        window.location.href = 'show/' + sessionId;
        document.getElementById('spinner').classList.remove('displayno');
        document.getElementById('btn-aption').textContent = 'Generating Slideshow'
      }
      else if (!ready)
        alert('Add 5 fotos')
     else if (!notLoaded)
        alert('files not loaded, please whait or reload and try again') 
  });
});
