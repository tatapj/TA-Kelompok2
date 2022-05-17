#import library yang digunakan
import cv2
import requests
import time
import json
import RPi.GPIO as GPIO

#setting ip server + nama folder web laravel
SERVER = "192.168.251.18/weather/public"


URL_save_capture = "http://"+SERVER+"/api/send-image"               #url untuk raspi mengirim gambar ke web dengan interval waktu tertentu
URL_klasifikasi_cuaca = "http://"+SERVER+"/api/getcuaca"            #url untuk mendapatkan hasil recognize cuaca dari web
URL_request_capture = "http://"+SERVER+"/api/cek-capture"           #url untuk cek secara berkala apakah ada perintah capture foto manual
URL_request_capture_save = "http://"+SERVER+"/api/capture-image"    #url untuk mengirim data foto dari perintah capture foto manual

#set camera default untuk capture foto
cam = cv2.VideoCapture(0)
img_name = "capture.jpg"                    #nama default foto saat capture

capture_interval = 60                       # detik interval pengiriman foto
last_capture = time.time()
capture_flag = False

print("starting system")

GPIO.setmode(GPIO.BCM)                      #set mode pinout GPIO
GPIO.setwarnings(False)

Relay = 4                                   #GPIO 4 

GPIO.setup(R1,GPIO.OUT)

GPIO.output(R1,True)                        # set relay OFF

while True:
    #check interval capture foto
    if time.time() - last_capture > capture_interval:
        capture_flag = True
    else:
        print("waiting time capture")

    if capture_flag:                        #jika waktunya capture foto
        try:
            ret, frame = cam.read()
            if not ret:                     #bila gagal membuka camera, maka ulangi 
                print("failed to grab frame")
                cam.release()
                cam = cv2.VideoCapture(0)
                ret, frame = cam.read()
            #cv2.imshow("Capture Img", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            cv2.imwrite(img_name, frame)                #save image foto
            print("Image captured")
            last_capture = time.time()
            files = {'gambar_cuaca': open(img_name, 'rb')}
            send_img = requests.post(URL_save_capture, files=files, timeout=3)      #kirim foto method POST ke web laravel
            #print(send_img.text)
            send_img_json = send_img.json()             #convert response dari web menjadi json
            if send_img_json['status'] == 'success':    #jika response sukses
                print("berhasil kirim gambar")
            capture_flag = False
            cam.release()
            cv2.destroyAllWindows()
            cam = cv2.VideoCapture(0)
                
        except Exception as e:                          #function handle error saat capture camera
            print(e)
            cam.release()
            cv2.destroyAllWindows()
            cam = cv2.VideoCapture(0)


    #cek klasifikasi cuaca
    try:
        check_klasifikasi_cuaca = requests.get(URL_klasifikasi_cuaca, timeout=3) #mengambil data hasil recognize cuaca dari web method GET
        #print(check_klasifikasi_cuaca.text)
        klasifikasi_cuaca_json = check_klasifikasi_cuaca.json()
        #print(klasifikasi_cuaca_json['message'])
        print(klasifikasi_cuaca_json['cuaca']['kondisi_cuaca'])
        print(klasifikasi_cuaca_json['cuaca']['kondisi_jendela'])
        if klasifikasi_cuaca_json['cuaca']['kondisi_jendela'] == "1":           # jika response kondisi_jendela adalah 1 (string), artinya mengaktifkan relay untuk menjalankan motor buka jendela
            GPIO.output(R1,False)           #relay aktif
            print("Jendela Terbuka")
        else:
            GPIO.output(R1,True)            #relay off
            print("jendela Tertutup")
    except Exception as e:
        print(e)


    #cek manual capture
    try:
        check_request = requests.get(URL_request_capture, timeout=3)  #cek perintah manual tombol capture dari web
        print(check_request.text)
        check_request_json = check_request.json()
        if check_request_json['status'] == 'success':                   #jika response status sukses maka artinya tombol capture di tekan
            #capture img
            ret, frame = cam.read()                                     #open camera
            if not ret:
                print("failed to grab frame")
                cam.release()
                cam = cv2.VideoCapture(0)
                ret, frame = cam.read()
            #cv2.imshow("Capture Img", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            cv2.imwrite(img_name, frame)                                #capture image foto
            print("Image manual captured")
            last_capture = time.time()
            files = {'gambar_cuaca': open(img_name, 'rb')}
            send_img = requests.post(URL_request_capture_save, files=files, timeout=3)      #kirim foto ke web method POST
            #print(send_img.text)
            send_img_json = send_img.json()
            if send_img_json['status'] == 'success':                    #bila response pengiriman sukses maka print berhasil kirim gambar
                print("berhasil kirim gambar")
            capture_flag = False
            cam.release()
            cv2.destroyAllWindows()
            cam = cv2.VideoCapture(0)
    except Exception as e:
        print(e)
        
    time.sleep(2)                                       #delay 2 detik sebelum program looping
        

