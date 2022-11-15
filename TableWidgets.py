from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QTabWidget, QVBoxLayout, QGridLayout, QTextEdit
from PyQt5 import QtCore, QtGui
import sys
from MplCanvas import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.transforms as mtransforms

def add_right_cax(ax, pad, width):
    '''
    在一个ax右边追加与之等高的cax.
    pad是cax与ax的间距,width是cax的宽度.
    '''
    axpos = ax.get_position()
    caxpos = mtransforms.Bbox.from_extents(
        axpos.x1 + pad,
        axpos.y0,
        axpos.x1 + pad + width,
        axpos.y1
    )
    cax = ax.figure.add_axes(caxpos)

    return cax

class MyTableWidget(QWidget):
    def __init__(self, parent, data_x=None, data_y=None, time_x=None, time_y=None):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QTextEdit()

        self.data_x = data_x
        self.data_y = data_y
        self.time_x = time_x
        self.time_y = time_y
        self.fre = np.zeros(50)
        self.cb = None

        self.initTabs()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def initTabs(self):
        self.initTab1()
        self.initTab2()
        self.initTab3()
        self.initTab4()

    def initTab1(self):
        self.tabs.addTab(self.tab1, 'Profile X and Y')
        self.tab1.layout = QGridLayout(self)
        for i in range(20):
            self.tab1.layout.setColumnStretch(i,1)
            self.tab1.layout.setRowStretch(i,1)

        self.button0 = QPushButton('DAQ Init')
        self.button1 = QPushButton('DAQ Start')
        self.button2 = QPushButton('DAQ Stop')
        self.button3 = QPushButton('Plot Start')
        self.button4 = QPushButton('Plot Stop')
        self.button0.setFixedSize(150,50)
        self.button1.setFixedSize(150,50)
        self.button2.setFixedSize(150,50)
        self.button3.setFixedSize(150,50)
        self.button4.setFixedSize(150,50)
        self.fig1 = MplCanvas(self, width=12, height=6)
        self.profile_x = self.fig1.fig.add_subplot(211)
        self.profile_y = self.fig1.fig.add_subplot(212)
        self.profile_x.set_title('Profile X')
        self.profile_x.set_xlim(0,128)
        self.profile_x.set_ylabel('NHit')
        self.profile_y.set_title('Profile Y')
        self.profile_y.set_xlim(0,128)
        self.profile_y.set_xlabel('Fiber No.')
        self.profile_y.set_ylabel('NHit')

        self.tab1.layout.addWidget(self.button0, 1, 1)
        self.tab1.layout.addWidget(self.button1, 3, 1)
        self.tab1.layout.addWidget(self.button2, 5, 1)
        self.tab1.layout.addWidget(self.button3, 7, 1)
        self.tab1.layout.addWidget(self.button4, 9, 1)
        self.tab1.layout.addWidget(self.fig1, 1, 3, 18, 18)
        self.tab1.setLayout(self.tab1.layout)

    def initTab2(self):
        self.tabs.addTab(self.tab2, '2D Profile')
        self.tab2.layout = QGridLayout(self)

        self.fig2 = MplCanvas(self, width=12, height=12)
        self.profile_xy = self.fig2.fig.add_subplot(111)
        profile_xy = self.profile_xy.hist2d([0],[0])
        self.profile_xy.set_title('2D Profile')
        self.profile_xy.set_xlabel('X Fiber No.')
        self.profile_xy.set_ylabel('Y Fiber No.')
        self.profile_xy.set_xlim(0,128)
        self.profile_xy.set_ylim(0,128)
        norm = mcolors.LogNorm(vmin=1E0, vmax=1E4)
        im = plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.Reds)
        cax = add_right_cax(self.profile_xy, pad=0.02, width=0.02)
        #self.cb = self.fig2.fig.colorbar(profile_xy[3], ax=self.profile_xy)
        self.cb = self.fig2.fig.colorbar(im, cax=cax)

        self.tab2.layout.addWidget(self.fig2, 1, 3, 18, 18)
        self.tab2.setLayout(self.tab2.layout)

    def initTab3(self):
        self.tabs.addTab(self.tab3, 'Trigger Rate')
        self.tab3.layout = QGridLayout(self)

        self.fig3 = MplCanvas(self, width=12, height=12)
        self.rate = self.fig3.fig.add_subplot(111)
        self.rate.set_title('Trigger Rate')
        self.rate.set_xlabel('Time [ms]')
        self.rate.set_ylabel('Rate [Hz]')
        self.rate.set_xlim(0,1000)
        
        self.tab3.layout.addWidget(self.fig3, 1, 3, 18, 18)
        self.tab3.setLayout(self.tab3.layout)

    def initTab4(self):
        self.tabs.addTab(self.tab4, 'Log Info')


    def updateTabs(self):
        self.updateTab1()
        self.updateTab2()
        self.updateTab3()
        self.updateTab4()

    def updateTab1(self):
        data_x = self.data_x
        data_y = self.data_x
        #data_y = self.data_y[::2,0]
        
        self.profile_x.clear()
        self.profile_y.clear()
        self.profile_x.hist(data_x, bins=17, range=(0,17), histtype='step')
        self.profile_x.set_title('Profile X')
        self.profile_x.set_ylabel('NHits')
        self.profile_x.set_xlim(0,17)
        self.profile_x.set_yscale('log')
        self.profile_y.hist(data_y, bins=17, range=(0, 17), histtype='step')
        self.profile_y.set_title('Profile Y')
        self.profile_y.set_xlabel('Fiber No.')
        self.profile_y.set_ylabel('NHits')
        self.profile_y.set_xlim(0,17)
        self.profile_y.set_yscale('log')
        self.fig1.draw()

    def updateTab2(self):
        data_x = self.data_x
        data_y = self.data_x
        x_bins = np.linspace(0, 16, 17)
        y_bins = np.linspace(0, 16, 17)

        #self.fig2.fig.clear()
        #if(self.cb is not None):
            #self.cb.remove()
        self.profile_xy.clear()
        #self.cb.ax.clear()
        profile_xy = self.profile_xy.hist2d(data_x, data_y, bins=[x_bins, y_bins], cmap=plt.cm.Reds)
        self.profile_xy.set_title('2D Profile')
        self.profile_xy.set_xlabel('X Fiber No.')
        self.profile_xy.set_ylabel('Y Fiber No')
        self.profile_xy.set_xlim(0,16)
        self.profile_xy.set_ylim(0,16)
        self.fig2.draw()
        #self.fig2.fig.colorbar(profile_xy[3], ax=self.profile_xy, cax=self.cb.ax)

    def updateTab3(self):
        N = len(self.time_x)
        time = self.time_x.sum()*5/1e9
        Fre = N/time
        self.fre[1:] = self.fre[:-1]
        self.fre[0] = Fre
        self.rate.clear()
        self.rate.plot(self.fre, 'ro-')
        self.rate.set_title('Trigger Rate')
        self.rate.set_xlabel('Time [s]')
        self.rate.set_ylabel('Rate [Hz]')
        self.rate.set_xlim(0,50)
        self.fig3.draw()

    def updateTab4(self):
        pass
