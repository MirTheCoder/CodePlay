import shutil

from flask import Flask, render_template,request,jsonify
import subprocess
import os, base64
#This is how we will initially create our uploads directory
if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads", exist_ok=True)

app = Flask(__name__)

#This method will check and see if the uploads directory exists, and if it does then it will delete the directory (think of it as a directory reset),
#And then create teh same directory, but now it will be empty
def clear_directory(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # delete directory and everything inside
    os.makedirs(dir_path)
#This route will take us to the home page where we will call the home method to reset our uploads directory and then render the video template
@app.route('/')
def home():
    clear_directory("static/uploads")
    return render_template('video.html')

#This method right here is how we will the video file input from the user and save it to our uploads file
@app.route('/upload', methods=['POST'])
def upload():
    #Here we will check if the "uploads" directory exists and if it doesn't then we will create it
    if not os.path.exists("static/uploads"):
        try:
            os.makedirs("static/uploads", exist_ok=True)
        except Exception as e:
            #We will through this exception if there is an error in the creation of the uploads directory
            return jsonify({"message": f"Error: {e}" })
    try:
        #We will reset the upload directory
        clear_directory("static/uploads")
        #In this try statement, we will check to see if 1. The video file within the formData we are getting actually has a key value oor file attached to it
        #2. Check to see if the video file is a mp4 video
        if 'video' not in request.files:
            return jsonify({"message": "No video found"})
            #Where we request the video file from the HTML and store it
        file = request.files['video']
        filename = file.filename

        if not filename.lower().endswith('.mp4'):
            return jsonify({"message": "Only mp4 videos are allowed"})
            #We save the file to our uploads directory
        save_path = os.path.join("static/uploads", filename)
        file.save(save_path)
        #Return a jsonified data letting the user know that the upload to teh directory was a success
        return jsonify({"message": "upload was successful indeed"})
    except Exception as e:
        print("Error: ", e)


#Because we are using window.location.href (a javascript method) to navigate to the editor template, we have
#to make GET one of the acceptable methods since window.location uses GET request to navigate to a new window or location
@app.route('/editor',methods=['POST', 'GET'])
def editor():
    return render_template('editor.html')

def remove_audio(input_file, output_video):
    # This is the path hat we will be using to save out edited video to
    output_path = os.path.join("static/uploads", "output.mp4")
    #This is our FFMpeg command that is programmed to remove the audio from the users video
    command = [
        "ffmpeg",
        "-i", input_file,  #used to identify what the input file is
        "-an", #removes the audio from the video
        output_path, #saves the edited video to our output path which will save the video directly to our uploads folder as output.mp4, #sets the edited video as the output video
    ]
    #Needed to actually run the ffmpeg command
    try:
     subprocess.run(command, check=True)
    except Exception as e:
        print("Video editing error")
    # We use this following code to get the file name of the video in order to create a new path for the video in which we can use to store
    # the video within our uploads directory
    return output_path

def change_brightness(input_file, output_video, level):
    # This is the path hat we will be using to save out edited video to
    output_path = os.path.join("static/uploads", "output.mp4")
    # This is our FFMpeg command that is programmed to change the brightness of the users video
    command = [
        "ffmpeg",
        "-i", input_file, #used to identify what the input file is
        "-vf", f"eq=brightness={level}", #changes the brightness according to the users preference
        "-c:a", "copy",  # Ensures audio is copied without re-encoding
        output_path #saves the edited video to our output path which will save the video directly to our uploads folder as output.mp4
    ]
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print("Video editing error")
    # We use this following code to get the file name of the video in order to create a new path for the video in which we can use to store
    # the video within our uploads directory
    return output_path

def change_speed(input_file, output_video, speed):
    #This is the path hat we will be using to save out edited video to
    output_path = os.path.join("static/uploads", "output.mp4")
    #This is the value we will use to ensure that the audio matches the speed of the video
    match = 1/speed
    # This is our FFMpeg command that is programmed to change the brightness of the users video
    command = [
        "ffmpeg",
        "-i", input_file, #used to identify what the input file is
        "-vf", f"setpts={speed}*PTS", #changes the speed according to the users preference
        "-af", f"atempo ={match}",  # Ensures audio is copied without re-encoding
        output_path #saves the edited video to our output path which will save the video directly to our uploads folder as output.mp4
    ]
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print("Video editing error")
    # We use this following code to get the file name of the video in order to create a new path for the video in which we can use to store
    # the video within our uploads directory
    return output_path
@app.route("/change_audio_api", methods=['POST'])
def change_audio_api():
    #We get the data from the fetch command on teh javascript end
    data = request.json
    #We store all the file paths within the directory into this file and then select the first file
    files = [f for f in os.listdir("static/uploads") if os.path.isfile(os.path.join("static/uploads", f))]
    first_file = files[0]
    #will only run if the first_file has a file in it
    if first_file:
        #We fill the audio remover parameters with our video file and output video name
        input_file = first_file
        output_video = data.get('output_video')
        result = remove_audio(input_file, output_video)
        return jsonify({"message": result})
    else:
        #We return this if the first_file does not contain any files
        return jsonify({"message": "Unable to retrieve video for audio editing"})
@app.route("/change_brightness_api", methods=['POST'])
def change_brightness_api():
    # We get the data from the fetch command on teh javascript end
    data = request.json
    # We store all the file paths within the directory into this file and then select the first file
    files = [f for f in os.listdir("static/uploads") if os.path.isfile(os.path.join("static/uploads", f))]
    first_file = files[0]
    # will only run if the first_file has a file in it
    if first_file:
        # We fill the audio remover parameters with our video file, output video name, and the degree of which we want to change
        # the brightness of our video
        input_file = first_file
        output_video = data.get('output_video')
        light = float(data.get('light'))
        result = change_brightness(input_file, output_video, light)
        return jsonify({"message": result})
    else:
        # We return this if the first_file does not contain any files
        return jsonify({"message": "Unable to retrieve video for audio editing"})
@app.route('/change_speed_api', methods=['POST'])
def change_speed_api():
    # We get the data from the fetch command on teh javascript end
    data = request.json
    # We store all the file paths within the directory into this file and then select the first file
    files = [f for f in os.listdir("static/uploads") if os.path.isfile(os.path.join("static/uploads", f))]
    first_file = files[0]
    # will only run if the first_file has a file in it
    if first_file:
        # We fill the speed changer parameters with our video file, output video name, and degree we want to change our speed by
        input_file = first_file
        output_video = data.get('output_video')
        speed = float(data.get('speed'))
        result = change_speed(input_file, output_video, speed)
        return jsonify({"message": result})
    else:
        # We return this if the first_file does not contain any files
        return jsonify({"message": "Unable to retrieve video for audio editing"})
#This is what we will call to reveal the final video product after the video has been completely edited
@app.route("/product")
def product():
    files = [f for f in os.listdir("static/uploads") if os.path.isfile(os.path.join("static/uploads", f))]
    first_file = files[0]
    path = os.path.join("static/uploads",first_file)
    return render_template("product.html", video = path)
if __name__ == '__main__':
    app.run(debug=True)