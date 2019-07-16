#######################################################################################################################################
#   By: SupremeDrones Team; Alex Baraker, Dean, Kelsey, Hammad
#   Date: 3/06/2019
#   Info: Widget for displaying loaded image
#######################################################################################################################################

from threading import Thread
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from gui.opencv_image import OpenCvImageWidget


class ImageViewerWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
    
        self.v_layout       = QVBoxLayout()
        self.opencv_image   = OpenCvImageWidget(self)
        #self.load_image_btn = QPushButton("Load Image")

        #self.load_image_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.load_image_btn.clicked[bool].connect(self.load_file_button_clicked)

        self.v_layout.addWidget(self.opencv_image)
        #self.v_layout.addWidget(self.load_image_btn)

        self.setLayout(self.v_layout)

    #    self.thread = Thread(target=self.display_loop, args=())
    #    self.thread.daemon = True
    #    self.thread.start()
    
    
    #def load_file_button_clicked(self):
    #    self.opencv_image.open_cv_image()


    #def display_loop(self):
    #    while True:
    #        self.opencv_image.refresh_image()
    #        time.sleep(0.05)

        
    def strName_out(self):		
        self.opencv_image.strName()