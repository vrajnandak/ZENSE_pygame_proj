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
        self.animation_speed=0.4    #The speed at which the frame index increases.

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

        #Magic variables
        self.magic_cooldown=500
        self.magicing=False
        self.magic_time=None
        self.createMagic=None
        self.destroyMagic=None

        #Weapon variables
        self.weapon_index=0
        self.weapon_name=list(WEAPON_INFO.keys())[self.weapon_index]
        self.weapon_switch_cooldown=200
        self.can_switch_weapon=True
        self.weapon_switch_time=None

        #Magic dynamic variables.
        self.magic_index=0
        self.magic_name=list(MAGIC_INFO.keys())[self.magic_index]
        self.magic_switch_cooldown=200
        self.can_switch_magic=True
        self.magic_switch_time=None

        #Player stats.
        self.stats={'health':500,'energy':60,'attack':10,'magic':4,'speed':PLAYER_SPEED}        #These are the default or caps on player stats.
        self.health=self.stats['health']
        self.energy=self.stats['energy']
        self.exp=1
        self.exp_cap=100                        #This will be updated to a new cap whenever the self.exp >= self.exp_cap.
        self.speed=self.stats['speed']

        #Player UI
        self.health_bar_rect=pygame.rect.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.health_text_surf=UI_TEXT_FONT.render("HP",True,'black')
        self.health_text_surf_pos=(self.health_bar_rect.centerx-self.health_text_surf.get_width()//2,self.health_bar_rect.centery-self.health_text_surf.get_height()//2)
        self.energy_bar_rect=pygame.rect.Rect(10,40,ENERGY_BAR_WIDTH,BAR_HEIGHT)
        self.energy_text_surf=UI_TEXT_FONT.render("MP",True,'black')
        self.energy_text_surf_pos=(self.energy_bar_rect.centerx-self.energy_text_surf.get_width()//2,self.energy_bar_rect.centery-self.energy_text_surf.get_height()//2)
        self.exp_bar_rect=pygame.rect.Rect(10,70,EXP_BAR_WIDTH,BAR_HEIGHT)
        self.exp_text_surf=UI_TEXT_FONT.render("EXP",True,'black')
        self.exp_text_surf_pos=(self.exp_bar_rect.centerx-self.exp_text_surf.get_width()//2,self.exp_bar_rect.centery-self.exp_text_surf.get_height()//2)

    #A method to initialize the function to create the weapon and destroy the weapon.
    def getAttackFunctions(self,createAttack,destroyAttack):
        self.createAttack=createAttack
        self.destroyAttack=destroyAttack

    #A method to initialize the function to create the magic and destroy it.
    def getMagicFunctions(self,createMagic,destroyMagic):
        self.createMagic=createMagic
        self.destroyMagic=destroyMagic
        pass

    #A method to return the total attack by combining the base attack of player(basically fist power) and the weapon power.
    def get_full_damage(self):
        base_damage=self.stats['attack']
        weapon_damage=WEAPON_INFO[self.weapon_name]['damage']
        print('returning ', base_damage+weapon_damage)
        return base_damage+weapon_damage
        pass

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

            'right_magic':[],
            'left_magic':[],
            'up_magic':[],
            'down_magic':[]
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
            elif 'magic' in self.status:
                self.status=self.status.replace('magic','idle')
            else:
                self.status=self.status+'_idle'

        #Attack status
        if self.attacking:
            if 'idle' in self.status:
                self.status=self.status.replace('idle','attack')
            elif 'attack' in self.status:
                pass
            elif 'magic' in self.status:
                self.status=self.status.replace('magic','attack')
            else:
                self.status=self.status+'_attack'

        #Magic status
        if self.magicing:
            if 'idle' in self.status:
                self.status=self.status.replace('idle','magic')
            elif 'magic' in self.status:
                pass
            elif 'attack' in self.status:
                self.status=self.status.replace('attack','magic')
            else:
                self.status=self.status+'_magic'

    #A method to set the direction of player, attack mode, magic mode etc.
    def use_controls(self,keys,level):
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

        #Switching the weapons.
        if self.can_switch_weapon:
            inc=1 if keys[pygame.K_n] else 0
            dec=-1 if keys[pygame.K_p] else 0
            if(inc==1 or dec==-1):
                self.can_switch_weapon=False
                self.weapon_switch_time=pygame.time.get_ticks()

                #Changing the weapon index to be within the range.
                self.weapon_index+=(inc+dec)
                self.weapon_index=self.weapon_index if self.weapon_index>=0 else len(WEAPON_INFO)-1
                self.weapon_index=self.weapon_index if self.weapon_index<len(WEAPON_INFO) else 0

                self.weapon_name=list(WEAPON_INFO.keys())[self.weapon_index]
                level.curr_selected_weapon=pygame.image.load(os.path.join(PLAYER_WEAPONS_DIRECTORY_PATH,f'{self.weapon_name}','full.png'))

        #Switching to next Attack
        # if(keys[pygame.K_n] and self.can_switch_weapon):
        #     self.can_switch_weapon=False
        #     self.weapon_switch_time=pygame.time.get_ticks()
        #     self.weapon_index+=1
        #     if(self.weapon_index>=len(WEAPON_INFO)):
        #         self.weapon_index=0
        #     self.weapon_name=list(WEAPON_INFO.keys())[self.weapon_index]
        #     level.curr_selected_weapon=pygame.image.load(os.path.join(PLAYER_WEAPONS_DIRECTORY_PATH,f'{self.weapon_name}',f'full.png'))

        # #Switching to previous Attack.
        # if(keys[pygame.K_p] and self.can_switch_weapon):
        #     self.can_switch_weapon=False
        #     self.weapon_switch_time=pygame.time.get_ticks()
        #     self.weapon_index-=1
        #     if(self.weapon_index<0):
        #         self.weapon_index=len(WEAPON_INFO)-1
        #     self.weapon_name=list(WEAPON_INFO.keys())[self.weapon_index]
        #     level.curr_selected_weapon=pygame.image.load(os.path.join(PLAYER_WEAPONS_DIRECTORY_PATH,f'{self.weapon_name}',f'full.png'))

        #Using the Magic Moves
        if(keys[pygame.K_LCTRL] and not(self.attacking) and not(self.magicing)):
            self.magicing=True
            self.magic_time=pygame.time.get_ticks()
            style=self.magic_name
            strength=MAGIC_INFO[style]['strength'] + self.stats['magic']
            cost=MAGIC_INFO[style]['cost']
            self.createMagic(style,strength,cost)
            pass

        #Switching the Magic
        if self.can_switch_magic:
            inc=1 if keys[pygame.K_m] else 0
            dec=-1 if keys[pygame.K_o] else 0
            if(inc==1 or dec==-1):
                self.can_switch_magic=False
                self.magic_switch_time=pygame.time.get_ticks()

                #Changing the weapon index to be within the range.
                self.magic_index+=(inc+dec)
                self.magic_index=self.magic_index if self.magic_index>=0 else len(MAGIC_INFO)-1
                self.magic_index=self.magic_index if self.magic_index<len(MAGIC_INFO) else 0

                self.magic_name=list(MAGIC_INFO.keys())[self.magic_index]
                # img=pygame.Surface((BASE_SIZE,BASE_SIZE))
                # img.fill('blue')
                # if(self.magic_index!=0):
                #     img.fill('pink')
                level.curr_selected_magic=pygame.image.load(os.path.join(PLAYER_MAGIC_DIRECTORY_PATH,f'{self.magic_name}.png'))
        pass

    def apply_cooldown(self):
        current_time=pygame.time.get_ticks()

        #Applying cooldown for attack
        if self.attacking:
            if current_time-self.attack_time >=self.attack_cooldown + WEAPON_INFO[self.weapon_name]['cooldown']:
                self.attacking=False
                self.destroyAttack()

        #Applying cooldown for switching weapons.
        if not self.can_switch_weapon:
            if current_time-self.weapon_switch_time >=self.weapon_switch_cooldown:
                self.can_switch_weapon=True

        #Applying cooldown for Magic
        if self.magicing:
            if current_time-self.magic_time >=self.magic_cooldown:
                self.magicing=False

        #Applying cooldown for switching magic.
        if not self.can_switch_magic:
            if current_time-self.magic_switch_time>=self.magic_switch_cooldown + MAGIC_INFO[self.magic_name]['cooldown']:
                self.can_switch_magic=True
    
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
            self.rect=self.img.get_rect(center=self.rect.center)

    def move(self,keys,level):
        #Gettings the controls
        self.use_controls(keys,level)
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

    #A method to display only the Bar name on the bar.
    def draw_box_bars(self,text_surf,text_surf_pos,display_surf,BOX_BG_COLOR,BAR_COLOR,BORDER_COLOR,box_rect,curr_val,max_val,BAR_WIDTH,):
        #Displaying the bars.
        pygame.draw.rect(display_surf,BOX_BG_COLOR,box_rect,0,border_radius=2)
        box_width=int((curr_val*BAR_WIDTH)//max_val)
        curr_rect=box_rect.copy()
        curr_rect.width=box_width
        pygame.draw.rect(display_surf,BAR_COLOR,curr_rect,0,border_radius=2)
        pygame.draw.rect(display_surf,BORDER_COLOR,box_rect,2,border_radius=2)

        #Displaying the text on the bar.
        display_surf.blit(text_surf,text_surf_pos)

    #A method to display the HP,MP,EXP.
    def display_ui(self,display_surf):
        #Displaying the health bar.
        self.draw_box_bars(self.health_text_surf,self.health_text_surf_pos,display_surf,HEALTH_BAR_BGCOLOR,HEALTH_BAR_COLOR,HEALTH_BAR_BORDER_COLOR,self.health_bar_rect,self.health,self.stats['health'],HEALTH_BAR_WIDTH)

        #Displaying the energy bar.
        self.draw_box_bars(self.energy_text_surf,self.energy_text_surf_pos,display_surf,ENERGY_BAR_BGCOLOR,ENERGY_BAR_COLOR,ENERGY_BAR_BORDER_COLOR,self.energy_bar_rect,self.energy,self.stats['energy'],ENERGY_BAR_WIDTH)
       
        #Displaying the exp bar.
        self.draw_box_bars(self.exp_text_surf,self.exp_text_surf_pos,display_surf,EXP_BAR_BGCOLOR,EXP_BAR_COLOR,EXP_BAR_BORDER_COLOR,self.exp_bar_rect,self.exp,self.exp_cap,EXP_BAR_WIDTH)
        pass