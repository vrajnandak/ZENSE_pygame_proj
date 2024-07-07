import pygame
from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        #There are a few methods which are called only for a specific method and nowhere else. Inorder to maintain a bit of abstraction and improve readability, I have put a separate class 'PlayerHelperMethods' which has all the helper methods. It is equivalent to the '__funcs' that are frequently used in linux kernel code.
        
        self.pos=pos

        # ***************************************HAS TO BE REPLACED BY THE PROPER STARTING IMAGE***********************************
        self.img=pygame.image.load(
                        os.path.join(
                            os.path.join((GRAPHICS_DIR_PATH),"Player"),"player.png"
                            )
                        )
        self.rect=self.img.get_rect(topleft=self.pos)
        self.mask=pygame.mask.from_surface(self.img)

        self.direction=pygame.math.Vector2()        #A vector to only get the directions of the player.
        self.offset=pygame.math.Vector2()   #A vector to hold the position at which the player has to be blit at. The value is set in the get_offset() in Level.
        self.helper_methods=Player.PlayerHelperMethods(self)

    #A method to set the direction of player, attack mode, heal mode etc.
    def use_controls(self,keys):
        #Using the normal movement controls.
        self.direction.x=0
        self.direction.y=0
        if(keys[pygame.K_w] or keys[pygame.K_UP]):
            self.direction.y=-1
        if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.direction.x=-1
        if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.direction.y=1
        if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.direction.x=1

        #Using the Attack Moves
        #Using the Heal Moves
        pass
    
    #A method to check collisions
    def handle_collisions(self,direction, level):
        self.helper_methods.handle_spritegroup_collision(direction,level.enemy_sprites,0)
        self.helper_methods.handle_spritegroup_collision(direction,level.obstacle_sprites,0)
        ret_val=self.helper_methods.handle_spritegroup_collision(direction,level.transport_sprites,1)       #We would only check transportation for the teleportation sprites.
        return ret_val
        
    def move(self,keys,level):
        self.use_controls(keys)

        if(self.direction.magnitude()!=0):
            self.direction=self.direction.normalize()

            #Move player horizontally and then check collisions. If player has to transport, then return '1'
            self.rect.x=self.rect.x+PLAYER_SPEED*self.direction.x
            shd_transport=self.handle_collisions("Horizontal",level)
            if(shd_transport==1):
                self.rect.x=self.rect.x-PLAYER_SPEED*self.direction.x           #Undoing the transportation since the next time we load into this level, we might end up transporting again as there would be a collision with the teleportation portal.
                return shd_transport
            #Move player Vertically and then check collisions. If player has to transport, then return '1'.
            self.rect.y=self.rect.y+PLAYER_SPEED*self.direction.y
            shd_transport=self.handle_collisions("Vertical",level)
            if(shd_transport==1):
                self.rect.y=self.rect.y-PLAYER_SPEED*self.direction.y
                return shd_transport
        pass

    def draw(self,display_surf):
        newpos=self.rect.topleft-self.offset
        display_surf.blit(self.img,newpos)

    #This function isn't needed as player doesn't belong to any spriteGroup. We handle him separetly.
    # def update(self):
    #     display_surf=pygame.display.get_surface()
    #     # display_surf.blit(self.image,self.rect.topleft)
    #     display_surf.blit(self.image,(0,0))
    
    class PlayerHelperMethods:
        def __init__(self,player_instance):
            self.player=player_instance

        #A method to get the max number of pixels that the player can move without having collision.
        def get_pixel_counter(self,sprite,movement,player_moved,is_horizontal,is_vertical):
            lower_lim=0
            upper_lim=abs(int(player_moved))
            left=lower_lim
            right=upper_lim
            while left<=right:
                mid=left+(right-left)//2
                #If you were to calculate the offset for only horizontal movement then you would'nt want to consider the movement for y-axis and similarily vice-versa. So, this variable offest term that we're adding would be the same if written separately for horizontal, vertical collisions but since we've wrote them in one function, we set them to 0 appropriately.
                offset_x=sprite.rect.left-self.player.rect.left-mid*movement*is_horizontal      #Considering only to add horizontal movement.
                offset_y=sprite.rect.top-self.player.rect.top-mid*movement*is_vertical          #Considering only to add vertical movement.
                offset=(offset_x,offset_y)
                if self.player.mask.overlap(sprite.mask,offset):
                    right=mid-1
                else:
                    left=mid+1
                    pass
            return right

        def handle_horizontal_collision(self,sprite):
            movement= 1 if self.player.direction.x > 0 else -1
            player_moved=self.player.direction.x*PLAYER_SPEED
            self.player.rect.x-=player_moved        #Undoing the added direction in x-axis as this caused mask collision.
            can_move_pixel=self.get_pixel_counter(sprite,movement,player_moved,1,0)
            self.player.rect.x+=movement*can_move_pixel
            pass

        def handle_vertical_collision(self,sprite):
            movement=1 if self.player.direction.y > 0 else -1
            player_moved=self.player.direction.y*PLAYER_SPEED
            self.player.rect.y-=player_moved        #Undoing the added direction in y-axis as this caused the mask collision.
            can_move_pixel=self.get_pixel_counter(sprite,movement,player_moved,0,1)
            self.player.rect.y+=movement*can_move_pixel
            pass

        def handle_spritegroup_collision(self,direction, spriteGroup, is_transportation_portal):
            for sprite in spriteGroup:
                if sprite.rect.colliderect(self.player.rect):
                    if(is_transportation_portal):
                        #Transport the player
                        return 1
                    elif(self.player.mask.overlap(sprite.mask,(sprite.rect.left-self.player.rect.left, sprite.rect.top-self.player.rect.top))):
                        if(direction=="Horizontal"):
                            self.handle_horizontal_collision(sprite)
                        elif(direction=="Vertical"):
                            self.handle_vertical_collision(sprite)
            return 0