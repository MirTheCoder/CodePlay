from flask import Flask, render_template,request,jsonify
import subprocess
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('video.html')

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
        "-vf", f"setpts={speed}*PTS", #changes the brightness according to the users preference
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