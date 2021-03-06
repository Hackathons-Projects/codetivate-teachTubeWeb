from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import boto3,os

app = Flask(__name__)
data_file_folder = os.path.join(os.getcwd(), 'static')
  

s3 = boto3.client('s3',
    aws_access_key_id='AKIAS25EY3UPREEMHTW5',
    aws_secret_access_key= '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'
)
BUCKET_NAME='codetivate-teachtube'

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        json = request.get_json()
        name = json['name']
        title = json['title']
        classs = json['class']
        subject = json['subject']
        for file in os.listdir(data_file_folder):
            if file.startswith('v'):

                s3.upload_file(
                    os.path.join(data_file_folder, file),
                    BUCKET_NAME,
                    file
                )
                msg = "Upload Done !"
    return jsonify(msg="Uploaded Successfully")

if __name__ == '__main__':
    app.run(threaded=True)