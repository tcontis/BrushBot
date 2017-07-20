"""UI Layout"""

from PyQt5.QtCore import QObject
import sys
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QGridLayout, QMainWindow)


class UiMainWindow(QMainWindow):
    """The Main Window for the BrushBot Project"""

    def __init__(self):
        """Initialize Window"""
        super(UiMainWindow, self).__init__([])
        self.setupUi()

    def setupUi(self):

        # Size window to default dimensions
        self.resize(1800, 900)
        self.setWindowTitle("BrushBot")
        self.showMaximized()

        # Create a central Widget
        self.central_widget = QtWidgets.QWidget(self)

        self.master_grid_layout = QGridLayout()

        self.mode_box = QtWidgets.QGroupBox(self.central_widget, title="Modes")
        self.mode_box.setAlignment(QtCore.Qt.AlignCenter)
        self.comm_box = QtWidgets.QGroupBox(self.central_widget, title="Communications")
        self.comm_box.setAlignment(QtCore.Qt.AlignCenter)
        self.log_box = QtWidgets.QGroupBox(self.central_widget, title="Log")
        self.log_box.setAlignment(QtCore.Qt.AlignCenter)
        self.gyro_box = QtWidgets.QGroupBox(self.central_widget, title="Delta Gyro Plot")
        self.gyro_box.setAlignment(QtCore.Qt.AlignCenter)
        self.accel_box = QtWidgets.QGroupBox(self.central_widget, title="Delta Accelerometer Plot")
        self.accel_box.setAlignment(QtCore.Qt.AlignCenter)
        self.pos_box = QtWidgets.QGroupBox(self.central_widget, title="Delta Position Plot")
        self.pos_box.setAlignment(QtCore.Qt.AlignCenter)

        self.mode_selection_group_box = QtWidgets.QGroupBox()
        self.mode_label = QtWidgets.QLabel("Mode Selection:")
        self.mode_selection_combo_box = QtWidgets.QComboBox()
        self.mode_selection_combo_box.addItem("Manual")
        self.mode_selection_combo_box.addItem("Automatic")

        self.comm_text = QtWidgets.QPlainTextEdit()
        self.comm_text.setReadOnly(True)

        self.log_text = QtWidgets.QPlainTextEdit()
        self.log_text.setReadOnly(True)

        self.gyro_plot = pg.PlotWidget()

        self.accel_plot = pg.PlotWidget()

        self.pos_plot = pg.PlotWidget()

        self.mode_vertical_layout = QtWidgets.QVBoxLayout(self.mode_box)
        self.mode_vertical_layout.addWidget(self.mode_selection_group_box)
        self.mode_selection_group_box_horizontal_layout = QtWidgets.QHBoxLayout(self.mode_selection_group_box)
        self.mode_selection_group_box_horizontal_layout.addWidget(self.mode_label)
        self.mode_selection_group_box_horizontal_layout.addWidget(self.mode_selection_combo_box)
        self.mode_vertical_layout.addWidget(self.log_box)

        self.comm_vertical_layout = QtWidgets.QVBoxLayout(self.comm_box)
        self.comm_vertical_layout.addWidget(self.comm_text)

        self.log_vertical_layout = QtWidgets.QVBoxLayout(self.log_box)
        self.log_vertical_layout.addWidget(self.log_text)

        self.gyro_vertical_layout = QtWidgets.QVBoxLayout(self.gyro_box)
        self.gyro_vertical_layout.addWidget(self.gyro_plot)

        self.accel_vertical_layout = QtWidgets.QVBoxLayout(self.accel_box)
        self.accel_vertical_layout.addWidget(self.accel_plot)

        self.pos_vertical_layout = QtWidgets.QVBoxLayout(self.pos_box)
        self.pos_vertical_layout.addWidget(self.pos_plot)

        self.master_grid_layout.addWidget(self.mode_box, 0, 0, 1, 1)
        self.master_grid_layout.addWidget(self.comm_box, 0, 1, 1, 1)
        #self.master_grid_layout.addWidget(self.log_box, 0, 2, 1, 1)
        self.master_grid_layout.addWidget(self.gyro_box, 1, 0, 1, 1)
        self.master_grid_layout.addWidget(self.accel_box, 1, 1, 1, 1)
        self.master_grid_layout.addWidget(self.pos_box, 1, 2, 1, 1)
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
