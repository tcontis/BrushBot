from BrushBotHandler import BrushBotHandler
from GamePadHandler import GamePadHandler
import time

if __name__ == '__main__':
    vendor_id = 0x046d
    product_id = 0xc216
    bb = BrushBotHandler("192.168.2.103",8888,4,1)
    gph = GamePadHandler(vendor_id,product_id)
    if bb.mode == 1:
        gph.connectToDevice()
        while bb.mode == 1:
            data, addr = bb.sendMessage("%s %s" %(gph.leftJoyStickY,gph.rightJoyStickY), True)
            time.sleep(0.05)
