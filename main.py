from cProfile import label
from importlib.resources import path
from pickle import GLOBAL
from tkinter import Y
from tkinter import *
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSlider
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pathlib
from sympy import init_printing
from sympy import S, symbols, printing



import pandas as pd 





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
        # self.fit_button.clicked.connect(self.split_chunks) 
        self.degree_slider.valueChanged.connect(self.chunks) 
      
    
    def open(self):
        global data
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

    def chunks(self):
        
        global degree
        degree = self.degree_slider.value()
       
        p = np.polyfit(self.time, self.magnitude, degree)
        xSymbols = symbols("x")
        poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1]))
        eq_latex = printing.latex(poly)
        label="{}".format(eq_latex)
        
        self.equation_label.setText(label)
        
       
        
        
        # self.equation_label.setText(label)
        

        # xSymbols = symbols("x")
        # poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1]))
        
        # eq_latex = printing.latex(poly)
        # self.equation_label.setText(eq_latex)
        # init_printing() 
        # # label="${}$".format(eq_latex)
        
        # # self.equation_label.setText(label)
       

           

          
       
    
    # def split_chunks(self):
    #     # converting to arrays if needed
    #     # time_array = np.array(self.time)
    #     # magnitude_array = np.array(self.magnitude)
    #     self.chunk_num = self.num_chunks_input.value()
    #     self.chunk_size = int(len(self.magnitude) / self.chunk_num)
    #     overlap_size = int((self.overlap_input.value() / 100) * self.chunk_size)

    #      # ERROR MESSAGE popup   
    #     if self.chunk_num > 20:
    #         msg = QMessageBox()
    #         msg.setIcon(QMessageBox.Critical)
    #         msg.setText("Error!")
    #         msg.setInformativeText('The maximum number of chunks is 20')
    #         msg.setWindowTitle("Error")
    #         msg.exec_()
    #         self.chunk_num = 20
            
        # split the arrays into chunks (if needed)
        # chunked_time = np.array_split(time_array, chunk_num)
        # chunked_mag = np.array_split(magnitude_array, chunk_num)

       # plotting the chunks with different colors di hatb2a function tanya aslun interpolation bas da for testing
        # #colors = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255)]
        # self.plot_widget.clear() # clearing hear not in plotting function because we only want to clear when opening a new file
        # self.plotting() 
        # for i in range (0, len(self.magnitude), self.chunk_size - overlap_size): # (initial, final but not included)
        # #    print(self.time[i:i+self.chunk_size])
        #     curvePen = pg.mkPen(color=(0, 0, 255), style=QtCore.Qt.DashLine)
        #     self.plot_widget.plot(self.time[i:i+self.chunk_size], self.magnitude[i:i+self.chunk_size], pen = curvePen)

        # #interpolation
        #     model_interpolation =np.polyfit(self.time, self.magnitude, self.degree_slider)
        #     self.MplWidget.canvas.axes.plot(self.magnitude, model_interpolation(self.magnitude), '-.')
                
        
    
    
        #------------------in case it is needed-----------------------
        # # Convert chunked arrays into lists
        # chunked_list = [list(array) for array in chunked_mag]
        # #print(chunked_list)
        #-------------------------------------------------------------
    
    def error_map(self):
        x_value = 0
        y_value = 0
        if(self.x_dropdown.currentText() == "Number of Chunks"):
            x_value = self.chunk_num
        elif(self.x_dropdown.currentText() == "Fitting Polynomial Order"):
            x_value = self.chunk_num
        elif(self.x_dropdown.currentText() == "Overlapping Between Chunks"):
            x_value = self.chunk_num
        
        if(self.y_dropdown.currentText() == "Number of Chunks"):
            y_value = self.chunk_num
        elif(self.y_dropdown.currentText() == "Fitting Polynomial Order"):
            y_value = self.chunk_num
        elif(self.y_dropdown.currentText() == "Overlapping Between Chunks"):
            y_value = self.chunk_num
        
        x_value = range(1,x_value+1)
        y_value = range(1,y_value+1)

        a = np.random.random((x_value, y_value))
        plt.imshow(a, cmap='hot', interpolation='nearest')
        plt.show()  
        


    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
