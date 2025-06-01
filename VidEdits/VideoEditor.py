import shutil

from flask import Flask, render_template,request,jsonify
import subprocess
import os, base64

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

def clear_directory(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # delete directory and everything inside
    os.makedirs(dir_path)
@app.route('/')
def home():
    clear_directory(UPLOAD_FOLDER)
    return render_template('video.html')

@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists("uploads"):
        try:
            os.makedirs("uploads", exist_ok=True)
        except Exception as e:
            return jsonify({"message": f"Error: {e}" })
    try:
            if 'video' not in request.files:
                return jsonify({"message": "No video found"})

            file = request.files['video']
            filename = file.filename

            if not filename.lower().endswith('.mp4'):
                return jsonify({"message": "Only mp4 videos are allowed"})

            save_path = os.path.join("uploads", filename)
            file.save(save_path)

            return jsonify({"video": "upload was successful indeed"})
    except Exception as e:
        print("Error: ", e)



@app.route('/editor',methods=['POST'])
def editor():
    return render_template('editor.html')

def remove_audio(input_file, output_video):
    command = [
        "ffmpeg",
        "-i", input_file,  #used to identify what the input file is
        "-an", #removes the audio from the video
        output_video, #sets the edited video as the output video
    ]
    subprocess.run(command)
    return output_video

def change_brightness(input_file, output_video, level):
    command = [
        "ffmpeg",
        "-i", input_file, #used to identify what the input file is
        "-vf", f"eq=brightness={level}", #changes the brightness according to the users preference
        "-c:a", "copy",  # Ensures audio is copied without re-encoding
        output_video #sets the edited video as the output video
    ]
    subprocess.run(command)
    return output_video

def change_speed(input_file, output_video, speed):
    match = 1/speed
    command = [
        "ffmpeg",
        "-i", input_file, #used to identify what the input file is
        "-vf", f"setpts={speed}*PTS", #changes the speed according to the users preference
        "-af", f"atempo = {match}",  # Ensures audio is copied without re-encoding
        output_video #sets the edited video as the output video
    ]
    subprocess.run(command)
    return output_video
@app.route("/change_audio_api", methods=['POST'])
def change_audio_api():
    data = request.json
    input_file = data.get('input_file')
    output_video = data.get('output_video')
    result = remove_audio(input_file, output_video)
    return jsonify({"output_video": result})
@app.route("/change_brightness_api", methods=['POST'])
def change_brightness_api():
    data = request.json
    input_file = data.get('input_file')
    output_video = data.get('output_video')
    light = float(data.get('light'))
    result = change_brightness(input_file, output_video, light)
    return jsonify({"output_video": result})
@app.route('/change_speed_api', methods=['POST'])
def change_speed_api():
    data = request.json
    input_file = data.get('input_file')
    output_video = data.get('output_video')
    speed = float(data.get('speed'))

    result = change_speed(input_file, output_video, speed)
    return jsonify({"output_video": result})
@app.route("/product")
def product():
    return render_template("product.html")
if __name__ == '__main__':
    app.run(debug=True)