from flask import Flask, render_template, request, redirect, url_for, send_from_directory,session
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
import os
from PIL import Image
import string
import urllib.request
from image_process import imgfilter
import datetime

SAVE_DIR = "./images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_url_path="")
app.secret_key = b'random string...'

@app.route('/')
def index():
    if "path" in session:
        msg = session["path"] +"が保存されました"
    else:
        msg = "何も保存されていません"
    return render_template("imagedemo.html",
            title="風景画モザイク処理",
            message = msg,
            images=os.listdir(SAVE_DIR)[::-1])

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)

@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        # 変換            
        img = imgfilter(stream)
        # 保存
        dt_now = "image" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        save_path = os.path.join(SAVE_DIR, dt_now + ".png")
        img.save(save_path)
        session["path"] = dt_now
        print("save", dt_now)

        return redirect('/')

if __name__ =="__main__":
    app.debug = True
    app.run(host="localhost")