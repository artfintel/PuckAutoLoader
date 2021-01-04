# import system module
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

# import Opencv module
import cv2

from PuckAutoLoader.ui.mainWinodwMgr import *
from PuckAutoLoader.device.video import Video
from PuckAutoLoader.db.ContainerDAO import ContainersDAO

from PuckAutoLoader.utils.config_parser import ConfigParser

class MainWindow(QMainWindow):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_MainWindow()

        self.image = None
        self.video = Video()
        self.video.set_mgrmode()

        self.puck_count = 0
        self.container_count = 0
        self.count = 0
        self.load = 0
        self.edit = False
        self.time_check = time.time()
        self.current_time = time.time()
        self.db_refresh_timer = time.time()

        self.config = ConfigParser('utils/config.ini').get_config()
        self.url = self.config['CAMERA']['Url']
        self.cap = cv2.VideoCapture(self.url)

        self.containersDao = ContainersDAO()

        self.ui.setupUi(self)
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.play_btn.clicked.connect(self.controlTimer)
        self.timer.start(1)

        self.ui.info_btn.clicked.connect(self.show_info)
        self.ui.save_btn.clicked.connect(self.save)
        self.ui.reset_btn.clicked.connect(self.reset)
        self.ui.barcode_text.setFocus()

        self.ui.new_puck_position_label.setFont(QtGui.QFont("SansSerif", 40, QtGui.QFont.Bold))
        self.ui.barcode_text.setFont(QtGui.QFont("SansSerif", 30, QtGui.QFont.Bold))
        self.ui.barcode_text.textChanged.connect(self.barcode_input)

        self.ui.notice_label.setAlignment(Qt.AlignCenter)
        self.ui.notice_label.setFont(QtGui.QFont("SansSerif", 20, QtGui.QFont.Bold))

        self.ui.set_backgroun_btn.clicked.connect(self.set_background)

    def barcode_input(self):
        if not self.edit and len(self.ui.barcode_text.toPlainText()) != 0:
            if len(self.ui.barcode_text.toPlainText()) > 4:
                self.time_check = time.time()
                self.edit = True

    # view camera
    def viewCam(self):
        # read image in BGR format
        self.ret, self.image = self.cap.read()

        self.puck_detection(self.image)
        self.find_new_puck(self.image)
        self.image = cv2.resize(self.image, (self.image.shape[1] // 3, self.image.shape[0] // 3))

        # convert image to RGB format
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = self.image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(self.image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.video_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(self.url)
            # start timer
            self.timer.start(1)
            # update control_bt text
            self.ui.play_btn.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.play_btn.setText("Start")

    def set_background(self):
        ret, image = self.cap.read()
        self.video.set_background(image)

    def puck_detection(self, img):
        self.image = self.video.puck_detection(img)

    def find_new_puck(self, img):
        # Database Refresh time 1 hour
        if (time.time() - self.db_refresh_timer) > 3600:
            self.db_refresh_timer = time.time()
            self.containersDao.reconnect()

        container_list = self.containersDao.get_container_list()

        self.diff_puck = []
        for i in range(len(self.video.dewar.puckDetection)):
            if self.video.dewar.puckDetection[i] == 1:
                self.diff_puck.append(self.video.dewar.puckPosition[i])

        self.puck_count = len(self.diff_puck)
        self.container_count = len(container_list)

        find_position = 0

        if self.puck_count > self.container_count:
            for container in container_list:
                for diff in self.diff_puck:
                    if diff == container.get_location_id():
                        self.diff_puck.remove(diff)

            find_position = self.video.dewar.puckPosition.index(self.diff_puck[0])

            self.ui.new_puck_position_label.setStyleSheet("Color:blue")
            self.ui.new_puck_position_label.setFont(QtGui.QFont("SansSerif", 40, QtGui.QFont.Bold))
            self.ui.new_puck_position_label.setText(self.video.dewar.puckPositionName[find_position])
            self.load = 1

        elif self.puck_count < self.container_count:
            for diff in self.diff_puck:
                for container in container_list:
                    if diff == container.get_location_id():
                        container_list.remove(container)

            unloaded_puck = ""
            self.ui.new_puck_position_label.setStyleSheet("Color:red")
            count = 0
            self.diff_puck = []

            for container in container_list:
                find_position = self.video.dewar.puckPosition.index(container.get_location_id())
                self.diff_puck.append(container.get_location_id())
                if count == 3:
                    unloaded_puck = unloaded_puck + "\n"
                unloaded_puck = unloaded_puck + self.video.dewar.puckPositionName[find_position] + " "
                count += 1

            self.ui.new_puck_position_label.setFont(QtGui.QFont("SansSerif", 40-(len(container_list)*3), QtGui.QFont.Bold))
            self.ui.new_puck_position_label.setText(unloaded_puck)
            self.load = -1

        else:
            self.ui.new_puck_position_label.setStyleSheet("Color:black")
            self.ui.new_puck_position_label.setText("None")
            self.load = 0

        if self.edit:
            self.current_time = time.time()
            if (self.current_time - self.time_check) > 1:
                self.time_check = time.time()
                self.edit = False
                self.save()

    def show_info(self):
        self.video.set_info()
        self.ui.barcode_text.setFocus()

    def reset(self):
        self.ui.notice_label.setText("Reset")
        self.edit = False
        self.containersDao.reconnect()
        self.ui.barcode_text.clear()
        self.ui.barcode_text.setFocus()

    def save(self):
        if self.load == 1:
            if self.containersDao.check_empty_location(self.diff_puck[0]):
                if self.containersDao.validate_check_puck(self.ui.barcode_text.toPlainText()):
                    if self.containersDao.validate_check_position(self.ui.barcode_text.toPlainText()):
                        self.containersDao.load_container(self.ui.barcode_text.toPlainText(), self.diff_puck[0])
                        self.ui.notice_label.setText("The puck is loaded.")
                    else:
                        self.ui.notice_label.setText("This puck is already loaded.")
                else:
                    self.ui.notice_label.setText("This puck is invalid")
            else:
                self.ui.notice_label.setText("Wrong location")

            self.time_check = time.time()
            self.edit = False

        elif self.load == -1:
            for diff in self.diff_puck:
                self.ui.notice_label.setText("Pucks unloaded.")
                self.containersDao.unload_container_loc(diff)

            self.time_check = time.time()
            self.edit = False

        else:
            self.time_check = time.time()
            self.edit = False
            self.ui.notice_label.setText("no change")

        self.ui.barcode_text.setText("")
        self.ui.barcode_text.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
    sys.exit(app.exec_())
