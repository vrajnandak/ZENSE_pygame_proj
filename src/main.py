import pygame, sys
from Settings import *
from Game import *
from Level import Level
from Button import Button


class MyGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.gui_font=pygame.font.Font(None, 30)

        # self.screen=pygame.display.set_mode(SCREEN_SIZE,pygame.RESIZABLE)
        self.screen=pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)

        #Game's clock
        self.clock=pygame.time.Clock()

        #Buttons. Every screen has a separate button due to having different sizes, positions in the screen. We could've otherwise re-used the same buttons.
            #Start Screen - "New Game","Saved Games", "Quit", "Settings"
        self.startNewGame=Button((100,100),200,60,"New Game",self.gui_font,"white","red","gray","blue")
        # self.startSavedGames=Button()
        # self.startQuit=Button()
        # self.startSettings=Button()
        # self.StartButtons=[self.startNewGame,self.startSavedGames,self.startQuit,self.startSettings]
            #Pause Screen - "Resume", "Save", "Quit", "Settings"
        # self.pauseResume=Button()
        # self.pauseSave=Button()
        # self.pauseQuit=Button()
        # self.pauseSettings=Button()
        # self.PauseButtons=[self.pauseResume,self.pauseSave,self.pauseQuit,self.pauseSettings]
            #Settings Screen -
        # self.SettingsButtons=[]

        #The Games available.
        self.curr_Game=None
        self.savedGames=[]

        #Starting the Code.
        self.start()

    def start(self):
        #Display the Start Screen.
        in_start_screen=0
        running=1
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=0
                    break
            self.screen.fill('black')
            self.startNewGame.draw(self.screen)
            pygame.display.flip()
        
        if(running==0):
            pygame.quit()
            #If New Game.
        # self.curr_game=Game(self.clock)
            #If one of the saved Games, Then the select the one and set it to be the self.curr_Game.


        # self.curr_game.run()
        pass


if __name__=='__main__':
    playGame=MyGame()