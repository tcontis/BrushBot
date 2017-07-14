from PyQt5 import QtCore, QtGui, QtWidgets
import random, sys, warnings,time
from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout,QMainWindow,QApplication,QAction, QGroupBox)
from PyQt5.Qt import Qt
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

warnings.simplefilter("ignore", DeprecationWarning)


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        #Size window to default dimensions
        self.resize(1800, 8900)
        self.setWindowTitle("BrushBot")

        #Create a central Widget
        self.centralwidget = QtWidgets.QWidget(self)

        self.masterGridLayout = QGridLayout()

        self.modeBox = QtWidgets.QGroupBox(self.centralwidget, title="Modes")
        self.modeBox.setAlignment(QtCore.Qt.AlignCenter)
        self.commBox = QtWidgets.QGroupBox(self.centralwidget, title="Communications")
        self.commBox.setAlignment(QtCore.Qt.AlignCenter)
        self.logBox = QtWidgets.QGroupBox(self.centralwidget, title="Log")
        self.logBox.setAlignment(QtCore.Qt.AlignCenter)

        self.modeSelectionGroupBox = QtWidgets.QGroupBox()
        self.modeLabel = QtWidgets.QLabel("Mode Selection:")
        self.modeSelectionComboBox = QtWidgets.QComboBox()
        self.modeSelectionComboBox.addItem("Manual")
        self.modeSelectionComboBox.addItem("Automatic")

        self.commText = QtWidgets.QPlainTextEdit()
        self.commText.setReadOnly(True)

        self.logText = QtWidgets.QPlainTextEdit()
        self.logText.setReadOnly(True)

        self.modeVerticalLayout = QtWidgets.QVBoxLayout(self.modeBox)
        self.modeVerticalLayout.addWidget(self.modeSelectionGroupBox)
        self.modeSelectionGroupBoxHorizontalLayout = QtWidgets.QHBoxLayout(self.modeSelectionGroupBox)
        self.modeSelectionGroupBoxHorizontalLayout.addWidget(self.modeLabel)
        self.modeSelectionGroupBoxHorizontalLayout.addWidget(self.modeSelectionComboBox)

        self.commVerticalLayout = QtWidgets.QVBoxLayout(self.commBox)
        self.commVerticalLayout.addWidget(self.commText)

        self.logVerticalLayout = QtWidgets.QVBoxLayout(self.logBox)
        self.logVerticalLayout.addWidget(self.logText)

        self.masterGridLayout.addWidget(self.modeBox,0,0,1,1)
        self.masterGridLayout.addWidget(self.commBox,0,1,1,1)
        self.masterGridLayout.addWidget(self.logBox,0,2, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(self.masterGridLayout)

        menubar = self.menuBar()

        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setWeight(50)
        menubar.setFont(font)
        menuFile = QtWidgets.QMenu(menubar)
        menuFile.setObjectName("menuFile")

        menuFile.setTitle("File")
        menubar.addAction(menuFile.menuAction())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        QtCore.QMetaObject.connectSlotsByName(self)

    def closeEvent(self, event):
        event.accept()
        sys.exit()

if __name__ == "__main__":
    app = QApplication([])
    form = Ui_MainWindow()
    form.show()
    form.update()
    while True:
        QtWidgets.QApplication.processEvents()
        time.sleep(0.05)
