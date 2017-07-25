"""Handles BrushBot - Python communications"""

import socket


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

    def __init__(self, device_address, port, data_points, mode):
        self.device_address = device_address
        assert isinstance(device_address, str), "Invalid Device Address, not a string"
        self.port = port
        assert isinstance(port, int), "Invalid Port, not an integer"
        self.mode = mode
        assert mode == 1 or mode == 2, "Invalid Mode, must be either 1 or 2"
        self.data_points = data_points
        assert isinstance(data_points, int), "Invalid Datapoint Numbers, not an integer"
        self.sock = None
        self.log_path = None

    def write_to_log(self, data, log_path):
        """Log anything to a file"""
        self.log_path = log_path
        with open(self.log_path, 'a') as log_file:
            log_file.write(data + '\n')
            log_file.close()

    def send_message(self, string, receive=True):
        """Send message to BrushBot, detect connection issues"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(2.0)
            self.sock.sendto(bytes(string, encoding='utf-8'), (self.device_address, self.port))
            data, address = self.sock.recvfrom(128)
            if receive:
                return data, address
        except socket.timeout:
            if receive:
                return None, None
        except BlockingIOError:
            if receive:
                return None, None
        finally:
            self.sock.close()

    def process_data(self, string):
        """Transform a string of integer into a list of integers"""
        received = string.split()
        received = [float(i) for i in received]
        if len(received) == self.data_points:
            return received
