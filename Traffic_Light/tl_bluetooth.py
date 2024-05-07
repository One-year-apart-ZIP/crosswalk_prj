import bluetooth
import typing

class TrafficLightBluetooth:
    server_socket: typing.Any = None
    client_socket: typing.Any = None
    clinet_info: typing.Any = None
    port: typing.Any = None
    sent = False 

    def __init__(self):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_socket.bind(("", bluetooth.PORT_ANY))

    def listen(self):
        self.server_socket.listen(1)
        port = self.server_socket.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        bluetooth.advertise_service(
                self.server_socket,
                name="TrafficLightServer",
                service_id=uuid,
                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE],
        )
        print("Waiting for connection on RFCOMM channel", port)
        self.client_socket, self.client_info = self.server_socket.accept()
        print("Accepted connection from", self.clinet_info)

    def receive_data(self, sec, state):
        while True:
            if state.value == "red": 
                sent = False
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data == 'S' and sec.value < 10 and state.value == "green" and sent == False:
                    sec.value += 5
                    sent = True
                    print("Received bluetooth signal", data)  # remove
            except bluetooth.BluetoothSocket(bluetooth.RFCOMM):
                break
        self.destroy()

    def destroy(self):
        self.client_socket.close()
        self.server_socket.close()
