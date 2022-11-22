from os import environ
import os
# import mongoengine

import urllib.request

# import cors as cors
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from heyoo import WhatsApp
from flask import Flask
# from flask_mongoengine import MongoEngine #ModuleNotFoundError: No module named 'flask_mongoengine' = (venv) C:\flaskmyproject>pip install flask-mongoengine
from os import environ

UPLOAD_FOLDER = 'static/images/'

app = Flask(__name__)
app.secret_key = "umer"
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'crud',
#     'host': 'localhost',
#     'port': 27017
# }
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','wav','mpeg','mp3','mp4'])
# db = MongoEngine()
# db.init_app(app)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('template.html')


# class User(db.Document):
#     profile_pic = db.StringField()

from flask_cors import CORS, cross_origin
CORS(app)
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # file.save(secure_filename(file.filename))
        # usersave = User( profile_pic=file.filename)
        # usersave.save()
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        o=url_for('static', filename='uploads/' + filename)
        l = 'https://myupla.herokuapp.com'+url_for('static', filename='images/' + filename)
        messenger = WhatsApp(environ.get("TOKEN"), phone_number_id=environ.get("PHONE_NUMBER_ID")) #this should be writen as

        # For sending  images
        # response = messenger.send_image(image=l,recipient_id="923462901820",)
        # response = messenger.send_audio(audio=l,recipient_id="923462901820")
        # response = messenger.send_video(video=l,recipient_id="923462901820",)
        response = messenger.send_document(document=l,recipient_id="923462901820",)
        # For sending an Image
        # messenger.send_image(
        #         image="https://i.imgur.com/YSJayCb.jpeg",
        #         recipient_id="91989155xxxx",
        #     )
        print(response)
        print('url is',l)

        return redirect(url_for('static', filename='images/' + filename), code=301)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@cross_origin()
@app.route('/pets', methods=['POST'])
def create_pet():
    pet_data = request.json

    name = pet_data['pet_name']
    print(name)


    return jsonify({"success": True, "response": "Pet added"})
if __name__ == "__main__":
    app.run(port=9900, debug=True)