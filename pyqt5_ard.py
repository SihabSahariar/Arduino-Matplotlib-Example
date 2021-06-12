#Developed By Sihab Sahariar
import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import random
import matplotlib.pyplot as plt
import time
import threading 
import  serial
plt.style.use('dark_background')
ser = serial.Serial('COM4',9600) #Set your arduino port
ser.flushInput()
ser.flushOutput()

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Arduino Live data plot")
        self.canvas = MplCanvas(self, width=10, height=10, dpi=100)
        self.setCentralWidget(self.canvas)
        self.xdata = []
        self.ydata = []
        self.update_plot()
   
        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.data_raw = ser.readline().decode("utf-8") #Readling arduino data
        t = time.localtime()
        p = time.strftime("%H:%M:%S", t)
        self.ydata.append(int(self.data_raw))
        self.xdata.append(p)        
        print(self.ydata,"\n",self.xdata)

        if len(self.ydata) and len(self.xdata)>5: #deleting the very first data when data number is more than 5
            self.xdata.pop(0)
            self.ydata.pop(0) 

        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()