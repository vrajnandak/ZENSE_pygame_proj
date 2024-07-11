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
        print(information)
        # self.get_user_info()

        #The player for the Game.
        self.player=Player(GAME_START_PLAYER_POS)

        #All the levels unlocked till now
        self.levels=[]
        self.curr_level=Level(STARTING_LEVEL_ID,self.player)
        self.levels.append(self.curr_level)

    #     #A function to display the given text on the screen.
    # def display_text_box(self,display_surf,text_font,textbox_name,textbox_pos, user_string):
    #     #Displaying the textbox name.
    #     text_surface=text_font.render(textbox_name, True, 'white')
    #     display_surf.blit(text_surface,textbox_pos)

    #     #Displaying what the user has entered till now to the right of the name of the box.
    #     user_surface=text_font.render(user_string,True,'black')
    #     white_bg_box=pygame.rect.Rect(textbox_pos[0]+text_surface.get_width(), textbox_pos[1], user_surface.get_width()+20,user_surface.get_height())
    #     pygame.draw.rect(display_surf,'white',white_bg_box,0,border_radius=3)
    #     display_surf.blit(user_surface,(textbox_pos[0] + text_surface.get_width() + 10, textbox_pos[1])) 
    #     pass
    
    # def get_user_info(self):

    #     name_text="Name: "
    #     user_name=""
    #     name_rect=pygame.rect.Rect(100,50,200,100)
    #     remove_last_letter_name=0

    #     age_text="Age: "
    #     user_age=""
    #     age_rect=pygame.rect.Rect(100,200,200,100)
    #     remove_last_letter_age=0

    #     submit_surf=self.font.render("Submit",True,'white')
        
    #     while True:
    #         new_user_age=user_age
    #         new_user_name=user_name
    #         for event in pygame.event.get():
    #             if event.type==pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             if event.type==pygame.KEYDOWN:
    #                 mouse_pos=pygame.mouse.get_pos()
    #                 if name_rect.collidepoint(mouse_pos):
    #                     if event.type==pygame.K_BACKSPACE:
    #                         # new_user_name=user_name[:-1]
    #                         # remove_last_letter_name=1
    #                         user_name=user_name[:-1]
    #                         # user_name=user_name[0:len(user_name)-1]
    #                         # user_name=user_name.rstrip(user_name[-1])
    #                     else:
    #                         user_name+=event.unicode
    #                         # print(type(event.unicode))

    #                 if age_rect.collidepoint(mouse_pos):
    #                     if event.type==pygame.K_BACKSPACE:
    #                         # new_user_age=user_age[:-1]
    #                         # remove_last_letter_age=1
    #                         user_age=user_age[:-1]
    #                     else:
    #                         user_age+=event.unicode
    #                         remove_last_letter_age=1
    #         # if(remove_last_letter_name):
    #         #     user_name=user_name[:-1]
    #         # if(remove_last_letter_age):
    #         #     user_age=user_age[:-1]

    #         # if(new_user_name!=user_name):
    #         #     user_name=new_user_name
    #         # if(new_user_age!=user_age):
    #         #     user_age=new_user_age
            
    #         display_surf=pygame.display.get_surface()
    #         display_surf.fill('black')
    #         self.display_text_box(display_surf,self.font,name_text,name_rect.topleft,user_name)
    #         self.display_text_box(display_surf,self.font,age_text,age_rect.topleft,user_age)
    #         # self.display_text_box(display_surf,self.font,"Submit",(100,300),"")
    #         display_surf.blit(submit_surf,(100,300))
    #         pygame.display.flip()
    #         print(user_name)
    #         # print(type(user_name))
    #         # print(user_name[:-1])
    #     pass

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
            shd_transport=self.curr_level.run(keys)
            pygame.display.flip()
            self.clock.tick(GAME_FPS)

            if(shd_transport==1):
                self.changeMap()
                pass
        pass
