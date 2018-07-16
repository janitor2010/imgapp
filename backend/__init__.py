from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import os
import logging
import urllib
#import requests
import numpy as np
import cv2

import sys
#sys.path.append('backend/') # указываем директорию с проектом
#from imgApp import img as ImageDetection
from ImgApp.img import ImageDetection

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.secret_key = "super secret key"
app.debug = True

@app.route('/random',methods=['GET', 'POST'])
def upload_file():
    print(request.files)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in request.files:
            flash('No file part')
            return jsonify({'ok': 2})
        file = request.files['files']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return jsonify({'ok': 3,"method":request.method})
        if file:
            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            path = os.path.join(__location__, os.path.join('dist/static/up/', file.filename))
        #    path = os.path.join('/', file.filename)
        #    path = os.path.join('u/', file.filename)
            # return jsonify({'ok': 899,"method":path})
            file.save(path)

            im = ImageDetection.readImg(path)

            classes = ['Абстракционизм', 'Академизм','Импрессионизм']
        #    return jsonify({'ok': 25, 'os': os.getcwd(), 'ospath':os.path.dirname(__file__)})
            res, info = ImageDetection.mmainLight(im)
            print(info)
        #    im.saveToCSV()
            # prediction, accuracy = im.predict()
            return jsonify({'ok': 25,"class":classes[res[0]], "path": os.path.join('/static/up/', file.filename), 'info': info})

    # return jsonify({'ok': 1,"res":classes[res[0]],"path":path})
    else:
        return jsonify({'ok': 1,"res":"getettetetette"})

@app.route('/file-by-url',methods=['POST'])
def upload():
    url = request.get_json()['url']
    if request.method == 'POST':
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'

        classes = ['Абстракционизм', 'Академизм','Импрессионизм']
        res, info = ImageDetection.mmainLight(img)
    #    im.saveToCSV()
        # prediction, accuracy = im.predict()
        return jsonify({'ok': 25,"class":classes[res[0]],"path":url, 'info': info})

    # return jsonify({'ok': 1,"res":classes[res[0]],"path":path})
    else:
        return jsonify({'ok': 1,"res":"getettetetette"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return error

@app.errorhandler(405)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return error

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return e

if __name__ == '__main__':
    # app.debug = True

    # Use said info
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler("error1.log")
    # file_handler = logging.RotatingFileHandler("mylogFile.log",maxBytes= 2*1024*1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)


    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.run(debug=True)
