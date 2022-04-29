from pickle import GLOBAL
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSlider
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import pandas as pd
import pathlib
from PyQt5.QtWidgets import QMessageBox
from sympy import degree
import more_itertools as mit 



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('task4.ui', self)
        self.time = []
        self.magnitude = []
        #initially without ny changes to the spinboxes
        self.chunk_num = 1
        self.chunk_size = len(self.magnitude)
        self.action_open.triggered.connect(self.open) 
        self.fit_button.clicked.connect(self.split_chunks)  
    
    def open(self):
        # open any csv file
        files_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open only CSV ', os.getenv('HOME'), "csv(*.csv)")
        path = files_name[0]
        pathlib.Path(path).suffix == ".csv"
        # read the data in the file
        data = pd.read_csv(path)
        # place the data in time and magnitude arrays
        self.time = data.values[:, 0] # the data is read in case it is needed later but won't be used in plotting, for now at least
        self.magnitude = data.values[:, 1]
        # plot the data
        self.plot_widget.clear() # clearing hear not in plotting function because we only want to clear when opening a new file
        self.plotting()      

    def plotting(self):
           
       self.plot_widget.plot(self.time, self.magnitude)
       
    
    def split_chunks(self):
        # converting to arrays if needed
        self.time_array = np.array(self.time)
        self.magnitude_array = np.array(self.magnitude)
        self.chunk_num = self.num_chunks_input.value()
        self.chunk_size = int(len(self.magnitude) / self.chunk_num)
        overlap_size = int((self.overlap_input.value() / 100) * self.chunk_size)

         # ERROR MESSAGE popup
        self.degree= self.degree_slider.value()
        # if (self.chunk_num==1): #one chunk logic
        #     Fitted = np.polyfit(self.time_array, self.magnitude_array, 2)
        #     self.plot_widget.clear()
        #     self.plotting()
        #     Poly = np.poly1d(Fitted) #fit line equation
        #     self.newy = []
        #     for i in range(len(self.magnitude_array)):
        #         fittedvalues = Poly(i)
        #         self.newy.append(fittedvalues)
        #     self.plt2 = self.plot_widget.plot(self.time_array, self.newy,pen=None, symbol="x", symbolPen=(255,140,0), symbolBrush = (255,140,0))
        
        if(self.chunk_num==1):
            self.fitted=np.poly1d(np.polyfit(self.time_array,self.magnitude_array,1))
            self.plot_widget.clear()
            self.plotting()
            self.interrpolation = self.fitted(self.time_array)
            self.curvePen = pg.mkPen(color=(0, 0, 255), style=QtCore.Qt.DashLine)

            self.plot_widget.plot(self.time_array, self.interrpolation,pen=self.curvePen )
        else:
            self.overlap=int(self.overlap_input.value())
            self.n=int((len(self.time_array))/self.chunk_num)
            self.curvePen = pg.mkPen(color=(0, 0, 255), style=QtCore.Qt.DashLine)
            if(self.overlap>=0 and self.overlap<=25):
                self.k=int((self.overlap/100)*((len(self.time_array))/self.chunk_num))
                self.time_chunks = list(mit.windowed(self.time_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-self.k))
                self.mag_chunks = list(mit.windowed(self.magnitude_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-self.k))
                self.plot_widget.clear()
            self.plotting()    
            for i in range(self.chunk_num):
               
                self.Interpolation = np.poly1d(np.polyfit(self.time_chunks[i], self.mag_chunks[i], 2))
                self.plot_widget.plot(self.time_chunks[i], self.Interpolation(self.time_chunks[i]), pen=self.curvePen)    
        if self.chunk_num > 20:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error!")
            msg.setInformativeText('The maximum number of chunks is 20')
            msg.setWindowTitle("Error")
            msg.exec_()
            self.chunk_num = 20
            
        # split the arrays into chunks (if needed)
        # chunked_time = np.array_split(time_array, chunk_num)
        # chunked_mag = np.array_split(magnitude_array, chunk_num)

       # plotting the chunks with different colors di hatb2a function tanya aslun interpolation bas da for testing
        #colors = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255)]
        # self.plot_widget.clear() # clearing hear not in plotting function because we only want to clear when opening a new file
        # self.plotting() 
        # for i in range (0, len(self.magnitude), self.chunk_size - overlap_size): # (initial, final but not included)
        # #    print(self.time[i:i+self.chunk_size])
        #     curvePen = pg.mkPen(color=(0, 0, 255), style=QtCore.Qt.DashLine)
        #     self.plot_widget.plot(self.time[i:i+self.chunk_size], self.magnitude[i:i+self.chunk_size], pen = curvePen)
        
    
    
        #------------------in case it is needed-----------------------
        # # Convert chunked arrays into lists
        # chunked_list = [list(array) for array in chunked_mag]
        # #print(chunked_list)
        #-------------------------------------------------------------
    


    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
