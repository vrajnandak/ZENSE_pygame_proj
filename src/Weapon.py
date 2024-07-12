import pygame
from Settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)

        self.player=player
        self.player_direction=player.status.split('_')[0]

        #Weapon graphics
        # full_path=os.path.join(GRAPHICS_DIR_PATH,os.path.join("PLAYER_WEAPON",os.path.join(self.player.weapon,f'{self.player_direction}.png')))
        full_path=os.path.join(PLAYER_WEAPONS_DIRECTORY_PATH,os.path.join(self.player.weapon_name,f'{self.player_direction}.png'))
        self.img=pygame.image.load(full_path).convert_alpha()       #convert_alpha() as the background is black.
        self.rect=self.img.get_rect(center=player.rect.center)
        self.update_rect()

    def update_rect(self):
        if self.player_direction=='right':
            self.rect=self.img.get_rect(midleft=self.player.rect.midright)
            pass
        elif self.player_direction=='left':
            self.rect=self.img.get_rect(midright=self.player.rect.midleft)
            pass
        elif self.player_direction=='up':
            self.rect=self.img.get_rect(midbottom=self.player.rect.midtop)
            pass
        elif self.player_direction=='down':
            self.rect=self.img.get_rect(midtop=self.player.rect.midbottom)
            pass
        pass

    def update(self,display_surf,offset):
        self.update_rect()
        # display_surf.blit(self.img,self.rect.topleft)
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)