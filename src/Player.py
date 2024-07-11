import pygame
from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        self.pos=pos

        #Loading player graphics.
        self.player_graphics_path=PLAYER_DIRECTORY_PATH
        self.load_my_graphics()

        #Default image.
        self.img=self.graphics['right_idle'][0]
        self.rect=self.img.get_rect(topleft=self.pos)
        self.mask=pygame.mask.from_surface(self.img)
        self.status='down'          #Used for controlling the images to be loaded of the player.
        self.frame_index=0.1        #To loop over the list of images for a certain animation state.
        self.animation_speed=0.1    #The speed at which the frame index increases.

        #Player Dimensions - Used for updating the tiles.
        self.width_tiles=int(self.rect.width//BASE_SIZE)
        self.height_tiles=int(self.rect.height//BASE_SIZE)

        #Player movement
        self.direction=pygame.math.Vector2()        #A vector to only get the directions of the player.
        self.offset=pygame.math.Vector2()   #A vector to hold the position at which the player has to be blit at. The value is set in the get_offset() in Level.

        #Attack variables
        self.attack_cooldown=400
        self.attacking=False
        self.attack_time=None
        self.createAttack=None
        self.destroyAttack=None

        #Healing variables
        self.healing_cooldown=500
        self.healing=False
        self.healing_time=None

        #Weapon variables
        self.weapon_index=0
        self.weapon=list(WEAPON_INFO.keys())[self.weapon_index]
        self.weapon_switch_cooldown=200
        self.can_switch_weapon=True
        self.weapon_switch_time=None

    #A method to initialize the function to create the weapon and destroy the weapon.
    def getAttackFunctions(self,createAttack,destroyAttack):
        self.createAttack=createAttack
        self.destroyAttack=destroyAttack

    #A method to load the graphics of the players.
    def load_my_graphics(self):
        self.graphics={
            'right':[],
            'left':[],
            'up':[],
            'down':[],

            'right_idle':[],
            'left_idle':[],
            'up_idle':[],
            'down_idle':[],

            'right_attack':[],
            'left_attack':[],
            'up_attack':[],
            'down_attack':[],

            'right_heal':[],
            'left_heal':[],
            'up_heal':[],
            'down_heal':[]
        }

        for animation in self.graphics.keys():
            full_path=os.path.join(self.player_graphics_path,animation)
            files=os.listdir(full_path)
            imgs=[]
            for image_file in files:
                img=pygame.image.load(os.path.join(full_path,image_file))
                imgs.append(img)
            self.graphics[animation]=imgs

            pass
        pass

    #A method to set the status of the player.
    def set_status(self):

        #Idle status
        if self.direction.x==0 and self.direction.y==0:
            if 'attack' in self.status:
                self.status=self.status.replace('attack','idle')
            elif 'idle' in self.status:
                pass
            elif 'heal' in self.status:
                self.status=self.status.replace('heal','idle')
            else:
                self.status=self.status+'_idle'

        #Attack status
        if self.attacking:
            if 'idle' in self.status:
                self.status=self.status.replace('idle','attack')
            elif 'attack' in self.status:
                pass
            elif 'heal' in self.status:
                self.status=self.status.replace('heal','attack')
            else:
                self.status=self.status+'_attack'

        #Heal status
        if self.healing:
            if 'idle' in self.status:
                self.status=self.status.replace('idle','heal')
            elif 'heal' in self.status:
                pass
            elif 'attack' in self.status:
                self.status=self.status.replace('attack','heal')
            else:
                self.status=self.status+'_heal'

    #A method to set the direction of player, attack mode, heal mode etc.
    def use_controls(self,keys):
        #Using the normal movement controls.
        self.direction.x=0
        self.direction.y=0
        if(keys[pygame.K_w] or keys[pygame.K_UP]):
            self.direction.y=-1
            self.status='up'
        if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.direction.y=1
            self.status='down'
        if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.direction.x=-1
            self.status='left'
        if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.direction.x=1
            self.status='right'

        #Using the Attack Moves
        if(keys[pygame.K_SPACE] and not(self.attacking)):
            self.attacking=True
            self.attack_time=pygame.time.get_ticks()
            self.createAttack()
            pass

        #Switching to next Attack
        if(keys[pygame.K_n] and self.can_switch_weapon):
            self.can_switch_weapon=False
            self.weapon_switch_time=pygame.time.get_ticks()
            self.weapon_index+=1
            if(self.weapon_index>=len(WEAPON_INFO)):
                self.weapon_index=0
            self.weapon=list(WEAPON_INFO.keys())[self.weapon_index]

        #Using the Heal Moves
        if(keys[pygame.K_LCTRL] and not(self.attacking) and not(self.healing)):
            self.healing=True
            self.healing_time=pygame.time.get_ticks()
            pass
        pass

    def apply_cooldown(self):
        current_time=pygame.time.get_ticks()

        #Applying cooldown for attack
        if self.attacking:
            if current_time-self.attack_time >=self.attack_cooldown:
                self.attacking=False
                self.destroyAttack()

        #Applying cooldown for switching weapons.
        if not self.can_switch_weapon:
            if current_time-self.weapon_switch_time >=self.weapon_switch_cooldown:
                self.can_switch_weapon=True

        #Applying cooldown for healing
        if self.healing:
            if current_time-self.healing_time >=self.healing_cooldown:
                self.healing=False
    
    #A method to check collisions
    def handle_collisions(self,direction, level):
        ret1=level.collision_detector.handle_spritegroup_collision(self,PLAYER_SPEED,direction,level.enemy_sprites,0)
        ret2=level.collision_detector.handle_spritegroup_collision(self,PLAYER_SPEED,direction,level.obstacle_sprites,0)
        ret_val=level.collision_detector.handle_spritegroup_collision(self,PLAYER_SPEED,direction,level.transport_sprites,1)
        if(ret_val==1):
            return ret_val
        elif(ret1==2 or ret2==2):
            return 2
        return 0
    
    #A method to animate the player.
    def animate(self):
        animation=self.graphics[self.status]

        if(len(animation)>0):
            self.frame_index+=self.animation_speed
            if(int(self.frame_index)>=len(animation)):
                self.frame_index=0
                
            self.img=animation[int(self.frame_index)]
        # self.rect=self.img.get_rect(center=self.img.center)

    def move(self,keys,level):
        #Gettings the controls
        self.use_controls(keys)
        self.set_status()
        # debug_print(self.status,(10,10),pygame.display.get_surface())

        #Applying the cooldown
        self.apply_cooldown()

        #Moving the player
        if(self.direction.magnitude()!=0):
            self.direction=self.direction.normalize()

            #Move player horizontally and then check collisions. If player has to transport, then return '1'
            self.rect.x=self.rect.x+PLAYER_SPEED*self.direction.x
            shd_transport=self.handle_collisions("Horizontal",level)
            if(shd_transport==1):
                self.rect.x=self.rect.x-PLAYER_SPEED*self.direction.x           #Undoing movement as we have to transport. Next time we load back into this map, no collision happens.
                return shd_transport
            #Move player Vertically and then check collisions. If player has to transport, then return '1'.
            self.rect.y=self.rect.y+PLAYER_SPEED*self.direction.y
            shd_transport=self.handle_collisions("Vertical",level)
            if(shd_transport==1):
                self.rect.y=self.rect.y-PLAYER_SPEED*self.direction.y
                return shd_transport

        self.animate()
        pass

    def draw(self,display_surf):
        newpos=self.rect.topleft-self.offset
        display_surf.blit(self.img,newpos)