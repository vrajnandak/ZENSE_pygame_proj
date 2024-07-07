# import pygame
# import os

# pygame.init()
# WORKING_DIRECTORY_PATH=os.getcwd()
# GRAPHICS_DIR_PATH=os.path.join(WORKING_DIRECTORY_PATH,"graphics")
# def getSpriteFromSpriteSheet(spritesheet_path,sprite_width,sprite_height,sprite_location_left,sprite_location_top,colorKey=None):
#     spritesheet=pygame.image.load(spritesheet_path)
#     sprite=pygame.Surface((sprite_width,sprite_height)).convert_alpha()
#     sprite.blit(spritesheet,(0,0),(sprite_location_left,sprite_location_top,sprite_width,sprite_height))
#     if(colorKey==None):
#         sprite.set_colorkey(colorKey)
#     return sprite

# Window=pygame.display.set_mode((550,550),pygame.RESIZABLE)
# img=getSpriteFromSpriteSheet(os.path.join(GRAPHICS_DIR_PATH,"Blocks.png"),32,32,32,0,'Black')
# while True:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             pygame.quit()
#     Window.fill('white')
#     surf=pygame.image.load('EXAMPLE_IMAGES_FOR_SPRITES/Archaeologist_sprites.png')    #The player sprite to be used is the 'Archaeologist_sprites.png'
#     surf=pygame.transform.scale(surf,(1024,448))

#     Window.blit(surf,(0,0))
#     Window.blit(img,(1100,0))
#     pygame.display.flip()

# class Player:
#     def __init__(self, name):
#         self.name = name
#         self.level = 1  # Example attribute
#         self.helper = Player.PlayerHelperMethods(self)  # Pass a reference to self

#     def play(self):
#         print(f"{self.name} is playing at level {self.level}.")
#         self.helper.do_something()

#     def pause(self):
#         print(f"{self.name} paused.")

#     class PlayerHelperMethods:
#         def __init__(self, player_instance):
#             self.player = player_instance
        
#         def do_something(self):
#             # Accessing attributes from the outer class and potentially modifying them
#             print(f"Helper method doing something for {self.player.name} at level {self.player.level}.")
#             # Modifying the outer class attribute]
#             self.player.level+=3

# # Example usage:
# player = Player("Alice")
# player.play()
# player.pause()
# player.play()
# player.pause()


# import pygame
# import os
# # from TMPPortal import Portal
# pygame.init()
# pygame.font.init()

# current_Dir=os.getcwd()
# current_Dir=os.path.join(current_Dir,"graphics")
# current_Dir=os.path.join(current_Dir,"Ruins")
# current_Dir=os.path.join(current_Dir,"Ruin0")
# current_Dir=os.path.join(current_Dir,"Portals")
# # current_Dir=os.path.join(current_Dir,"1.png")
# screen=pygame.display.set_mode((500,500))
# # img=pygame.image.load(current_Dir)
# # img_rect=img.get_rect(topleft=(0,0))
# print('curren',current_Dir)
# # print('img size: ',img_rect.width,img_rect.height)
# # portal=Portal((100,100),current_Dir)
# while True:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             pygame.quit()
#             break
#     # screen.fill('white')
#     # portal.update(screen,pygame.math.Vector2(0,0))
#     # screen.blit(img,(0,0))
#     pygame.display.flip()

import time
my_timer_start=time.time()
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

my_matrix=[
    [1,1,1,0,1,1],
    [1,0,1,1,1,1],
    [1,0,0,1,1,1]
]
my_grid=Grid(matrix=my_matrix)
start_x=0       #Starting cell col number
start_y=0       #Starting cell row number
start_cell=my_grid.node(start_x,start_y)
end_x=5
end_y=2
end_cell=my_grid.node(end_x,end_y)

#Create a finder with a movement style.
finder=AStarFinder()

#path is as implied, runs is the number of cells you have to go through
path,runs=finder.find_path(start_cell,end_cell,my_grid)
my_timer_end=time.time()
print(path,runs)
print("Total time: ", my_timer_end-my_timer_start)