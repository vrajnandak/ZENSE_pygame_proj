import pygame, sys
from Settings import *
from Game import *
from Level import Level
from Button import Button
# from LoadDataManager import *


class MyGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        #Checking if there is a game screen that exists already. Delete it if it already exists.
        self.path_to_screen_img=os.path.join(GRAPHICS_DIR_PATH,"GameScreen.png")
        if(os.path.isfile(self.path_to_screen_img)):
            os.remove(self.path_to_screen_img)

        self.gui_font=pygame.font.Font(None, 30)

        # self.screen=pygame.display.set_mode(SCREEN_SIZE)
        # pygame.display.set_caption(GAME_TITLE)
        self.screen=pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)

        self.quit_game=0        #Is set inside the display screen method.

        #Game's clock
        self.clock=pygame.time.Clock()

        #Buttons. Every screen has a separate button due to having different sizes, positions in the screen. We could've otherwise re-used the same buttons.
            #Start Screen - "New Game","Saved Games", "Quit", "Settings"
        # self.startNewGame=Button((100,100),200,60,"New Game","white",self.gui_font,"red","gray","blue")
        self.startNewGame=Button((200,100),200,60,"New Game",self.gui_font,-200)
        self.startSavedGames=Button((400,200),200,60,"Saved Games", self.gui_font,-300)
        self.startQuit=Button((600,300),200,60,"Quit",self.gui_font,-400)
        self.startSettings=Button((800,400),200,60,"Settings",self.gui_font,-500)
        self.StartButtons=[self.startNewGame,self.startSavedGames,self.startQuit,self.startSettings]
            #Pause Screen - "Resume", "Save", "Quit", "Settings", "Back To Home", "Restart"
        self.pauseResume=Button((200,100),200,60,"Resume",self.gui_font,-100)
        self.pauseSave=Button((200,250),200,60,"Save", self.gui_font,-200)
        self.pauseQuit=Button((200,400),200,60,"Quit",self.gui_font,-300)
        self.pauseSettings=Button((800,100),200,60,"Settings",self.gui_font,-100)
        self.pauseBackToHome=Button((800,250),200,60,"Back To Home",self.gui_font,-200)
        self.pauseRestart=Button((800,400),200,60,"Restart", self.gui_font,-300)
        self.PauseButtons=[self.pauseResume,self.pauseSave,self.pauseQuit,self.pauseSettings,self.pauseBackToHome,self.pauseRestart]
        # for button in self.PauseButtons:                #This is because we don't want the animation on pausing the game.
        #     button.animation_phase=None
            #Settings Screen -
        self.settingsResume=None
        self.SettingsButtons=[self.settingsResume]
            #Victory Screen -
        self.VictoryButtons=[]
            #Loss Screen -
        self.LossButtons=[]
            #Are you sure you want to Quit Screen - "Yes", "No"
        self.AreYouSureYouWantToQuitYes=Button((400,SCREEN_HEIGHT_HALF),200,60,"Yes",self.gui_font,-200)
        self.AreYouSureYouWantToQuitNo=Button((700,SCREEN_HEIGHT_HALF),200,60,"No",self.gui_font,-200)
        self.AreYouSureYouWantToQuitButtons=[self.AreYouSureYouWantToQuitYes,self.AreYouSureYouWantToQuitNo]

        #The Games available.
        self.curr_Game=None
        self.savedGames=[]
        # self.gameDataManager=LoadDataManager()

        #Starting the Code.
        self.curr_screen="Start"         #Can be ["Start","Pause","Settings","Victory","Loss","AreYouSureYouWantToQuit"]
        self.curr_buttons=self.StartButtons
        self.screen_shade_color=SCREEN_BG_SHAD_POS
        self.action=None                 #Can be ["New Game", "Saved Games","Quit","Settings","Resume","Save","Back To Home","Restart", "Yes","No"]
        self.previous_esc_applied=pygame.time.get_ticks()
        self.startGame()

    def chooseWhichButtons(self):
        if(self.curr_screen=="Start"):
            self.curr_buttons=self.StartButtons
            self.screen_shade_color=SCREEN_BG_DARK_COLOR
        elif(self.curr_screen=="Pause"):
            self.curr_buttons=self.PauseButtons
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        elif(self.curr_screen=="Settings"):
            self.curr_buttons=self.SettingsButtons
            self.screen_shade_color=SCREEN_BG_DARK_COLOR
        elif(self.curr_screen=="Victory"):
            self.curr_buttons=self.VictoryButtons
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        elif(self.curr_screen=="Lose"):
            self.curr_buttons=self.LossButtons
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        elif(self.curr_screen=="AreYouSureYouWantToQuit"):
            self.curr_buttons=self.AreYouSureYouWantToQuitButtons
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        pass

    #A method to reset the animation states of the buttons.
    def Reset_button_animations(self,buttons):
        for button in buttons:
            button.animation_phase=1
            button.curr_left=button.start_left_pos

    #A method to display the given screen. Returns the text of the button on which the mouse is released on.
    def displayScreen(self,screen_bg_shade,buttons):

        #Getting the game screen
        gameScreen=None
        if(os.path.isfile(self.path_to_screen_img)):
            gameScreen=pygame.image.load(self.path_to_screen_img)
        running=True
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.quit_game=1
                    running=False
                if(event.type==pygame.KEYDOWN):
                    if event.key==pygame.K_ESCAPE and self.curr_screen=="Pause":
                        self.previous_esc_applied=pygame.time.get_ticks()
                        # print('Returned resume')
                        self.Reset_button_animations(buttons)
                        return "Resume"

                if event.type==pygame.MOUSEBUTTONUP and event.button==1:        #To indicate a left release on mouse.
                    for button in buttons:
                        if(button.bottom_rect.collidepoint(pygame.mouse.get_pos())):
                            # self.button_chosen_text=button.text
                            self.Reset_button_animations(buttons)
                            if(self.curr_Game==None and button.text=="Resume"):
                                return "NOT_POSSIBLE"
                            else:
                                return button.text
            if(running==False):
                return ""

            if(gameScreen):
                self.screen.blit(gameScreen,(0,0))
            else:
                drawShadedBGScreen(self.screen,screen_bg_shade)
            for button in buttons:
                button.draw(self.screen)
            pygame.display.flip()
        return ""
    
    #A method to display the Starting Screen.
    def startGame(self):
        running=True
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
            if(running==False):
                #Call the "Are you Sure you want to Quit?" screen
                    #If yes
                self.gameDataManager.saveTheGame(self.curr_Game)
                    #If no
                #self.quit_game=0
                break
            
            #Displaying the appropriate screen after Choosing the required buttons based on current game state.
            self.chooseWhichButtons()
            self.action=self.displayScreen(self.screen_shade_color,self.curr_buttons)

            if(self.quit_game==1):
                #Call the "Are you Sure you want to Quit?" screen
                break

            #Performing the Actions.
            if(self.action=="Resume"):
                # print('running the game')
                self.curr_screen=self.curr_Game.run(self.previous_esc_applied)       #Returns either of ["Pause","Victory","Lose","Quit"]
            elif(self.action=="New Game"):
                newGame=Game(self.clock)
                self.curr_Game=newGame
                self.curr_screen=self.curr_Game.run(self.previous_esc_applied)
                pass
            elif(self.action=="Saved Games"):
                pass
            elif(self.action=="Quit"):
                pygame.quit()
                break
                pass
            elif(self.action=="Settings"):
                pass
            elif(self.action=="Save"):
                # self.gameDataManager.saveTheGame(self.curr_Game)
                # self.curr_screen="Start"
                # self.curr_Game=None
                pass
            elif(self.action=="Back To Home"):
                self.curr_screen="Start"
                pass
            elif(self.action=="Restart"):
                self.curr_Game=Game(self.clock)
                self.curr_Game.run(self.previous_esc_applied)
                pass
            elif(self.action=="Yes"):
                pass
            elif(self.action=="No"):
                pass
            elif(self.action=="NOT_POSSIBLE"):
                #Show a msg on the bottom of the screen for a certain time saying "Please create a game or join one".
                pass
        pass
        pass


if __name__=='__main__':
    playGame=MyGame()