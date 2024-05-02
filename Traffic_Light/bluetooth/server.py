import bluetooth
import signal
import sys

HOST = "D8:3A:DD:81:DB:24"  # 라즈베리파이 MAC 주소
PORT = bluetooth.PORT_ANY
UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


def signal_handler(sig, frame):
    try:
        connected_socket.close()

    except:
        pass

    server_socket.close()
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)

# 블루투스 서버 소켓 생성
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

port = server_socket.getsockname()[1]
print("포트 :", port)

# 블루투스 서비스 advertise
bluetooth.advertise_service(
    server_socket,
    name="server",
    service_id=UUID,
    service_classes=[UUID, bluetooth.SERIAL_PORT_CLASS],
    profiles=[bluetooth.SERIAL_PORT_PROFILE],
)

# 클라이언트 접속 대기
connected_socket, client_address = server_socket.accept()

try:
    while True:
        data = connected_socket.recv(1024)
        print("client : ", data)
        connected_socket.send(data)

except:
    pass

connected_socket.close()
server_socket.close()