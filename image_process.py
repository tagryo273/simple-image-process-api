from tensorflow.keras.models import load_model
import tensorflow as tf
from PIL import Image
import numpy as np


def loss_function(y_true, y_pred):
    return tf.reduce_mean(tf.abs(y_true-y_pred), axis=(1,2,3))

def psnr(y_true, y_pred):
    return tf.image.psnr(y_true, y_pred, max_val=1.0)

def imgfilter(img):
    img = Image.open(img)
    img = img.resize((64,64), Image.LANCZOS)#リサイズする
    img = np.asarray(img, np.float32)/255.0#値を0~1にする
    img = img.reshape([1,64,64,3])
    model =load_model('./Unet_landscape.h5',custom_objects = {'loss_function': loss_function,'psnr':psnr})
    img = model.predict(img)*255
    img = img.reshape([64,64,3])
    img = np.asarray(img, np.uint8)
    img = Image.fromarray(img)
    return img

