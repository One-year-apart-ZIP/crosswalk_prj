import time
import cv2

class TrafficLightGUI:
    red_light: cv2.typing.MatLike = None
    green_light: cv2.typing.MatLike = None
    current_image: cv2.typing.MatLike = None
    position = (10, 720)

    def __init__(self):
        self.red_light = cv2.imread("/home/pi/crosswalk_prj/Traffic_RaspberryPi/red_light.jpg", cv2.IMREAD_COLOR)
        self.green_light = cv2.imread("/home/pi/crosswalk_prj/Traffic_RaspberryPi/green_light.jpg", cv2.IMREAD_COLOR)
        self.current_image = self.red_light

    def create_window(self):
        cv2.namedWindow("Traffic")

    def toggle_light(self, state):
        if state.value == "green":
            self.current_image = self.red_light
            state.value = "red"
        elif state.value == "red":
            self.current_image = self.green_light
            state.value = "green"

    def run_gui(self, sec, state):
        while True:
            print(sec)
            time.sleep(1)
            if sec.value > 1:
                sec.value -= 1
            elif sec.value == 1:
                sec.value = 20
                self.toggle_light(state)
            img = self.current_image.copy()
            cv2.putText(img, str(sec.value), self.position, cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 0, 255), 24) 
            cv2.imshow("Traffic", img)
            if cv2.waitKey(1) == ord('q'):
                break
        self.destroy()

    def destroy():
        cv2.destroyAllWindows()
