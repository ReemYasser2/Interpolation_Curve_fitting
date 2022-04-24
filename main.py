from pickle import GLOBAL
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QSlider
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('task4.ui', self)
        self.action_open.triggered.connect(self.open)
    
    def open(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)')



   
    
    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())