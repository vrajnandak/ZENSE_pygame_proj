import pygame
import os
from csv import reader

#Others
GAME_TITLE="Time Rift Rescue"


#Speeds
GAME_FPS=30
PLAYER_SPEED=10

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

#Folder Paths
WORKING_DIRECTORY_PATH=os.getcwd()
GRAPHICS_DIR_PATH=os.path.join(WORKING_DIRECTORY_PATH,"graphics")
MAPS_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"Ruins")            #Folder path to getting Maps and Other Graphics
BASEMAP_NAME="BaseMap.png"                          #Name of Floor maps which are basically the 1st drawn image.
FLOORINFO_DIR_NAME="FloorInfo"
BLOCKS_PATH=os.path.join(GRAPHICS_DIR_PATH,"Blocks.png")

#Function to get a single sprite from the given spritesheet.
def getSpriteFromSpriteSheet(spritesheet_path,sprite_width,sprite_height,sprite_location_left,sprite_location_top,colorKey=None):
    spritesheet=pygame.image.load(spritesheet_path)
    sprite=pygame.Surface((sprite_width,sprite_height)).convert_alpha()
    sprite.blit(spritesheet,(0,0),(sprite_location_left,sprite_location_top,sprite_width,sprite_height))
    if(colorKey==None):
        sprite.set_colorkey(colorKey)
    return sprite

# Just realized this isn't needed as long as we follow the below format.
# #ALL_BLOCKS - Has 'elem_id' as key, the block 'img' as value. This will be initialized in the Level object's using 'load_ALL_BLOCKS()'.
#     #elem_id: 1000     ==> 'Invisible'                        ==>"RED" color in Tiled map.
#     #elem_id: 1001     ==> 'Player start position'            ==>"GREEN" color in Tiled map.
#     #elem_id: 1002     ==> 'Enemy start position'             ==>"YELLOW" color in Tiled map.
#     #elem_id: 1003     ==> 'Transport gates'                  ==>"BLACK" color in Tiled map.
#     #elem_id: 1004     ==> 'Strong enemy start position'      ==>"BLUE" color in Tiled map.
# ALL_BLOCKS={}
# def load_ALL_BLOCKS():
#     ALL_BLOCKS[1000]=getSpriteFromSpriteSheet(BLOCKS_PATH,32,32,0,0,'Black')
#     ALL_BLOCKS[1001]=getSpriteFromSpriteSheet(BLOCKS_PATH,32,32,32,0,'Black')
