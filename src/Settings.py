import pygame
import os
from csv import reader

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
MAPS_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"Ruins")            #Folder path to getting Maps and Other Graphics
BASEMAP_NAME="BaseMap.png"                          #Name of Floor maps which are basically the 1st drawn image.
FLOORINFO_DIR_NAME="FloorInfo"
BLOCKS_PATH=os.path.join(GRAPHICS_DIR_PATH,"Blocks.png")


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