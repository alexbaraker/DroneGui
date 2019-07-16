#######################################################################################################################################
#   By: SupremeDrones Team; Alex Baraker, Dean, Kelsey, Hammad
#   Date: 3/06/2019
#   Info: Class for converting OpenCV image type to QT image type
#######################################################################################################################################

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import urllib.request
import cv2
import numpy as np

from network.address import IP_ADDR


class OpenCvImageWidget(QLabel, QThread):

    #update_sig = pyqtSignal(np.ndarray, list)
    update_sig = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        
        self.cv_img  = []
        self.pixmap  = QPixmap()

        #self.update_sig.connect(self.update_image)
        

    def refresh_image(self, image):
        cv_image = cv2.imdecode(image, -1)
        #self.update_sig.emit(cv_image, [ (None, None) ])
        self.update_sig.emit(cv_image)


    def update_image(self, cv_image, centroids=[]):
        height, width, colors = cv_image.shape
        bytesPerLine = 3*width

        qt_image = QImage(cv_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qt_image = qt_image.rgbSwapped()

        painter  = QPainter()

        if len(centroids) > 0:
            painter.begin(qt_image)
            painter.setPen(QPen(Qt.red))
            painter.setFont(QFont('Arial', 12, QFont.Bold))

            xpos, ypos = centroids[0]
            painter.drawText(qt_image.rect(), Qt.AlignLeft, '(' + str(xpos) + ', ' + str(ypos) + ')')
            
            painter.end()

        pixmap = QPixmap.fromImage(qt_image)
        self.setPixmap(pixmap)

    
    def __open_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters([ 'jpg files (*.jpg)', 'png files (*.png)'  ])
        file_dialog.selectNameFilter('jpg files (*.jpg)')
        
        if file_dialog.exec_():
            return str(file_dialog.selectedFiles()[0])