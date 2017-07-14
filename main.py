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

    def initializeHandlers(self,ip,port,vID,pID):
        self.ip = ip
        self.port = port
        self.vID = vID
        self.pID = pID
        self.bb = BrushBotHandler(ip, port, 4, 1)
        self.gph = GamePadHandler(vID,pID)

    def log(self,text):
        self.bb.write_To_Log(text,self.logPath)

    def windowLog(self,text):
        self.form.logText.appendPlainText(text)

    def windowComm(self,text):
        self.form.commText.appendPlainText(text)

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
                self.log("%s ESP: %s" % (datetime.datetime.now(), self.data))
        else:
            if self.gph.connected:
                self.windowLog("BrushBot Now Running in Automatic Mode")
                self.log("BrushBot Now Running in Automatic Mode")
                self.gph.disconnectFromDevice()

        PyQt5.QtWidgets.QApplication.processEvents()
        time.sleep(0.05)

if __name__ == '__main__':
    ip, port = "192.168.1.23", 8888
    vendor_id, product_id = 0x046d, 0xc216
    m = Main(r"C:\Users\thoma_000\Desktop\BrushBot\log.txt")
    m.createWindow()
    m.initializeHandlers(ip,port,vendor_id,product_id)
    while True:
        m.mainLoop()