var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");
var buttonUpload = document.getElementById("download");
buttonStop.disabled = true;
buttonUpload.disabled=true;
buttonRecord.onclick = function() {
    // var url = window.location.href + "record_status";
    buttonRecord.disabled = true;
    buttonStop.disabled = false;
    
    // disable download link
    // var downloadLink = document.getElementById("download");
    // downloadLink.text = "";
    // downloadLink.href = "";

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "true" }));
};

buttonStop.onclick = function() {
    buttonRecord.disabled = false;
    buttonStop.disabled = true;    
    buttonUpload.disabled = false;
    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    // xhr.onreadystatechange = function() {
    //     if (xhr.readyState == 4 && xhr.status == 200) {
    //         // alert(xhr.responseText);

    //         // enable download link
    //         var downloadLink = document.getElementById("download");
    //         downloadLink.text = "Download Video";
    //         console.log("dl: ",downloadLink);
    //         downloadLink.href = "/static/video.avi";
    //     }
    // }
    // xhr.open("POST", "/record_status");
    // xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // xhr.send(JSON.stringify({ status: "false" }));
};

function openForm() {
    document.getElementById("form1").style.display = "block";
  }
  
  function closeForm() {
    document.getElementById("myForm").style.display = "none";
  }