import pygame
import os
from csv import reader
import sys
from math import sin        #To toggle between 0 to 255 for the flicker animation when the enemy or player sprite gets hit.
from random import randint

pygame.init()
pygame.font.init()


#######################Original Settings####################
#Speeds
GAME_FPS=30
PLAYER_SPEED=10
ENEMY_SPEED=5
KEYBOARD_CAMERA_SPEED=20
MOUSE_CAMERA_SPEED=20


#Potion values
HEALTH_POTION_VAL=[100,150,200,300,500]
EXP_POTION_VAL=[200,300,400,600,1000]
ENERGY_POTION_VAL=[20,30,40,50,100]

#Others
GAME_TITLE="Time Rift Rescue"
GAME_START_PLAYER_POS=(1979,1206)
STARTING_LEVEL_ID=0
TELEPORTATION_MAP={             #A dictionary of key (<level_id>_<teleportation_portal_top_left>) and value (a list of form [new_level_to_transport_to, new_player_pos])
    '0': [],
    '1': [],
    '2': [],
    '3': []
}
ENEMY_HEALTH=200
ENEMY_NOTICE_RADIUS=9         #A radius 5 BASE_SIZE's
ENEMY_ATTACK_RADIUS=1
INC_EXP_CAP=1.9                #A variable to indicate the factor by which the exp cap grows for the player.
    #A dictionary of key(weapon name) and value(a dictionary containing {cooldown_time, damage})
WEAPON_INFO={           #The last 3 attributes are list containing the said values for cooldown, damage respectively in the list.
    # 'whip': {'cooldown':150, 'damage': 15, 'min_val': [100,10], 'max_val': [300,30], 'cost_to_upgrade_one_unit': [10,50]},     
    'sword':{'cooldown': 200, 'damage': 30, 'min_val': [100,20], 'max_val': [300,50], 'cost_to_upgrade_one_unit': [10,40]},
    'lance':{'cooldown': 100, 'damage': 20, 'min_val': [100,20], 'max_val': [200,40], 'cost_to_upgrade_one_unit': [10,40]},
    'axe':{'cooldown': 150, 'damage': 40, 'min_val': [100,30], 'max_val': [200,70], 'cost_to_upgrade_one_unit': [10,40]},
    # 'gun':{'cooldown': 200, 'damage': 30, 'min_val': [150,20], 'max_val': [300,40], 'cost_to_upgrade_one_unit': [10,50]}
}
MAGIC_INFO={
    'flame':{'cooldown':100,'strength':15,'cost':30, 'min_val': [100,15,25], 'max_val': [250,50,40], 'cost_to_upgrade_one_unit': [20,50,70]},
    'heal':{'cooldown':150,'strength':20,'cost':40, 'min_val': [100,15,25], 'max_val': [250,40,40], 'cost_to_upgrade_one_unit': [20,50,80]}
}
ZOMBIE_ENEMIES_INFO={
    'zombie1':{'health':100,'exp':20,'damage':10, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'claw', 'speed':ENEMY_SPEED},
    'zombie2':{'health':150,'exp':30,'damage':20, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'claw', 'speed':ENEMY_SPEED},
    'zombie3':{'health':200,'exp':50,'damage':50, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+1, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'slash', 'speed':ENEMY_SPEED+1},
    'zombie4':{'health':400,'exp':100,'damage':75, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+2, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'sparkle', 'speed':ENEMY_SPEED+2},
    'zombieBoss':{'health':1000,'exp':500,'damage':150, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+4, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'thunder', 'speed':ENEMY_SPEED+5}
}

#Sizes
BASE_SIZE=32
SCREEN_WIDTH=1240
SCREEN_HEIGHT=800
SCREEN_WIDTH_HALF=SCREEN_WIDTH//2
SCREEN_HEIGHT_HALF=SCREEN_HEIGHT//2
SCREEN_SIZE=(SCREEN_WIDTH,SCREEN_HEIGHT)
PLAYER_SIZE=(2*BASE_SIZE,3*BASE_SIZE)
ENEMY_SIZE=(2*BASE_SIZE,3*BASE_SIZE)
STRONG_ENEMY_SIZE=(3*BASE_SIZE,3*BASE_SIZE)


#Colors
SCREEN_BG_SHADE_COLOR=(127,127,127,0)
SCREEN_BG_DARK_COLOR=(0,255,0)
TEXT_COLOR=(255,255,255)
BUTTON_BACKGROUND_COLOR=(133,133,133)
BUTTON_HOVER_COLOR=(83,83,83)
BUTTON_CLICK_COLOR=(0,0,0)


#The Background Shade when a Screen is active. These are the default values used.
SCREEN_BG_SHADE_SURF=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
SCREEN_BG_SHAD_POS=(0,0)


