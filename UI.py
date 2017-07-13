from PyQt5 import QtCore, QtGui, QtWidgets
import random, sys, warnings
from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout,QMainWindow,QApplication,QAction)
from PyQt5.Qt import Qt
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

warnings.simplefilter("ignore", DeprecationWarning)


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):

        #Initilize variables for tutorial box pages
        self.current_page, self.max_Page = 0, 0
        self.app = 1

        #Size window to default dimensions
        self.resize(300, 200)
        self.setWindowTitle("AbaML")

        #Create a central Widget
        self.centralwidget = QtWidgets.QWidget(self)

        self.masterGridLayout = QGridLayout()

        self.gridLayoutRow1 = QGridLayout()
        self.setWAction = QAction("Set Enter", self, shortcut=Qt.Key_W, triggered=self.setW)
        self.addAction(self.setWAction)
        self.button1 = QtWidgets.QPushButton('W',clicked=self.setWAction.triggered)
        self.gridLayoutRow1.addWidget(self.button1, 0, 0, 1, 1)

        self.gridLayoutRow2 = QGridLayout()
        self.button2 = QtWidgets.QPushButton('A')
        self.button3 = QtWidgets.QPushButton('S')
        self.button4 = QtWidgets.QPushButton('D',)
        self.gridLayoutRow2.addWidget(self.button2, 0, 1, 1, 1)
        self.gridLayoutRow2.addWidget(self.button3, 0, 2, 1, 1)
        self.gridLayoutRow2.addWidget(self.button4, 0, 3, 1, 1)

        self.row1 = QtWidgets.QWidget()
        self.row1.setLayout(self.gridLayoutRow1)
        self.row2 = QtWidgets.QWidget()
        self.row2.setLayout(self.gridLayoutRow2)

        self.masterGridLayout.addWidget(self.row1,0,0,1,1)
        self.masterGridLayout.addWidget(self.row2, 1, 0, 1, 1)
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

    def setW(self):
        print('W')

