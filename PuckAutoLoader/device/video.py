import cv2 as cv
from PuckAutoLoader.device.dewar import Dewar

class Video:

    def __init__(self):
        self.zero = 0
        self.detection_box = 35
        self.result = [0 for i in range(29)]
        self.queue = []
        self.info_flag = False
        self.mgr_flag = False

        self.dewar = Dewar()

    def puck_detection(self, img):
        img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

        average = []
        for coord in self.dewar.puckCoords:
            sum = 0
            avg = 0
            cnt = 0

            for i in range(-self.detection_box, self.detection_box):
                for j in range(-self.detection_box, self.detection_box):
                    sum += img_gray[coord[1] + i, coord[0] + j]
                    cnt += 1

            if self.mgr_flag:
                cv.rectangle(img, (coord[0] - self.detection_box, coord[1] - self.detection_box),
                              (coord[0] + self.detection_box, coord[1] + self.detection_box), (0, 255, 0), 3)
            avg = sum // cnt
            average.append(avg)

        if len(self.queue) <= 10:
            self.queue.append(average)

        for i in range(len(self.result)):
            for q in self.queue:
                self.result[i] += q[i]
            self.result[i] = self.result[i] // len(self.queue)

        for i in range(len(self.dewar.puckBackground)):
            if self.dewar.puckBackground[i] - self.result[i] >= self.zero:
                cv.circle(img, (self.dewar.puckCoords[i][0], self.dewar.puckCoords[i][1]), 75, (255, 0, 0), 5)
                self.dewar.puckDetection[i] = 1
                if self.info_flag == True:
                    cv.putText(img, str(self.dewar.puckBackground[i] - self.result[i]),
                               (self.dewar.puckCoords[i][0] - 25, self.dewar.puckCoords[i][1] + 40),
                               cv.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
            else:
                cv.circle(img, (self.dewar.puckCoords[i][0], self.dewar.puckCoords[i][1]), 75, (0, 0, 255), 5)
                self.dewar.puckDetection[i] = 0
                if self.info_flag == True:
                    cv.putText(img, str(self.dewar.puckBackground[i] - self.result[i]),
                               (self.dewar.puckCoords[i][0] - 25, self.dewar.puckCoords[i][1] + 40),
                               cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

            cv.putText(img, self.dewar.puckPositionName[i],
                       (self.dewar.puckCoords[i][0] - 45, self.dewar.puckCoords[i][1] + 10),
                       cv.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 2)

        if len(self.queue) >= 10:
            self.queue.pop(0)

        return img

    # set infomation
    def set_info(self):
        self.info_flag = not self.info_flag

    def set_background(self, img):
        image_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

        average = []
        for coord in self.dewar.puckCoords:
            sum = 0
            avg = 0
            cnt = 0
            for i in range(-self.detection_box, self.detection_box):
                for j in range(-self.detection_box, self.detection_box):
                    sum += image_gray[coord[1] + i, coord[0] + j]
                    cnt += 1

            avg = sum // cnt
            average.append(avg)

        self.dewar.set_config(average)


    def set_mgrmode(self):
        self.mgr_flag = True
