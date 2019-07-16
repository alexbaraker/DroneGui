#######################################################################################################################################
#   By: SupremeDrones Team; Alex Baraker, Dean, Kelsey, Hammad
#   Date: 3/06/2019
#   Info: Widget for the callibration settings
#######################################################################################################################################

import sys
import ast
import numpy as np

from PyQt4 import QtGui, QtCore
from misc.callback import callback
from gui.image_processing import *
from gui.image_viewer import *
from gui.opencv_image import *



# Used for dynamic generation of sliders, and is needed because the QT function 
# doesn't have an extra parameter to pass the name of the slider.
# So this hack allows to inject a parameter into a function
def NameInsert(func):

    def Func(*args, **kwargs):
        return func(name=Func.name, *args, **kwargs)

    class FuncHelper():

        @staticmethod
        def set_name(name):
            Func.name = name
            return Func

    Func.set_name = FuncHelper.set_name
    Func.name = ''

    return Func


class Calibration(QtGui.QWidget):

    CUSTOM     = 0
    BLUE_BALL  = 1
    GREEN_BALL = 2

    def __init__(self, parent=None):
        super(Calibration, self).__init__(parent)
        
        # Holds the slider and edit generated widget
        self.settings      = {}
        self.label_titles  = {}
        self.sliders       = {}
        self.slider_edit   = {}
        self.slider_groups = {}

        self.custom = False  # Do manual set sliders affect detection?
        self.detect = None

        self.create_slider("dp", 1, 1, 254, 1, self.dp_edit_changed, self.dp_slider_changed)
        self.create_slider("minDist", 1, 1, 254, 1 , self.min_dist_edit_changed, self.mid_dist_slider_changed)
        self.create_slider("gradient", 1, 1, 254, 1, self.gradient_edit_changed, self.gradient_slider_changed)
        self.create_slider("accumulator", 1, 1, 254, 1, self.accumulator_edit_changed, self.accumulator_slider_changed)
        self.create_slider("minRadius", 1, 1, 254, 1, self.min_radius_edit_changed, self.min_radius_slider_changed)
        self.create_slider("maxRadius", 1, 1, 254, 1, self.max_radius_edit_changed, self.max_radius_slider_changed)
        
        self.load_file_button = QtGui.QPushButton("Load Calibration")
        self.load_file_button.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.load_file_button.clicked[bool].connect(self.load_file_button_clicked)
        
        self.save_file_button = QtGui.QPushButton("Save Calibration")
        self.save_file_button.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.save_file_button.clicked[bool].connect(self.save_file_button_clicked)
        
        self.green_button = QtGui.QPushButton("Green")
        self.green_button.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.green_button.clicked[bool].connect(self.green_button_clicked)
		
        self.blue_button = QtGui.QPushButton("Blue")
        self.blue_button.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.blue_button.clicked[bool].connect(self.blue_button_clicked)
		
        layout2 = QtGui.QHBoxLayout()		
        layout2.addWidget(self.load_file_button)
        layout2.addWidget(self.save_file_button)
        layout2.addWidget(self.green_button)
        layout2.addWidget(self.blue_button)
		
        self.kill_switch_button = QtGui.QPushButton("KILL SWITCH")
        self.kill_switch_button.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.kill_switch_button.clicked[bool].connect(self.kill_switch_button_clicked)
        self.kill_switch_button.setStyleSheet(
            "QPushButton"
            "{"
            "    background-color: #FF0000;"
            "}"
            "QPushButton:pressed"
            "{"
            "    background-color: #550000;"
            "}")

        layout = QtGui.QVBoxLayout()

        for slider_group in self.slider_groups.values():
            layout.addWidget(slider_group) 
        
        layout.addLayout(layout2)
        layout.addWidget(self.kill_switch_button)

        self.setLayout(layout)
        self.show()


    def create_slider(self, name, step, min_val, max_val, default_value, edit_changed_callback, slider_changed_callback):
        edit_changed_callback.set_name(name)
        slider_changed_callback.set_name(name)

        self.label_titles[name] = QtGui.QLabel(self)
        self.label_titles[name].setText(name)
        
        self.sliders[name] = QtGui.QSlider(QtCore.Qt.Horizontal, self, objectName=name)
        self.sliders[name].setSingleStep(step)
        self.sliders[name].setMinimum(min_val)
        self.sliders[name].setMaximum(max_val)
        self.sliders[name].valueChanged[int].connect(slider_changed_callback) 

        self.slider_edit[name] = QtGui.QLineEdit(self, objectName=name)
        self.slider_edit[name].returnPressed.connect(edit_changed_callback)

        self.slider_groups[name] = QtGui.QGroupBox()

        slider_layout = QtGui.QHBoxLayout()
        slider_layout.addWidget(self.label_titles[name])
        slider_layout.addWidget(self.slider_edit[name])

        slider_layout_vertical = QtGui.QVBoxLayout()
        slider_layout_vertical.addLayout(slider_layout)
        slider_layout_vertical.addWidget(self.sliders[name])

        self.slider_groups[name].setLayout(slider_layout_vertical)
        #self.sliders[name].setValue(default_value)

    
