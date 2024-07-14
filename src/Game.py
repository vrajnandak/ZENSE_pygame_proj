import pygame
from Settings import *
from Level import Level
from Button import Button
from Player import Player
import re       #Imported for removing the last letter from a string.

class Game:
    def __init__(self,clock):
        self.clock=clock

        self.GameSettings=Settings()

        self.createTeleportationMap()

        #Get some credentials from the user, like the name, age etc.
        self.font=pygame.font.Font(None,32)
        information=getRequiredInfo(["Name","Age"],self.font)
        self.GameSettings.my_Name=information[0]
        self.GameSettings.my_age=information[1]

        #The player for the Game.
        self.player=Player(GAME_START_PLAYER_POS,self.GameSettings)

        #All the levels unlocked till now
        self.has_displayed_basic_game_info=False
        self.levels=[]
        self.curr_level=Level(STARTING_LEVEL_ID,self.player,self.GameSettings,self.has_displayed_basic_game_info)
        self.levels.append(self.curr_level)

        self.esc_time_duration=100
        self.previous_esc_keydown=pygame.time.get_ticks()

    def createTeleportationMap(self):
        #For Ruin0
        # Ruin0_entrance1
        #For Ruin1
        #For Ruin2
        #For Ruin3
        pass

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

    def run(self,previous_esc_time):
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
            if(keys[pygame.K_ESCAPE] and pygame.time.get_ticks()-previous_esc_time>=500):          #Pause screen has to be visible if the user hits 'esc'
                SaveGameScreen()
                return "Pause"
            

            #Setting the player's speed to the given speed.
            self.player.speed=self.GameSettings.PLAYER_SPEED
            
            #Running the Level logic.
            ret_val=self.curr_level.run(keys)
            pygame.display.flip()
            self.clock.tick(self.GameSettings.GAME_FPS)

            self.has_displayed_basic_game_info=True

            if(ret_val==1):     #Code for changing the map.
                self.changeMap()
                pass
            elif(ret_val==10):
                return "Lose"
        pass
