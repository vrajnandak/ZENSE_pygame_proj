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
        self.attack_radius=ENEMY_ATTACK_RADIUS

    def update_vector2_player(self,player):
        self.vector_to_player.x=player.rect.centerx-self.rect.centerx
        self.vector_to_player.y=player.rect.centery-self.rect.centery
        pass

    def get_pixel_counter(self,sprite,movement,enemy_moved,is_horizontal,is_vertical):
        lower_lim=0
        upper_lim=abs(int(enemy_moved))
        left=lower_lim
        right=upper_lim
        while left<=right:
            mid=left+(right-left)//2
            offset_x=sprite.rect.left-self.rect.left-mid*movement*is_horizontal      #Considering only to add horizontal movement.
            offset_y=sprite.rect.top-self.rect.top-mid*movement*is_vertical          #Considering only to add vertical movement.
            offset=(offset_x,offset_y)
            if self.mask.overlap(sprite.mask,offset):
                right=mid-1
            else:
                left=mid+1
                pass
        return right
        pass

    def handle_horizontal_collision(self,sprite):
        movement= 1 if self.vector_to_player.x > 0 else -1
        enemy_moved=self.vector_to_player.x*ENEMY_SPEED
        self.rect.x-=enemy_moved        #Undoing the added direction in x-axis as this caused mask collision.
        can_move_pixel=self.get_pixel_counter(sprite,movement,enemy_moved,1,0)
        self.rect.x+=movement*can_move_pixel
        pass

    def handle_vertical_collision(self,sprite):
        movement=1 if self.vector_to_player.y > 0 else -1
        enemy_moved=self.vector_to_player.y*ENEMY_SPEED
        self.rect.y-=enemy_moved        #Undoing the added direction in y-axis as this caused the mask collision.
        can_move_pixel=self.get_pixel_counter(sprite,movement,enemy_moved,0,1)
        self.rect.y+=movement*can_move_pixel
        pass

    def handle_spriteGroup_collisions(self,direction,spriteGroup):
        for sprite in spriteGroup:
            if sprite.rect.colliderect(self.rect) and (sprite.rect.center!=self.rect.center):       #The second condition is to check if it is the sprite calling this function itself.
                if(self.mask.overlap(sprite.mask,(sprite.rect.left-self.rect.left, sprite.rect.top-self.rect.top))):
                    if(direction=="Horizontal"):
                        self.handle_horizontal_collision(sprite)
                    elif(direction=="Vertical"):
                        self.handle_vertical_collision(sprite)
                # if(direction=="Horizontal"):
                #     self.rect.x-=self.vector_to_player.x*ENEMY_SPEED
                # elif(direction=="Vertical"):
                #     self.rect.y-=self.vector_to_player.y*ENEMY_SPEED
                pass
        pass

    def handle_collisions(self,direction,level):
        self.handle_spriteGroup_collisions(direction,level.transport_sprites)
        self.handle_spriteGroup_collisions(direction,level.obstacle_sprites)
        self.handle_spriteGroup_collisions(direction,level.enemy_sprites)
        self.handle_spriteGroup_collisions(direction,[level.player])
        pass

    def update(self,display_surf,offset,level):
        self.update_vector2_player(level.player)

        #Moving the enemy sprite if player within range.
        if(self.vector_to_player.magnitude()<=self.attack_radius):
            if(self.vector_to_player.magnitude()!=0):
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