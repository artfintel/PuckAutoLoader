import os
import sys
import configparser

class ConfigParser():
    def __init__(self, file):
        self.loadConfig(file)
        self.file = file

    def loadConfig(self, file):
        if os.path.exists(file) == False:
            raise Exception('%s file does not exist. \n' %file)

        self.config = configparser.ConfigParser()
        self.config.read(file)

    def get_config(self):
        return self.config
