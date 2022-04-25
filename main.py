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



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('task4.ui', self)
        self.time = []
        self.magnitude = []
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
        time_array = np.array(self.time)
        magnitude_array = np.array(self.magnitude)
        chunk_num = self.num_chunks_input.value()

         # ERROR MESSAGE popup   
        if chunk_num > 20:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error!")
            msg.setInformativeText('The maximum number of chunks is 20')
            msg.setWindowTitle("Error")
            msg.exec_()
            chunk_num = 20
            
        # split the arrays into chunks
        chunked_time = np.array_split(time_array, chunk_num)
        chunked_mag = np.array_split(magnitude_array, chunk_num)

       # plotting the chunks with different colors di hatb2a function tanya aslun interpolation bas da for testing
        colors = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255)]
        self.plot_widget.clear() # clearing hear not in plotting function because we only want to clear when opening a new file
        self.plotting() 
        for i in range (0, chunk_num + 1): # (initial, final but not included)
            curvePen = pg.mkPen(color=colors[i], style=QtCore.Qt.DashLine)
            self.plot_widget.plot(chunked_time[i], chunked_mag[i], pen = curvePen)
    
        #------------------in case it is needed-----------------------
        # # Convert chunked arrays into lists
        # chunked_list = [list(array) for array in chunked_mag]
        # #print(chunked_list)
        #-------------------------------------------------------------
    


    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
