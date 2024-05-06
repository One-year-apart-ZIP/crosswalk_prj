import sys
import bluetooth

class PiBluetooth:
    mac_addr:str = None
    bluetooth_name = None
    device = None
    port = None
    host = None
    sock:bluetooth.BluetoothSocket = None

    def bluetooth_init(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
        for addr, name in nearby_devices:
            if name == "pi":
                self.mac_addr = addr
                self.bluetooth_name = name
                
    def find_device(self):
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        service_matches = bluetooth.find_service(name=None, uuid=uuid, address=self.mac_addr)

        if len(service_matches) == 0:
            print("Couldn't find the service.")
            sys.exit(0)

        self.device = service_matches[0]
        self.port = self.device["port"]
        self.bluetooth_name = self.device["name"]
        self.host = self.device["host"]
        print("find device done...")

    def connect(self):
        self.sock.connect((self.host, self.port))

    def send_data(self, data: str):
        self.sock.send(data)

    def disconnect(self):
        self.sock.close()