import pygame
from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        #There are a few methods which are called only for a specific method and nowhere else. Inorder to maintain a bit of abstraction and improve readability, I have put a separate class 'PlayerHelperMethods' which has all the helper methods. It is equivalent to the '__funcs' that are frequently used in linux kernel code.
        
        self.pos=pos

        # ***************************************HAS TO BE REPLACED BY THE PROPER STARTING IMAGE***********************************
        self.img=pygame.Surface((BASE_SIZE,BASE_SIZE))
        self.img.fill('green')
        # self.img=pygame.image.load(
        #                 os.path.join(
        #                     os.path.join((GRAPHICS_DIR_PATH),"Player"),"player.png"
        #                     )
        #                 )
        self.rect=self.img.get_rect(topleft=self.pos)
        self.mask=pygame.mask.from_surface(self.img)

        #Player Dimensions - Used for updating the tiles.
        self.width_tiles=int(self.rect.width//BASE_SIZE)
        self.height_tiles=int(self.rect.height//BASE_SIZE)

        self.direction=pygame.math.Vector2()        #A vector to only get the directions of the player.
        self.offset=pygame.math.Vector2()   #A vector to hold the position at which the player has to be blit at. The value is set in the get_offset() in Level.

        # self.dum_counter=0

    #A method to set the direction of player, attack mode, heal mode etc.
    def use_controls(self,keys):
        #Using the normal movement controls.
            #We could also set the direction in just 2 lines but then you would have to do a separate logic for the w,a,s,d keys.
            # self.direction.x=(keys[pygame.K_DOWN]-keys[pygame.K_UP])
            # self.direction.y=(keys[pygame.K_RIGHT]-keys[pygame.K_LEFT])
        self.direction.x=0
        self.direction.y=0
        ########HAVE TO MAKE THE BELOW IF CONDITIONALS TO BE PART OF AN if-else LADDER INORDER FOR THERE TO BE NO PROBLEM IN UPDATING THE DETECTION TILES.
        # if(keys[pygame.K_w] or keys[pygame.K_UP]):
        #     self.direction.y=-1
        # if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
        #     self.direction.x=-1
        # if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
        #     self.direction.y=1
        # if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            # self.direction.x=1
        if(keys[pygame.K_w] or keys[pygame.K_UP]):
            self.direction.y=-1
        elif(keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.direction.y=1
        if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.direction.x=-1
        elif(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.direction.x=1

        #Using the Attack Moves
        #Using the Heal Moves
        pass
    
    #A method to check collisions
    def handle_collisions(self,direction, level):
        ret1=level.collision_detector.handle_spritegroup_collision(self,PLAYER_SPEED,direction,level.enemy_sprites,0,collision_type="rect_collision")
        ret2=level.collision_detector.handle_spritegroup_collision(self,PLAYER_SPEED,direction,level.obstacle_sprites,0,collision_type="rect_collision")
        ret_val=level.collision_detector.handle_spritegroup_collision(self,PLAYER_SPEED,direction,level.transport_sprites,1,collision_type="rect_collision")
        if(ret_val==1):
            return ret_val
        elif(ret1==2 or ret2==2):
            return 2
        else:
            return 0
        # return ret_val
        
    def move(self,keys,level):
        self.use_controls(keys)
        if(self.direction.magnitude()!=0):
            self.direction=self.direction.normalize()

            #Move player horizontally and then check collisions. If player has to transport, then return '1'
            self.rect.x=self.rect.x+PLAYER_SPEED*self.direction.x
            shd_transport=self.handle_collisions("Horizontal",level)
            if(shd_transport==1):
                self.rect.x=self.rect.x-PLAYER_SPEED*self.direction.x           #Undoing movement as we have to transport. Next time we load back into this map, no collision happens.
                return shd_transport
            elif(shd_transport==0):
                level.collision_detector.update_detection_tiles_horizontal(self,PLAYER_SPEED*self.direction.x)
                pass
            #Move player Vertically and then check collisions. If player has to transport, then return '1'.
            self.rect.y=self.rect.y+PLAYER_SPEED*self.direction.y
            shd_transport=self.handle_collisions("Vertical",level)
            if(shd_transport==1):
                self.rect.y=self.rect.y-PLAYER_SPEED*self.direction.y
                return shd_transport
            elif(shd_transport==0):
                level.collision_detector.update_detection_tiles_vertical(self,PLAYER_SPEED*self.direction.y)
        pass

    def draw(self,display_surf):
        newpos=self.rect.topleft-self.offset
        display_surf.blit(self.img,newpos)