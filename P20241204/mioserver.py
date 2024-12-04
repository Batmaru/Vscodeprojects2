from flask import Flask, render_template, request
import os

api = Flask(__name__)

@api.route('/', methods=['GET'])
def index():
    return render_template('sendfile.html',pippo='ciao')


@api.route('/mansendfile', methods=['POST'])
def ricevidati():
    sDomanda = request.form.get("question")
    image = request.files.get("image")
    if image:
        image.save("./pippo.jpg")
    mio_answer = "ciao a tutti, MA PER ORA NON RISPONDO alla domanda " + sDomanda + "con file " 
    return render_template('sendfile.html',pippo=mio_answer)

api.run(host="0.0.0.0", port=8085)