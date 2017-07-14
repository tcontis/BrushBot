from BrushBotHandler import BrushBotHandler
from GamePadHandler import GamePadHandler
import UI
from PyQt5.Qt import QApplication
import PyQt5.QtWidgets
import time,sys,datetime

if __name__ == '__main__':
    app = QApplication([])
    form = UI.Ui_MainWindow()
    form.show()
    form.update()
    vendor_id = 0x046d
    product_id = 0xc216
    log = r"C:\Users\thoma_000\Desktop\BrushBot\log.txt"
    d = {"Manual":1,"Automatic":2}
    bb = BrushBotHandler("192.168.1.23",8888,4,1)
    gph = GamePadHandler(vendor_id,product_id)
    while True:
        bb.mode = d.get(form.modeSelectionComboBox.currentText())
        if bb.mode == 1:
            if gph.connected == False:
                try:
                    form.logText.appendPlainText("BrushBot Now Running in Manual Mode")
                    bb.write_To_Log("BrushBot Now Running in Manual Mode", log)
                    form.logText.appendPlainText("Connecting to Gamepad...")
                    bb.write_To_Log("Connecting to Gamepad...", log)
                    gph.connectToDevice()
                    form.logText.appendPlainText("GamePad Connected")
                    bb.write_To_Log("GamePad Connected", log)
                except Exception as e:
                    form.logText.appendPlainText("Error, could not find GamePad? Is it connected?")
                    bb.write_To_Log("Error, could not find GamePad? Is it connected?", log)
                    form.modeSelectionComboBox.setCurrentIndex(1)

            motor1,motor2 = -((gph.leftJoyStickY*2) - 255), -((gph.rightJoyStickY*2) - 255)
            form.commText.appendPlainText("%s PC: %s %s" % (datetime.datetime.now(),motor1, motor2))
            bb.write_To_Log("%s PC: %s %s" % (datetime.datetime.now(),motor1, motor2),log)
            data, addr = bb.sendMessage("%s %s" %(motor1,motor2), True)
            if data == None and addr == None:
                form.commText.appendPlainText("Error communicating with BrushBot.")
                bb.write_To_Log("Error communicating with BrushBot.",log)
            else:
                form.commText.appendPlainText("%s ESP: %s" % (datetime.datetime.now(),data))
                bb.write_To_Log("%s ESP: %s" % (datetime.datetime.now(),data),
                                r"C:\Users\thoma_000\Desktop\BrushBot\log.txt")
        else:
            if gph.connected == True:
                form.logText.appendPlainText("BrushBot Now Running in Automatic Mode")
                bb.write_To_Log("BrushBot Now Running in Automatic Mode",log)
                gph.disconnectFromDevice()

        PyQt5.QtWidgets.QApplication.processEvents()
        time.sleep(0.05)