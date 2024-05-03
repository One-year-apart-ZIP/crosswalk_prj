# Import libraries
import platform
import os

import cv2
import numpy as np
import sys
import bluetooth

from client4 import PiBluetooth
from PedestrianDetection2 import PedestrianDetection
from multiprocessing import Process, Manager

data:str = None
frame:cv2.typing.MatLike = None
cap:cv2.VideoCapture = None
pd = PedestrianDetection()
pb = PiBluetooth()

# 마우스 이벤트 콜백 함수
def mouse_callback(event, x, y, flags, param):
  # global pd.pts
  if event == cv2.EVENT_LBUTTONDOWN:
      if len(pd.pts) < 4:
          pd.pts.append((x, y))
          cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
          
def run(data):
  pd.model_init()
  # video_path = "crosswalk4.mp4"  # 수정된 부분: 저장된 영상 파일 경로 입력
  # cap = cv2.VideoCapture(video_path)  # 수정된 부분: 저장된 영상 파일 열기
  cv2.namedWindow("Crosswalk")
  # 마우스 이벤트 처리
  cv2.setMouseCallback('Crosswalk', mouse_callback)
  cap = cv2.VideoCapture(0)  # 실시간 영상
  
  while cap.isOpened():
    ret, frame = cap.read()
    cX = 0
    
    if ret == True:
      pd.generate_images(frame)
      boxes = pd.generating_boxes()
      pedestrian_position = pd.crop_images(boxes)
      result_image = pd.convert_result_to_image(boxes)    

      # 4개의 점을 찍으면 다각형 그리기
      if len(pd.pts) == 4:
        pd.pts = np.array(pd.pts, np.int32)
        cv2.polylines(result_image, [pd.pts], True, (0, 255, 0), 2)

        mid = [(pd.max_xpts() + pd.min_xpts()) // 2, (pd.max_ypts() + pd.min_ypts()) // 2]
        cv2.circle(frame, tuple(mid), 2, (0, 0, 255), -1)
        
        if pedestrian_position:
          cX = round((pedestrian_position[0][0] + pedestrian_position[0][2]) / 2)
          ymax = pedestrian_position[0][3]
          
          if pd.f1(cX, ymax) == pd.f1(mid[0], mid[1]) and pd.f2(cX, ymax) == pd.f2(mid[0], mid[1]) and pd.f3(cX, ymax) == pd.f3(mid[0], mid[1]) and pd.f4(cX, ymax) == pd.f4(mid[0], mid[1]):
            cv2.putText(result_image, "Pedstrain is crossing the crosswalk", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            print("Data Value is : ", data.value)
            data.value = str("pedestrian")
                          
      cv2.imshow("Crosswalk", result_image)

      if cv2.waitKey(25) & 0xFF == ord('q'):
          break

    else:
        break
      
  cap.release()
  cv2.destroyAllWindows()
      
def bluetooth_run(data):
  pb.bluetooth_init()  
  pb.find_device()
  pb.connect()
  while True:
    if data.value == "pedestrian":
      print("2 : ", data.value)
      pb.send_data(data.value)
      data.value = '1'

if __name__ == "__main__":
  manager = Manager()
  
  d = manager.Value('data', "1")
  
  pedestrian_detection = Process(target=run, args=(d,))
  pedestrian_detection.start()
  pi_bluetooth = Process(target=bluetooth_run, args=(d,))
  pi_bluetooth.start()
  
  pedestrian_detection.join()
  # pi_bluetooth.join()

  
  