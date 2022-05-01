from pickle import GLOBAL
from ssl import ALERT_DESCRIPTION_NO_RENEGOTIATION
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSlider, QLCDNumber
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import pandas as pd
import pathlib
from PyQt5.QtWidgets import QMessageBox
from sympy import degree
import more_itertools as mit
from sympy import S, symbols, printing 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg



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
        self.predict_button.clicked.connect(self.extrapolation) 
        self.degree_slider.valueChanged.connect(self.equation) 

        # self.degree_slider.setMinimum(1)
        # self.degree_slider.setMaximum(10)
        self.percentage_display_2= self.findChild(QLCDNumber, "percentage_display_2")
        self.degree_slider.valueChanged.connect(lambda: self.percentage_display_2.display(self.degree_slider.value()))
        self.percentage_slider.valueChanged.connect(self.equation) 
        # self.percentage_slider.setMinimum(1)
        # self.percentage_slider.setMaximum(100)
        self.percentage_display= self.findChild(QLCDNumber, "percentage_display")
        self.percentage_slider.valueChanged.connect(lambda: self.percentage_display.display(self.percentage_slider.value()))

    
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

    
    def equation(self):
        
        global degree
        degree = self.degree_slider.value()
       
        p = np.polyfit(self.time, self.magnitude, degree)
        xSymbols = symbols("x")
        poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1]))
        eq_latex = printing.latex(poly)
        label="{}".format(eq_latex)
       


        self.equation_label.setText(label)
    
    def extrapolation(self):
        percent_data = self.percentage_slider.value()
        percent_predict = 100 - percent_data
        # cut the list into a certain percentage of data according to the slider
        split_time = self.time[:int(len(self.time) * percent_data / 100)]
        split_magnitude = self.magnitude[:int(len(self.magnitude) * percent_data / 100)]
        # convert lists to arrays
        arr_time = np.array(split_time) 
        arr_magnitude = np.array(split_magnitude)
        #prediction array
        prediction = np.polyfit(split_time, split_magnitude, degree)
        arr_predict = np.array(prediction)
        # append both
        mag_predict = np.append(arr_magnitude, arr_predict)
        
        self.plot_widget.clear()
        
        self.plot_widget.plot(mag_predict) # self.time, 
        


       
    
    def split_chunks(self):
        # converting to arrays if needed
        self.time_array = np.array(self.time)
        self.magnitude_array = np.array(self.magnitude)
        self.chunk_num = self.num_chunks_input.value()
        self.chunk_size = int(len(self.magnitude) / self.chunk_num)
        overlap_size = int((self.overlap_input.value() / 100) * self.chunk_size)

      
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
        
        
        # self.fitted=np.poly1d(np.polyfit(self.time_array,self.magnitude_array,self.degree))
        # self.plot_widget.clear()
        # self.plotting()
        # self.interrpolation = self.fitted(self.time_array)
        # self.curvePen = pg.mkPen(color=(0, 0, 255), style=QtCore.Qt.DashLine)

        # self.plot_widget.plot(self.time_array, self.interrpolation,pen=self.curvePen )
    
        self.overlap=int(self.overlap_input.value())
        self.n=int((len(self.time_array))/self.chunk_num)
        self.curvePen = pg.mkPen(color=(0, 0, 255), style=QtCore.Qt.DashLine)
        if(self.overlap>=0 and self.overlap<=25):
            self.overlapsizee=int((self.overlap/100)*((len(self.time_array))/self.chunk_num))
            self.time_chunks = list(mit.windowed(self.time_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-self.overlapsizee))
            self.mag_chunks = list(mit.windowed(self.magnitude_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-self.overlapsizee))
            self.plot_widget.clear()
        self.plotting()    
        for i in range(self.chunk_num):
            
            self.Interpolation = np.poly1d(np.polyfit(self.time_chunks[i], self.mag_chunks[i], self.degree))
            self.plot_widget.plot(self.time_chunks[i], self.Interpolation(self.time_chunks[i]), pen=self.curvePen)    
            
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
