"""Decision Network for BrushBot"""

"""from keras.models import load_model, Sequential
from keras.layers import Dropout, LSTM, Activation, Dense
from keras.optimizers import RMSprop"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import QObject
from PyQt5.Qt import QApplication, QTimer
import sys
import time
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QGridLayout, QMainWindow)

class VisualizerMainWindow(QMainWindow):
    """The Main Window for the BrushBot Project"""

    def __init__(self):
        """Initialize Window"""
        super(VisualizerMainWindow, self).__init__()
        self.setupUi()
        self.value_1 = None
        self.value_2 = None
        self.value_3 = None
        self.value_4 = None
        self.value_5 = None
        self.number_of_values = 0
        self.is_processed = False

    def setupUi(self):

        # Size window to default dimensions
        self.resize(1800, 900)
        self.setWindowTitle("BrushBot Dynamics Visualizer")
        self.showMaximized()

        # Create a central Widget
        self.central_widget = QtWidgets.QWidget(self)

        self.master_grid_layout = QGridLayout()

        self.value_selection_box = QtWidgets.QGroupBox(self.central_widget, title="Value Selection")
        self.value_selection_box.setAlignment(QtCore.Qt.AlignCenter)

        self.quantity_selection_box_group_box = QtWidgets.QGroupBox()
        self.quantity_selection_label = QtWidgets.QLabel("Number of variables to analyze:")
        self.quantity_selection_combo_box = QtWidgets.QComboBox()
        self.quantity_selection_combo_box.addItem("2")
        self.quantity_selection_combo_box.addItem("3")
        self.quantity_selection_combo_box.addItem("4")
        self.quantity_selection_combo_box.addItem("5")
        self.quantity_selection_combo_box.currentIndexChanged.connect(self.show_values)

        self.value_selection_vertical_layout = QtWidgets.QVBoxLayout(self.value_selection_box)
        self.value_selection_vertical_layout.addWidget(self.quantity_selection_box_group_box)

        self.letters = ["", "_2", "_3", "_4", "_5"]
        self.adjs = ["First", "Second", "Third", "Fourth", "Fifth"]
        for number in self.letters:
            exec("self.value_selection_box_group_box%s = QtWidgets.QGroupBox()" % number)
            exec("self.value_selection_box_group_box%s = QtWidgets.QGroupBox()" % number)
            exec("self.value_selection_label%s = QtWidgets.QLabel('Choose %s variable:')" % (number, self.adjs[self.letters.index(number)]))
            exec("self.value_selection_combo_box%s = QtWidgets.QComboBox()" % number)
            exec("self.value_selection_combo_box%s.addItem('Left Joystick Values')" % number)
            exec("self.value_selection_combo_box%s.addItem('Right Joystick Values')" % number)
            exec("self.value_selection_combo_box%s.addItem('Change in Acceleration on X-axis')" % number)
            exec("self.value_selection_combo_box%s.addItem('Change in Acceleration on Y-axis')" % number)
            exec("self.value_selection_combo_box%s.addItem('Change in Rotation on Z-axis')" % number)
            exec("self.value_selection_vertical_layout.addWidget(self.value_selection_box_group_box%s)" % number)
            exec("self.value_selection_box_horizontal_layout%s = QtWidgets.QHBoxLayout(self.value_selection_box_group_box%s)" % (number, number))
            exec("self.value_selection_box_horizontal_layout%s.addWidget(self.value_selection_label%s)" % (number, number))
            exec("self.value_selection_box_horizontal_layout%s.addWidget(self.value_selection_combo_box%s)" % (number, number))
            if number != self.letters[0] and number != self.letters[1]:
                exec("self.value_selection_box_group_box%s.hide()" % number)

        self.value_selection_button = QtWidgets.QPushButton("Visualize!")
        self.value_selection_button.pressed.connect(self.process_values_selected)

        self.value_selection_vertical_layout.addWidget(self.value_selection_button)

        self.quantity_selection_box_horizontal_layout = QtWidgets.QHBoxLayout(self.quantity_selection_box_group_box)
        self.quantity_selection_box_horizontal_layout.addWidget(self.quantity_selection_label)
        self.quantity_selection_box_horizontal_layout.addWidget(self.quantity_selection_combo_box)

        self.master_grid_layout.addWidget(self.value_selection_box, 0, 0, 1, 1)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.master_grid_layout)

        menubar = self.menuBar()

        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setWeight(50)
        menubar.setFont(font)
        menu_file = QtWidgets.QMenu(menubar)
        menu_file.setObjectName("menuFile")

        menu_file.setTitle("File")
        menubar.addAction(menu_file.menuAction())

        actionExit = QtWidgets.QAction(self)
        actionExit.setShortcut('Ctrl+Q')
        actionExit.triggered.connect(self.close)
        menubar.addAction(actionExit)
        self.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        QtCore.QMetaObject.connectSlotsByName(self)

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self, 'Exit', "Are you sure you want to quit?",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()

    def process_values_selected(self):
        self.number_of_values = int(self.quantity_selection_combo_box.currentText())
        self.value_1 = self.value_selection_combo_box.currentIndex()
        self.value_2 = self.value_selection_combo_box_2.currentIndex()
        self.value_3 = self.value_selection_combo_box_3.currentIndex()
        self.value_4 = self.value_selection_combo_box_4.currentIndex()
        self.value_5 = self.value_selection_combo_box_5.currentIndex()
        self.is_processed = True

    def show_values(self):
        self.number_of_values = int(self.quantity_selection_combo_box.currentText())
        for letter in self.letters[:self.number_of_values]:
            exec("self.value_selection_box_group_box%s.show()" % letter)
        for letter in self.letters[self.number_of_values:]:
            exec("self.value_selection_box_group_box%s.hide()" % letter)

class DataProcessor(object):
    """A data processing class that allows for the loading of data and preprocessing for neural network"""

    def __init__(self, gyro_file, accelX_file, accelY_file, joy_file):
        self.gyro_file = gyro_file
        self.accelX_file = accelX_file
        self.accelY_file = accelY_file
        self.joy_file = joy_file
        self.accuracy = 3
        self.relative_pos = []
        self.delta_accelX = []
        self.delta_gyro = []
        self.delta_accelY = []
        self.times = []
        self.data = []
        self.sequences = []
        self.joys = []

    def load_data(self, accuracy, return_values=True):
        """Load data from textfile rounding it to desired decimal place. Returns a list of times, relative positions,
        changes in position, changes in acceleration, and changes in rotation."""
        self.accuracy = accuracy
        for line in open(self.joy_file, "r"):
            time, left, right = line.replace("\n", "").split(',')
            self.joys.append([int(left), int(right)])
        for line in open(self.gyro_file, "r"):
            time, value = line.split(',')
            self.times.append(round(float(time), self.accuracy))
            self.delta_gyro.append(round(float(value), self.accuracy))
        for line in open(self.accelX_file, "r"):
            time, value = line.split(',')
            self.delta_accelX.append(round(float(value), self.accuracy))
        for line in open(self.accelY_file, "r"):
            time, value = line.split(',')
            self.delta_accelY.append(round(float(value), self.accuracy))
        if return_values:
            return self.times, self.delta_gyro, self.delta_accelX, self.delta_accelY, self.joys

    def preprocess(self):
        """Preprocess the data into sequences. Returns chunks of sequences and a list of next sequences"""
        # Separate data for joystick
        self.left_joys = []
        self.right_joys = []
        self.data = []
        for joy in self.joys:
            self.left_joys.append(joy[0])
            self.right_joys.append(joy[1])
        # Normalize data with time changes.
        for i in range(1, len(self.times)):
            t = self.times[i] - self.times[i - 1]
            t = round(float(t), 3)
            self.delta_gyro[i] = int(round(float(self.delta_gyro[i] / t), 3))
            self.delta_accelX[i] = round(float(self.delta_accelX[i] / t), 3)
            self.delta_accelY[i] = round(float(self.delta_accelY[i] / t), 3)
        for g, x, y in zip(self.delta_gyro, self.delta_accelX, self.delta_accelY):
            self.data.append([g, x, y])
        return self.joys, self.left_joys, self.right_joys, self.data, self.delta_gyro, self.delta_accelX, self.delta_accelY, self.times


class DecisionNetwork(object):
    """Decision Network that guides BrushBot's actions."""

    def __init__(self, savefile):
        self.savefile = savefile
        self.model = None
        self.optimizer = None

    def create_model(self, inputs, outputs, epochs, load=False):
        if load:
            self.load_model()
        else:
            self.inputs = inputs
            self.outputs = outputs
            self.epochs = epochs
            self.model = Sequential()
            self.model.add(Dense(10, input_dim=2, activation='relu'))
            self.model.add(Dense(5, activation='relu'))
            self.model.add(Dense(1))
            print(self.model.input_shape)
            self.model.summary()
            self.optimizer = RMSprop(lr=0.01)
            self.model.compile(loss='mse', optimizer="adam")

    def load_model(self):
        self.model = load_model(self.savefile)

    def save_model(self):
        self.model.save(self.savefile)

    def train_model(self, validate=False):
        for i in range(self.epochs):
            if validate:
                pass
            else:
                self.model.fit(self.inputs, self.outputs, batch_size=1000, epochs=1)
                self.save_model()

    def predict(self, to_predict):
        return self.model.predict(to_predict)

