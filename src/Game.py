import pygame
from Settings import *
from Level import Level
from Button import Button
from Player import Player
import re       #Imported for removing the last letter from a string.

class Game:
    def __init__(self,clock):
        self.clock=clock

        #Get some credentials from the user, like the name, age etc.
        self.font=pygame.font.Font(None,32)
        information=getRequiredInfo(["Name","Age"],self.font)

        #The player for the Game.
        self.player=Player(GAME_START_PLAYER_POS)

        #All the levels unlocked till now
        self.levels=[]
        self.curr_level=Level(STARTING_LEVEL_ID,self.player)
        self.levels.append(self.curr_level)

    def changeMap(self):
        #Have to Transport the player
            #If the level to teleport to doesn't exist in the self.levels.
                #Create the New Level.
                #Append this New Level to the self.levels
                #Set this New Level to the curr_level.
                #put 'continue'
            #If level already exists
                #set level_found to be the level to be teleported to.
                #self.curr_level=level_found
                #put 'continue'
        pass

    def run(self):
        running=True
        while running:
            #The basic event loop to run the game.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
                    break

            if(running==False):
                break
            
            #Getting the mouse Keys
            keys=pygame.key.get_pressed()
            if(keys[pygame.K_ESCAPE]):          #Pause screen has to be visible if the user hits 'esc'
                return "Pause"
            
            #Running the Level logic.
            ret_val=self.curr_level.run(keys)
            pygame.display.flip()
            self.clock.tick(GAME_FPS)

            if(ret_val==1):     #Code for changing the map.
                self.changeMap()
                pass
            elif(ret_val==10):
                return "Lose"
        pass