###############################################################################
# link the edit boxes to the sliders
###############################################################################

    @NameInsert
    def dp_edit_changed(self, name):
        self.settings[name] = int(self.slider_edit[name].text())
        self.sliders[name].setValue(self.settings[name])


    @NameInsert
    def min_dist_edit_changed(self, name):
        self.settings[name] = int(self.slider_edit[name].text())
        self.sliders[name].setValue(self.settings[name])


    @NameInsert
    def gradient_edit_changed(self, name):
        self.settings[name] = int(self.slider_edit[name].text())
        self.sliders[name].setValue(self.settings[name])


    @NameInsert
    def accumulator_edit_changed(self, name):
        self.settings[name] = int(self.slider_edit[name].text())
        self.sliders[name].setValue(self.settings[name])

    
    @NameInsert
    def min_radius_edit_changed(self, name):
        self.settings[name] = int(self.slider_edit[name].text())
        self.sliders[name].setValue(self.settings[name])

    @NameInsert
    def max_radius_edit_changed(self, name):
        self.settings[name] = int(self.slider_edit[name].text())
        self.sliders[name].setValue(self.settings[name])


    @NameInsert
    def dp_slider_changed(self, value, name):
        self.settings[name] = int(value)
        self.slider_edit[name].setText(str(value))
        self.apply_slider_settings()


    @NameInsert
    def mid_dist_slider_changed(self, value, name):
        self.settings[name] = int(value)
        self.slider_edit[name].setText(str(value))
        self.apply_slider_settings()


    @NameInsert
    def gradient_slider_changed(self, value, name):
        self.settings[name] = int(value)
        self.slider_edit[name].setText(str(value))
        self.apply_slider_settings()


    @NameInsert
    def accumulator_slider_changed(self, value, name):
        self.settings[name] = int(value)
        self.slider_edit[name].setText(str(value))
        self.apply_slider_settings()
    

    @NameInsert
    def min_radius_slider_changed(self, value, name):
        self.settings[name] = int(value)
        self.slider_edit[name].setText(str(value))
        self.apply_slider_settings()


    @NameInsert
    def max_radius_slider_changed(self, value, name):
        self.settings[name] = int(value)
        self.slider_edit[name].setText(str(value))
        self.apply_slider_settings()


###############################################################################
# save and load and color calibration files
###############################################################################

    def load_file_button_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(None, "Enter Filename.", ".txt", "(*.txt)")
        if not fileName: return

        with open(fileName) as f:
            self.settings = ast.literal_eval(f.read())

        for name, value in self.settings.items():
            self.sliders[name].setValue(value)
   

    def save_file_button_clicked(self):
        fileName = QtGui.QFileDialog.getSaveFileName(None, "Enter Filename",".txt","(*.txt)") 
        if fileName == "": return
    
        with open(fileName, "w") as f:
            f.write(str(self.settings))


    @callback
    def kill_switch_button_clicked(self, _):
        self.kill_switch_button_clicked.emit()



###############################################################################
# Apply blue/green and custom settings detection
###############################################################################

    @callback
    def apply_slider_settings(self):
        slider_vals = [ slider.value() for slider in list(self.sliders.values()) ]
        self.apply_slider_settings.emit(Calibration.CUSTOM, slider_vals)


    @callback
    def blue_button_clicked(self, _):
        self.blue_button_clicked.emit(Calibration.BLUE_BALL)


    @callback
    def green_button_clicked(self, _):
        self.green_button_clicked.emit(Calibration.GREEN_BALL)