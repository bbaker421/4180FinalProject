from app import app
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import face_recognition

# Load the jpg files into numpy arrays
daniel_image = face_recognition.load_image_file("known_people/daniel.jpg")
apurva_image = face_recognition.load_image_file("known_people/apurva.jpg")

daniel_face_encoding = face_recognition.face_encodings(daniel_image)[0]
apurva_face_encoding = face_recognition.face_encodings(apurva_image)[0]

known_faces = [
    daniel_face_encoding,
    apurva_face_encoding
]

@app.route('/')
@app.route('/index')
def index():
    return "Huzzah Authentication"

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    try:
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        unknown_image = face_recognition.load_image_file("./unknown_people/unknown_image.jpg")
        try:
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        except Exception as err:
            print('No faces')
            return "NO FACES"
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

        if results[1]:
            print("auth")
            #os.remove('unknown_people/unknown_image.jpg')
            return "1"
        else:
            #os.remove('unknown_people/unknown_image.jpg')
            print("inv")
            return "0"
    except Exception as err:
        print('error')
        return 'ERROR'