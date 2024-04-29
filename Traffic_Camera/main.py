# Import libraries
import platform
import os

import cv2

from PedestrianDetection import PedestrianDetection

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('x = %d, y = %d'%(x, y))

pd = PedestrianDetection()
pd.model_init()
cap = cv2.VideoCapture(0)

cv2.namedWindow("Crosswalk")
cv2.setMouseCallback("Crosswalk", onMouse)

while cap.isOpened():
    ret, frame = cap.read()
    
    if ret == True:
        pd.generate_images(frame)
        boxes = pd.generating_boxes()
        pedestrian_position = pd.crop_images(boxes)
        result_image = pd.convert_result_to_image(boxes)

        final = cv2.rectangle(result_image, (212, 351), (436, 438), (255, 0, 0), 2)

        cv2.imshow("Crosswalk", final)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()