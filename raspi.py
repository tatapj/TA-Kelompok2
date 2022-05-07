import cv2
import requests
import time
import json

SERVER = "192.168.251.18/weather/public"

URL_save_capture = "http://"+SERVER+"/api/send-image"
URL_klasifikasi_cuaca = "http://"+SERVER+"/api/getcuaca"
URL_request_capture = "http://"+SERVER+"/api/cek-capture"
URL_request_capture_save = "http://"+SERVER+"/api/capture-image"

cam = cv2.VideoCapture(0)
img_name = "capture.jpg"

capture_interval = 60     # detik
last_capture = time.time()
capture_flag = False

print("starting system")

while True:
    #check interval capture
    if time.time() - last_capture > capture_interval:
        capture_flag = True
    else:
        print("waiting time capture")

    if capture_flag:
        try:
            ret, frame = cam.read()
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
            cv2.imwrite(img_name, frame)
            print("Image captured")
            last_capture = time.time()
            files = {'gambar_cuaca': open(img_name, 'rb')}
            send_img = requests.post(URL_save_capture, files=files, timeout=3)
            #print(send_img.text)
            send_img_json = send_img.json()
            if send_img_json['status'] == 'success':
                print("berhasil kirim gambar")
            capture_flag = False
            cam.release()
            cv2.destroyAllWindows()
            cam = cv2.VideoCapture(0)
                
        except Exception as e:
            print(e)
            cam.release()
            cv2.destroyAllWindows()
            cam = cv2.VideoCapture(0)


    #cek klasifikasi cuaca
    try:
        check_klasifikasi_cuaca = requests.get(URL_klasifikasi_cuaca, timeout=3)
        #print(check_klasifikasi_cuaca.text)
        klasifikasi_cuaca_json = check_klasifikasi_cuaca.json()
        #print(klasifikasi_cuaca_json['message'])
        print(klasifikasi_cuaca_json['cuaca']['kondisi_cuaca'])
        print(klasifikasi_cuaca_json['cuaca']['kondisi_jendela'])
        if klasifikasi_cuaca_json['cuaca']['kondisi_jendela'] == "1":
            print("Jendela Terbuka")
        else:
            print("jendela Tertutup")
    except Exception as e:
        print(e)


    #cek manual capture
    try:
        check_request = requests.get(URL_request_capture, timeout=3)
        print(check_request.text)
        check_request_json = check_request.json()
        if check_request_json['status'] == 'success':
            #capture img
            ret, frame = cam.read()
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
            cv2.imwrite(img_name, frame)
            print("Image manual captured")
            last_capture = time.time()
            files = {'gambar_cuaca': open(img_name, 'rb')}
            send_img = requests.post(URL_request_capture_save, files=files, timeout=3)
            #print(send_img.text)
            send_img_json = send_img.json()
            if send_img_json['status'] == 'success':
                print("berhasil kirim gambar")
            capture_flag = False
            cam.release()
            cv2.destroyAllWindows()
            cam = cv2.VideoCapture(0)
    except Exception as e:
        print(e)
        
    time.sleep(2)
        

