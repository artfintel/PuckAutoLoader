from PuckAutoLoader.utils.config_parser import ConfigParser

class Dewar:

    puckCoords = [
        (940, 195), (1112, 195), (1290, 195), (1460, 195), (1638, 195),
        (855, 347), (1028, 347), (1208, 347), (1380, 345), (1555, 342), (1730, 342),
        (940, 495), (1120, 495), (1292, 495), (1470, 495), (1650, 495),
        (855, 650), (1028, 645), (1210, 645), (1384, 645), (1565, 645), (1740, 645),
        (940, 800), (1120, 800), (1300, 800), (1480, 800), (1660, 800),
        (1212, 960), (1390, 955)
    ]

    puckBackground = [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0
    ]

    # puck detection
    puckDetection = [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0
    ]

    puckPosition = [
        147, 153, 159, 164, 169,
        148, 154, 160, 165, 170, 174,
        149, 155, 161, 166, 171,
        150, 156, 162, 167, 172, 175,
        151, 157, 163, 168, 173,
        152, 158
    ]

    puckPositionName = [
        "1A", "2A", "3A", "4A", "5A",
        "1B", "2B", "3B", "4B", "5B", "6B",
        "1C", "2C", "3C", "4C", "5C",
        "1D", "2D", "3D", "4D", "5D", "6D",
        "1E", "2E", "3E", "4E", "5E",
        "1F", "2F"
    ]

    def __init__(self):
        self.config = ConfigParser('utils/background.ini').get_config()
        for i in range(len(self.config.items('BACKGROUND'))):
            self.puckBackground[i] = int(self.config.items('BACKGROUND')[i][1])

    def set_config(self, value):
        for i in range(len(self.config.items('BACKGROUND'))):
            self.config['BACKGROUND'][self.puckPositionName[i]] = str(value[i])
            self.puckBackground[i] = value[i]

        with open('utils/background.ini', 'w') as f:
            self.config.write(f)

    def get_config(self):
        return self.config

    def get_puck_coords(self):
        return self.puckCoords

    def get_puck_detection(self):
        return self.puckDetection

    def get_puck_position(self):
        return self.puckPosition

    def get_puck_position_name(self):
        return self.puckPositionName

    def get_puck_background(self):
        return self.puckBackground
