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
        self.core = ov.Core()
        self.device = self.core.available_devices[0]

    # use for model initialize
    def model_init(self):
        base_model_dir = Path("model")
        detection_model_name = "pedestrian-detection-adas-0002"
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
            if ((x_min <= 436) and (y_max >= 351)) and ((x_max >= 212) and (y_max >= 246)):
                image_to_return = cv2.rectangle(image_to_return, (x_min, y_min), (x_max, y_max), colors["red"], 2)
        return image_to_return
    
