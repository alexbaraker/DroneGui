import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from main.gui import MainWindow
from main.net_client import NetClient


def main():
    net_client = NetClient()
    try:
        app = QApplication(sys.argv)
        main_window = MainWindow()

        NetClient.pwm1_callback.connect(main_window.metrics_display.update_motor_1_status)
        NetClient.pwm2_callback.connect(main_window.metrics_display.update_motor_2_status)
        NetClient.pwm3_callback.connect(main_window.metrics_display.update_motor_3_status)
        NetClient.pwm4_callback.connect(main_window.metrics_display.update_motor_4_status)

        NetClient.cam_callback.connect(main_window.image_viewer.opencv_image.refresh_image)

        main_window.calibration.kill_switch_button_clicked.connect(net_client.send_killsig_to_drone)
        main_window.send_detection_to_drone.connect(net_client.send_detection_to_drone)

        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
    finally:
        net_client.kill()


if __name__ == '__main__':
    main()