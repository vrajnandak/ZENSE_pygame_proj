import pygame
import os
from csv import reader
import sys

pygame.init()
pygame.font.init()


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
ENEMY_ATTACK_RADIUS=12         #A radius 5 BASE_SIZE's
    #A dictionary of key(weapon name) and value(a dictionary containing {cooldown_time, damage})
WEAPON_INFO={
    'whip': {'cooldown':150, 'damage': 15},
    'sword':{'cooldown': 200, 'damage': 30},
    'lance':{'cooldown': 100, 'damage': 20},
    'axe':{'cooldown': 150, 'damage': 40},
    'gun':{'cooldown': 200, 'damage': 30}
}                 

#Sizes
BASE_SIZE=32
SCREEN_WIDTH=1240
SCREEN_HEIGHT=600
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


#Speeds
GAME_FPS=30
PLAYER_SPEED=10
ENEMY_SPEED=5
KEYBOARD_CAMERA_SPEED=25
MOUSE_CAMERA_SPEED=25


#Folder Paths
WORKING_DIRECTORY_PATH=os.getcwd()
SAVED_DATA_DIR_PATH=os.path.join(WORKING_DIRECTORY_PATH,"SavedData")
GRAPHICS_DIR_PATH=os.path.join(WORKING_DIRECTORY_PATH,"graphics")
PLAYER_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"Player")
MAPS_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"Ruins")            #Folder path to getting Maps and Other Graphics
BASEMAP_NAME="BaseMap.png"                          #Name of Floor maps which are basically the 1st drawn image.
FLOORINFO_DIR_NAME="FloorInfo"
BLOCKS_PATH=os.path.join(GRAPHICS_DIR_PATH,"Blocks.png")


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
def getRequiredInfo(textBoxNames,font,text_color='black'):
    display_surf=pygame.display.get_surface()
    user_strings=[]             #Holds the strings obtained from the user. This is what is returned by this function.
    textBoxSurfs=[]             #Hold the rendered surfaces for the textboxNames.
    textBoxCollideRects=[]      #The rectangles on these rendered surfaces to check for collision.
    textBoxes_left=100          #The left position of all the textboxe names.
    extra_box_space=20          #Used to maintain a bit more space in the textboxes.
    for index,textboxname in enumerate(textBoxNames):
        text_surf=font.render(textboxname,True,text_color)
        text_box=pygame.rect.Rect(textBoxes_left,50+index*150, text_surf.get_width()+extra_box_space, text_surf.get_height()+extra_box_space)
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
            if event.type==pygame.KEYDOWN:
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

# #Function to display the textbox along with the value in the string.
# def display_textbox(display_surf,text_rect,textbox_name,user_info,font):
#     #Displaying the textbox name.
#     text_surface=font.render(textbox_name, True, 'white')
#     display_surf.blit(text_surface,(text_rect.left+text_surface.get_width()//2, text_rect.top+text_surface.get_height()//2))

#     #Displaying the string right beside it.
#     user_surface=font.render(user_info,True,'black')
#     white_bg_width=user_surface.get_width()
#     if(len(user_info)>0):
#         white_bg_width+=20
#     white_bg_box=pygame.rect.Rect(text_rect.left+text_surface.get_width(), text_rect.top, white_bg_width,user_surface.get_height())
#     pygame.draw.rect(display_surf,'white',white_bg_box,0,border_radius=3)
#     display_surf.blit(user_surface,(text_rect.left + text_surface.get_width() + 10, text_rect.top))

#     pass

# #Function to run the event loop and get the required information from the user.
# def getReqInfo(textboxNames, font):
#     #Getting the display surface.
#     display_surf=pygame.display.get_surface()

#     #Making a rectangle for each textbox values. This is for checking the mouse collision with the textboxName
#     display_rect=[]
#     user_strings=[]         #Will hold the information obtained from keyboard.
#     for i in range(len(textboxNames)):
#         box_rect=pygame.rect.Rect(100,50+i*50,100,30)
#         display_rect.append(box_rect)
#         user_strings.append("")

#     #Submit button.
#     submit_rect=pygame.rect.Rect(SCREEN_WIDTH_HALF + 100,SCREEN_HEIGHT_HALF,100,80)
#     submit_surf=font.render("Submit",True,'black')
#     submit_surf_pos=(submit_rect.centerx-submit_surf.get_width()//2, submit_rect.centery-submit_surf.get_height()//2)

