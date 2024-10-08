# -*- coding: utf-8 -*-


from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.2
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='/home/zeeshan/DsProjects/tomato/model_vgg.h5'

# Load your trained VGG model
model = load_model(MODEL_PATH)

def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))  # VGG expects 224x224 image size

    # Preprocessing the image
    x = image.img_to_array(img)
    x = x / 255.0  # Normalize pixel values to [0, 1] range for VGG
    x = np.expand_dims(x, axis=0)  # Add batch dimension

    # Make predictions
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)

    # Map the prediction index to the respective disease label
    if preds == 0:
        preds = "The Disease is Bacterial_spot"
    elif preds == 1:
        preds = "The Disease is Early_blight"
    elif preds == 2:
        preds = "The Disease is Late_blight"
    elif preds == 3:
        preds = "The Disease is Leaf_Mold"
    elif preds == 4:
        preds = "The Disease is Septoria_leaf_spot"
    elif preds == 5:
        preds = "The Disease is Spider_mites Two-spotted_spider_mite"
    elif preds == 6:
        preds = "The Disease is Target_Spot"
    elif preds == 7:
        preds = "The Disease is Tomato_Yellow_Leaf_Curl_Virus"
    elif preds == 8:
        preds = "The Disease is Tomato_mosaic_virus"
    elif preds == 9:
        preds = "The Disease is healthy"
    elif preds == 10:
        preds = "The Disease is powdery_mildew"
       
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result = preds
        return result
    return None


if __name__ == '__main__':
    app.run(port=5001, debug=True)
