# Import libraries
import cv2
import numpy as np

from PiBluetooth import PiBluetooth
from PedestrianDetection import PedestrianDetection
from multiprocessing import Process, Manager

data:str = None
frame:cv2.typing.MatLike = None
cap:cv2.VideoCapture = None
pd = PedestrianDetection()
pb = PiBluetooth()

# Mouse Event Callback
def mouse_callback(event, x, y, flags, param):
  if event == cv2.EVENT_LBUTTONDOWN:
      if len(pd.pts) < 4:
          pd.pts.append((x, y))
          cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
          
# Designation of crosswalk area and pedestrian detection
def run(data):
  pd.model_init()
  
  cv2.namedWindow("Crosswalk")
  
  cv2.setMouseCallback('Crosswalk', mouse_callback)
  cap = cv2.VideoCapture(0)
  
  while cap.isOpened():
    ret, frame = cap.read()
    cX = 0
    
    if ret == True:
      pd.generate_images(frame)
      boxes = pd.generating_boxes()
      pedestrian_position = pd.crop_images(boxes)
      result_image = pd.convert_result_to_image(boxes)    

      # Draw a polygon if you draw four dots
      if len(pd.pts) == 4:
        pd.pts = np.array(pd.pts, np.int32)
        cv2.polylines(result_image, [pd.pts], True, (0, 255, 0), 2)

        # The center of the Square
        mid = [(pd.max_xpts() + pd.min_xpts()) // 2, (pd.max_ypts() + pd.min_ypts()) // 2]
        cv2.circle(frame, tuple(mid), 2, (0, 0, 255), -1)
        
        # If pedestrian is detected in the crosswalk area, Send a signal to Bluetooth
        if pedestrian_position:
          cX = round((pedestrian_position[0][0] + pedestrian_position[0][2]) / 2)  # Middle point of pedestrian x value
          ymax = pedestrian_position[0][3]  # Bottom of the pedestrian's Square
          
          if pd.f1(cX, ymax) == pd.f1(mid[0], mid[1]) and pd.f2(cX, ymax) == pd.f2(mid[0], mid[1]) and pd.f3(cX, ymax) == pd.f3(mid[0], mid[1]) and pd.f4(cX, ymax) == pd.f4(mid[0], mid[1]):
            cv2.putText(result_image, "Pedstrain is crossing the crosswalk", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)   
            data.value = str("S")
                          
      cv2.imshow("Crosswalk", result_image)

      if cv2.waitKey(25) & 0xFF == ord('q'):
          break

    else:
        break
      
  cap.release()
  cv2.destroyAllWindows()
      
# Bluetooth
def bluetooth_run(data):
  pb.bluetooth_init()  
  pb.find_device()
  pb.connect()
  while True:
    # Send to server when data value becomes 'S'
    if data.value == "S":
      pb.send_data(data.value)
      data.value = "1"

if __name__ == "__main__":
  manager = Manager()
  
  d = manager.Value('data', "1")
  
  pedestrian_detection = Process(target=run, args=(d,))
  pedestrian_detection.start()
  pi_bluetooth = Process(target=bluetooth_run, args=(d,))
  pi_bluetooth.start()
  
  pedestrian_detection.join()
  
  