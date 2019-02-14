import cv2
import numpy as np
import requests
import base64
from PIL import Image


cam = cv2.VideoCapture(0)

cv2.namedWindow("test")
cv2.moveWindow("test", 40,30)

img_counter = 0

url = 'http://192.168.0.101:5000/sanushost/api/v1.0/add_face'
headers = {"Content-Type": "application/json", "Accept": "text/plain"}

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        # img_name = "opencv_frame_{}.png".format(img_counter)
        img_name = input("Enter your name:")

        cv2.imwrite(img_name + ".png", cv2.resize(frame, (0,0), fx=0.3, fy=0.3))
        try:
            image = np.asarray(Image.open(img_name + ".png"), dtype=np.uint8)
            shape_string = str(image.shape)
            image = image.astype(np.float64)
            img_64 = base64.b64encode(image).decode('ascii')
            payload = {"Image": img_64, "Shape": shape_string, "ID": img_name}
            result = requests.post(url, json=payload, headers=headers)
            print(result)
        except:
            print("image upload fail")
        # print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()