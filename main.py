from pickle import GLOBAL
from ssl import ALERT_DESCRIPTION_NO_RENEGOTIATION
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSlider, QLCDNumber
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import numpy 
import pandas as pd
import pathlib
from PyQt5.QtWidgets import QMessageBox
from sympy import degree
import more_itertools as mit
from sympy import S, symbols, printing 
from PyQt5.QtGui import QIcon, QPixmap
from io import BytesIO
import matplotlib.pyplot as plt


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('task4.ui', self)
        self.time = []
        self.magnitude = []
        #initially without ny changes to the spinboxes
        self.chunk_num = 1
        self.overlap = 0
        self.chunk_size = len(self.magnitude)
        self.action_open.triggered.connect(self.open) 
        self.fit_button.clicked.connect(self.poly_interpolate) 
        self.predict_button.clicked.connect(self.extrapolation) 
        self.degree_slider.valueChanged.connect(self.equation) 
        self.percentage_display_2= self.findChild(QLCDNumber, "percentage_display_2")
        self.degree_slider.valueChanged.connect(lambda: self.percentage_display_2.display(self.degree_slider.value()))
        self.percentage_slider.valueChanged.connect(self.equation) 
        self.percentage_display= self.findChild(QLCDNumber, "percentage_display")
        self.percentage_slider.valueChanged.connect(lambda: self.percentage_display.display(self.percentage_slider.value()))
        self.time_chunks = []
        self.mag_chunks = []

        
        
        # else:
        #     msg = QMessageBox()
        #     msg.setIcon(QMessageBox.Critical)
        #     msg.setText("Error!")
        #     msg.setInformativeText('You did not choose an interpolation type')
        #     msg.setWindowTitle("Error")
        #     msg.exec_()


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
        # time = np.linspace(0,len(self.magnitude),len(self.magnitude))
        self.plot_widget.clear() # clearing hear not in plotting function because we only want to clear when opening a new file
        self.plot_widget.plot(self.magnitude)   

        if self.poly_button.isChecked():
            print(1)

        if self.cubic_button.isChecked(): 
            print(2)
 


    # def plotting(self):
           
    #    self.plot_widget.plot(self.time, self.magnitude)

    
    def render_latex(self,formula, fontsize=12, dpi=300, format_='svg'):
        """Renders LaTeX formula into image.
        """
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, u'${}$'.format(formula), color='white',fontsize=fontsize)
        buffer_ = BytesIO()
        fig.savefig(buffer_, dpi=dpi, transparent=True, format=format_, bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)
        return buffer_.getvalue()

    def equation(self):
        global degree
        degree = self.degree_slider.value()
        p = np.polyfit(self.time, self.magnitude, degree)
        xSymbols = symbols("x")
        poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1]))
        eq_latex = printing.latex(poly)     
        image_bytes = self.render_latex(eq_latex, fontsize=7, dpi=200, format_='png')
        qp = QPixmap()
        qp.loadFromData(image_bytes)
        self.equation_label.setPixmap(qp)
        

    
    def split_chunks(self):
        # converting to arrays if needed
        self.time_array = np.array(self.time)
        self.magnitude_array = np.array(self.magnitude)
        self.chunk_num = self.num_chunks_input.value()
        self.chunk_size = int(len(self.magnitude) / self.chunk_num)
        overlap_size = int((self.overlap_input.value() / 100) * self.chunk_size)
        self.degree= self.degree_slider.value()
        self.overlap=int(self.overlap_input.value())
        self.n=int((len(self.time_array))/self.chunk_num)
    
    def poly_interpolate(self):


        self.split_chunks()
        self.curvePen = pg.mkPen(color=(255, 0, 0), style=QtCore.Qt.DashLine)
        self.time_array = np.array(self.time)
        self.magnitude_array = np.array(self.magnitude)
        if(self.overlap>=0 and self.overlap<=25):
            self.overlapsizee=int((self.overlap/100)*((len(self.time_array))/self.chunk_num))
            self.time_chunks = list(mit.windowed(self.time_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-self.overlapsizee))
            self.mag_chunks = list(mit.windowed(self.magnitude_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-self.overlapsizee))
        
        self.plot_widget.clear()
        self.plot_widget.plot(self.time, self.magnitude)  

        for i in range(self.chunk_num):
            
            self.Interpolation = np.poly1d(np.polyfit(self.time_chunks[i], self.mag_chunks[i], self.degree))
            self.plot_widget.plot(self.time_chunks[i], self.Interpolation(self.time_chunks[i]), pen=self.curvePen)    #self.time_chunks[i], 
            #print(self.Interpolation(self.time_chunks[i]))
        

    def extrapolation(self):
        percent_data = self.percentage_slider.value()
        percent_predict = 100 - percent_data
        # cut the list into a certain percentage of data according to the slider
        # split_time = self.time[:int(len(self.time) * percent_data / 100)]
        # split_magnitude = self.magnitude[:int(len(self.magnitude) * percent_data / 100)]
        for i in range(self.chunk_num):
            split_time = self.time_chunks[i][:int(len(self.time_chunks[i]) * percent_predict / 100)]
            split_magnitude = self.mag_chunks[i][:int(len(self.mag_chunks[i]) * percent_predict / 100)]
        # convert lists to arrays
        arr_time = np.array(split_time) 
        arr_magnitude = np.array(split_magnitude)
        #prediction array
        coeff = np.polyfit(split_time, split_magnitude, degree)
        prediction = np.polyval(coeff, split_time)
        arr_predict = np.array(prediction)
        # append both
        mag_predict = np.append(arr_magnitude, arr_predict)
        self.plot_widget.clear()
        self.plot_widget.plot(self.magnitude)
        
        mag_arr = np.array(split_magnitude)
        time_inter = np.linspace(0,int(len(self.magnitude)* percent_data / 100), len(mag_arr))
        self.fitted=np.poly1d(np.polyfit(time_inter,mag_arr,degree))
        self.interrpolation = self.fitted(time_inter)
        self.curvePen = pg.mkPen(color=(255, 255, 0), style=QtCore.Qt.DashLine)
        # print(len(time_inter))
        # print(len(mag_arr))

        self.plot_widget.plot(time_inter, self.interrpolation,pen=self.curvePen )
     
        time_arr = np.array(self.time)
        # prediction time - blue
        time_pre = np.linspace(int(len(self.magnitude)* percent_data / 100),len(self.magnitude), int(len(self.magnitude)* percent_predict / 100))
        # interpolation time - red
        self.curPen = pg.mkPen(color=(0, 0, 255), style=QtCore.Qt.DashLine)
        self.plot_widget.plot(time_pre, arr_predict, pen = self.curPen) # self.time, 
        
    


    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