#     while True:
#         for event in pygame.event.get():
#             if event.type==pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:      #1st condition to check for mouse click, 2nd condition to check for left click.
#                 mouse_pos=pygame.mouse.get_pos()
#                 if submit_rect.collidepoint(mouse_pos):
#                     return user_strings
#             if event.type==pygame.KEYDOWN:
#                 mouse_pos=pygame.mouse.get_pos()
#                 for index,rect in enumerate(display_rect):
#                     if rect.collidepoint(mouse_pos):
#                         if event.type==pygame.K_BACKSPACE:
#                             user_strings[index]=user_strings[index][:-1]
#                         else:
#                             user_strings[index]+=event.unicode
        
#         #Black background.
#         display_surf.fill('black')

#         #Displaying all the textboxes.
#         for index,rect in enumerate(display_rect):
#             display_textbox(display_surf,rect,textboxNames[index],user_strings[index],font)
#             pygame.draw.rect(display_surf,'yellow',rect,3,border_radius=3)
        
#         #Displaying the submit button.
#         pygame.draw.rect(display_surf,'white',submit_rect,border_radius=3)
#         display_surf.blit(submit_surf,submit_surf_pos)
#         pygame.display.flip()
#     pass

#Function to draw a half-transparent background with a shade of the given color. Used only when displaying a screen.
def drawShadedBGScreen(display_surf,shaded_color=SCREEN_BG_SHADE_COLOR):
    pygame.draw.rect(SCREEN_BG_SHADE_SURF,shaded_color,[0,0,SCREEN_WIDTH,SCREEN_HEIGHT])       #Fills the rectangle with specified color and draws this on the surface.
    display_surf.blit(SCREEN_BG_SHADE_SURF,SCREEN_BG_SHAD_POS)

#Function to get a single sprite from the given spritesheet.
def getSpriteFromSpriteSheet(spritesheet_path,sprite_width,sprite_height,sprite_location_left,sprite_location_top,colorKey=None):
    spritesheet=pygame.image.load(spritesheet_path)
    sprite=pygame.Surface((sprite_width,sprite_height)).convert_alpha()
    sprite.blit(spritesheet,(0,0),(sprite_location_left,sprite_location_top,sprite_width,sprite_height))
    if(colorKey==None):
        sprite.set_colorkey(colorKey)
    return sprite

#A function to display the given text on the screen.
debug_font=pygame.font.Font(None,30)
def debug_print(text,pos,display_surf):
    debug_surf=debug_font.render(str(text),'True','Black')
    display_surf.blit(debug_surf,pos)
    pass

# Just realized this isn't needed as long as we follow the below format.
# #ALL_BLOCKS - Has 'elem_id' as key, the block 'img' as value. This will be initialized in the Level object's using 'load_ALL_BLOCKS()'.
#     #elem_id: 500      ==> 'Gate_being_revealed'              ==>"None". The image will have id of 500. Any elem having id of 500 will slowly appear once player has unlocked achievement.
#     #elem_id: 1000     ==> 'Invisible'                        ==>"RED" color in Tiled map.
#     #elem_id: 1001     ==> 'Player start position'            ==>"GREEN" color in Tiled map.
#     #elem_id: 1002     ==> 'Enemy start position'             ==>"YELLOW" color in Tiled map.
#     #elem_id: 1003     ==> 'Transport gates'                  ==>"BLACK" color in Tiled map.
#     #elem_id: 1004     ==> 'Strong enemy start position'      ==>"BLUE" color in Tiled map.
# ALL_BLOCKS={}
# def load_ALL_BLOCKS():
#     ALL_BLOCKS[1000]=getSpriteFromSpriteSheet(BLOCKS_PATH,32,32,0,0,'Black')
#     ALL_BLOCKS[1001]=getSpriteFromSpriteSheet(BLOCKS_PATH,32,32,32,0,'Black')



###############         MAP FOR TELEPORTING                   ##############
#Ruin0 has 3 entraces.




#TO_ADD_FEATURES
#--->Must add player,enemy sprites of size 32x32 or width:32, height:64 only.
# 1. Add the map for teleporting between maps.
# 2. Add the functionality where the gate opens only when the code is entered.(Hint has to be displayed on the screen after some time).
# 3. Be able to add Animations
# 4. Be able to view inventory
# 5. Be able to talk with NPC
# 6. Be able to give out Quests