from math import ceil, fabs
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
from scipy.interpolate import make_interp_spline
from sklearn.metrics import mean_absolute_error
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import ctypes


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
        self.interpolated=[]
        self.action_open.triggered.connect(self.open) 
        self.interpolation_type.activated.connect(self.choose_type)
        self.start_button.clicked.connect(self.create_error_map)
        # self.fit_button.clicked.connect(self.poly_interpolate) 
        # self.spline_button.clicked.connect(self.spline) 
        # self.cubic_button.clicked.connect(self.cubic)
        # self.interpolation_type.setCurrentIndex(0)
        self.predict_button.clicked.connect(self.extrapolation) 
        self.degree_slider.valueChanged.connect(self.equation) 

        self.degree_display= self.findChild(QLCDNumber, "degree_display")
        self.degree_slider.valueChanged.connect(lambda: self.degree_display.display(self.degree_slider.value()))
        self.percentage_slider.valueChanged.connect(self.equation) 
        self.percentage_display= self.findChild(QLCDNumber, "percentage_display")
        self.percentage_slider.valueChanged.connect(lambda: self.percentage_display.display(self.percentage_slider.value()))
        self.time_chunks = []
        self.mag_chunks = []
        self.extrapolation_check = 0

        


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
        self.plotting()
         


    def plotting(self):
       self.plot_widget.clear()  
       self.plot_widget.plot(self.time, self.magnitude)
       

    
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
        if int(self.interpolation_type.currentIndex()) == 1: #cubic interpolation
            degree = 3
        else:
            degree = self.degree_slider.value()

        p = np.polyfit(self.time, self.magnitude, degree)
        xSymbols = symbols("x")
        poly = sum(S("{:6.2f}".format(v))*xSymbols**i for i, v in enumerate(p[::1]))
        eq_latex = printing.latex(poly)     
        image_bytes = self.render_latex(eq_latex, fontsize=7, dpi=200, format_='png')
        qp = QPixmap()
        qp.loadFromData(image_bytes)
        self.equation_label.setPixmap(qp)
    

    def spline(self):
        percent_data = self.percentage_slider.value()
        deg= self.degree_slider.value()
        self.time_array = np.array(self.time)
        self.magnitude_array = np.array(self.magnitude)

        if deg % 2 == 0 and deg != 2 and int(self.interpolation_type.currentIndex()) == 2:
            self.plotting()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error!")
            msg.setInformativeText('Spline degree must be odd or 2! \n It has been reset to (degree - 1)')
            msg.setWindowTitle("Error")
            msg.exec_()
        if deg % 2 == 0 and deg != 2:
            deg -= 1
        
        X_=np.linspace(self.time_array.min(), self.time_array.max(), 500)

        if self.extrapolation_check ==2:
            data_time = X_[0:int(len(X_) * percent_data / 100)]
        else:
            data_time = X_
     
        Y_ = make_interp_spline(self.time_array , self.magnitude_array, k= deg)(data_time)
        self.plotting()  
        self.extrapolation_check = 0
        self.plot_widget.plot(data_time, Y_, pen='b')
       


    def cubic(self):
        percent_data = self.percentage_slider.value()
        # self.degree= self.degree_slider.value()
        self.time_array = np.array(self.time)
        self.magnitude_array = np.array(self.magnitude)

        # Plotting the Graph
        X_= np.linspace(self.time_array.min(), self.time_array.max(), 500)

        if self.extrapolation_check ==1:
            data_time = X_[0:int(len(X_) * percent_data / 100)]
        else:
            data_time = X_
     
        Y_ = make_interp_spline(self.time_array , self.magnitude_array)(data_time)
        self.equation()
        self.plotting()  
        self.extrapolation_check = 0
        self.plot_widget.plot(data_time, Y_, pen='y')
    
     
        
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
        
        self.plotting() 
        

        for i in range(self.chunk_num):
            
            self.Interpolation = np.poly1d(np.polyfit(self.time_chunks[i], self.mag_chunks[i], self.degree))
            self.interpolated.append(self.Interpolation) # ???
            self.plot_widget.plot(self.time_chunks[i], self.Interpolation(self.time_chunks[i]), pen=self.curvePen)   
            
        return self.interpolated   # ???
    
    def choose_type(self):
        if int(self.interpolation_type.currentIndex()) == 0:
            self.fit_button.clicked.connect(self.poly_interpolate) 
            self.degree_slider.setVisible(True)
            self.degree_display.setVisible(True) 
            self.degree_label.setVisible(True)
            self.show_widgets()
            
          
        elif int(self.interpolation_type.currentIndex()) == 1:
            self.fit_button.clicked.connect(self.cubic) 
            self.degree_slider.setVisible(False)
            self.degree_display.setVisible(False) 
            self.degree_label.setVisible(False)
            self.hide_widgets()
           

        elif int(self.interpolation_type.currentIndex()) == 2:
            self.fit_button.clicked.connect(self.spline) 
            self.degree_slider.setVisible(True)
            self.degree_display.setVisible(True) 
            self.degree_label.setVisible(True)
            self.hide_widgets()
            

    def hide_widgets(self):
        
            self.num_chunks_label.setVisible(False)
            self.num_chunks_input.setVisible(False)
            self.overlap_label.setVisible(False)
            self.overlap_input.setVisible(False)
            self.error_map.setVisible(False)
            self.start_button.setVisible(False)
            self.progress_bar.setVisible(False)
            self.error_label.setVisible(False)
            self.x_axis_label.setVisible(False)
            self.y_axis_label.setVisible(False)
            self.x_dropdown.setVisible(False)
            self.y_dropdown.setVisible(False) 

    def show_widgets(self):
            self.num_chunks_label.setVisible(True)
            self.num_chunks_input.setVisible(True)
            self.overlap_label.setVisible(True)
            self.overlap_input.setVisible(True)
            self.error_map.setVisible(True)
            self.start_button.setVisible(True)
            self.progress_bar.setVisible(True)
            self.error_label.setVisible(True)
            self.x_axis_label.setVisible(True)
            self.y_axis_label.setVisible(True)
            self.x_dropdown.setVisible(True)
            self.y_dropdown.setVisible(True) 
            

    def extrapolation(self):
        percent_data = self.percentage_slider.value()
        #percent_predict = 100 - percent_data
        
        split_time = self.time[0:int(len(self.time) * percent_data / 100)]
        time_predict =  self.time[int(len(self.time) * percent_data / 100):(len(self.time))]
        split_magnitude = self.magnitude[0:int(len(self.magnitude) * percent_data / 100)]

        coeff = np.polyfit(split_time, split_magnitude, degree)
        prediction = np.polyval(coeff, time_predict)
        arr_predict = np.array(prediction)
       
        self.plot_widget.setYRange(min(self.magnitude), max(self.magnitude))
        self.plotting()

        self.curvePen = pg.mkPen(color=(255, 0, 0), style=QtCore.Qt.DashLine)
        self.curPen = pg.mkPen(color=(255, 0, 255), style=QtCore.Qt.DashLine)

        if int(self.interpolation_type.currentIndex()) == 0:

            mag_arr = np.array(split_magnitude)
            self.fitted=np.poly1d(np.polyfit(split_time,mag_arr,degree))
            self.interrpolation = self.fitted(split_time)
            self.plot_widget.plot(split_time, self.interrpolation,pen=self.curvePen)
        elif int(self.interpolation_type.currentIndex()) == 1:
            self.extrapolation_check = 1
            self.cubic()
        elif int(self.interpolation_type.currentIndex()) == 2:
            self.extrapolation_check = 2
            self.spline() 
        self.plot_widget.plot(time_predict, arr_predict, pen = self.curPen)          
        
    
    # def computeError(self,y_interpolated,y_original):
    #     # Compute the error
    #     error = np.average(abs((y_interpolated - y_original)/y_original))
    #     print(error)
    #     return error

    def create_error_map(self):
        self.poly_interpolate()
        # self.time_chunks = list(mit.windowed(self.time_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-self.overlapsizee))
        # self.mag_chunks = list(mit.windowed(self.magnitude_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-self.overlapsizee))
        x_axis = self.x_dropdown.currentText()
        y_axis = self.y_dropdown.currentText()

        if(x_axis==y_axis):
            
            ctypes.windll.user32.MessageBoxW(0, "Please change one of the axes", "ERROR", 16)

        if not (x_axis==y_axis):

            if(x_axis == "Number of Chunks"):
                value_x = self.chunk_num
            elif(x_axis == "Polynomial Order"):
                value_x = self.degree
            elif(x_axis == "Overlap"):
                value_x = self.overlap
                
            
            if(y_axis == "Number of Chunks"):
                value_y = self.chunk_num
            elif(y_axis == "Polynomial Order"):
                value_y = self.degree
            elif(y_axis == "Overlap"):
                value_y = self.overlap
            
            x_range =range(1, value_x+1 ) 
            y_range =range(1, value_y+1 )

            errors=[]

            

            for i in y_range:
                currentChunk    = self.chunk_num
                currentDegree   = self.degree
                currentOverlap  = self.overlap
            
                if(y_axis == "Number of Chunks"):
                    currentChunk = i - 1
                elif(y_axis == "Polynomial Order"):
                    currentDegree = i
                elif(y_axis == "Overlap"):
                    currentOverlap = i
                
                for j in x_range:
                    if(x_axis == "Number of Chunks"):
                        currentChunk = j - 1
                    elif(x_axis == "Polynomial Order"):
                        currentDegree = j
                    elif(x_axis == "Overlap"):
                        currentOverlap = j

                    if(currentOverlap>=0 and currentOverlap<=25):
                        tempOverlapsizee    = int((currentOverlap/100)*((len(self.time_array))/self.chunk_num))
                        tempTime_chunks     = list(mit.windowed(self.time_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-tempOverlapsizee))
                        tempMag_chunks      = list(mit.windowed(self.magnitude_array, n=int(len(self.time_array)/self.chunk_num), step=self.n-tempOverlapsizee))
                
                    degrees = np.poly1d(np.polyfit(tempTime_chunks[currentChunk], tempMag_chunks[currentChunk], currentDegree))
                    errors.append(mean_absolute_error(tempMag_chunks[currentChunk],degrees(tempTime_chunks[currentChunk])))

                    # to get errors by formula:
                    # calculate_error=((self.mag_chunks[j]-degrees(self.time_chunks[j])/self.mag_chunks[j])
                    # errors.append(calculate_error)

            rounded_error = round(np.average(errors)*100,2)
            errors_2d = np.reshape(errors, (value_y, value_x))

            self.error_map.canvas.axes.clear()        
            self.error_map.canvas.axes.tick_params(axis="x", colors="black")
            self.error_map.canvas.axes.tick_params(axis="y", colors="black")        
            self.error_map.canvas.axes.set_title("Percentage Error = " + str(rounded_error) + ' %', color='black', fontsize=15)
            
            edit_axes = make_axes_locatable(self.error_map.canvas.axes).append_axes("right", size="5%", pad="2%")
            edit_axes.tick_params(axis="x", colors="black")
            edit_axes.tick_params(axis="y", colors="black")
            
            data = self.error_map.canvas.axes.contourf(x_range,y_range,errors_2d)
            self.error_map.canvas.axes.figure.colorbar(data , cax=edit_axes)
            self.error_map.canvas.draw()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
