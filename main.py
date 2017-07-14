from BrushBotHandler import BrushBotHandler
from GamePadHandler import GamePadHandler
import UI
from PyQt5.Qt import QApplication
import PyQt5.QtWidgets
import time,sys,datetime

class Main(object):
    """
    Main Class
    """

    def __init__(self, logPath):
        self.logPath = logPath

    def createWindow(self):
        self.app = QApplication([])
        self.form = UI.Ui_MainWindow()
        self.form.show()
        self.form.update()
        self.start = time.time()
        self.prevGyro = 0
        self.prevAccel = 0
        self.prevPos = 0

    def initializeHandlers(self,ip,port,vID,pID):
        self.ip = ip
        self.port = port
        self.vID = vID
        self.pID = pID
        self.bb = BrushBotHandler(ip, port, 3, 1)
        self.gph = GamePadHandler(vID,pID)

    def log(self,text):
        self.bb.write_To_Log(text,self.logPath)

    def windowLog(self,text):
        self.form.logText.appendPlainText(text)

    def windowComm(self,text):
        self.form.commText.appendPlainText(text)

    def gyroPlot(self,textfile):
        xs, ys = [], []
        for line in open(textfile, 'r').readlines():
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
        xs = xs[-300:]
        ys = ys[-300:]
        self.form.gyroPlot.plotItem.plot(xs,ys,symbol='o',pen='r',clear=True)

    def accelPlot(self,textfile):
        xs, ys = [], []
        for line in open(textfile, 'r').readlines():
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
        xs = xs[-300:]
        ys = ys[-300:]
        self.form.accelPlot.plotItem.plot(xs,ys,symbol='o',pen='r',clear=True)

    def posPlot(self,textfile):
        xs, ys = [], []
        for line in open(textfile, 'r').readlines():
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
        xs = xs[-300:]
        ys = ys[-300:]
        self.form.posPlot.plotItem.plot(xs,ys,symbol='o',pen='r',clear=True)

    def processData(self):
        open("gyro.txt", "a").write(
            "%s,%s\n" % (round(time.time() - self.start, 3), round(float(self.data.split()[0])) - self.prevGyro))
        open("accel.txt", "a").write(
            "%s,%s\n" % (round(time.time() - self.start, 3), round(float(self.data.split()[1])) - self.prevAccel))
        open("pos.txt", "a").write(
            "%s,%s\n" % (round(time.time() - self.start, 3), round(float(self.data.split()[2])) - self.prevPos))
        self.gyroPlot('gyro.txt')
        self.accelPlot('accel.txt')
        self.posPlot('pos.txt')
        self.prevGyro = round(float(self.data.split()[0]), 3)
        self.prevAccel = round(float(self.data.split()[1]), 3)
        self.prevPos = round(float(self.data.split()[2]), 3)

    def mainLoop(self):
        d = {"Manual": 1, "Automatic": 2}
        self.bb.mode = d.get(self.form.modeSelectionComboBox.currentText())
        if self.bb.mode == 1:
            if self.gph.connected == False:
                try:
                    self.windowLog("BrushBot Now Running in Manual Mode")
                    self.log("BrushBot Now Running in Manual Mode")
                    self.windowLog("Connecting to Gamepad...")
                    self.log("Connecting to Gamepad...")
                    self.gph.connectToDevice()
                    self.windowLog("GamePad Connected")
                    self.log("GamePad Connected")
                except Exception as e:
                    self.windowLog("Error, could not find GamePad? Is it connected?")
                    self.log("Error, could not find GamePad? Is it connected?")
                    self.form.modeSelectionComboBox.setCurrentIndex(1)

            self.motor1, self.motor2 = -((self.gph.leftJoyStickY * 2) - 255), -((self.gph.rightJoyStickY * 2) - 255)
            self.windowComm("%s PC: %s %s" % (datetime.datetime.now(), self.motor1, self.motor2))
            self.log("%s PC: %s %s" % (datetime.datetime.now(), self.motor1, self.motor2))
            self.data, self.addr = self.bb.sendMessage("%s %s" % (self.motor1, self.motor2), True)
            if self.data == None and self.addr == None:
                self.windowComm("Error communicating with BrushBot.")
                self.log("Error communicating with BrushBot.")
            else:
                self.windowComm("%s ESP: %s" % (datetime.datetime.now(), self.data))
                self.processData()
                self.log("%s ESP: %s" % (datetime.datetime.now(), self.data))
        elif self.bb.mode == 2:
            if self.gph.connected:
                self.windowLog("BrushBot Now Running in Automatic Mode")
                self.log("BrushBot Now Running in Automatic Mode")
                self.gph.disconnectFromDevice()
            self.motor1 = 0
            self.motor2 = 0
            self.windowComm("%s PC: %s %s" % (datetime.datetime.now(), self.motor1, self.motor2))
            self.log("%s PC: %s %s" % (datetime.datetime.now(), self.motor1, self.motor2))
            self.data, self.addr = self.bb.sendMessage("%s %s" % (self.motor1, self.motor2), True)
            if self.data == None and self.addr == None:
                self.windowComm("Error communicating with BrushBot.")
                self.log("Error communicating with BrushBot.")
            else:
                self.windowComm("%s ESP: %s" % (datetime.datetime.now(), self.data))
                self.processData()
                self.log("%s ESP: %s" % (datetime.datetime.now(), self.data))

        PyQt5.QtWidgets.QApplication.processEvents()
        time.sleep(0.05)

if __name__ == '__main__':
    open('gyro.txt','w+').write("0,0\n")
    open('accel.txt', 'w+').write("0,0\n")
    open('pos.txt', 'w+').write("0,0\n")
    ip, port = "192.168.1.23", 8888
    vendor_id, product_id = 0x046d, 0xc216
    m = Main(r"C:\Users\thoma_000\Desktop\BrushBot\log.txt")
    m.createWindow()
    m.initializeHandlers(ip,port,vendor_id,product_id)
    while True:
        m.mainLoop()