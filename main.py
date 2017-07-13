import socket,time, datetime
import msvcrt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
import UI,time, ast,warnings
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets


device_Address = ""
manualMode = True
path_to_log = r""
data, times, rots, accels, dists, vels = [[0.0,0.0,0.0]], [0.0], [0.0], [0.0], [0.0], [0.0]
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def write_To_Log(data):
    with open(path_to_log, 'a') as f:
        f.write(data + '\n')
        f.close()

def sendMessage(string,receive=True):
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(bytes(string, encoding='utf-8'), (device_Address, 8888))
    data, addr = sock.recvfrom(1024)
    if receive:
        return data,addr

if __name__ == '__main__':
    app = QApplication([])
    form = UI.Ui_MainWindow()
    form.show()
    form.update()
    start = time.time()
    while 1:
        QtWidgets.QApplication.processEvents()
        #time.sleep(0.01)
        if manualMode == False:
            received = input().split()
            received = [float(i) for i in received]
            if len(received) == 3:
                accel, gyro, ultrasonic = received
                t = "%.3f" % (time.time()-start)
                times.append(float(t))
                data.append(received)
                rots.append(gyro)
                accels.append(accel)
                dists.append(ultrasonic)
                vel = (dists[len(dists)-1]-dists[len(dists)-2])/(times[len(times)-1]-times[len(times)-2])
                vels.append(vel)
                print('====================')
                print("Time: %.3f" % float(t))
                print("Rotation: %.3f" % gyro)
                print("Relative Position: %.3f" % ultrasonic)
                print("Velocity: %.3f" % vel)
                print("Acceleration: %.3f" % accel)
                print('====================')

