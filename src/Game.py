import pygame
from Settings import *
from Level import Level
from Button import Button

class Game:
    def __init__(self,clock):
        self.clock=clock
        self.levels=[]
        self.curr_level=Level(0)

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
            

            self.curr_level.run(keys)
            pygame.display.flip()
            self.clock.tick(GAME_FPS)
        pass
