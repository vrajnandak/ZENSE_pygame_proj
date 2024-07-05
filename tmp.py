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

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1  # Example attribute
        self.helper = Player.PlayerHelperMethods(self)  # Pass a reference to self

    def play(self):
        print(f"{self.name} is playing at level {self.level}.")
        self.helper.do_something()

    def pause(self):
        print(f"{self.name} paused.")

    class PlayerHelperMethods:
        def __init__(self, player_instance):
            self.player = player_instance
        
        def do_something(self):
            # Accessing attributes from the outer class and potentially modifying them
            print(f"Helper method doing something for {self.player.name} at level {self.player.level}.")
            # Modifying the outer class attribute]
            self.player.level+=3

# Example usage:
player = Player("Alice")
player.play()
player.pause()
player.play()
player.pause()