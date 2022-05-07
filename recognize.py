#pip install pyyaml h5py
#pip install matplotlib

print("loading")
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import PIL
from keras.preprocessing import image
import requests
import json
import time

SERVER = "192.168.251.18/weather/public"
URL_get_new_img = "http://"+SERVER+"/api/get-new-image"
URL_update_img = "http://"+SERVER+"/api/update-image"

model = keras.models.load_model('model_TA.h5')

filename_img = "gambar.jpg"

def classify(path):
  print("classify")
  #predicting images
  #path = fn
  img = image.load_img(path, target_size = (150, 150))
  implot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis = 0)

  images = np.vstack([x])
  classes = model.predict(images, batch_size = 100)
  return classes

#print(classify("cuaca2.jpg"))

print("Starting system")
while True:
  try:
    print("check new img")
    check_new_img = requests.get(URL_get_new_img, timeout=3)
    #print(check_new_img.text)
    check_new_img_json = check_new_img.json()
    if check_new_img_json['status'] == 'success':
      #print(check_new_img_json)
      id_img = check_new_img_json['id']
      URL_download_img = check_new_img_json['image']
      #print(id_img)
      #print(URL_download_img)
      img_data = requests.get(URL_download_img).content
      with open(filename_img, 'wb') as handler:
          handler.write(img_data)
      result = classify(filename_img)
      print(result[0])
      cerah = int(result[0][0])
      hujan = int(result[0][1])
      mendung = int(result[0][2])
      Status_Klasifikasi = "-"
      Status_Jedela = 0
      if cerah == 1:
        Status_Klasifikasi = "Cerah"
        Status_Jedela = 1
      if hujan == 1:
        Status_Klasifikasi = "Hujan"
      if mendung == 1:
        Status_Klasifikasi = "Mendung"

      print(Status_Klasifikasi)
      print(Status_Jedela)
      dataPost = {'id':int(id_img), 'kondisi_cuaca':Status_Klasifikasi, 'kondisi_jendela':int(Status_Jedela)}
      updateData = requests.post(URL_update_img, data=dataPost, timeout=3)
      print(updateData.text)
      updateData_json = updateData.json()
      print(updateData_json['status'])
  except Exception as e:
    print(e)

  time.sleep(2)
