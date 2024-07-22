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
        self.path_to_start_screen=os.path.join(GRAPHICS_DIR_PATH,"GameStartingScreen.png")
        self.start_screen_img=pygame.image.load(self.path_to_start_screen)
        self.path_to_curr_screen=os.path.join(GRAPHICS_DIR_PATH,"Curr_Screen.png")
        self.path_to_screen_img=self.path_to_start_screen

        #Game's clock,settings,font
        self.clock=pygame.time.Clock()
        self.OriginalSettings=Settings()
        self.gui_font=pygame.font.Font(None, 30)

        # self.screen=pygame.display.set_mode(SCREEN_SIZE)
        # pygame.display.set_caption(GAME_TITLE)
        self.screen=pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)

        #Buttons. Every screen has a separate button due to having different sizes, positions in the screen. We could've otherwise re-used the same buttons.
            #Start Screen - "New Game","Saved Games", "Quit", "Settings"
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
            #Settings Screen - "Resume","Back to home", "Reset Settings", "Apply Changes"
        self.settingsResume=Button((80,100),200,60,"Resume",self.gui_font,-100)
        self.settingsBackToHome=Button((300,100),200,60,"Back To Home",self.gui_font,-200)
        self.settingsResetSettings=Button((520,100),200,60,"Reset Settings", self.gui_font,-300)
        self.settingsApplyChanges=Button((740,100),200,60,"Apply Changes",self.gui_font,-400)
        self.SettingsButtons=[self.settingsResume,self.settingsBackToHome,self.settingsResetSettings,self.settingsApplyChanges]
        self.scroll_settings_screen=0
        self.accumulated_scroll=0
        self.SETTINGS_SCREEN_TOP=0
        self.SETTINGS_SCREEN_BOTTOM=-SCREEN_HEIGHT+120
            #Victory Or Loss Screen Buttons - "Play Again", "Quit"
        # self.victory_or_loss_text=["You have Won", "You have Lost"]
        text_font=pygame.font.FontType(None,60)
        self.victory_text_surf=text_font.render("You Have WON!!!", True, 60)
        self.lose_text_surf=text_font.render("You Have LOST!!",True,60)
        self.victory_or_lose_pos=(SCREEN_WIDTH_HALF-self.victory_text_surf.get_width()//2,100)
        self.victory_or_loss_PlayAgain=Button((SCREEN_WIDTH_HALF-120,SCREEN_HEIGHT_HALF-100),200,60,"Play Again",self.gui_font,-100)
        self.victory_or_loss_Quit=Button((SCREEN_WIDTH_HALF-120,((3*SCREEN_HEIGHT)//4)-100),200,60,"Quit",self.gui_font,-100)
        self.victory_or_lose="Lose"
        self.Victory_or_lossButtons=[self.victory_or_loss_PlayAgain,self.victory_or_loss_Quit]
            #Are you sure you want to Quit Screen - "Yes", "No"
        self.AreYouSureYouWantToQuit_text=["Are you sure you want to Quit?"]
        self.AreYouSureYouWantToQuitYes=Button((400,SCREEN_HEIGHT_HALF),200,60,"Yes",self.gui_font,-200)
        self.AreYouSureYouWantToQuitNo=Button((700,SCREEN_HEIGHT_HALF),200,60,"No",self.gui_font,-200)
        self.AreYouSureYouWantToQuitButtons=[self.AreYouSureYouWantToQuitYes,self.AreYouSureYouWantToQuitNo]

        #The Games available.
        self.curr_Game=None
        self.savedGames=[]
        # self.gameDataManager=LoadDataManager()

        #Starting the Code.
        self.display_text_also=""
        self.curr_screen="Start"         #Can be ["Start","Pause","Settings","Victory","Loss","AreYouSureYouWantToQuit"]
        self.curr_buttons=self.StartButtons
        self.screen_shade_color=SCREEN_BG_SHAD_POS
        self.action=None                 #Can be ["New Game", "Saved Games","Quit","Settings","Resume","Save","Back To Home","Restart", "Yes","No"]
        self.previous_esc_applied=pygame.time.get_ticks()
        self.startGame()

    def chooseWhichButtons(self):
        self.victory_or_lose=""
        if(self.curr_screen=="Start"):
            self.curr_buttons=self.StartButtons
            self.screen_shade_color=SCREEN_BG_DARK_COLOR
        elif(self.curr_screen=="Pause"):
            self.path_to_screen_img=self.path_to_curr_screen
            self.curr_buttons=self.PauseButtons
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        elif(self.curr_screen=="Settings"):
            self.curr_buttons=self.SettingsButtons
            self.screen_shade_color=SCREEN_BG_DARK_COLOR
        elif(self.curr_screen=="Victory"):
            self.path_to_screen_img=self.path_to_curr_screen
            self.curr_buttons=self.Victory_or_lossButtons
            self.victory_or_lose="Victory"
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        elif(self.curr_screen=="Lose"):
            self.path_to_screen_img=self.path_to_curr_screen
            self.curr_buttons=self.Victory_or_lossButtons
            self.victory_or_lose="Lose"
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

    #A method to clamp the scroll settings variable so that the page doesn't scroll out of bounds
    def configure_scroll_settings_screen(self):
        if self.accumulated_scroll>self.SETTINGS_SCREEN_TOP:
            self.accumulated_scroll-=self.scroll_settings_screen
            self.scroll_settings_screen=0
        elif self.accumulated_scroll<self.SETTINGS_SCREEN_BOTTOM:
            self.accumulated_scroll-=self.scroll_settings_screen
            self.scroll_settings_screen=0
        # if self.accumulated_scroll<self.SETTINGS_SCREEN_TOP:
        #     self.accumulated_scroll-=self.scroll_settings_screen
        #     self.scroll_settings_screen=0
        # elif self.accumulated_scroll>self.SETTINGS_SCREEN_BOTTOM:
        #     self.accumulated_scroll-=self.scroll_settings_screen
        #     self.scroll_settings_screen=0
        pass

    #A method to display the given screen. Returns the text of the button on which the mouse is released on.
    def displayScreen(self,screen_bg_shade,buttons):

        #Getting the game screen
        gameScreen=self.start_screen_img
        if(self.path_to_screen_img!=self.path_to_start_screen and os.path.isfile(self.path_to_screen_img)):
            gameScreen=pygame.image.load(self.path_to_screen_img)
        running=True
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEWHEEL:
                    if (self.curr_screen=="Settings"):
                        self.scroll_settings_screen=event.y*SCROLL_SETTINGS_SPEED
                        self.accumulated_scroll+=self.scroll_settings_screen
                        pass
                    pass
                if(event.type==pygame.KEYDOWN):
                    if event.key==pygame.K_ESCAPE and self.curr_screen=="Pause":
                        self.previous_esc_applied=pygame.time.get_ticks()
                        self.Reset_button_animations(buttons)
                        return "Resume"

                if event.type==pygame.MOUSEBUTTONUP and event.button==1:        #To indicate a left release on mouse.
                    for button in buttons:
                        if(button.bottom_rect.collidepoint(pygame.mouse.get_pos())):
                            self.Reset_button_animations(buttons)
                            if(self.curr_Game==None and button.text=="Resume"):
                                return "NOT POSSIBLE"
                            else:
                                if(button.text=="Apply Changes"):
                                    if(self.curr_Game!=None):
                                        self.curr_Game.GameSettings.apply_changes(self.curr_Game)
                                    else:
                                        return "NOT POSSIBLE"
                                else:
                                    return button.text
            
            self.configure_scroll_settings_screen()
            self.screen.blit(gameScreen,(0,0))
            
            # if(gameScreen):
            #     self.screen.blit(gameScreen,(0,0))
            # else:
            #     drawShadedBGScreen(self.screen,screen_bg_shade)
            if self.victory_or_lose=="Lose":
                self.screen.blit(self.lose_text_surf,self.victory_or_lose_pos)
                # DISPLAY_MSG(self.lose_text_surf,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
                pass
            elif self.victory_or_lose=="Victory":
                self.screen.blit(self.victory_text_surf,self.victory_or_lose_pos)
                # DISPLAY_MSG(self.victory_text_surf,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
                pass

            for button in buttons:
                button.draw(self.screen,self.scroll_settings_screen)
            if(self.curr_screen=="Settings"):
                if(self.curr_Game!=None):
                    self.curr_Game.GameSettings.display_settings(self.screen,self.curr_Game,can_change_values=1,scroll_settings_screen=self.scroll_settings_screen)
                else:
                    # print('returning not possible')
                    # self.OriginalSettings.display_settings(self.screen,self.Temporary_Game,can_change_values=0)
                    return "NOT POSSIBLE"
            # if(self.curr_Game!=None):
            #     debug_print(self.curr_Game.GameSettings.selected_attr_index,(SCREEN_WIDTH_HALF,SCREEN_HEIGHT_HALF))
            self.scroll_settings_screen=0
            pygame.display.flip()
        return "NOT POSSIBLE"
    
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

            #Performing the Actions.
            if(self.action=="Resume"):
                self.curr_screen=self.curr_Game.run(self.previous_esc_applied)       #Returns either of ["Pause","Victory","Lose","Quit"]
            elif(self.action=="New Game"):
                self.saveCurrentGame()
                newGame=Game(self.clock)
                self.curr_Game=newGame
                self.curr_screen=self.curr_Game.run(self.previous_esc_applied)
                pass
            elif(self.action=="Saved Games"):
                pass
            elif(self.action=="Quit"):
                self.curr_screen="AreYouSureYouWantToQuit"
                # pygame.quit()
                break
                pass
            elif(self.action=="Settings"):
                self.curr_screen="Settings"
                # print('current screen is now settings')
                pass
            elif(self.action=="Save"):
                self.saveCurrentGame()
                self.curr_screen="Start"
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
                for button in self.curr_buttons:
                    button.animation_phase=None
                # print('not possible')
                #Show a msg on the bottom of the screen for a certain time saying "Please create a game or join one".
                pass
            elif(self.action=="Reset Settings"):
                if self.curr_Game!=None:
                    self.curr_Game.GameSettings.reset_settings()
                else:
                    pass
                
                    # for button in self.curr_buttons:
                    #     button.animation_phase=None
            else:
                # self.curr
                pass

        pass
        pass

    #A method to save the current game.
    def saveCurrentGame(self):
        if self.curr_Game!=None:
            pass
        pass


if __name__=='__main__':
    playGame=MyGame()