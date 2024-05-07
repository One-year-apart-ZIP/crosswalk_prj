from tl_bluetooth import TrafficLightBluetooth
from tl_gui import TrafficLightGUI
from multiprocessing import Process, Manager

seconds = 10
current_light: str = None

bt = TrafficLightBluetooth()
tf_gui = TrafficLightGUI()

if __name__ == "__main__":
    manager = Manager()
    sec = manager.Value("seconds", 10)
    state = manager.Value("current_light", "red")

    bt.listen()
    bluetooth_process = Process(target=bt.receive_data, args=(sec,state,))
    bluetooth_process.start()

    gui_process = Process(target=tf_gui.run_gui, args=(sec, state,))
    gui_process.start()

    bluetooth_process.join()
    gui_process.join()

