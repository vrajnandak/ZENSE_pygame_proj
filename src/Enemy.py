import pygame
from Settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.pos=pos

        # ***************************************HAS TO BE REPLACED BY THE PROPER STARTING IMAGE***********************************
        self.img=pygame.image.load(
            os.path.join(
                os.path.join(
                    GRAPHICS_DIR_PATH,"Enemy"
                    ),
                    "tmpENEMY.png"
            )
        )
        self.mask=pygame.mask.from_surface(self.img)        #This will be used by the player for collision detection.
        self.rect=self.img.get_rect(topleft=self.pos)

        #Variables to move towards player.
        self.vector_to_player=pygame.math.Vector2()
        self.direction=pygame.math.Vector2()
        self.attack_radius=ENEMY_ATTACK_RADIUS

    def update_vector2_player(self,player):
        self.vector_to_player.x=player.rect.centerx-self.rect.centerx
        self.vector_to_player.y=player.rect.centery-self.rect.centery
        # self.direction.x=1 if self.vector_to_player.x > 0 else -1
        # self.direction.y=1 if self.vector_to_player.x > 0 else -1
        pass

    def handle_spriteGroup_collisions(self,direction,spriteGroup,enemy_type):
        for sprite in spriteGroup:
            if sprite.rect.colliderect(self.rect) and (sprite.rect.center!=self.rect.center):       #The second condition is to check if it is the sprite calling this function itself.
                # Enemies will only have rect collision detection and not mask collision detection, because AStar path finding algorithm might tell it to move up but since the obstacle mask collision is on, it would not move at all despite having the path.
                print(enemy_type)
                if(direction=="Horizontal"):
                    self.rect.x-=self.vector_to_player.x*ENEMY_SPEED
                elif(direction=="Vertical"):
                    self.rect.y-=self.vector_to_player.y*ENEMY_SPEED
                pass
        pass

    def handle_collisions(self,direction,level):
        self.handle_spriteGroup_collisions(direction,level.transport_sprites,1)
        self.handle_spriteGroup_collisions(direction,level.obstacle_sprites,1)
        self.handle_spriteGroup_collisions(direction,level.enemy_sprites,1)
        self.handle_spriteGroup_collisions(direction,[level.player],0)
        pass

    def update(self,display_surf,offset,level):
        self.update_vector2_player(level.player)

        #Moving the enemy sprite if player within range.
        if(self.vector_to_player.magnitude()<=self.attack_radius):
            self.vector_to_player=self.vector_to_player.normalize()
            self.rect.x+=self.vector_to_player.x*ENEMY_SPEED
            self.handle_collisions("Horizontal",level)
            self.rect.y+=self.vector_to_player.y*ENEMY_SPEED
            self.handle_collisions("Vertical",level)
            pass

        self.draw(display_surf,offset)
        pass

    def draw(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)
        # print(newpos)
        pass