#Folder Paths
WORKING_DIRECTORY_PATH=os.getcwd()
SAVED_DATA_DIR_PATH=os.path.join(WORKING_DIRECTORY_PATH,"SavedData")
GRAPHICS_DIR_PATH=os.path.join(WORKING_DIRECTORY_PATH,"graphics")
PLAYER_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"Player")
MAPS_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"Ruins")            #Folder path to getting Maps and Other Graphics
PLAYER_MAGIC_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"PLAYER_MAGIC")
PLAYER_WEAPONS_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"PLAYER_WEAPON")
BASEMAP_NAME="BaseMap.png"                          #Name of Floor maps which are basically the 1st drawn image.
FLOORINFO_DIR_NAME="FloorInfo"
BLOCKS_PATH=os.path.join(GRAPHICS_DIR_PATH,"Blocks.png")


#UI Information.
UI_TEXT_FONT=pygame.font.Font(None,20)
BAR_HEIGHT=20                       #Common for all the bars being displayed
HEALTH_BAR_WIDTH=int(SCREEN_WIDTH//8)
HEALTH_BAR_BGCOLOR=(60,60,60)
HEALTH_BAR_COLOR=(0,255,0)
HEALTH_BAR_BORDER_COLOR=(0,0,0)
ENERGY_BAR_WIDTH=int((3*HEALTH_BAR_WIDTH)//4)
ENERGY_BAR_BGCOLOR=(60,60,60)
ENERGY_BAR_COLOR=(103,146,160)
ENERGY_BAR_BORDER_COLOR=(0,0,0)
EXP_BAR_WIDTH=int(HEALTH_BAR_WIDTH//2)
EXP_BAR_BGCOLOR=(60,60,60)
EXP_BAR_COLOR=(255,255,0)
EXP_BAR_BORDER_COLOR=(0,0,0)
ITEM_BOX_SIZE=80
ITEM_BOX_BG_COLOR=(60,60,60)
ITEM_BOX_BORDER_COLOR=(0,0,0)
ITEM_BOX_BORDER_COLOR_ACTIVE=(255,215,0)


#COLORS for Changing the Settings.
TEXT_COLOR='white'
TEXT_COLOR_SELECTED='black'
BG_COLOR=BUTTON_BACKGROUND_COLOR
BG_COLOR_SELECTED='white'
BG_BORDER_COLOR='black'
BAR_COLOR='white'
BAR_COLOR_SELECTED='black'


#COST TO UPGRADE ANYTHING THAT IS UPGRADABLE.
COST_TO_UPGRADE_SPEEDS={
    "GAME_FPS":[30,60,10],
    "PLAYER_SPEED":[8,20,50],
    "ENEMY_SPEED":[4,15,20],
    "KEYBOARD_CAMERA_SPEED":[15,35,40],
    "MOUSE_CAMERA_SPEED":[15,35,40],
    # "Weapon Cooldown":[],         #The other variable information(WEAPON_INFO, MAGIC_INFO) itself have these values.              
    # "Wepon Damage":[],
    # "Magic Strength":[],
    # "Magic Cost":[],
    # "Magic Cooldown":[]
}



#A method to continuously toggle between 0 and 255.
def wave_value():
    value=sin(pygame.time.get_ticks()//2)
    if value>=0:
        return 255
    return 0
    pass



#Function to display the textbox along with the value in the string.
def display_textbox(display_surf,text_surf,text_rect,user_info,text_color,font):
    #Drawing the text_surf using text_rect.
    pygame.draw.rect(display_surf,'white',text_rect,0,border_radius=3)
    display_surf.blit(text_surf,(text_rect.centerx-text_surf.get_width()//2,text_rect.centery-text_surf.get_height()//2))

    #Drawing the user string.
    user_surf=font.render(user_info,True,text_color)
    white_bgrect=pygame.rect.Rect(text_rect.right+30, text_rect.top,user_surf.get_width()+(20 if len(user_info)>0 else 0),user_surf.get_height()+20)
    pygame.draw.rect(display_surf,'white',white_bgrect,0,border_radius=3)
    display_surf.blit(user_surf,(white_bgrect.centerx-user_surf.get_width()//2, white_bgrect.centery-user_surf.get_height()//2))

#Function to get the required credentials from the user.
def getRequiredInfo(textBoxNames,font,text_color='black',start_pos_y=50):
    display_surf=pygame.display.get_surface()
    user_strings=[]             #Holds the strings obtained from the user. This is what is returned by this function.
    textBoxSurfs=[]             #Hold the rendered surfaces for the textboxNames.
    textBoxCollideRects=[]      #The rectangles on these rendered surfaces to check for collision.
    textBoxes_left=100          #The left position of all the textboxe names.
    extra_box_space=20          #Used to maintain a bit more space in the textboxes.
    for index,textboxname in enumerate(textBoxNames):
        text_surf=font.render(textboxname,True,text_color)
        text_box=pygame.rect.Rect(textBoxes_left,start_pos_y+index*100, text_surf.get_width()+extra_box_space, text_surf.get_height()+extra_box_space)
        textBoxSurfs.append(text_surf)
        textBoxCollideRects.append(text_box)
        user_strings.append("")

    #Submit button and surface.
    submit_surf=font.render("Submit",True,text_color)
    submit_rect=pygame.rect.Rect(int((3*SCREEN_WIDTH)//4), int((3*SCREEN_HEIGHT)//8), submit_surf.get_width()+extra_box_space, submit_surf.get_height()+extra_box_space)
    submit_rect_pos=(submit_rect.centerx-submit_surf.get_width()//2,submit_rect.centery-submit_surf.get_height()//2)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:      #1st condition to check for mouse click, 2nd condition to check for left click.
                mouse_pos=pygame.mouse.get_pos()
                if submit_rect.collidepoint(mouse_pos):
                    return user_strings
            if event.type==pygame.KEYDOWN:      #If user clicks enter(which is often referred to as 'carriage return'), then return the strings.
                if event.key==pygame.K_RETURN:
                    return user_strings
                mouse_pos=pygame.mouse.get_pos()
                for index,rect in enumerate(textBoxCollideRects):
                    if rect.collidepoint(mouse_pos):
                        if event.type==pygame.K_BACKSPACE:
                            user_strings[index]=user_strings[index][:-1]
                        else:
                            user_strings[index]+=event.unicode
        
        #Blitting all the textboxes and the submit button.
        display_surf.fill('black')
        for index,text_surf in enumerate(textBoxSurfs):
            display_textbox(display_surf,text_surf,textBoxCollideRects[index],user_strings[index],text_color,font)
        pygame.draw.rect(display_surf,'white',submit_rect,0,border_radius=3)
        display_surf.blit(submit_surf,submit_rect_pos)
        pygame.display.flip()
    pass

#Function to draw a half-transparent background with a shade of the given color. Used only when displaying a screen.
def drawShadedBGScreen(display_surf,shaded_color=SCREEN_BG_SHADE_COLOR):
    pygame.draw.rect(SCREEN_BG_SHADE_SURF,shaded_color,[0,0,SCREEN_WIDTH,SCREEN_HEIGHT])       #Fills the rectangle with specified color and draws this on the surface.
    display_surf.blit(SCREEN_BG_SHADE_SURF,SCREEN_BG_SHAD_POS)

#Function to save the image of the screen whenever a different screen is going to be displayed.
def SaveGameScreen(display_surf=None):
    if(display_surf==None):
        display_surf=pygame.display.get_surface()
    rect=pygame.rect.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
    screenshot=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    screenshot.blit(display_surf,rect.topleft,area=rect)
    pygame.image.save(screenshot,os.path.join(GRAPHICS_DIR_PATH,"GameScreen.png"))
    pass


#A function to save the current screen into the given filename.
def SAVE_CURR_SCREEN(filename):
    pass


#A function which uses the DISPLAY_MSG to continuously display all the messages.
def DISPLAY_DIALOGS(DialogBox,message_box_left,message_box_top,message_box_width,message_box_height,font=pygame.font.Font(None,30)):
    if len(DialogBox)==0:
        return
    display_msg_index=0
    dialogs=list(DialogBox)
    num_of_msgs=len(dialogs)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    display_msg_index+=1

        if display_msg_index >=num_of_msgs:
            break
        

        DISPLAY_MSG(dialogs[display_msg_index],message_box_left,message_box_top,message_box_width,message_box_height,font)
        pygame.display.flip()
    pass

#A function to display a message. The function splits the message into different lines if the message is long.
def DISPLAY_MSG(message, message_box_left,message_box_top,message_box_width,message_box_height,font=pygame.font.Font(None,30)):
    display_surf=pygame.display.get_surface()
    pygame.draw.rect(display_surf,BG_COLOR,(message_box_left,message_box_top,message_box_width,message_box_height),0,border_radius=10)
    pygame.draw.rect(display_surf,BG_BORDER_COLOR,(message_box_left,message_box_top,message_box_width,message_box_height),3,border_radius=10)
    collection=[word.split(' ') for word in message.splitlines()]
    space=font.size(' ')[0]
    x=message_box_left+20
    y=message_box_top+20
    for lines in collection:
        for words in lines:
            word_surf=font.render(words,True,'white')
            word_width, word_height=word_surf.get_size()
            if x+word_width>=message_box_width:
                x=message_box_left
                y+=word_height+20
            display_surf.blit(word_surf,(x,y))

            x+=word_width+space
        x=message_box_left+20
        y+=word_height+20
    
    next_msg_prompt="'Enter' for next message"
    next_msg_surf=font.render(next_msg_prompt,False,'white')
    next_msg_rect=pygame.rect.Rect(message_box_width-next_msg_surf.get_width()-20,message_box_height-next_msg_surf.get_height()-20,next_msg_surf.get_width(),next_msg_surf.get_height())
    display_surf.blit(next_msg_surf,next_msg_rect)
    pass


# #Function to get a single sprite from the given spritesheet.
# def getSpriteFromSpriteSheet(spritesheet_path,sprite_width,sprite_height,sprite_location_left,sprite_location_top,colorKey=None):
#     spritesheet=pygame.image.load(spritesheet_path)
#     sprite=pygame.Surface((sprite_width,sprite_height)).convert_alpha()
#     sprite.blit(spritesheet,(0,0),(sprite_location_left,sprite_location_top,sprite_width,sprite_height))
#     if(colorKey==None):
#         sprite.set_colorkey(colorKey)
#     return sprite

#A function to display the given text on the screen.
debug_font=pygame.font.Font(None,30)
def debug_print(text,pos,display_surf=None):
    if display_surf==None:
        display_surf=pygame.display.get_surface()
    debug_surf=debug_font.render(str(text),'True','Black')
    display_surf.blit(debug_surf,pos)
    pass

# # Just realized this isn't needed as long as we follow the below format.
# # #ALL_BLOCKS - Has 'elem_id' as key, the block 'img' as value. This will be initialized in the Level object's using 'load_ALL_BLOCKS()'.
# #     #elem_id: 500      ==> 'Gate_being_revealed'              ==>"BROWN". The image will have id of 500. Any elem having id of 500 will slowly appear once player has unlocked achievement.
# #     #elem_id: 300      ==> 'Scientist1'                       ==>"ORANGE" color in Tiled map.
# #     #elem_id: 301      ==> 'Scientist2'                       ==>"MAGENTA" color in Tiled map.
# #     #elem_id: 302      ==> 'Scientist3'                       ==>"WHITE" color in Tiled map.

# #     #elem_id: 100      ==> 'zombie1 start position'           ==>"PINK" color in Tiled map.
# #     #elem_id: 101      ==> 'zombie2 start position'           ==>"YELLOW" color in Tiled map.
# #     #elem_id: 102      ==> 'zombie3 start position'           ==>"PURPLE" color in Tiled map.
# #     #elem_id: 103      ==> 'zombie4 start position'           ==>"BLUE" color in Tiled map.
# #     #elem_id: 104      ==> 'zombieBoss start position'        ==>"SILVER" color in Tiled map.
# #     #elem_id: 1000     ==> 'Invisible'                        ==>"RED" color in Tiled map.
    ###################################################### elem_id: 1001     ==> 'Player start position'            ==>"GREEN" color in Tiled map.
# #     #elem_id: 1003     ==> 'Transport gates'                  ==>"BLACK" color in Tiled map.
# # ALL_BLOCKS={}
# # def load_ALL_BLOCKS():
# #     ALL_BLOCKS[1000]=getSpriteFromSpriteSheet(BLOCKS_PATH,32,32,0,0,'Black')
# #     ALL_BLOCKS[1001]=getSpriteFromSpriteSheet(BLOCKS_PATH,32,32,32,0,'Black')



# ###############         MAP FOR TELEPORTING                   ##############
# #Ruin0 has 3 entraces.




# #TO_ADD_FEATURES
# #--->Must add player,enemy sprites of size 32x32 or width:32, height:64 only.
# # 1. Add the map for teleporting between maps.
# # 2. Add the functionality where the gate opens only when the code is entered.(Hint has to be displayed on the screen after some time).
# # 3. Be able to add Animations
# # 4. Be able to view inventory
# # 5. Be able to talk with NPC
# # 6. Be able to give out Quests


SUB_SURFACE=SCREEN_BG_SHADE_SURF
SUB_SURFACE.fill('green')


#This class contains the variables that can be changed in the game.
class Settings:
    def __init__(self):
        self.my_Name=None
        self.my_age=None

        #Speeds
        self.GAME_FPS=GAME_FPS
        self.PLAYER_SPEED=PLAYER_SPEED
        self.ENEMY_SPEED=ENEMY_SPEED
        self.KEYBOARD_CAMERA_SPEED=KEYBOARD_CAMERA_SPEED
        self.MOUSE_CAMERA_SPEED=MOUSE_CAMERA_SPEED

        # self.WEAPON_INFO=WEAPON_INFO
        # self.MAGIC_INFO=MAGIC_INFO
        # self.ZOMBIE_ENEMIES_INFO=ZOMBIE_ENEMIES_INFO

        #A dictionary of key(weapon name) and value(a dictionary containing {cooldown_time, damage})
        self.WEAPON_INFO={           #The last 3 attributes are list containing the said values for cooldown, damage respectively in the list.
            # 'whip': {'cooldown':150, 'damage': 15, 'min_val': [100,10], 'max_val': [300,30], 'cost_to_upgrade_one_unit': [10,50]},     
            'sword':{'cooldown': 200, 'damage': 30, 'min_val': [100,20], 'max_val': [300,50], 'cost_to_upgrade_one_unit': [10,40]},
            'lance':{'cooldown': 100, 'damage': 20, 'min_val': [100,20], 'max_val': [200,40], 'cost_to_upgrade_one_unit': [10,40]},
            'axe':{'cooldown': 150, 'damage': 40, 'min_val': [100,30], 'max_val': [200,70], 'cost_to_upgrade_one_unit': [10,40]},
            # 'gun':{'cooldown': 200, 'damage': 30, 'min_val': [150,20], 'max_val': [300,40], 'cost_to_upgrade_one_unit': [10,50]}
        }
        self.MAGIC_INFO={
            'flame':{'cooldown':100,'strength':15,'cost':30, 'min_val': [100,15,25], 'max_val': [250,50,40], 'cost_to_upgrade_one_unit': [20,50,70]},
            'heal':{'cooldown':150,'strength':20,'cost':40, 'min_val': [100,15,25], 'max_val': [250,40,40], 'cost_to_upgrade_one_unit': [20,50,80]}
        }
        self.ZOMBIE_ENEMIES_INFO={
            'zombie1':{'health':100,'exp':20,'damage':10, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'claw', 'speed':ENEMY_SPEED},
            'zombie2':{'health':150,'exp':30,'damage':20, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'claw', 'speed':ENEMY_SPEED},
            'zombie3':{'health':200,'exp':50,'damage':50, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+1, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'slash', 'speed':ENEMY_SPEED+1},
            'zombie4':{'health':400,'exp':100,'damage':75, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+2, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'sparkle', 'speed':ENEMY_SPEED+2},
            'zombieBoss':{'health':1000,'exp':500,'damage':150, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+4, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'thunder', 'speed':ENEMY_SPEED+5}
        }


        #Attributes you can change .
        self.attributes_num=10         #To change the 5 speed attributes, WEAPON_INFO, MAGIC_INFO attributes.
        self.attribute_names=[         #The list contains in order [min_val,max_val,cost_of_exp_for_increasing_by_one_unit]
            "GAME_FPS",
            "PLAYER_SPEED",
            "ENEMY_SPEED",
            "KEYBOARD_CAMERA_SPEED",
            "MOUSE_CAMERA_SPEED",
            "Weapon Cooldown",              
            "Wepon Damage",
            "Magic Cooldown",
            "Magic Strength",
            "Magic Cost",
        ]

        #Attributes for selecting the value you want to change.
        self.selected_attr_index=0
        self.selected_time=None
        self.can_select_different=True
        self.can_select_duration=400

        #Value changer dimensions.
        self.val_changer_height=int((3*SCREEN_HEIGHT)//9)
        self.val_changer_width=int(SCREEN_WIDTH//6)
        self.width_gap=35
        self.height_gap=60
        self.base_height=200

        self.items=None
        self.create_items()

        self.info_font=pygame.font.Font(None,40)

        pass

    def reset_settings(self):
        self.GAME_FPS=GAME_FPS
        self.PLAYER_SPEED=PLAYER_SPEED
        self.ENEMY_SPEED=ENEMY_SPEED
        self.KEYBOARD_CAMERA_SPEED=KEYBOARD_CAMERA_SPEED
        self.MOUSE_CAMERA_SPEED=MOUSE_CAMERA_SPEED

        self.WEAPON_INFO={           #The last 3 attributes are list containing the said values for cooldown, damage respectively in the list.
            # 'whip': {'cooldown':150, 'damage': 15, 'min_val': [100,10], 'max_val': [300,30], 'cost_to_upgrade_one_unit': [10,50]},     
            'sword':{'cooldown': 200, 'damage': 30, 'min_val': [100,20], 'max_val': [300,50], 'cost_to_upgrade_one_unit': [10,40]},
            'lance':{'cooldown': 100, 'damage': 20, 'min_val': [100,20], 'max_val': [200,40], 'cost_to_upgrade_one_unit': [10,40]},
            'axe':{'cooldown': 150, 'damage': 40, 'min_val': [100,30], 'max_val': [200,70], 'cost_to_upgrade_one_unit': [10,40]},
            # 'gun':{'cooldown': 200, 'damage': 30, 'min_val': [150,20], 'max_val': [300,40], 'cost_to_upgrade_one_unit': [10,50]}
        }
        self.MAGIC_INFO={
            'flame':{'cooldown':100,'strength':15,'cost':30, 'min_val': [100,15,25], 'max_val': [250,50,40], 'cost_to_upgrade_one_unit': [20,50,70]},
            'heal':{'cooldown':150,'strength':20,'cost':40, 'min_val': [100,15,25], 'max_val': [250,40,40], 'cost_to_upgrade_one_unit': [20,50,80]}
        }
        self.ZOMBIE_ENEMIES_INFO={
            'zombie1':{'health':100,'exp':20,'damage':10, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'claw', 'speed':ENEMY_SPEED},
            'zombie2':{'health':150,'exp':30,'damage':20, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'claw', 'speed':ENEMY_SPEED},
            'zombie3':{'health':200,'exp':50,'damage':50, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+1, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'slash', 'speed':ENEMY_SPEED+1},
            'zombie4':{'health':400,'exp':100,'damage':75, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+2, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'sparkle', 'speed':ENEMY_SPEED+2},
            'zombieBoss':{'health':1000,'exp':500,'damage':150, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+4, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'thunder', 'speed':ENEMY_SPEED+5}
        }
        
        for item in self.items:
            item.has_been_selected=False
        pass

    def apply_cooldown(self):
        if not self.can_select_different:
            if pygame.time.get_ticks()-self.selected_time >= self.can_select_duration:
                self.can_select_different=True

    def select_the_item(self,can_change_values):
        keys=pygame.key.get_pressed()
        
        if(self.can_select_different and can_change_values):
            previous_index=self.selected_attr_index
            if(keys[pygame.K_RIGHT]):
                self.selected_attr_index+=1
                self.can_select_different=False
                self.selected_time=pygame.time.get_ticks()
                pass
            elif(keys[pygame.K_LEFT]):
                self.selected_attr_index-=1
                self.can_select_different=False
                self.selected_time=pygame.time.get_ticks()
                pass
            elif(keys[pygame.K_UP]):
                self.selected_attr_index-=5         #Assuming there are 5 value changers being displayed in one row.
                self.can_select_different=False
                self.selected_time=pygame.time.get_ticks()
                pass
            elif(keys[pygame.K_DOWN]):
                self.selected_attr_index+=5         #Assuming there are 5 value changers being displayed in one row.
                self.can_select_different=False
                self.selected_time=pygame.time.get_ticks()
                pass
            
            #Handling the cases when you go out of the index list and when you go to the end of a row/column.
            if(self.selected_attr_index==5 and previous_index==4):
                self.selected_attr_index=0
            elif(self.selected_attr_index==-1 and previous_index==0):
                self.selected_attr_index=4
            elif(self.selected_attr_index==4 and previous_index==5):
                self.selected_attr_index=9
            elif(self.selected_attr_index==10 and previous_index==9):
                self.selected_attr_index=5
            
            
            if(self.selected_attr_index>=self.attributes_num):
                self.selected_attr_index=self.selected_attr_index-self.attributes_num
            if(self.selected_attr_index<0):
                self.selected_attr_index=self.selected_attr_index+self.attributes_num
            debug_print(self.selected_attr_index,(700,300))
        pass

    #A method to display the name, age.
    def display_my_information(self,display_surf):
        name_surf=self.info_font.render(self.my_Name,False,'black')
        age_surf=self.info_font.render(self.my_age,False,'black')

        display_surf.blit(name_surf,(SCREEN_WIDTH//3,20))
        display_surf.blit(age_surf,(SCREEN_WIDTH//2 + SCREEN_WIDTH//6,20))
        # print(self.my_Name,self.my_age)
        pass

    def display_settings(self,display_surf,Game,can_change_values=0):
        self.display_my_information(display_surf)
        self.select_the_item(can_change_values)
        self.apply_cooldown()

        for index,item in enumerate(self.items):
            if(index<5):        #Displaying the speeds, so we select the current val by doing level.GameSettings.attr_name.
                attr_name=self.attribute_names[index]
                upgrading_costs=COST_TO_UPGRADE_SPEEDS[attr_name]

                item.display_item(display_surf,attr_name,self.selected_attr_index,getattr(Game.GameSettings,attr_name),upgrading_costs[0],upgrading_costs[1],upgrading_costs[2])
            elif(index<7):      #Displaying the WEAPON_INFO, so we select the values those of the current weapon.
                weaponName=Game.player.weapon_name
                curr_weapon=Game.GameSettings.WEAPON_INFO[weaponName]
                curr_val=[curr_weapon['cooldown'],curr_weapon['damage']]
                # print('curr_val for weapon: ',curr_val)
                item.display_item(display_surf,weaponName,self.selected_attr_index,curr_val[index-5],curr_weapon['min_val'][index-5],curr_weapon['max_val'][index-5],curr_weapon['cost_to_upgrade_one_unit'][index-5])
            else:
                # print('index-7', index-7)
                magicName=Game.player.magic_name
                curr_magic=Game.GameSettings.MAGIC_INFO[magicName]
                curr_val=[curr_magic['cooldown'],curr_magic['strength'],curr_magic['cost']]
                # print('curr magic ', curr_val)
                item.display_item(display_surf,magicName,self.selected_attr_index,curr_val[index-7],curr_magic['min_val'][index-7],curr_magic['max_val'][index-7],curr_magic['cost_to_upgrade_one_unit'][index-7])

    def create_items(self):
        self.items=[]
        extra_attr_names=['(Cooldown)','(Damage)','(Cooldown)', '(Strength)','(Cost)']
        for index,item_name in enumerate(self.attribute_names):
            left=self.width_gap+(index%5)*self.val_changer_width+self.width_gap*(index%5)
            top=self.base_height+int(index//5)*(self.val_changer_height + self.height_gap)
            extra_attr=None
            if(index>4):
                extra_attr=extra_attr_names[index-5]
            item=Item(left,top,self.val_changer_width,self.val_changer_height,index,UI_TEXT_FONT,extra_attr)
            self.items.append(item)
        pass
    
    def apply_changes(self,game):
        for index,item in enumerate(self.items):
            if index<5:
                item.apply_changes(self.selected_attr_index,self.attribute_names[index],game,COST_TO_UPGRADE_SPEEDS[self.attribute_names[index]][0],COST_TO_UPGRADE_SPEEDS[self.attribute_names[index]][1])
            elif index<7:
                weaponName=game.player.weapon_name
                weapon=game.GameSettings.WEAPON_INFO[weaponName]
                extra_attr_name=['cooldown','damage']
                item.apply_changes(self.selected_attr_index,weaponName,game,weapon['min_val'][index-5],weapon['max_val'][index-5],extra_attr_name[index-5])
                pass
            elif index<10:
                magicName=game.player.magic_name
                magic=game.GameSettings.MAGIC_INFO[magicName]
                extra_attr_name=['cooldown','strength','cost']
                item.apply_changes(self.selected_attr_index,magicName,game,magic['min_val'][index-7],magic['max_val'][index-7],extra_attr_name[index-7])
                pass
        pass

class Item:
    def __init__(self,left,top,width,height,index,font,extra_attr_name=None):
        self.rect=pygame.rect.Rect(left,top,width,height)
        self.index=index
        self.font=font
        self.extra_attr_name=extra_attr_name

        self.top=self.rect.midtop+pygame.math.Vector2(0,35)
        self.bottom=self.rect.midbottom-pygame.math.Vector2(0,55)
        if(extra_attr_name!=None):
            self.top=self.top + pygame.math.Vector2(0,20)

        self.curr_rect=pygame.rect.Rect(self.top[0]-10,self.top[1],20,5)
        self.curr_from_bottom_pos=None
        self.has_been_selected=False
        self.cost_for_upgrading=None
        self.mouse_collider_rect=pygame.rect.Rect(self.rect.centerx-10,self.top[1],20,self.bottom[1]-self.top[1])

    def apply_changes(self,selected_index,attr_name,game,min_val,max_val,extra_attr_name=None):
        if selected_index==self.index:
            #Find the curr_val value.
            if(self.has_been_selected and game.player.exp >= self.cost_for_upgrading):
                game.player.exp -= self.cost_for_upgrading
                self.cost_for_upgrading=0
                self.has_been_selected=False
                #Based on mouse pos, get the curr_val.
                #self.curr_from_bottom_pos is the selected position to change the value to.
                height_of_line=self.bottom[1]-self.top[1]
                distance_from_bottom=self.bottom[1]-self.curr_from_bottom_pos
                curr_new_val=min_val+ (((max_val-min_val)*distance_from_bottom)//height_of_line)
                pass
            elif(self.has_been_selected):
                self.cost_for_upgrading=0
                self.has_been_selected=False
                #DISPLAY A MESSAGE SAYING COULD NOT APPLY.
                return
            
            if self.index<5:
                # curr_val=0
                setattr(game.GameSettings,attr_name,curr_new_val)
                pass
            elif self.index<7:
                # curr_val=0
                game.GameSettings.WEAPON_INFO[attr_name][extra_attr_name]=curr_new_val
                pass
            elif self.index<10:
                # curr_val=0
                game.GameSettings.MAGIC_INFO[attr_name][extra_attr_name]=curr_new_val
                pass

    def select_the_upgraded_val(self,is_selected,curr_val,min_val,max_val,cost_of_one_unit):
        if(is_selected):
            is_left_click=pygame.mouse.get_pressed()[0]
            mouse_pos=pygame.mouse.get_pos()
            if(is_left_click and self.mouse_collider_rect.collidepoint(mouse_pos)):
                self.curr_from_bottom_pos=mouse_pos[1]
                self.has_been_selected=True

                height_of_line=self.bottom[1]-self.top[1]
                curr_val_height_from_bottom=((curr_val-min_val)*height_of_line)//(max_val-min_val)
                curr_pos=self.bottom[1]-curr_val_height_from_bottom
                self.cost_for_upgrading=(abs(curr_pos-mouse_pos[1])*(cost_of_one_unit*(max_val-min_val)))//(height_of_line)
            pass
        pass

    def display_name(self,surface,name,cost,curr_val,is_selected):
        txt_color=TEXT_COLOR_SELECTED if is_selected else TEXT_COLOR
        #Displaying attribute name
        text_surf=self.font.render(str(name).capitalize(),True,txt_color)
        text_rect=text_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0,10))
        surface.blit(text_surf,text_rect)

        #Displaying the extra attribute name if any.
        if(self.index>4):
            extra_text_surf=self.font.render(str(self.extra_attr_name),True,txt_color)
            surface.blit(extra_text_surf,(text_rect.centerx-extra_text_surf.get_width()//2, text_rect.bottom + 10))

        #Displaying the current value.
        curr_val_surf=self.font.render(f'Current val: {curr_val}',False,txt_color)
        surface.blit(curr_val_surf,(self.rect.centerx-curr_val_surf.get_width()//2,self.rect.bottom-2*curr_val_surf.get_height()-20))


        #Displaying the cost.
        cost_surf=self.font.render(f'upgrade cost: {cost}', False, txt_color)
        surface.blit(cost_surf,(self.rect.centerx-cost_surf.get_width()//2, self.rect.bottom-cost_surf.get_height()-10))
        pass

    def display_bar(self,surface,curr_val,min_val,max_val,is_selected):
        bar_color=BAR_COLOR_SELECTED if is_selected else BAR_COLOR
        # pygame.draw.rect(surface,'blue',self.mouse_collider_rect)     #If you uncomment this, you will understand the need for the above dimensions of the self.mouse_collide_rect rectangle.
        #Drawing the line.
        pygame.draw.line(surface,bar_color,self.top,self.bottom,width=3)

        #Drawing the curr_rect for curr_val
        curr_pos=None
        if(self.has_been_selected):
            curr_pos=self.curr_from_bottom_pos
            # self.curr_rect=pygame.rect.Rect(self.top[0]-10,self.curr_from_bottom_pos,20,5)
            pass
        else:
            height_of_line=self.bottom[1]-self.top[1]
            curr_val_height_from_bottom=((curr_val-min_val)*height_of_line)//(max_val-min_val)
            curr_pos=self.bottom[1]-curr_val_height_from_bottom
            # self.curr_rect=pygame.rect.Rect(self.top[0]-10,self.bottom[1]-curr_val_height_from_bottom,20,5)
        self.curr_rect=pygame.rect.Rect(self.top[0]-10,curr_pos,20,5)
        pygame.draw.rect(surface,bar_color,self.curr_rect)
        pass

    #Min val is bottom position. Max val is top position.
    def display_item(self,display_surf,attr_name,selected_index,curr_val,min_val,max_val,cost_to_upgrade_by_one_unit,newly_selected_val=None):
        is_selected=1 if (self.index==selected_index) else 0
        # self.has_been_selected=False
        # self.curr_rect=None
        # self.curr_from_bottom_pos=None
        if is_selected:
            pygame.draw.rect(display_surf,BG_COLOR_SELECTED, self.rect,border_radius=3)
        else:
            pygame.draw.rect(display_surf,BG_COLOR, self.rect,border_radius=3)
        pygame.draw.rect(display_surf,BG_BORDER_COLOR,self.rect,4,border_radius=3)

        self.select_the_upgraded_val(is_selected,curr_val,min_val,max_val,cost_to_upgrade_by_one_unit)
        # cost_to_upgrade=cost_to_upgrade_by_one_unit
        cost_to_upgrade=0
        if(self.has_been_selected):
            cost_to_upgrade=self.cost_for_upgrading
            pass
        self.display_name(display_surf,attr_name,cost_to_upgrade,curr_val,is_selected)
        self.display_bar(display_surf,curr_val,min_val,max_val,is_selected)
        pass