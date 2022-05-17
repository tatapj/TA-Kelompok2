print("loading")
#import library yang di butuhkan
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

#setting ip server + nama folder web laravel
SERVER = "192.168.251.18/weather/public"

URL_get_new_img = "http://"+SERVER+"/api/get-new-image"   #url untuk check gambar baru yang masuk ke web laravel
URL_update_img = "http://"+SERVER+"/api/update-image"     #url untuk update status gambar setelah di recognize

model = keras.models.load_model('model_TA.h5')            #load model klasifikasi

filename_img = "gambar.jpg"                               #nama default gambar yang di download dari laravel ke python untuk proses recognize

def classify(path):             #fungsi klasifikasi cuaca
  print("classify")
  #predicting images
  #path = fn
  img = image.load_img(path, target_size = (150, 150))
  implot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis = 0)

  images = np.vstack([x])
  classes = model.predict(images, batch_size = 100)
  return classes                #output klasifikasi berupa array [1, 0, 0] artinya cuaca cerah | [0, 1, 0] cuaca hujan | [0, 0, 1] cuaca mendung



print("Starting system")
while True:
  #chek image terbaru yang masuk ke laravel dengan status belum di recognize
  try:
    print("check new img")
    check_new_img = requests.get(URL_get_new_img, timeout=3)  #check image terbaru dengan method GET
    #print(check_new_img.text)
    check_new_img_json = check_new_img.json()
    if check_new_img_json['status'] == 'success':  #bila ada image terbaru yang belum di recognize, status response laravel sukses
      #print(check_new_img_json)
      id_img = check_new_img_json['id']               #ambil ID image untuk keperluan update data recognize
      URL_download_img = check_new_img_json['image']  #ambil nama image untuk keperluan download image dan di recognize
      #print(id_img)
      #print(URL_download_img)
      img_data = requests.get(URL_download_img).content   #download gambar untuk proses recognize cuaca
      with open(filename_img, 'wb') as handler:
          handler.write(img_data)                 #save image after download
      result = classify(filename_img)             #proses klasifikasi cuaca, akan bernilai [1, 0, 0] / [0, 1, 0] / [0, 0, 1] selain kondisi di samping maka status recognize akan terisi "-"
      print(result[0])                            #tampilkan hasil klasifikasi
      cerah = int(result[0][0])                   #cerah array ke 0
      hujan = int(result[0][1])                   #hujan array ke 1
      mendung = int(result[0][2])                 #mendung array ke 2
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
      dataPost = {'id':int(id_img), 'kondisi_cuaca':Status_Klasifikasi, 'kondisi_jendela':int(Status_Jedela)}   #persiapan data update
      updateData = requests.post(URL_update_img, data=dataPost, timeout=3)    #update data image setelah hasil recognize
      print(updateData.text)
      updateData_json = updateData.json()
      print(updateData_json['status'])    #print response dari laravel
  except Exception as e:
    print(e)

  time.sleep(2)     #delay 2 detik sebelum looping program
