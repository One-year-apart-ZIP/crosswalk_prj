# Import libraries
import platform
import os

import cv2
import numpy as np

from PedestrianDetection import PedestrianDetection

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('x = %d, y = %d'%(x, y))

pd = PedestrianDetection()
pd.model_init()

video_path = "crosswalk4.mp4"  # 수정된 부분: 저장된 영상 파일 경로 입력
cap = cv2.VideoCapture(video_path)  # 수정된 부분: 저장된 영상 파일 열기
# cap = cv2.VideoCapture(0)  # 실시간 영상

cv2.namedWindow("Crosswalk")
cv2.setMouseCallback("Crosswalk", onMouse)

# 점 좌표를 저장할 리스트
pts = []

# 마우스 이벤트 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global pts
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(pts) < 4:
            pts.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

def f1(x, My):
  if pts is not None:
    y = ((pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])) * (x - pts[0][0]) + pts[0][1]
  if My < y:  # y=f1(Mx) 
    return True  # y<f1(x)
  else:
    return False  # y>f1(x)

def f2(x, My):
  if pts is not None:
    y = ((pts[2][1] - pts[1][1]) / (pts[2][0] - pts[1][0])) * (x - pts[1][0]) + pts[1][1]
  if My < y:  # y=f2(Mx) 
    return True  # y<f2(x)
  else:
    return False  # y>f2(x)
  
def f3(x, My):
  if pts is not None:
    y = ((pts[3][1] - pts[2][1]) / (pts[3][0] - pts[2][0])) * (x - pts[2][0]) + pts[2][1]
  if My < y:  # y=f3(Mx) 
    return True  # y<f3(x)
  else:
    return False  # y>f3(x)
  
def f4(x, My):
  if pts is not None:
    y = ((pts[0][1] - pts[3][1]) / (pts[0][0] - pts[3][0])) * (x - pts[3][0]) + pts[3][1]
  if My < y:  # y=f4(Mx) 
    return True  # y<f4(x)
  else:
    return False  # y>f4(x)
  
while cap.isOpened():
    ret, frame = cap.read()
    cX = 0
    
    if ret == True:
      pd.generate_images(frame)
      boxes = pd.generating_boxes()
      pedestrian_position = pd.crop_images(boxes)
      result_image = pd.convert_result_to_image(boxes)

      # final = cv2.rectangle(result_image, (212, 351), (436, 438), (255, 0, 0), 2)
      # final = cv2.polylines(result_image, [pts], True, (255, 0, 0), 2)
      # 마우스 이벤트 처리
      cv2.setMouseCallback('Crosswalk', mouse_callback)

        # 4개의 점을 찍으면 다각형 그리기
      if len(pts) == 4:
        pts = np.array(pts, np.int32)
        cv2.polylines(result_image, [pts], True, (0, 255, 0), 2)
        
        mid = [(pts[0][0] + pts[2][0]) // 2, (pts[0][1] + pts[2][1]) // 2]
        cv2.circle(frame, tuple(mid), 2, (0, 0, 255), -1)
        # print("최댓값(x) : ", max_xpts(pts))
        # print("최솟값(x) : ", min_xpts(pts))
        
        if pedestrian_position:
          # print(pedestrian_position)
          cX = round((pedestrian_position[0][0] + pedestrian_position[0][2]) / 2)
          ymax = pedestrian_position[0][3]
          
          if f1(cX, ymax) == f1(mid[0], mid[1]) and f2(cX, ymax) == f2(mid[0], mid[1]) and f3(cX, ymax) == f3(mid[0], mid[1]) and f4(cX, ymax) == f4(mid[0], mid[1]):
            cv2.putText(result_image, "Pedstrain is crossing the crosswalk", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            # print("pedestrian is walking in the crosswalk")
                          
      cv2.imshow("Crosswalk", result_image)

      if cv2.waitKey(25) & 0xFF == ord('q'):
          break

    else:
        break

cap.release()
cv2.destroyAllWindows()