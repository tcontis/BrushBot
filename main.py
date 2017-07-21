"""Class that runs entire BrushBot project"""

import time
import datetime
import UI
from PyQt5.Qt import QApplication, QTimer
import numpy as np
from BrushBotHandler import BrushBotHandler
from GamePadHandler import GamePadHandler
#from DecisionNetwork import DecisionNetwork, DataProcessor


class Main(QApplication):
    """
    Main Class
    """

    def __init__(self, log_path):
        super(Main, self).__init__([])
        self.log_path = log_path
        self.app = None
        self.form = None
        self.start = None
        self.previous_gyro = 0
        self.previous_accel = 0
        self.previous_pos = 0
        self.ip = None
        self.port = None
        self.vendor_id = None
        self.product_id = None
        self.brush_bot_handler = None
        self.game_pad_handler = None
        self.address = None
        self.motor1 = 0
        self.motor2 = 0
        self.data = None
        self.sequences = []
        self.next_sequences = []
        #self.dn = DecisionNetwork("models/model.h5")
        #self.dn.load_model()
        #self.dp = None
        self.decision = [0, 0, 0, 0]
        self.prev_time = 0

    def create_window(self):
        """Creates a window and application"""
        self.form = UI.UiMainWindow()
        self.form.show()
        self.form.update()
        self.start = time.time()

    def initialize_handlers(self, _ip, _port, _vendor_id, _product_id):
        """Creates BrushBot and GamePad Handlers"""
        self.ip = _ip
        self.port = _port
        self.vendor_id = _vendor_id
        self.product_id = _product_id
        self.brush_bot_handler = BrushBotHandler(self.ip, self.port, 3, 1)
        self.game_pad_handler = GamePadHandler(self.vendor_id, self.product_id)

    def log(self, text):
        """Quickly Logs test"""
        self.brush_bot_handler.write_to_log(text, self.log_path)

    def window_log(self, text):
        """Logs information to log window"""
        self.form.log_text.appendPlainText(text)
        self.processEvents()

    def window_comm(self, text):
        """Logs information to comm window"""
        self.form.comm_text.appendPlainText(text)
        self.processEvents()

    def gyro_plot(self, textfile):
        """Plots data on gyroscope plot"""
        xs, ys = [], []
        for line in open(textfile, 'r').readlines():
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
        xs = xs[-300:]
        ys = ys[-300:]
        self.form.gyro_plot.plotItem.plot(xs, ys, symbol='o', pen='r', clear=True)
        self.processEvents()

    def accel_plot(self, textfile):
        """Plots data on accelerometer plot"""
        xs, ys = [], []
        for line in open(textfile, 'r').readlines():
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
        xs = xs[-300:]
        ys = ys[-300:]
        self.form.accel_plot.plotItem.plot(xs, ys, symbol='o', pen='r', clear=True)
        self.processEvents()

    def pos_plot(self, textfile):
        """Plots data on position plot"""
        xs, ys = [], []
        for line in open(textfile, 'r').readlines():
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
        xs = xs[-300:]
        ys = ys[-300:]
        self.form.pos_plot.plotItem.plot(xs, ys, symbol='o', pen='r', clear=True)
        self.processEvents()

    def plot_data(self):
        self.gyro_plot('logs/gyro.txt')
        self.accel_plot('logs/accel.txt')
        self.pos_plot('logs/pos.txt')

    def process_data(self):
        """Processes incoming data"""
        open("logs/gyro.txt", "a").write(
            "%s,%s\n" % (
                round(time.time() - self.start, 4), round(float(self.data.split()[1])) - self.previous_gyro))
        open("logs/accel.txt", "a").write(
            "%s,%s\n" % (
                round(time.time() - self.start, 4), round(float(self.data.split()[2])) - self.previous_accel))
        open("logs/pos.txt", "a").write(
            "%s,%s\n" % (
                round(time.time() - self.start, 4), round(float(self.data.split()[0])) - self.previous_pos))
        open("logs/relative_pos.txt", "a").write(
            "%s,%s\n" % (round(time.time() - self.start, 4), round(float(self.data.split()[0]))))
        self.previous_gyro = round(float(self.data.split()[1]), 3)
        self.previous_accel = round(float(self.data.split()[2]), 3)
        self.previous_pos = round(float(self.data.split()[0]), 3)

    def main_loop(self):
            """The main function to loop"""
            d = {"Manual": 1, "Automatic": 2}
            self.brush_bot_handler.mode = d.get(self.form.mode_selection_combo_box.currentText())
            self.processEvents()
            if self.brush_bot_handler.mode == 1:
                if not self.game_pad_handler.connected:
                    try:
                        self.window_log("BrushBot Now Running in Manual Mode")
                        self.log("BrushBot Now Running in Manual Mode")
                        self.window_log("Connecting to Gamepad...")
                        self.log("Connecting to Gamepad...")
                        self.game_pad_handler.connect_to_device()
                        self.window_log("GamePad Connected")
                        self.log("GamePad Connected")
                    except TimeoutError:
                        self.window_log("Error communicating with BrushBot")
                    except AssertionError:
                        self.window_log("Error, could not find GamePad? Is it connected?")
                        self.log("Error, could not find GamePad? Is it connected?")
                        self.form.mode_selection_combo_box.setCurrentIndex(1)
                        self.processEvents()
                self.motor1 = -((self.game_pad_handler.leftJoyStickY * 2) - 256)
                self.motor2 = -((self.game_pad_handler.rightJoyStickY * 2) - 256)
                if self.motor1 < 0:
                    self.motor1 = 0
                if self.motor2 < 0:
                    self.motor2 = 0
                self.window_comm("%s PC: %s %s" % (datetime.datetime.now(), self.motor1, self.motor2))
                self.log("%s PC: %s %s" % (datetime.datetime.now(), self.motor1, self.motor2))
                self.data, self.address = self.brush_bot_handler.send_message("%s %s" % (self.motor1, self.motor2), True)
                if isinstance(self.data, type(None)) and isinstance(self.address, type(None)):
                    self.window_comm("Error communicating with BrushBot.")
                    self.log("Error communicating with BrushBot.")
                else:
                    self.process_data()
                    self.window_comm("%s ESP: %s" % (datetime.datetime.now(), self.data))
                    self.log("%s ESP: %s" % (datetime.datetime.now(), self.data))
                    self.plot_data()
            elif self.brush_bot_handler.mode == 2:
                if self.game_pad_handler.connected:
                    self.window_log("BrushBot Now Running in Automatic Mode")
                    self.log("BrushBot Now Running in Automatic Mode")
                    self.game_pad_handler.disconnect_from_device()
                self.motor1 = 0
                self.motor2 = 0
                if len(open("logs/relative_pos.txt").readlines()) >= 11:
                    #self.dp = DataProcessor("logs/relative_pos.txt", "logs/pos.txt", "logs/accel.txt", "logs/gyro.txt")
                    #self.dp.load_data(3,False)
                    #self.sequences, self.next_sequences = self.dp.preprocess(10, 1)
                    #self.decision = self.dn.predict(np.expand_dims(self.sequences[-1], axis=0))
                    #self.window_log("Neural Network Decision:\n%s\nBased on:\n%s" % (self.decision, self.sequences[-1]))
                    pass
                self.window_comm("%s PC: %s %s" % (datetime.datetime.now(), self.motor1, self.motor2))
                self.log("%s PC: %s %s" % (datetime.datetime.now(), self.motor1, self.motor2))
                #while not round((time.time()-self.prev_time),3).is_integer():
                    #pass
                self.data, self.address = self.brush_bot_handler.send_message("%s %s" % (self.motor1, self.motor2), True)
                self.prev_time = time.time()
                if isinstance(self.data, type(None)) and isinstance(self.address, type(None)):
                    self.window_comm("Error communicating with BrushBot.")
                    self.log("Error communicating with BrushBot.")
                else:
                    self.process_data()
                    self.window_comm("%s ESP: %s" % (datetime.datetime.now(), self.data))
                    self.log("%s ESP: %s" % (datetime.datetime.now(), self.data))
                    self.plot_data()
            self.processEvents()
            time.sleep(0.001)

if __name__ == '__main__':
    open('logs/gyro.txt', 'w+').write("")
    open('logs/accel.txt', 'w+').write("")
    open('logs/pos.txt', 'w+').write("")
    open('logs/relative_pos.txt', 'w+').write("")
    ip, port = "192.168.137.158", 8888
    vendor_id, product_id = 0x046d, 0xc216
    m = Main("logs/log.txt")
    m.create_window()
    m.initialize_handlers(ip, port, vendor_id, product_id)
    t = QTimer()
    t.timeout.connect(m.processEvents)
    t.start(0.1)
    while True:
        m.main_loop()
