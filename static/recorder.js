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
    document.getElementById("form2").style.display = "block";
    window.scrollTo(0,document.body.scrollHeight);
};

function uploadFunc(event){
    event.preventDefault();
    console.log("hello");
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload");
    var name = document.getElementById("inputEmail4").value;
    var title = document.getElementById("inputTitle").value;
    var classs = document.getElementById("inputState").value;
    var subject = document.getElementById("inputcategory").value;
    if(!name || !title){
        alert("Name or Title Cannot be Empty!");
    }
    else{
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        var data={"name":name,"title":title, "class": classs, "subject": subject};
        xhr.send(JSON.stringify({ name: name, title: title, class: classs, subject: subject }));
        xhr.onload = () => {
            console.log(xhr.responseText);
            const obj = JSON.parse(xhr.responseText);
            if(obj.msg=="Uploaded Successfully"){
                alert(obj.msg)
                document.getElementById("inputEmail4").value = "";
                document.getElementById("inputTitle").value = "";
                document.getElementById("form2").style.display = "none";
                buttonStop.disabled = true;
                buttonUpload.disabled=true;
                buttonRecord.disabled = false;
            }
            else{
                alert("Can't be Uploaded at this Moment! Try Again")
            }
        }
    } 
}