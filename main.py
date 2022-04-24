from pickle import GLOBAL
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QSlider
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pathlib




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('task4.ui', self)
        self.time = []
        self.magnitude = []
        self.action_open.triggered.connect(self.open)   
    
    def open(self):
        # open any csv file
        files_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open only CSV ', os.getenv('HOME'), "csv(*.csv)")
        path = files_name[0]
        pathlib.Path(path).suffix == ".csv"
        # read the data in the file
        data = pd.read_csv(path)
        # place the data in time and magnitude arrays
        self.time = data.values[:, 0]
        self.magnitude = data.values[:, 1]
        # plot the data
        self.plotting()      

    def plotting(self):
        self.plot_widget.plot(self.time, self.magnitude)
    
    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
