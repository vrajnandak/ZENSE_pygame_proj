import pygame
from Settings import *
from Level import Level

class Game:
    def __init__(self):
        # self.screen=pygame.display.set_mode(SCREEN_SIZE,pygame.RESIZABLE)
        self.screen=pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)

        self.clock=pygame.time.Clock()

        self.levels=[]
        self.curr_level=Level(0)
        self.run()

    def run(self):
        has_quit=0
        while True:

            #The basic event loop to run the game.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    has_quit=1
                    pygame.quit()
                    break
            if(has_quit):
                break

            keys=pygame.key.get_pressed()
            self.screen.fill('black')
            self.curr_level.run(keys)
            pygame.display.flip()
            self.clock.tick(GAME_FPS)
        pass

if __name__=='__main__':
    playGame=Game()