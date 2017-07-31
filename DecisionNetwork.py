"""Decision Network for BrushBot"""

import matplotlib
matplotlib.use('TkAgg')
from keras.models import load_model, Sequential
from keras.layers import Dropout, LSTM, Activation, Dense
from keras.callbacks import History
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import QObject
from PyQt5.Qt import QApplication, QTimer
import sys
import time
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QGridLayout, QMainWindow)


class VisualizerMainWindow(QMainWindow):
    """The Main Window for the BrushBot Project"""

    def __init__(self):
        """Initialize Window"""
        super(VisualizerMainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.to_show = ["", "_2"]
        self.number_of_values = 0
        self.number_of_input_values = 1
        self.number_of_output_values = 1
        self.number_of_layers_values = 2
        self.value_1 = None
        self.value_2 = None
        self.value_3 = None
        self.value_4 = None
        self.value_5 = None
        self.neurons = []
        self.activations = []
        self.is_processed = False
        self.network_processed = False

        # Size window to default dimensions
        self.resize(1800, 900)
        self.setWindowTitle("BrushBot Dynamics Visualizer")
        self.showMaximized()

        # Create a central Widget
        self.central_widget = QtWidgets.QWidget(self)

        self.master_grid_layout = QGridLayout()

        self.value_selection_box = QtWidgets.QGroupBox(self.central_widget, title="Value Selection")
        self.value_selection_box.setAlignment(QtCore.Qt.AlignCenter)

        self.neural_network_box = QtWidgets.QGroupBox(self.central_widget, title="Neural Network Training")
        self.neural_network_box.setAlignment(QtCore.Qt.AlignCenter)

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

        #Neural Network Stuff

        self.neural_network_train_button = QtWidgets.QPushButton("Train Network!")
        self.neural_network_train_button.pressed.connect(self.process_layers)

        self.neural_network_input_selection_box = QtWidgets.QGroupBox(title="Input Selection")
        self.neural_network_input_selection_box.setAlignment(QtCore.Qt.AlignCenter)

        self.neural_network_output_selection_box = QtWidgets.QGroupBox(title="Output Selection")
        self.neural_network_output_selection_box.setAlignment(QtCore.Qt.AlignCenter)

        self.neural_network_parameter_selection_box = QtWidgets.QGroupBox(title="Parameter Selection")
        self.neural_network_parameter_selection_box.setAlignment(QtCore.Qt.AlignCenter)

        self.neural_network_vertical_layout = QtWidgets.QVBoxLayout(self.neural_network_box)
        self.neural_network_vertical_layout.addWidget(self.neural_network_input_selection_box)
        self.neural_network_vertical_layout.addWidget(self.neural_network_output_selection_box)

        #Inputs
        self.neural_network_input_label = QtWidgets.QLabel("Number of Inputs")
        self.neural_network_input_selection_combo_box = QtWidgets.QComboBox()
        self.neural_network_input_selection_combo_box.addItem("1")
        self.neural_network_input_selection_combo_box.addItem("2")
        self.neural_network_input_selection_combo_box.addItem("3")
        self.neural_network_input_selection_combo_box.addItem("4")
        self.neural_network_input_selection_combo_box.addItem("5")
        self.neural_network_input_selection_combo_box.currentIndexChanged.connect(self.show_input_values)

        self.neural_network_input_number_selection_box = QtWidgets.QGroupBox()
        self.neural_network_input_number_horizontal_layout = QtWidgets.QHBoxLayout(self.neural_network_input_number_selection_box)
        self.neural_network_input_number_horizontal_layout.addWidget(self.neural_network_input_label)
        self.neural_network_input_number_horizontal_layout.addWidget(self.neural_network_input_selection_combo_box)

        self.neural_network_input_vertical_layout = QtWidgets.QVBoxLayout(self.neural_network_input_selection_box)
        self.neural_network_input_vertical_layout.addWidget(self.neural_network_input_number_selection_box)

        for number in self.letters:
            exec("self.input_value_selection_box_group_box%s = QtWidgets.QGroupBox()" % number)
            exec("self.input_value_selection_label%s = QtWidgets.QLabel('Choose %s input variable:')" % (
            number, self.adjs[self.letters.index(number)]))
            exec("self.input_value_selection_combo_box%s = QtWidgets.QComboBox()" % number)
            exec("self.input_value_selection_combo_box%s.addItem('Left Joystick Values')" % number)
            exec("self.input_value_selection_combo_box%s.addItem('Right Joystick Values')" % number)
            exec("self.input_value_selection_combo_box%s.addItem('Change in Acceleration on X-axis')" % number)
            exec("self.input_value_selection_combo_box%s.addItem('Change in Acceleration on Y-axis')" % number)
            exec("self.input_value_selection_combo_box%s.addItem('Change in Rotation on Z-axis')" % number)
            exec("self.neural_network_input_vertical_layout.addWidget(self.input_value_selection_box_group_box%s)" % number)
            exec(
                "self.input_value_selection_box_horizontal_layout%s = QtWidgets.QHBoxLayout(self.input_value_selection_box_group_box%s)" % (
                number, number))
            exec("self.input_value_selection_box_horizontal_layout%s.addWidget(self.input_value_selection_label%s)" % (
            number, number))
            exec(
                "self.input_value_selection_box_horizontal_layout%s.addWidget(self.input_value_selection_combo_box%s)" % (
                number, number))
            if number != self.letters[0]:
                exec("self.input_value_selection_box_group_box%s.hide()" % number)

        # Outputs
        self.neural_network_output_label = QtWidgets.QLabel("Number of Outputs")
        self.neural_network_output_selection_combo_box = QtWidgets.QComboBox()
        self.neural_network_output_selection_combo_box.addItem("1")
        self.neural_network_output_selection_combo_box.addItem("2")
        self.neural_network_output_selection_combo_box.addItem("3")
        self.neural_network_output_selection_combo_box.addItem("4")
        self.neural_network_output_selection_combo_box.addItem("5")
        self.neural_network_output_selection_combo_box.currentIndexChanged.connect(self.show_output_values)

        self.neural_network_output_number_selection_box = QtWidgets.QGroupBox()
        self.neural_network_output_number_horizontal_layout = QtWidgets.QHBoxLayout(self.neural_network_output_number_selection_box)
        self.neural_network_output_number_horizontal_layout.addWidget(self.neural_network_output_label)
        self.neural_network_output_number_horizontal_layout.addWidget(self.neural_network_output_selection_combo_box)

        self.neural_network_output_vertical_layout = QtWidgets.QVBoxLayout(self.neural_network_output_selection_box)
        self.neural_network_output_vertical_layout.addWidget(self.neural_network_output_number_selection_box)

        for num in self.letters:
            exec("self.output_value_selection_box_group_box%s = QtWidgets.QGroupBox()" % num)
            exec("self.output_value_selection_label%s = QtWidgets.QLabel('Choose %s output variable:')" % (
                num, self.adjs[self.letters.index(num)]))
            exec("self.output_value_selection_combo_box%s = QtWidgets.QComboBox()" % num)
            exec("self.output_value_selection_combo_box%s.addItem('Left Joystick Values')" % num)
            exec("self.output_value_selection_combo_box%s.addItem('Right Joystick Values')" % num)
            exec("self.output_value_selection_combo_box%s.addItem('Change in Acceleration on X-axis')" % num)
            exec("self.output_value_selection_combo_box%s.addItem('Change in Acceleration on Y-axis')" % num)
            exec("self.output_value_selection_combo_box%s.addItem('Change in Rotation on Z-axis')" % num)
            exec(
                "self.neural_network_output_vertical_layout.addWidget(self.output_value_selection_box_group_box%s)" % num)
            exec(
                "self.output_value_selection_box_horizontal_layout%s = QtWidgets.QHBoxLayout(self.output_value_selection_box_group_box%s)" % (
                    num, num))
            exec(
                "self.output_value_selection_box_horizontal_layout%s.addWidget(self.output_value_selection_label%s)" % (
                    num, num))
            exec(
                "self.output_value_selection_box_horizontal_layout%s.addWidget(self.output_value_selection_combo_box%s)" % (
                    num, num))
            if num != self.letters[0]:
                exec("self.output_value_selection_box_group_box%s.hide()" % num)

        #Parameters:
        self.neural_network_parameter_vertical_layout = QtWidgets.QVBoxLayout(self.neural_network_parameter_selection_box)

        self.neural_network_epochs_label = QtWidgets.QLabel("Epochs:")
        self.neural_network_epochs_spin_box = QtWidgets.QSpinBox()
        self.neural_network_epochs_spin_box.setMinimum(1)
        self.neural_network_epochs_spin_box.setMaximum(100000)
        self.neural_network_epochs_selection_box = QtWidgets.QGroupBox()
        self.neural_network_epochs_horizontal_layout = QtWidgets.QHBoxLayout(
        self.neural_network_epochs_selection_box)
        self.neural_network_epochs_horizontal_layout.addWidget(self.neural_network_epochs_label)
        self.neural_network_epochs_horizontal_layout.addWidget(self.neural_network_epochs_spin_box)
        self.neural_network_parameter_vertical_layout.addWidget(self.neural_network_epochs_selection_box)

        self.neural_network_batch_label = QtWidgets.QLabel("Batch Size:")
        self.neural_network_batch_spin_box = QtWidgets.QSpinBox()
        self.neural_network_batch_spin_box.setMinimum(1)
        self.neural_network_batch_spin_box.setMaximum(100000)
        self.neural_network_batch_selection_box = QtWidgets.QGroupBox()
        self.neural_network_batch_horizontal_layout = QtWidgets.QHBoxLayout(
        self.neural_network_batch_selection_box)
        self.neural_network_batch_horizontal_layout.addWidget(self.neural_network_batch_label)
        self.neural_network_batch_horizontal_layout.addWidget(self.neural_network_batch_spin_box)
        self.neural_network_parameter_vertical_layout.addWidget(self.neural_network_batch_selection_box)

        self.neural_network_optimizer_label = QtWidgets.QLabel("Optimizer: ")
        self.neural_network_optimizer_selection_combo_box = QtWidgets.QComboBox()
        self.neural_network_optimizer_selection_combo_box.addItem("sgd")
        self.neural_network_optimizer_selection_combo_box.addItem("rmsprop")
        self.neural_network_optimizer_selection_combo_box.addItem("adagrad")
        self.neural_network_optimizer_selection_combo_box.addItem("adadelta")
        self.neural_network_optimizer_selection_combo_box.addItem("adam")
        self.neural_network_optimizer_selection_combo_box.addItem("adamax")
        self.neural_network_optimizer_selection_combo_box.addItem("nadam")
        self.neural_network_optimizer_selection_box = QtWidgets.QGroupBox()
        self.neural_network_optimizer_horizontal_layout = QtWidgets.QHBoxLayout(self.neural_network_optimizer_selection_box)
        self.neural_network_optimizer_horizontal_layout.addWidget(self.neural_network_optimizer_label)
        self.neural_network_optimizer_horizontal_layout.addWidget(self.neural_network_optimizer_selection_combo_box)
        self.neural_network_parameter_vertical_layout.addWidget(self.neural_network_optimizer_selection_box)

        self.neural_network_layers_label = QtWidgets.QLabel("Number of Layers")
        self.neural_network_layers_selection_combo_box = QtWidgets.QComboBox()
        self.neural_network_layers_selection_combo_box.addItem("2")
        self.neural_network_layers_selection_combo_box.addItem("3")
        self.neural_network_layers_selection_combo_box.addItem("4")
        self.neural_network_layers_selection_combo_box.addItem("5")
        self.neural_network_layers_selection_combo_box.currentIndexChanged.connect(self.show_parameters_values)

        self.neural_network_layers_number_selection_box = QtWidgets.QGroupBox()
        self.neural_network_layers_number_horizontal_layout = QtWidgets.QHBoxLayout(
        self.neural_network_layers_number_selection_box)
        self.neural_network_layers_number_horizontal_layout.addWidget(self.neural_network_layers_label)
        self.neural_network_layers_number_horizontal_layout.addWidget(self.neural_network_layers_selection_combo_box)
        self.neural_network_parameter_vertical_layout.addWidget(self.neural_network_layers_number_selection_box)

        self.numbers = [i for i in range(1,6)]
        for num, n in zip(self.letters, self.numbers):
            exec("self.layers_value_selection_box_group_box%s = QtWidgets.QGroupBox()" % num)
            exec("self.layers_value_selection_label%s = QtWidgets.QLabel('Neurons in Layer %s')" % (
                num, n))
            exec("self.layers_value_selection_spin_box%s = QtWidgets.QSpinBox()" % num)
            exec("self.layers_value_selection_spin_box%s.setMinimum(1)" % num)
            exec("self.layers_value_selection_spin_box%s.setMaximum(100000)" % num)

            exec("self.activation_value_selection_box_group_box%s = QtWidgets.QGroupBox()" % num)
            exec("self.activation_value_selection_label%s = QtWidgets.QLabel('Activation in Layer %s')" % (
                num, n))
            exec("self.activation_value_selection_spin_box%s = QtWidgets.QComboBox()" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('None')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('softmax')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('elu')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('selu')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('softplus')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('softsign')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('relu')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('tanh')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('sigmoid')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('hard_sigmoid')" % num)
            exec("self.activation_value_selection_spin_box%s.addItem('linear')" % num)
            exec(
                "self.activation_value_selection_box_horizontal_layout%s = QtWidgets.QHBoxLayout(self.activation_value_selection_box_group_box%s)" % (
                    num, num))
            exec(
                "self.activation_value_selection_box_horizontal_layout%s.addWidget(self.activation_value_selection_label%s)" % (
                    num, num))
            exec(
                "self.activation_value_selection_box_horizontal_layout%s.addWidget(self.activation_value_selection_spin_box%s)" % (
                    num, num))

            exec(
                "self.layers_value_selection_box_horizontal_layout%s = QtWidgets.QHBoxLayout(self.layers_value_selection_box_group_box%s)" % (
                    num, num))
            exec(
                "self.layers_value_selection_box_horizontal_layout%s.addWidget(self.layers_value_selection_label%s)" % (
                    num, num))
            exec(
                "self.layers_value_selection_box_horizontal_layout%s.addWidget(self.layers_value_selection_spin_box%s)" % (
                    num, num))
            exec(
                "self.neural_network_parameter_vertical_layout.addWidget(self.layers_value_selection_box_group_box%s)" % num)
            exec(
                "self.neural_network_parameter_vertical_layout.addWidget(self.activation_value_selection_box_group_box%s)" % num)

            if num != self.letters[0] and num != self.letters[1]:
                exec("self.layers_value_selection_box_group_box%s.hide()" % num)
                exec("self.activation_value_selection_box_group_box%s.hide()" % num)
        exec("self.layers_value_selection_spin_box%s.setValue(self.number_of_output_values)" % self.to_show[-1])
        exec("self.layers_value_selection_spin_box%s.setReadOnly(True)" % self.to_show[-1])
        self.neural_network_parameter_vertical_layout.addWidget(self.neural_network_train_button)

        self.master_grid_layout.addWidget(self.value_selection_box, 0, 0, 1, 1)
        self.master_grid_layout.addWidget(self.neural_network_box, 0, 1, 1, 1)
        self.master_grid_layout.addWidget(self.neural_network_parameter_selection_box, 0, 2, 1, 1)
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

    def process_layers(self):
        self.neurons = []
        for i in self.letters[0:self.number_of_layers_values]:
            string = "self.layers_value_selection_spin_box%s.value()" % i
            self.neurons.append(eval(string))
        self.inputs = []
        for i in self.letters[0:self.number_of_input_values]:
            string = "self.input_value_selection_combo_box%s.currentIndex()" % i
            self.inputs.append(eval(string))
        self.outputs = []
        for i in self.letters[0:self.number_of_output_values]:
            string = "self.output_value_selection_combo_box%s.currentIndex()" % i
            self.outputs.append(eval(string))
        self.activations = []
        for i in self.letters[0:self.number_of_layers_values]:
            string = "self.activation_value_selection_spin_box%s.currentText()" % i
            if eval(string) == 'None':
                self.activations.append(None)
            else:
                self.activations.append(eval(string))
        self.network_processed = True

    def show_values(self):
        self.number_of_values = int(self.quantity_selection_combo_box.currentText())
        for letter in self.letters[:self.number_of_values]:
            exec("self.value_selection_box_group_box%s.show()" % letter)
        for letter in self.letters[self.number_of_values:]:
            exec("self.value_selection_box_group_box%s.hide()" % letter)

    def show_input_values(self):
        self.number_of_input_values = int(self.neural_network_input_selection_combo_box.currentText())
        for letter in self.letters[:self.number_of_input_values]:
            exec("self.input_value_selection_box_group_box%s.show()" % letter)
        for letter in self.letters[self.number_of_input_values:]:
            exec("self.input_value_selection_box_group_box%s.hide()" % letter)

    def show_output_values(self):
        self.number_of_output_values = int(self.neural_network_output_selection_combo_box.currentText())
        for letter in self.letters[:self.number_of_output_values]:
            exec("self.output_value_selection_box_group_box%s.show()" % letter)
        for letter in self.letters[self.number_of_output_values:]:
            exec("self.output_value_selection_box_group_box%s.hide()" % letter)
        exec("self.layers_value_selection_spin_box%s.setValue(self.number_of_output_values)" % self.to_show[-1])

    def show_parameters_values(self):
        self.number_of_layers_values = int(self.neural_network_layers_selection_combo_box.currentText())
        self.to_show = self.letters[:self.number_of_layers_values]
        for letter in self.to_show:
            exec("self.layers_value_selection_box_group_box%s.show()" % letter)
            exec("self.activation_value_selection_box_group_box%s.show()" % letter)
            if letter == self.to_show[-1]:
                exec("self.layers_value_selection_spin_box%s.setValue(self.number_of_output_values)" % letter)
                exec("self.layers_value_selection_spin_box%s.setReadOnly(True)" % letter)
            elif letter != self.to_show[0]:
                exec("self.layers_value_selection_spin_box%s.setValue(1)" % letter)
                exec("self.layers_value_selection_spin_box%s.setReadOnly(False)" % letter)
            else:
                exec("self.layers_value_selection_spin_box%s.setReadOnly(False)" % letter)
        for letter in self.letters[self.number_of_layers_values:]:
            exec("self.layers_value_selection_spin_box%s.setValue(0)" % letter)
            exec("self.layers_value_selection_box_group_box%s.hide()" % letter)
            exec("self.activation_value_selection_box_group_box%s.hide()" % letter)

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

    def create_model(self, inputs, outputs, epochs, batch, neurons, activations, optimizer, load=False):
        if load:
            self.load_model()
        else:
            self.inputs = inputs
            self.outputs = outputs
            self.epochs = epochs
            self.batch = batch
            self.model = Sequential()
            self.optimizer = optimizer
            for i, a in zip(neurons, activations):
                if i == neurons[0]:
                    if a == None:
                        exec("self.model.add(Dense(%s, input_dim=len(inputs[0]), activation=%s))" % (i, a))
                    else:
                        exec("self.model.add(Dense(%s, input_dim=len(inputs[0]), activation='%s'))" % (i, a))
                elif i == neurons[-1]:
                    exec("self.model.add(Dense(%s))" % i)
                else:
                    if a == None:
                        exec("self.model.add(Dense(%s, activation=%s))" % (i, a))
                    else:
                        exec("self.model.add(Dense(%s, activation='%s'))" % (i, a))
            self.loss = []
            self.epoch_list = []
            print(self.model.input_shape)
            self.input_shape = self.model.input_shape
            self.model.summary()
            exec("self.model.compile(loss='mse', optimizer='%s')" % self.optimizer)

    def load_model(self):
        self.model = load_model(self.savefile)

    def save_model(self):
        self.model.save(self.savefile)

    def train_model(self, validate=False):
        for i in range(self.epochs):
            if validate:
                pass
            else:
                print("Iteration: ", i)
                hist = History()
                self.model.fit(self.inputs, self.outputs, batch_size=self.batch, epochs=1, callbacks=[hist])
                self.save_model()
                self.loss.append(float(hist.history.get('loss')[0]))
                self.epoch_list.append(i)

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

if __name__ == '__main__':
    m = VisualizerMain("/logs")
    m.create_window()
    dp = DataProcessor("logs/gyro.txt", "logs/accelX.txt", "logs/accelY.txt", "logs/joy.txt")
    dp.load_data(3, False)
    joys, left_joys, right_joys, data, delta_gyro, delta_accelX, delta_accelY, times = dp.preprocess()
    s = set(left_joys + right_joys)
    d = {0: left_joys, 1: right_joys, 2: delta_accelX, 3: delta_accelY, 4: delta_gyro}
    print(len(set(left_joys)), ", ", len(set(right_joys)))
    text_list = [m.form.value_selection_combo_box.itemText(i) for i in range(len(d))]
    while True:
        if m.form.is_processed:
            if m.form.number_of_values == 3:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(d.get(m.form.value_1), d.get(m.form.value_2), d.get(m.form.value_3), c='b', marker='o')
                ax.set_title("%s vs %s vs %s" % (text_list[m.form.value_1], text_list[m.form.value_2], text_list[m.form.value_3]))
                ax.set_xlabel(text_list[m.form.value_1])
                ax.set_ylabel(text_list[m.form.value_2])
                ax.set_zlabel(text_list[m.form.value_3])
            elif m.form.number_of_values == 2:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.scatter(d.get(m.form.value_1), d.get(m.form.value_2), c='b', marker='o')
                ax.set_title("%s vs %s" % (text_list[m.form.value_1], text_list[m.form.value_2]))
                ax.set_xlabel(text_list[m.form.value_1])
                ax.set_ylabel(text_list[m.form.value_2])
            m.form.is_processed = False

        if m.form.network_processed:
            inputs = []
            outputs = []
            temp_i = []
            temp_o = []
            for i in m.form.inputs:
                temp_i.append(d.get(i))
            for num in range(len(temp_i[0])):
                a = []
                for temp in temp_i:
                    a.append(temp[num])
                inputs.append(a)
            for o in m.form.outputs:
                temp_o.append(d.get(o))
            for num in range(len(temp_o[0])):
                b = []
                for temp in temp_o:
                    b.append(temp[num])
                outputs.append(b)

            dn = DecisionNetwork("models/dynamics_model.h5")
            dn.create_model(inputs, outputs, m.form.neural_network_epochs_spin_box.value(),
                            m.form.neural_network_batch_spin_box.value(), m.form.neurons, m.form.activations,
                            m.form.neural_network_optimizer_selection_combo_box.currentText(), False)
            dn.train_model()
            loss_fig = plt.figure()
            loss_ax = loss_fig.add_subplot(111)
            loss_ax.plot(dn.epoch_list, dn.loss, c='b', marker='o')
            loss_ax.set_title("Loss vs Epoch")
            loss_ax.set_xlabel("Epochs")
            loss_ax.set_ylabel("Loss")
            if (len(inputs[0]) + len(outputs[0])) == 2:
                y = []
                z = []
                fig2 = plt.figure()
                ax2 = fig2.add_subplot(111)
                ax2.set_title("Predicted (blue) vs Actual (red)")
                ax2.set_xlabel(text_list[m.form.input_value_selection_combo_box.currentIndex()])
                ax2.set_ylabel(text_list[m.form.output_value_selection_combo_box.currentIndex()])
                for i in range(-1023, 1023):
                    y.append(i)
                    z.append(dn.model.predict(np.array([i]))[0][0])
                ax2.plot(y, z, c='b', marker='o')
                ax2.scatter(inputs, outputs, c='r', marker='s')
            m.form.network_processed = False
            if (len(inputs[0]) + len(outputs[0])) == 3:
                x = []
                y = []
                z = []
                fig2 = plt.figure()
                ax2 = fig2.add_subplot(111, projection='3d')
                for i in range(-1024, 1025, 16):
                    for j in range(-1024, 1025, 16):
                        x.append(i)
                        y.append(j)
                        z.append(dn.model.predict(np.array([i,j]).reshape(1, dn.input_shape[1]))[0][0])
                ax2.set_title("Predicted (blue) vs Actual (red)")
                ax2.scatter(x, y, z, color='blue', marker='o', rasterized=True)
                ax2.set_xlim3d(min(x), max(x))
                ax2.set_ylim3d(min(y), max(y))
                ax2.set_zlim3d(min(z), max(z))
                if len(inputs[0]) > 1:
                    ax2.set_xlabel(text_list[m.form.input_value_selection_combo_box.currentIndex()])
                    ax2.set_ylabel(text_list[m.form.input_value_selection_combo_box_2.currentIndex()])
                    ax2.set_zlabel(text_list[m.form.output_value_selection_combo_box.currentIndex()])
                    xs = [inputs[i][0] for i in range(len(inputs))]
                    ys = [inputs[i][1] for i in range(len(inputs))]
                    zs = [outputs[i] for i in range(len(outputs))]
                    delx = []
                    dely = []
                    delz = []
                    for i in range(len(xs)):
                        if xs[i] < min(x) or xs[i] > max(x) or ys[i] < min(y) or ys[i] > max(y) or zs[i] < min(z) or zs[i] > max(z):
                            delx.append(xs[i])
                            dely.append(ys[i])
                            delz.append(zs[i])
                    for j in delx:
                        xs.remove(j)
                    for j in dely:
                        ys.remove(j)
                    for j in delz:
                        zs.remove(j)
                    ax2.scatter(xs, ys, zs, c='r', marker='s')
                else:
                    ax2.set_xlabel(text_list[m.form.input_value_selection_combo_box.currentIndex()])
                    ax2.set_ylabel(text_list[m.form.output_value_selection_combo_box.currentIndex()])
                    ax2.set_zlabel(text_list[m.form.output_value_selection_combo_box_2.currentIndex()])
                    ax2.scatter([inputs[i] for i in range(len(inputs)) if inputs[i] >= min(x) and inputs[i] <= max(x)],
                                [outputs[i][0] for i in range(len(outputs)) if outputs[i][0] >= min(z) and outputs[i][0] <= max(z)],
                                [outputs[i][1] for i in range(len(outputs)) if outputs[i][1] >= min(z) and outputs[i][1] <= max(z)], c='r', marker='s')
            m.form.network_processed = False
        plt.show()
        m.processEvents()
    sys.exit(m.exec_()) #BrushBot == Devil
