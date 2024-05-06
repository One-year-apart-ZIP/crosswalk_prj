import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

import typing

import openvino as ov

class PedestrianDetection:
  image: cv2.typing.MatLike
  resized_image: cv2.typing.MatLike
  input_image: np.ndarray[typing.Any]
  compiled_model: ov.CompiledModel
  input_keys: typing.Any
  output_keys: typing.Any

  def __init__(self):
    self.pts = []
    self.core = ov.Core()
    self.device = self.core.available_devices[0]

  # use for model initialize
  def model_init(self):
    base_model_dir = Path("model")
    # Specify the path where the model file is located
    detection_model_name = "C:\PRJ\crosswalk_prj\Traffic_Camera\model\intel\pedestrian-detection-adas-0002\FP16\pedestrian-detection-adas-0002"
    model_path = (base_model_dir / detection_model_name).with_suffix(".xml")
    model = self.core.read_model(model = model_path)
    self.compiled_model = self.core.compile_model(model=model, device_name=self.device)
    self.input_keys = self.compiled_model.input(0)
    self.output_keys = self.compiled_model.output(0)

  def generate_images(self, image:cv2.typing.MatLike):
    self.image = image
    height, width = list(self.input_keys.shape[2:])
    self.resized_image = cv2.resize(image, (width, height))
    self.input_image = np.expand_dims(self.resized_image.transpose(2, 0, 1), 0)

  # for utility
  def plt_show(raw_image):
    plt.figure(figsize=(10, 6))
    plt.axis("off")
    plt.imshow(raw_image)

  def generating_boxes(self) -> typing.Any:
    boxes = self.compiled_model([self.input_image])[self.output_keys]
    boxes = np.squeeze(boxes, (0, 1))
    boxes = boxes[~np.all(boxes==0, axis=1)]
    return boxes

  def crop_images(self, boxes, threshold=0.8) -> np.ndarray:
    (real_y, real_x), (resized_y, resized_x) = (
        self.image.shape[:2],
        self.resized_image.shape[:2],
    )

    ratio_x, ratio_y = real_x / resized_x, real_y / resized_y

    boxes = boxes[:, 2:]
    pedestrian_position = []

    for box in boxes:
        conf: float = box[0]
        if conf > threshold:
            (x_min, y_min, x_max, y_max) = [
                (int)(max(corner_position * ratio_y * resized_y, 10)) if idx % 2 else int(corner_position * ratio_x * resized_x)
                for idx, corner_position in enumerate(box[1:])
            ]
            pedestrian_position.append([x_min, y_min, x_max, y_max])
    
    return pedestrian_position

  def convert_result_to_image(self, boxes):
    # Color format: BGR
    colors = {"red" : (0, 0, 255)}
    image_to_return = self.image
    pedestrian_position = self.crop_images(boxes)
    for x_min, y_min, x_max, y_max in pedestrian_position:
        image_to_return = cv2.rectangle(image_to_return, (x_min, y_min), (x_max, y_max), colors["red"], 2)
    return image_to_return
  
  # f1,f2,f3,f4 : Definition of a straight line formed by 4 points
  def f1(self, x, My):
    if self.pts is not None:
      y = ((self.pts[1][1] - self.pts[0][1]) / (self.pts[1][0] - self.pts[0][0])) * (x - self.pts[0][0]) + self.pts[0][1]
    if My < y:  # y=f1(Mx) 
      return True  # y<f1(x)
    else:
      return False  # y>f1(x)

  def f2(self, x, My):
    if self.pts is not None:
      y = ((self.pts[2][1] - self.pts[1][1]) / (self.pts[2][0] - self.pts[1][0])) * (x - self.pts[1][0]) + self.pts[1][1]
    if My < y:  # y=f2(Mx) 
      return True  # y<f2(x)
    else:
      return False  # y>f2(x)
    
  def f3(self, x, My):
    if self.pts is not None:
      y = ((self.pts[3][1] - self.pts[2][1]) / (self.pts[3][0] - self.pts[2][0])) * (x - self.pts[2][0]) + self.pts[2][1]
    if My < y:  # y=f3(Mx) 
      return True  # y<f3(x)
    else:
      return False  # y>f3(x)
    
  def f4(self, x, My):
    if self.pts is not None:
      y = ((self.pts[0][1] - self.pts[3][1]) / (self.pts[0][0] - self.pts[3][0])) * (x - self.pts[3][0]) + self.pts[3][1]
    if My < y:  # y=f4(Mx) 
      return True  # y<f4(x)
    else:
      return False  # y>f4(x)
  
  # Maximum and minimum values of x, y for 4 points
  def max_xpts(self):
    if self.pts is not None:
      max_x = max(pt[0] for pt in self.pts)
    return max_x

  def min_xpts(self):
    if self.pts is not None:
      min_x = min(pt[0] for pt in self.pts)
    return min_x

  def max_ypts(self):
    if self.pts is not None:
      max_y = max(pt[1] for pt in self.pts)
    return max_y

  def min_ypts(self):
    if self.pts is not None:
      min_y = min(pt[1] for pt in self.pts)
    return min_y