import time
import bluetooth
from multiprocessing import Process, Value
import cv2

def Traffic_Light(seconds_red, seconds_green):
    img_red = cv2.imread('/home/pi/crosswalk_prj/Traffic_RaspberryPi/red_light.jpg', cv2.IMREAD_COLOR)
    img_green = cv2.imread('/home/pi/crosswalk_prj/Traffic_RaspberryPi/green_light.jpeg', cv2.IMREAD_COLOR)
    while True:
        for _ in range(seconds_red.value):
            cv2.imshow("Traffic", img_red)
            cv2.waitKey(1000)
            seconds_red.value -= 1
            print("Red Light Remaining: ", seconds_red.value)
            if seconds_red.value == 0:
                break
        #elif seconds2.value == 20:
        for _ in range(seconds_green.value):
            cv2.imshow("Traffic", img_green)
            cv2.waitKey(1000)
            seconds_green.value -= 1
            print("Green Light Remaining: ", seconds_green.value)
            if seconds_green.value == 0:
                seconds_red.value = 20
                seconds_green.value = 20
                break

def receive_bluetooth_signal(seconds_green):
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

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    while True:
        try:
            data = client_sock.recv(1024).decode('utf-8')
            if data == 'S':
                print("Received Bluetooth signal", data)
                if seconds_green.value < 10:
                    seconds_green.value = 10
                    print("Remain Green Light by 10 sec")
        except Exception as e:
            print("Bluetooth error:", e)
            break

    client_sock.close()
    server_sock.close()

if __name__ == "__main__":
    seconds_red = Value('i', 20)
    seconds_green = Value('i', 20)
    screen_process = Process(target=Traffic_Light, args=(seconds_red, seconds_green,))

    screen_process.start()
    receive_bluetooth_signal(seconds_green)

    screen_process.join()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
