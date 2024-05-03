import time
import bluetooth
from multiprocessing import Process, Manager
import cv2

img_red = cv2.imread('/home/pi/crosswalk_prj/Traffic_RaspberryPi/red_light.jpg', cv2.IMREAD_COLOR)
img_green = cv2.imread('/home/pi/crosswalk_prj/Traffic_RaspberryPi/green_light.jpeg', cv2.IMREAD_COLOR)
expand = cv2.resize(img_green, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
print(img_green)

# 타이머와 블루투스 데이터 변수
seconds = 10
light_state = 'red'  # 'red' 또는 'green'
 

def update_timer(sec):
    while True:
        print(sec.value)
        time.sleep(1)
        if sec.value > 0:
            sec.value -= 1
        elif sec.value == 0:
            # 빨간불과 초록불 상태 전환
            sec.value = 10
            toggle_lights()

def toggle_lights():
    global light_state
    print("toggle")
    light_state = 'green' if light_state == 'red' else 'red'
    print(light_state)
    if light_state == 'green':
        cv2.imshow("Traffic", img_green)
    elif light_state == 'red':
        print(light_state)
        cv2.imshow("Traffic", img_red)

def bluetooth_receive():
    global seconds
    while True:
        try:
            data = client_sock.recv(1024).decode('utf-8')
            if data == 'S':
                print("Received Bluetooth signal", data)
        except bluetooth.BluetoothSocket(bluetooth.RFCOMM):
            pass

def setup_bluetooth_server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    bluetooth.advertise_service(
            server_sock,
            name="TrafficLightServer",
            service_id=uuid,
            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE],
    )
    print("Waiting for connection on RFCOMM channel", port)
    return server_sock

def main_loop(sec):
    #update_timer(sec)
    print("Call main_loop")
    window.after(1000, update_timer, sec)

cv2.imshow("Traffic", img_red)

if __name__ == "__main__":
    manager = Manager()
    cv2.namedWindow("Traffic2")
    
  #  cv2.imshow("Traffic", expand)

    server_sock = setup_bluetooth_server()
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)


    sec = manager.Value('seconds', 10)

    timer_process = Process(target=update_timer, args=(sec,))
    timer_process.start()

    main_process = Process(target=bluetooth_receive)
    main_process.start()

    timer_process.join()
    main_process.join()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    client_sock.close()
    server_sock.close()
    window.destroy()


