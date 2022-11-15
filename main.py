import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
import time

from MplCanvas import MplCanvas
from TableWidgets import MyTableWidget
import paramiko
from itertools import zip_longest
from paramiko import SSHClient
from paramiko import AutoAddPolicy

import multiprocessing
import subprocess
from subprocess import *

host = '192.168.10.16'
username = 'root'
password = 'centos'

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'Muon Beam Monitor'
        self.width = 1640
        self.height = 1000
        self.idx = 0
        self.initUI()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(3000)
        #self.timer.start()
        self.init_daq.clicked.connect(self.init_sys)
        self.start_daq.clicked.connect(self.start)
        self.stop_daq.clicked.connect(self.stop)
        self.start_plot.clicked.connect(self.update)
        self.stop_plot.clicked.connect(self.stop_update)
#
        #sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        #sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table = MyTableWidget(self)
        self.setCentralWidget(self.table)
        self.init_daq = self.table.button0
        self.start_daq = self.table.button1
        self.stop_daq = self.table.button2
        self.start_plot = self.table.button3
        self.stop_plot = self.table.button4

        self.trans = paramiko.Transport((host, 22))
        self.trans.connect(username=username, password=password)
        self.ssh = MySSHClient()
        self.ssh._transport = self.trans
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        #stdin, stdout, stderr = self.ssh.run('./init.sh', console)

    def init_sys(self):
        stdin, stdout, stderr = self.ssh.run('./init.sh', console)

    def update_plot(self):
        subprocess.run('tail -20000 muon_test.dat > buf.dat', shell=True)
        #data_x = np.loadtxt('muon_test.dat', skiprows=1, usecols=0)
        #time_x = np.loadtxt('muon_test.dat', skiprows=1, usecols=2)
        data_x = np.loadtxt('buf.dat', usecols=0)
        time_x = np.loadtxt('buf.dat', usecols=2)
        data_x = data_x[::2]
        time_x = time_x[::2]
        self.table.data_x = data_x
        self.table.time_x = time_x
        self.table.updateTabs()
        self.idx = len(data_x)
        print('Current Event: ', self.idx)
        print(data_x[-1])
        self.show()


    def update(self):
        self.update_plot()
        self.timer.start()
        self.timer.timeout.connect(self.update_plot)
        self.show()

    def stop_update(self):
        self.timer.stop()

    def start(self):
        #start = Popen('python3 start.py', shell=True, stdout=PIPE, stderr=PIPE)
        start = Popen('python3 start.py', shell=True)     
#        for line in iter(start.stdout.readline, b''):
#            print(line)
#        start.stdout.close()

    def stop(self):
        #self.trans.connect(username=username, password=password)
        self.ssh.run('./stop.sh', console)
        #subprocess.run('pkill ')

class MySSHClient(SSHClient):
    def run(self, command, callback):
        stdin, stdout, stderr = self.exec_command(command, bufsize=1)

        stdout_iter = iter(stdout.readline, '')
        stderr_iter = iter(stderr.readline, '')

        for out, err in zip_longest(stdout_iter, stderr_iter):
            if out: callback(out.strip())
            if err: callback(err.strip())

        return stdin, stdout, stderr

def console(text):
    print(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