class VisualizerMain(QApplication):
    """
    Main Class
    """

    def __init__(self, log_path):
        super(VisualizerMain, self).__init__([])
        self.log_path = log_path

    def create_window(self):
        """Creates a window and application"""
        self.form = VisualizerMainWindow()
        self.form.show()
        self.form.update()

    def main_loop(self):
        self.processEvents()
        time.sleep(0.001)

if __name__ == '__main__':
    m = VisualizerMain("/logs")
    m.create_window()
    dp = DataProcessor("logs/gyro.txt", "logs/accelX.txt", "logs/accelY.txt", "logs/joy.txt")
    dp.load_data(3, False)
    joys, left_joys, right_joys, data, delta_gyro, delta_accelX, delta_accelY, times = dp.preprocess()
    s = set(left_joys + right_joys)
    while True:
        if m.form.is_processed:
            d = {0: left_joys, 1: right_joys, 2: delta_accelX, 3: delta_accelY, 4:delta_gyro}
            if m.form.number_of_values == 3:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(d.get(m.form.value_1), d.get(m.form.value_2), d.get(m.form.value_3), c='b', marker='o')
                plt.show()
            elif m.form.number_of_values == 2:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.scatter(d.get(m.form.value_1), d.get(m.form.value_2), c='b', marker='o')
                plt.show()
            m.form.is_processed = False
        m.processEvents()
    sys.exit(m.exec_())

    dn = DecisionNetwork("models/dynamics_model_accelX.h5")
    dn.create_model(joys, delta_accelX, 1000, False)
    dn.train_model()
    for i in sorted(s):
        for j in sorted(s):
            print(i, j)
            p = dn.predict(np.array([i, j]).reshape((1,2)))
            ax2.scatter([i], [j], p, c='b', marker='o')

    plt.show()
