#######################################################################################################################################
#   By: SupremeDrones Team; Alex Baraker, Dean, Kelsey, Hammad
#   Date: 3/06/2019
#   Info: Gui runnable for colored ball detection
#######################################################################################################################################

import sys
import cv2
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from misc.callback import callback
from gui.calibration import *
from gui.image_viewer import ImageViewerWidget
from gui.metrics_display import MetricsDisplay
from gui.image_processing import *


# Main window class that holds everything
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.setWindowTitle("Ball Tracker")
        self.settings = QSettings("RIT", "Supreme Drone Team")  
    
        self.h_layout     = QtGui.QHBoxLayout()
        self.calibration  = Calibration(self)
        self.image_viewer = ImageViewerWidget(self)
        self.metrics_display = MetricsDisplay(self)

        # load in the docks
        self.setup_docks()

        # setup collabration connections
        self.setup_calibration_connections()
            
        # load in the style sheet
        styleFile ="gui/styleSheet.txt"
        with open(styleFile, "r") as fh:
            self.setStyleSheet(fh.read())
          
        # restore dock locations
        if self.settings.value("state"):
            try:
                self.restoreGeometry(self.settings.value("geometry").toByteArray())        
                self.restoreState(self.settings.value("state").toByteArray())
                self.move(self.settings.value("windowPos", QVariant(QPoint(50, 50))).toPoint())
                self.resize(self.settings.value("windowSize", QVariant(QSize(555, 550))).toSize())
                self.setWindowState(Qt.WindowState(self.settings.value("windowState").toInt()[0]))
            except: pass
        

    def setup_docks(self):
        self.image_viewer_dock = QDockWidget(self)
        self.image_viewer_dock.setWidget(self.image_viewer)
        self.image_viewer_dock.setWindowTitle("Image viewer")
        self.image_viewer_dock.setObjectName("Image viewer")
        self.image_viewer_dock.setContentsMargins(0, 0, 0, 0)
        self.image_viewer_dock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.addDockWidget(Qt.TopDockWidgetArea, self.image_viewer_dock)
        
        self.calibrationDock = QDockWidget(self)
        self.calibrationDock.setWidget(self.calibration)
        self.calibrationDock.setWindowTitle("Calibration")
        self.calibrationDock.setObjectName("Calibration")
        self.calibrationDock.setContentsMargins(0, 0, 0, 0)
        self.calibrationDock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.addDockWidget(Qt.TopDockWidgetArea, self.calibrationDock)

        self.metrics_dock = QDockWidget(self)
        self.metrics_dock.setWidget(self.metrics_display)
        self.calibrationDock.setWindowTitle("Metrics")
        self.calibrationDock.setObjectName("Metrics")
        self.calibrationDock.setContentsMargins(0, 0, 0, 0)
        self.calibrationDock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.addDockWidget(Qt.TopDockWidgetArea, self.metrics_dock)

        DOCKOPTIONS = QMainWindow.AllowTabbedDocks
        DOCKOPTIONS = DOCKOPTIONS|QMainWindow.AllowNestedDocks
        DOCKOPTIONS = DOCKOPTIONS|QMainWindow.AnimatedDocks
        self.setDockOptions(DOCKOPTIONS)
        self.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.East)


    def setup_calibration_connections(self):
        self.image_viewer.opencv_image.update_sig.connect(self.apply_image_changes)


    #def apply_image_changes(self, detection_type, detection_settings=None):
    def apply_image_changes(self, cv_image):
        if len(cv_image) == 0: return
        center_x, center_y, radius = image_processing.detect_circle(cv_image)

        # Visualize detection and send it off for cv -> qt image conversion
        if center_x is not None and center_y is not None:
            detection_image = cv2.circle(cv_image.copy(), (center_x, center_y), radius, (0, 0, 255), 3)
            self.image_viewer.opencv_image.update_image(detection_image, [ (center_x, center_y) ])
            self.send_detection_to_drone(center_x, center_y)
        else:
            self.image_viewer.opencv_image.update_image(cv_image.copy(), [ (center_x, center_y) ])
            self.send_detection_to_drone(240, 376)
                

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())        
        self.settings.setValue('state', self.saveState())   
        self.settings.setValue("windowState", QVariant(self.windowState()))
        self.settings.setValue("windowSize", QVariant(self.size()))
        self.settings.setValue("windowPos", QVariant(self.pos()))
        self.settings.sync()
        QMainWindow.closeEvent(self, event)


    @callback
    def send_detection_to_drone(self, center_x, center_y):
        self.send_detection_to_drone.emit(center_x, center_y)