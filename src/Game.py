import pygame
from Settings import *
from Level import Level
from Button import Button
from Player import Player
import re       #Imported for removing the last letter from a string.
from LEVEL_THINGS import game_info
from LEVEL_THINGS import game_lore

class Game:
    def __init__(self,clock):
        self.clock=clock
        self.GameSettings=Settings()

        # self.createTeleportationMap()

        #Displaying the game lore then, Get some credentials from the user, like the name, age etc.
        self.font=pygame.font.Font(None,32)
        display_surf=pygame.display.get_surface()
        bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"GameStartingScreen.png"))
            #Displaying the game lore.
        DISPLAY_DIALOGS(game_lore,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
        display_surf.blit(bg_image,(0,0))
            #Getting the credentaials
        information=getRequiredInfo(["Name","Age"],self.font,start_pos_y=SCREEN_HEIGHT_HALF,bg_image=bg_image,display_this_msg_and_pos=["Hover the mouse over the textbox and type the appropriate credential. Press 'Enter' or the submit button to submit the credentials.",[60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2)]])
        self.GameSettings.my_Name=information[0]
        self.GameSettings.my_age=information[1]
        display_surf.blit(bg_image,(0,0))
            #Displaying the game info.
        DISPLAY_DIALOGS(game_info,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
        display_surf.blit(bg_image,(0,0))

        #The player for the Game.
        self.player=Player(GAME_START_PLAYER_POS,self.GameSettings)

        #All the levels unlocked till now
        self.levels=[]
        self.curr_level=Level(STARTING_LEVEL_ID,self.player,self.GameSettings)
        self.levels.append(self.curr_level)

        #A timer for pause screen.
        self.esc_time_duration=100
        self.previous_esc_keydown=pygame.time.get_ticks()

        #A timer for using the portals.
        self.can_teleport=True
        self.teleport_cooldown=1000
        self.previous_teleported_time=None

    # def createTeleportationMap(self):
        #For Ruin0
        # Ruin0_entrance1
        #For Ruin1
        #For Ruin2
        #For Ruin3
        # pass
    
    #A method to get the next level's ID.
    def get_next_level_id(self):
        #Have to check the player's positions and the collision between the created rects and then send the new level.
        new_level=self.curr_level.level_id
        if self.curr_level.level_id==0:
            if self.player.rect.colliderect(Ruin0_rect_enterCode) and self.player.has_entered_correct_code==True:
                new_level=1
            elif self.player.rect.colliderect(Ruin0_rect_Ruin2):
                print('going to Ruin2')
                new_level=2
            elif self.player.rect.colliderect(Ruin0_rect_Ruin3):
                new_level=3
            pass
        elif self.curr_level.level_id==1:
            if self.player.rect.colliderect(Ruin1_rect_Ruin0):
                new_level=0
            elif self.player.rect.colliderect(Ruin1_rect_Ruin1_Dummy):
                pass
            elif self.player.rect.colliderect(Ruin1_rect_Ruin1_hidden):
                pass
            pass
        elif self.curr_level.level_id==2:
            if self.player.rect.colliderect(Ruin2_rect_Ruin0):
                new_level=0
                pass
            elif self.player.rect.colliderect(Ruin2_rect_Ruin2_Dummy):
                pass
            elif self.player.rect.colliderect(Ruin2_rect_Ruin2_hidden):
                pass
            pass
        elif self.curr_level.level_id==3:
            if self.player.rect.colliderect(Ruin3_rect_Ruin0):
                new_level=0
            elif self.player.rect.colliderect(Ruin3_rect_Ruin3_hidden):
                pass
            pass
        # new_level=1
        return new_level

    def changeToMap(self):
        #Make a black screen and place it in 'bg_GameStartScreen.png' because the player has to go to the next screen. Or save the images to new maps beforehand.
        new_level_id=self.get_next_level_id()
        if(new_level_id==self.curr_level.level_id):
            return
        
        curr_level_selected_weapon=self.curr_level.curr_selected_weapon
        curr_level_selected_magic=self.curr_level.curr_selected_magic

        # if len(self.levels)>0:
        for level in self.levels:
            if level.level_id == new_level_id:
                print('the map already exists.')
                self.curr_level=level
                self.player.rect.topleft=self.curr_level.player_pos
                self.curr_level.curr_selected_weapon=curr_level_selected_weapon
                self.curr_level.curr_selected_magic=curr_level_selected_magic

                #Passing the player, the create and destroy functions for attack,magic which are specific to the level. Without these, the attacks would work on only the recently created level.
                self.player.getAttackFunctions(self.curr_level.create_attack,self.curr_level.destroy_attack)
                self.player.getMagicFunctions(self.curr_level.create_magic)
                return
        # print('hello')
        # self.levels.append(self.curr_level)
        self.curr_level=Level(new_level_id,self.player,self.GameSettings)
        self.curr_level.curr_selected_weapon=curr_level_selected_weapon
        self.curr_level.curr_selected_magic=curr_level_selected_magic
        self.levels.append(self.curr_level)
        print('created the new level')
        pass
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

    def apply_cooldown(self):
        curr_time=pygame.time.get_ticks()
        if self.can_teleport==False:
            if curr_time-self.previous_teleported_time>=self.teleport_cooldown:
                self.can_teleport=True

    def run(self,previous_esc_time):
        running=True
        while running:
            #The basic event loop to run the game.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
                    sys.exit()
                    break

            if(running==False):
                break
            
            #Getting the mouse Keys
            keys=pygame.key.get_pressed()
            if(keys[pygame.K_ESCAPE] and pygame.time.get_ticks()-previous_esc_time>=500):          #Pause screen has to be visible if the user hits 'esc'
                SaveGameScreen()
                return "Pause"
            
            #This is set when the change is applied itself.
            # #Setting the player's speed to the given speed.
            # self.player.speed=self.GameSettings.PLAYER_SPEED
            
            #Running the Level logic.
            ret_val=self.curr_level.run(keys)
            pygame.display.flip()
            self.apply_cooldown()

            # self.has_displayed_basic_game_info=True
            if(ret_val==1):
                if self.can_teleport:
                    self.previous_teleported_time=pygame.time.get_ticks()
                    self.can_teleport=False
                    self.changeToMap()
            elif(ret_val==100):
                return "Victory"
            elif(ret_val==101):
                return "Lose"
            else:     #Code for changing the map.
                # if self.can_teleport:
                #     self.previous_teleported_time=pygame.time.get_ticks()
                #     self.can_teleport=False
                #     self.changeToMap(ret_val)
                # print('after changing map.')
                pass
            
            
            self.clock.tick(self.GameSettings.GAME_FPS)
        pass
