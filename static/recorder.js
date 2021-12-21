var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");
var buttonUpload = document.getElementById("upload");
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
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "false" }));
};

buttonUpload.onclick = function(){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr)
        }
    }
    xhr.open("POST", "/upload");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({AuthorName: "Tanweer Ali", Class: "10", Category: "Science"}));
};

function openForm() {
    document.getElementById("form1").style.display = "block";
}
  
function closeForm() {
    document.getElementById("myForm").style.display = "none";
}