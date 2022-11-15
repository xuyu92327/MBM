import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import numpy as np
import time
import paramiko

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'Muon Beam Monitor'
        self.width = 1640
        self.height = 1200
        self.time0 = time.time()
        self.initUI()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.start()
        self.button.clicked.connect(self.update)
        self.stop_button.clicked.connect(self.timer.stop)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.m = PlotCanvas(self, width=15, height=8, N=10000)
        self.m.move(200,100)

        self.button = QPushButton('Start', self)
        self.button.setToolTip('This is an example button')
        self.button.move(50, 100)
        self.button.resize(100, 30)
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.move(50, 150)
        self.stop_button.resize(100, 30)

        self.show()

    def update(self):
        self.time1 = time.time()
        N = int((self.time1-self.time0)*10000)
        self.m.update_plot()
        self.timer.start()
        self.timer.timeout.connect(self.m.update_plot)
        self.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, N=1000):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.N = N
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data_x = []
        self.ax_x = self.figure.add_subplot(211)
        self.ax_x.hist(data_x, bins=128, histtype='step')
        self.ax_x.set_title('Profile X')
        #self.ax_x.set_xlabel('Fiber No.')
        self.ax_x.set_ylabel('N Hits')
        self.ax_x.set_xlim(0,128)
        data_y = [] #np.random.uniform(0,128,128)
        self.ax_y = self.figure.add_subplot(212)
        self.ax_y.hist(data_y, bins=128, histtype='step')
        self.ax_y.set_title('Profile Y')
        self.ax_y.set_xlabel('Fiber No.')
        self.ax_y.set_ylabel('N Hits')
        self.ax_y.set_xlim(0,128)
        self.draw()


    def update_plot(self):
        data_x = np.random.normal(64,12,self.N)
        #self.ax_x.hist(data_x, bins=128, histtype='step')
        data_y = np.random.normal(64,12,self.N)
        #self.ax_y.hist(data_y, bins=128, histtype='step')
        self.ax_x.clear()
        self.ax_x.hist(data_x, bins=128, histtype='step')
        self.ax_x.set_title('Profile X')
        self.ax_x.set_ylabel('N Hits')
        self.ax_x.set_xlim(0,128)
        self.ax_x.set_ylim(0,300)
        self.ax_y.clear()
        self.ax_y.hist(data_y, bins=128, histtype='step')
        self.ax_y.set_title('Profile Y')
        self.ax_y.set_xlabel('Fiber No.')
        self.ax_y.set_ylabel('N Hits')
        self.ax_y.set_xlim(0,128)
        self.ax_y.set_ylim(0,300)
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
