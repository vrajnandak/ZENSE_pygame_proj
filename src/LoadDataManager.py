import pygame
import json
import os
from Settings import *

class LoadDataManager:
    def __init__(self):
        self.file_extension=".save"
        self.save_dir=SAVED_DATA_DIR_PATH
        self.counter=1
        pass

    def saveTheGame(self,game):
        new_file_name=os.path.join(self.save_dir,f'{GAME_TITLE}{self.counter}{self.file_extension}')
        data_file=open(new_file_name,"wb")
        # game.clock=None
        json.dump(game,data_file)
        self.counter+=1
        pass

    def loadTheGame(self,game_id):
        file_name=os.path.join(self.save_dir,f'{GAME_TITLE}{game_id}{self.file_extension}')
        data_file=open(file_name,"rb")
        game=json.load(data_file)
        return game
        pass