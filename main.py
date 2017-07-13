import socket
import time
import GamePadHandler

class BrushBotHandler(object):

    """
    Description: Class used to handle interactions between BrushBot and a PC.

    Parameters:

        Device Address: IP Address of BrushBot.
        Port: Port of Brushbot
        Datapoints: The amount of datapoints to be received from BrushBot
        Mode:
            1: Manual -> Controlled Manually via Logitech Controller
            2: Automatic -> Controlled via Neural Net pipeline.
    """

    def __init__(self, deviceAddress, port, dataPoints, mode):
        self.deviceAddress = deviceAddress
        assert isinstance(deviceAddress, str), "Invalid Device Address, not a string"
        self.port = port
        assert isinstance(port, int), "Invalid Port, not an integer"
        self.mode = mode
        assert mode == 1 or mode == 2, "Invalid Mode, must be either 1 or 2"
        self.dataPoints = dataPoints
        assert isinstance(dataPoints,int), "Invalid Datapoint Numbers, not an integer"

    def write_To_Log(self,data, logPath):
        "Log anything"
        with open(logPath, 'a') as f:
            f.write(data + '\n')
            f.close()

    def sendMessage(self,string,receive=True):
        "Send message to BrushBot"
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        self.sock.sendto(bytes(string, encoding='utf-8'), (self.deviceAddress, self.port))
        data, addr = self.sock.recvfrom(1024)
        if receive:
            return data,addr

    def processData(self,string):
        "Transform a string of integer into a list of integers"
        received = string.split()
        received = [float(i) for i in received]
        if len(received) == self.dataPoints:
            return received

if __name__ == '__main__':
    vendor_id = 0x046d
    product_id = 0xc216
    bb = BrushBotHandler("192.168.2.103",8888,4,1)
    gph = GamePadHandler.GamePadHandler(vendor_id,product_id)
    if bb.mode == 1:
        gph.connectToDevice()
        print(gph.leftJoyStickY,gph.rightJoyStickY)
        data, addr = bb.sendMessage("%s %s" %(gph.leftJoyStickY,gph.rightJoyStickY), True)
        while 1:
            gph.connectToDevice()
            data, addr = bb.sendMessage("%s %s" %(gph.leftJoyStickY,gph.rightJoyStickY), True)
            time.sleep(0.05)
