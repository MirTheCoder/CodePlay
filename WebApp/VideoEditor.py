from flask import Flask, render_template
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
        "ffmpeg"
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
if __name__ == '__main__':
    app.run(debug=True)