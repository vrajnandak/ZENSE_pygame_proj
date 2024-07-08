import pygame
from Settings import *
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement     #To allow the enemies to move diagonally as well while searching the path.

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
        self.direction=pygame.math.Vector2()
        self.attack_radius=ENEMY_ATTACK_RADIUS

    def update_direction(self,player):
        self.direction.x=player.rect.centerx-self.rect.centerx
        self.direction.y=player.rect.centery-self.rect.centery
        pass

    def handle_collisions(self,direction,level):
        level.collision_detector.handle_spritegroup_collision(self,ENEMY_SPEED,direction,level.transport_sprites,1)
        level.collision_detector.handle_spritegroup_collision(self,ENEMY_SPEED,direction,level.obstacle_sprites,0)
        level.collision_detector.handle_spritegroup_collision(self,ENEMY_SPEED,direction,level.enemy_sprites,0)
        level.collision_detector.handle_spritegroup_collision(self,ENEMY_SPEED,direction,[level.player],0)
        pass

    def update(self,display_surf,offset,level):
        self.update_direction(level.player)

        #Moving the enemy sprite if player within range.
        if(self.direction.magnitude()<=self.attack_radius):
            if(self.direction.magnitude()!=0):
                self.direction=self.direction.normalize()
            self.rect.x+=self.direction.x*ENEMY_SPEED
            self.handle_collisions("Horizontal",level)
            self.rect.y+=self.direction.y*ENEMY_SPEED
            self.handle_collisions("Vertical",level)
            pass
        else:   #If there is even a bit of residual movement or a lag, there should still be collision detection done.
            self.handle_collisions("horizontal",level)
            self.handle_collisions("Vertical",level)

        self.draw(display_surf,offset)
        pass

    def draw(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)
        pass

    class ToPlayerPathFinder:
        def __init__(self,map_matrix):
            self.matrix=map_matrix
            self.grid=Grid(matrix=map_matrix)
            self.img=pygame.Surface((BASE_SIZE,BASE_SIZE))
            self.img.fill('black')

        def draw_active_cell(self,display_surf):
            mouse_pos=pygame.mouse.get_pos()
            col=mouse_pos[0]//BASE_SIZE
            row=mouse_pos[1]//BASE_SIZE
            display_surf.blit(self.img,(col,row))

        def update(self):
            self.draw_active_cell()