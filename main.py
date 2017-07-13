from BrushBotHandler import BrushBotHandler
from GamePadHandler import GamePadHandler
import UI
from PyQt5.Qt import QApplication
import PyQt5.QtWidgets
import time,sys

if __name__ == '__main__':
    app = QApplication([])
    form = UI.Ui_MainWindow()
    form.show()
    form.update()
    vendor_id = 0x046d
    product_id = 0xc216
    d = {"Manual":1,"Automatic":2}
    bb = BrushBotHandler("192.168.2.103",8888,4,1)
    gph = GamePadHandler(vendor_id,product_id)
    while True:
        bb.mode = d.get(form.modeSelectionComboBox.currentText())
        if bb.mode == 1:
            if gph.connected == False:
                try:
                    form.logText.appendPlainText("BrushBot Now Running in Manual Mode")
                    form.logText.appendPlainText("Connecting to Gamepad...")
                    gph.connectToDevice()
                    form.logText.appendPlainText("GamePad Connected")
                except Exception as e:
                    form.logText.appendPlainText("Error, could not find GamePad? Is it connected?")
                    form.modeSelectionComboBox.setCurrentIndex(1)
            form.commText.appendPlainText("PC: %s %s" % (gph.leftJoyStickY, gph.rightJoyStickY))
            data, addr = bb.sendMessage("%s %s" %(gph.leftJoyStickY,gph.rightJoyStickY), True)
            form.commText.appendPlainText("ESP: %s" % data)
        else:
            if gph.connected == True:
                form.logText.appendPlainText("BrushBot Now Running in Automatic Mode")
                gph.disconnectFromDevice()
        PyQt5.QtWidgets.QApplication.processEvents()
        time.sleep(0.02)