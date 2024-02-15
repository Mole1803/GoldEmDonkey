import configparser
import os
from pathlib import Path

config_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.ini')


class SetupHelper:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print(self.BASE_DIR)

    def run(self):
        self.create_database_directory()


    def create_database_directory(self):
        path = self.get_database_directory()
        if not os.path.exists(path):
            os.makedirs(path)

    def get_database_directory(self):
        for key in self.config['DEFAULT']:
            print(key)
        return Path(self.BASE_DIR) / Path(self.config['DEFAULT']['Database_Directory'])


setup_helper = SetupHelper()
setup_helper.run()

