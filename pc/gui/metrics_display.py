#######################################################################################################################################
#   By: SupremeDrones Team; Alex Baraker, Dean, Kelsey, Hammad
#   Date: 4/24/2019
#   Info: Widget for displaying drone metrics
#######################################################################################################################################

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MetricsDisplay(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
    
        self.v_layout = QVBoxLayout()
        self.v_layout.setAlignment(Qt.AlignTop)
        
        self.top_view = QLabel()
        self.top_view.setPixmap(QPixmap('drone_top_view.png'))

        self.side_view = QLabel()
        self.top_view.setPixmap(QPixmap('drone_side_view.png'))

        self.motor_1      = QLabel('Motor 1: N/A')
        self.motor_2      = QLabel('Motor 2: N/A')
        self.motor_3      = QLabel('Motor 3: N/A')
        self.motor_4      = QLabel('Motor 4: N/A')
        self.acceleration = QLabel('Accel: N/A')

        #self.v_layout.addWidget(self.top_view)
        #self.v_layout.addWidget(self.side_view)

        self.v_layout.addWidget(self.motor_1)
        self.v_layout.addWidget(self.motor_2)
        self.v_layout.addWidget(self.motor_3)
        self.v_layout.addWidget(self.motor_4)

        self.setLayout(self.v_layout)

    # TODO: These should be connected to a client subscriber to drone server pushing metrics
    def update_motor_1_status(self, status='N/A'):
        self.motor_1.setText('Motor 1: ' + str(status))


    def update_motor_2_status(self, status='N/A'):
        self.motor_2.setText('Motor 2: ' + str(status))


    def update_motor_3_status(self, status='N/A'):
        self.motor_3.setText('Motor 3: ' + str(status))


    def update_motor_4_status(self, status='N/A'):
        self.motor_4.setText('Motor 4: ' + str(status))