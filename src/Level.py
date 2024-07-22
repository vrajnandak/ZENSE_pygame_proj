import pygame
from Settings import *
from Obstacle import *
from Player import *
from Enemy import *
from Button import *
from Portal import *
from CollisionHelper import CollisionHelper
from Weapon import Weapon
from Particles import Animations
from PlayerMagic import *
from RandomLoot import RandomLoot
from LEVEL_THINGS import *

class Level:
    def __init__(self,level_id,player,settings):
        self.level_id=level_id
        self.GameSettings=settings

        #Getting the level information.
        self.level_information=LEVEL_INFO(self.level_id)
        bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"STARTSCREEN_IMAGES",f'Ruin{self.level_id}.png'))
        # bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"STARTSCREEN_IMAGES",f'Ruin{0}.png'))
        display_surf=pygame.display.get_surface()
        DISPLAY_DIALOGS(self.level_information.start_msg,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
        display_surf.blit(bg_image,(0,0))

        #Sprite groups of the level.
        self.enemy_sprites=pygame.sprite.Group()
        self.enemy_counter=0
        self.visible_sprites=pygame.sprite.Group()
        self.obstacle_sprites=pygame.sprite.Group()
        self.transport_sprites=pygame.sprite.Group()
        self.attack_sprites=pygame.sprite.Group()
        self.loot_drops=pygame.sprite.Group()
        self.unlockable_gate_sprites=pygame.sprite.Group()
        self.level_scientist=None

        self.curr_attack=None                               #The current weapon being used by player to attack.
        self.curr_selected_weapon=pygame.image.load(os.path.join(PLAYER_WEAPONS_DIRECTORY_PATH,list(self.GameSettings.WEAPON_INFO.keys())[0],'full.png'))
        self.curr_selected_magic=pygame.image.load(os.path.join(PLAYER_MAGIC_DIRECTORY_PATH,f'{list(self.GameSettings.MAGIC_INFO.keys())[0]}.png'))

        #Player of the level.
        self.player=player
        self.player.getAttackFunctions(self.create_attack,self.destroy_attack)
        self.player.getMagicFunctions(self.create_magic)
        self.player_pos=None
        self.visible_sprites.add(self.player)

        #Graphics of the level.
        self.graphics_path=os.path.join(MAPS_DIRECTORY_PATH,f'Ruin{self.level_id}')
        self.graphics={}            #Has 'elem_id' as key, and value is a list '[pygame_img,(imgwidth,imgheight)]
        self.loadGraphics()
        self.animation_player=Animations()
        self.magic_player=MagicPlayer(self.animation_player)

        #Collision Detecting class (Has all the functions needed for detecting collisions)
        self.collision_detector=CollisionHelper(self)
        self.detection_tiles=[]             #Will be filled with in createMap() itself. Used for pathfinding.
        self.createDetectionTiles()
        self.finder=AStarFinder()           #We don't mention diagonal movement as the sprites may not necessarily be able to move diagonally due to obstacles.

        self.random_loot_graphics={}
        self.getRandomLootGraphics()
        self.random_loot_graphics_names=list(self.random_loot_graphics.keys())
        # print(self.random_loot_graphics)

        #Creating the map.
        self.createMap()

        #Sizes for the Level. I am doing this in the hope that there will be less computations as these values are stored after __init__() is called.
        self.LEVEL_HEIGHT=self.baseFloorRect.bottom
        self.LEVEL_WIDTH=self.baseFloorRect.right

        #OFFSET
        self.offset=pygame.math.Vector2()           #This is the offset used for blitting sprites. This offset ranges from [0,self.RIGHT_OFFSET_VAL] for offset in x-axis and [0,self.BOTTOM_OFFSET_VAL] for offset in y-axis.
        self.LOWER_XOFFSET_LIM=0
        self.LOWER_YOFFSET_LIM=0
        self.UPPER_XOFFSET_LIM=self.LEVEL_WIDTH-SCREEN_WIDTH
        self.UPPER_YOFFSET_LIM=self.LEVEL_HEIGHT-SCREEN_HEIGHT
            #The below variables are used for calculating offsets for a good experience of camera movement. This is mainly with respect to player's position.
        self.RIGHT_OFFSET_BORDER=self.LEVEL_WIDTH-SCREEN_WIDTH_HALF
        self.LEFT_OFFSET_BORDER=SCREEN_WIDTH_HALF
        self.TOP_OFFSET_BORDER=SCREEN_HEIGHT_HALF
        self.BOTTOM_OFFSET_BORDER=self.LEVEL_HEIGHT-SCREEN_HEIGHT_HALF
        self.RIGHT_OFFSET_VAL=self.UPPER_XOFFSET_LIM
        self.BOTTOM_OFFSET_VAL=self.UPPER_YOFFSET_LIM
            #The below variables are used for calculating the offsets based on player movement, box position to show a box-camera movement.
        self.box_camera={'left':60,'right':60,'top':60,'bottom':60}
        default_left=self.player.rect.left
        default_top=self.player.rect.top
        box_width=SCREEN_WIDTH-(self.box_camera['left']+self.box_camera['right'])
        box_height=SCREEN_HEIGHT-(self.box_camera['top']+self.box_camera['bottom'])
        self.box_rect=pygame.Rect(default_left,default_top,box_width,box_height)
            #The below variables are used for calculating the offsets based on keyboard camera controls.
        self.keyboard_offset_counter=pygame.math.Vector2()      #'.x' is used for x-axis controlling, '.y' is used for y-axis controlling.
            #The below variables are used for calculating the offsets based on mouse positions.
        self.mouse_offset_counter=pygame.math.Vector2()         #'.x' is used for x-axis controlling, '.y' is used for y-axis controlling.
        self.MOUSE_RIGHT_LIMIT=SCREEN_WIDTH-30
        self.MOUSE_LEFT_LIMIT=30
        self.MOUSE_TOP_LIMIT=30
        self.MOUSE_BOTTOM_LIMIT=SCREEN_HEIGHT-30

    #A method to get the graphics of the random loot potions.
    def getRandomLootGraphics(self):
        graphics_path=os.path.join(GRAPHICS_DIR_PATH,"RANDOM_LOOT")
        files=os.listdir(graphics_path)
        for image_name in files:
            img=pygame.image.load(os.path.join(graphics_path,image_name))
            self.random_loot_graphics[image_name.split('.png')[0]]=img
        pass

    #A method to simply store the unique graphics for this level.
    def loadGraphics(self):
        #There is no need to load 'ALL_BLOCKS' as we already have the id's and the things we're going to follow.
        # Loading the ALL_BLOCKS dictionary.
        # load_ALL_BLOCKS()

        #Load the different graphics in this folder. Since all the images have their id's, we can just parse the names of the files and then set the graphics.
        all_files_in_ruin=os.listdir(self.graphics_path)
        for file in all_files_in_ruin:
            if '.png' in file and BASEMAP_NAME not in file and ('not_obstacle' not in file):
                use_file_name=file[:-4]             #Getting rid of the '.png' from the file name
                ind_strings=use_file_name.split('_',4)     #The ind_strings will be <name_of_obstacle>
                ind_strings[1:]=[int(num) if num.isdigit() else num for num in ind_strings[1:]]
                self.graphics[ind_strings[1]]=[pygame.image.load(os.path.join(self.graphics_path,file)),(ind_strings[2],ind_strings[3])]
                # print('loaded the file: ', file)
            pass
        pass

    #A method to create the level's detection Tiles. Called only during creation of the level.
    def createDetectionTiles(self):
        self.baseFloorImg=pygame.image.load(os.path.join(self.graphics_path,BASEMAP_NAME))
        self.baseFloorRect=self.baseFloorImg.get_rect(topleft=(0,0))
        width_tiles=self.baseFloorRect.width//BASE_SIZE
        height_tiles=self.baseFloorRect.height//BASE_SIZE
        self.detection_tiles=[[1 for _ in range(width_tiles)] for _ in range(height_tiles)]
        pass

    #A method to create the map.
    def createMap(self):
        #Figure out the Base Map.
        self.baseFloorImg=pygame.image.load(os.path.join(self.graphics_path,BASEMAP_NAME))
        self.baseFloorRect=self.baseFloorImg.get_rect(topleft=(0,0))

        #Figure out the layout using csv. User 'self.graphics' to create the objects
        FloorinfoPath=os.path.join(self.graphics_path,FLOORINFO_DIR_NAME)
        floorinfo_files=os.listdir(FloorinfoPath)
        print('Current level being created: ', self.level_id)
        #You now have the .csv files. Iterate through all of them and then create the objects. Use the comments in the settings to figure out where to place enemies, player, invisible_blocks based on id's.
        for file in floorinfo_files:
            with open(os.path.join(FloorinfoPath,file)) as map:
                layout=reader(map,delimiter=',')
                for row_index,row in enumerate(layout):
                    # print(row)
                    for col_index,val in enumerate(row):
                        x=col_index*BASE_SIZE
                        y=row_index*BASE_SIZE
                        if(val!='-1'):
                            val=int(val)
                            img_pos=(x,y)
                            if(val<100):
                                img=self.graphics[int(val)]
                                img=img[0]
                                Obstacle(img_pos,img,[self.visible_sprites,self.obstacle_sprites])      #The instance of this class created is added to the given spriteGroups.
                                img_width=int(img.get_rect().width//BASE_SIZE)
                                img_height=int(img.get_rect().height//BASE_SIZE)
                                detection_tiles_row=len(self.detection_tiles)
                                detection_tiles_cols=len(self.detection_tiles[0])
                                for i in range(img_width+2):
                                    for j in range(img_height+2):
                                        new_row_index=row_index-1+j
                                        new_col_index=col_index-1+i
                                        if((new_row_index>=0 and new_row_index<detection_tiles_row) and (new_col_index>=0 and new_col_index<detection_tiles_cols)):
                                            self.detection_tiles[new_row_index][new_col_index]=0
                                pass
                            
                            elif(val==100):
                                # if self.enemy_counter<=1:
                                Enemy(img_pos,'zombie1',[self.enemy_sprites])
                                self.enemy_counter+=1
                                pass
                            elif(val==101):
                                Enemy(img_pos,'zombie2',[self.enemy_sprites])
                                self.enemy_counter+=1
                                pass
                            elif(val==102):
                                Enemy(img_pos,'zombie3',[self.enemy_sprites])
                                self.enemy_counter+=1
                                pass
                            elif(val==103):
                                Enemy(img_pos,'zombie4',[self.enemy_sprites])
                                self.enemy_counter+=1
                                pass
                            elif(val==104):
                                Enemy(img_pos,'zombieBoss',[self.enemy_sprites])
                                self.enemy_counter+=1
                                pass
                            elif(val==300):     #Scientist1
                                self.level_scientist=Scientist((x,y),[self.visible_sprites],1)
                                pass
                            elif(val==301):     #Scientist2
                                self.level_scientist=Scientist((x,y),[self.visible_sprites],2)
                                pass
                            elif(val==302):     #Scientist3
                                self.level_scientist=Scientist((x,y),[self.visible_sprites],3)
                                pass
                            elif(val==500):             #A val which reveals the locked gate of Ruin1.
                                img=pygame.image.load(os.path.join(self.graphics_path,"not_obstacle_unlockable_gate.png"))
                                Obstacle(img_pos,img,[self.unlockable_gate_sprites,self.obstacle_sprites,self.visible_sprites])
                                pass
                            elif(val==1000):
                                Obstacle(img_pos,None,[self.obstacle_sprites])
                                pass
                            elif(val==1001):
                                #This is to update the detection tiles properly so that the player's tiles are marked as '0'.
                            #     self.player=Player(img_pos)
                                # print('player position, ', x, y)
                                self.player.rect.left=x
                                self.player.rect.top=y
                                pass
                            elif(val==1003):
                                print('portal dimensions: ', x,y)
                                Portal(img_pos,[self.visible_sprites,self.transport_sprites], os.path.join(self.graphics_path,"Portals"))
                                pass
                            elif(val==1004):
                                pass
            pass
        pass

    #A method to get the offset for all the visible objects to be blit at, with the player being at the center of the screen except for when the player is at the corners of the screen.
    def get_player_based_offset(self):
        player_pos=self.player.rect.topleft     #Since the visible sprites are being blit() using pos(which is initialized to topleft position in createMap()), we use topleft only.

        #Getting the x-offset.
        if(player_pos[0]<self.LEFT_OFFSET_BORDER):
            self.offset.x=0
            pass
        elif(player_pos[0]>self.RIGHT_OFFSET_BORDER):
            self.offset.x=self.RIGHT_OFFSET_VAL
            pass
        else:
            self.offset.x=player_pos[0]-SCREEN_WIDTH_HALF
            pass

        #Gettings the y-offset.
        if(player_pos[1]<self.TOP_OFFSET_BORDER):
            self.offset.y=0
            pass
        elif(player_pos[1]>self.BOTTOM_OFFSET_BORDER):
            self.offset.y=self.BOTTOM_OFFSET_VAL
            pass
        else:
            self.offset.y=player_pos[1]-SCREEN_HEIGHT_HALF
            pass
        # self.player.offset=self.player_based_offset
        pass
    
    #A method to get the offset for the box-camera using the box_rect and the player position.
    def get_box_based_offset(self):
        if(self.player.rect.left < self.box_rect.left):
            self.box_rect.left=self.player.rect.left
            pass
        if(self.player.rect.right > self.box_rect.right):
            self.box_rect.right=self.player.rect.right
            pass
        if(self.player.rect.top < self.box_rect.top):
            self.box_rect.top=self.player.rect.top
            pass
        if(self.player.rect.bottom > self.box_rect.bottom):
            self.box_rect.bottom=self.player.rect.bottom
            pass

        self.offset.x=self.box_rect.left-self.box_camera['left']
        self.offset.y=self.box_rect.top-self.box_camera['top']
        self.player.offset=self.offset
        pass

    #A method to add the offset accumulated by keyboard keys to the final offset used for blitting sprites.
    def get_keyboard_based_offset(self,keys):
        # if(keys[pygame.K_i]):
        if(keys[pygame.K_i] and ((self.offset.y + (self.keyboard_offset_counter.y-1)*self.GameSettings.KEYBOARD_CAMERA_SPEED)>0)):
        # if(keys[pygame.K_i] and ((self.offset.y + (self.mouse_offset_counter.y*MOUSE_CAMERA_SPEED) + (self.keyboard_offset_counter.y-1)*KEYBOARD_CAMERA_SPEED)>0)):
            self.keyboard_offset_counter.y-=1
            pass
        # if(keys[pygame.K_j]):
        if(keys[pygame.K_j] and ((self.offset.x + (self.keyboard_offset_counter.x-1)*self.GameSettings.KEYBOARD_CAMERA_SPEED)>0)):
        # if(keys[pygame.K_j] and ((self.offset.x + (self.mouse_offset_counter.x*MOUSE_CAMERA_SPEED) + (self.keyboard_offset_counter.x-1)*KEYBOARD_CAMERA_SPEED)>0)):
            self.keyboard_offset_counter.x-=1
            pass
        # if(keys[pygame.K_k]):
        if(keys[pygame.K_k] and ((self.offset.y + (self.keyboard_offset_counter.y+1)*self.GameSettings.KEYBOARD_CAMERA_SPEED) < self.UPPER_YOFFSET_LIM)):
        # if(keys[pygame.K_k] and ((self.offset.y + (self.mouse_offset_counter.y*MOUSE_CAMERA_SPEED) + (self.keyboard_offset_counter.y+1)*KEYBOARD_CAMERA_SPEED) < self.UPPER_YOFFSET_LIM)):
            self.keyboard_offset_counter.y+=1
            pass
        # if(keys[pygame.K_l]):
        if(keys[pygame.K_l] and ((self.offset.x + (self.keyboard_offset_counter.x+1)*self.GameSettings.KEYBOARD_CAMERA_SPEED) < self.UPPER_XOFFSET_LIM)):
        # if(keys[pygame.K_l] and ((self.offset.x + (self.mouse_offset_counter.x*MOUSE_CAMERA_SPEED) + (self.keyboard_offset_counter.x+1)*KEYBOARD_CAMERA_SPEED) < self.UPPER_XOFFSET_LIM)):
            self.keyboard_offset_counter.x+=1
            pass
        
        self.offset=self.offset+self.keyboard_offset_counter*self.GameSettings.KEYBOARD_CAMERA_SPEED

    #A method to add the offset accumulated by mouse position to the final offset used for blitting sprites.
    def get_mouse_based_offset(self):
        mouse_pos=pygame.math.Vector2(pygame.mouse.get_pos())
        if(mouse_pos.x<=self.MOUSE_LEFT_LIMIT and (self.offset.x+(self.mouse_offset_counter.x-1)*self.GameSettings.MOUSE_CAMERA_SPEED)>0):
            self.mouse_offset_counter.x-=1
        elif(mouse_pos.x>=self.MOUSE_RIGHT_LIMIT and (self.offset.x+(self.mouse_offset_counter.x-1)*self.GameSettings.MOUSE_CAMERA_SPEED)<self.UPPER_XOFFSET_LIM):
            self.mouse_offset_counter.x+=1
        if(mouse_pos.y<=self.MOUSE_TOP_LIMIT and (self.offset.y+(self.mouse_offset_counter.y-1)*self.GameSettings.MOUSE_CAMERA_SPEED)>0):
            self.mouse_offset_counter.y-=1
        elif(mouse_pos.y>=self.MOUSE_BOTTOM_LIMIT and (self.offset.y+(self.mouse_offset_counter.y+1)*self.GameSettings.MOUSE_CAMERA_SPEED)<self.UPPER_YOFFSET_LIM):
            self.mouse_offset_counter.y+=1
        #Can uncomment the below line but for best effects, it's better if you can set the values of self.MOUSE_LEFT_LIMIT and self.MOUSE_TOP_LIMIT to '0' and the values of self.MOUSE_RIGHT_LIMIT and self.MOUSE_BOTTOM_LIMIT so that the value subtracted is 0.
        # pygame.mouse.set_pos(min(max(self.MOUSE_LEFT_LIMIT,mouse_pos.x),self.MOUSE_RIGHT_LIMIT),min(max(self.MOUSE_TOP_LIMIT,mouse_pos.y),self.MOUSE_BOTTOM_LIMIT))     #Setting the mouse on the borders if it tries to go outside the borders, else it is set in it's current place.

        self.offset=self.offset+self.mouse_offset_counter*self.GameSettings.MOUSE_CAMERA_SPEED
        pass
    
    def apply_offset_limits(self):
        self.offset.x=min(max(self.LOWER_XOFFSET_LIM,self.offset.x),self.UPPER_XOFFSET_LIM)
        self.offset.y=min(max(self.LOWER_YOFFSET_LIM,self.offset.y),self.UPPER_YOFFSET_LIM)
        pass

    def get_offset(self,keys):
        #There are 3 types of offset. player_based_offset, (keyboard_keys_based_offset, mouse_based_offset). And pressing 'u' resets the offset to player_based_offset.
        if(keys[pygame.K_u]):       #Ressetting the camera.
            self.keyboard_offset_counter=pygame.math.Vector2()
            self.mouse_offset_counter=pygame.math.Vector2()
            pygame.mouse.set_pos((SCREEN_WIDTH_HALF,SCREEN_HEIGHT_HALF))
        elif(keys[pygame.K_b]):
            self.get_box_based_offset()
            pass
        else:
            self.get_player_based_offset()
            #Handling keyboard based camera movement.
            self.get_keyboard_based_offset(keys)
            self.get_mouse_based_offset()
            self.box_rect.center=self.player.rect.topleft               #So that there is no log when releasing or on clicking 'b'.
            pass
        self.apply_offset_limits()
        self.player.offset=self.offset

        pass

    #A method to create a weapon. It is better to handle the weapon as a separate entity from the player in order to not have to write extra code to deal with collisions.
    def create_attack(self):
        self.curr_attack=Weapon(self.player,[self.visible_sprites])
        pass

    #A method to destroy the created weapon.
    def destroy_attack(self):
        if self.curr_attack:
            self.curr_attack.kill()
            self.curr_attack=None

    #A method to create the magic.
    def create_magic(self,style,strength,cost):
        if(style=='heal'):
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
            pass
        if(style=='flame'):
            # print('flaming')
            self.magic_player.flame(self.player,cost,[self.attack_sprites,self.visible_sprites])
            pass
        if(style=='nova'):
            pass
        if(style=='aura'):
            pass
        pass

    #A method to display the weapon selections.
    def display_selection(self,display_surf,left,top,has_switched,img=None):
        bg_rect=pygame.rect.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(display_surf,ITEM_BOX_BG_COLOR,bg_rect,0,border_radius=2)
        if has_switched:
            pygame.draw.rect(display_surf,ITEM_BOX_BORDER_COLOR_ACTIVE,bg_rect,2,border_radius=2)
        else:
            pygame.draw.rect(display_surf,ITEM_BOX_BORDER_COLOR,bg_rect,2,border_radius=2)

        if(img):
            display_surf.blit(img,(bg_rect.centerx-img.get_width()//2,bg_rect.centery-img.get_height()//2))
        pass

    #A method to randomly drop a loot drop whenever an enemy sprite dies.
    def random_loot_drop(self,pos,zombieType):
        n=randint(0,2*len(self.random_loot_graphics_names))
        if(n<len(self.random_loot_graphics_names)):
            loot_name=self.random_loot_graphics_names[n]
            #Making the drop have stats based on the zombie Type killed.
            if(zombieType[-1].isdigit()):
                val=int(zombieType[-1])-1
            else:
                val=4
            RandomLoot(pos,[self.visible_sprites,self.loot_drops],self.random_loot_graphics[loot_name],loot_name,val)
        pass

    #A method to check if the player has attacked any sprite by checking the weapon sprite collision with the sprite groups.
    def player_attack(self):
        attacking_sprites=[self.attack_sprites,[self.curr_attack]]
        for index,sprite_group in enumerate(attacking_sprites):
            if sprite_group:
                for sprite in sprite_group:
                    if sprite:
                        collision_sprites=pygame.sprite.spritecollide(sprite,self.enemy_sprites,False)
                        if collision_sprites:
                            for target_sprite in collision_sprites:
                                target_sprite_pos=target_sprite.rect.topleft
                                ret_val=target_sprite.reduce_health(self.player,index)
                                if(ret_val==1):
                                    self.enemy_counter-=1
                                    self.random_loot_drop(target_sprite_pos,target_sprite.zombieType)
                                    if(self.enemy_counter==0):
                                        self.level_information.handle_event(EVENT_CODES[1],self)

        # if self.curr_attack:
        #     #Checking collision with player weapon
        #     collision_sprites=pygame.sprite.spritecollide(self.curr_attack, self.enemy_sprites, False)
        #     if collision_sprites:
        #         for target_sprite in collision_sprites:
        #             target_sprite_pos=target_sprite.rect.topleft
        #             ret_val=target_sprite.reduce_health(self.player,is_weapon=1)
        #             if(ret_val==1):
        #                 self.enemy_counter-=1
        #                 self.random_loot_drop(target_sprite_pos,target_sprite.zombieType)

        # if self.attack_sprites:
        #     #Checking collision with player magic.
        #     # print('lksdjflksdjf')
        #     for sprite in self.attack_sprites:
        #         collision_sprites=pygame.sprite.spritecollide(sprite,self.enemy_sprites,False)
        #         if collision_sprites:
        #             for target_sprite in collision_sprites:
        #                 target_sprite_pos=target_sprite.rect.topleft
        #                 ret_val=target_sprite.reduce_health(self.player,0)
        #                 if(ret_val==1):
        #                     self.enemy_counter-=1
        #                     self.random_loot_drop(target_sprite_pos,target_sprite.zombieType)

        pass
    
    #A method to damage the player whenever an enemy sprite attacks the player.
    def damage_the_player(self,amount,attack_type):
        if self.player.can_get_hit:
            self.player.health-=amount
            self.player.can_get_hit=False
            self.player.hit_time=pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
        pass

    # #A method to draw the sprites in sorted order of their y positions for better aesthetics. This would be useful only for some sprites which don't have a mask.
    # def draw_visible_sprites(self):
    #     display_surf=pygame.display.get_surface()
    #     for sprite in sorted(self.visible_sprites,key= lambda sprite: sprite.rect.centery):
    #         sprite.update(display_surf,self.offset)
    #     pass

    def run(self,keys):
        # if(self.enemy_sprites==None):
        # if(self.enemy_counter==0):
        #     print('all enemy sprites have been killed')
            # return 5
        #Move the Player
        shd_transport=self.player.move(keys,self)

        if(shd_transport==1):
            shd_use_portal_and_change_map=self.level_information.handle_event(EVENT_CODES[2],self)
            if(shd_use_portal_and_change_map):
                self.player_pos=self.player.rect.topleft        #Saving the player's position so that the next time player comes back to this level, he starts from here.
                return shd_transport
        
        #Get the Offset
        self.get_offset(keys)

        #Draw the BaseMap Image after considering offset
        display_surf=pygame.display.get_surface()
        baseFloor_offset=self.baseFloorRect.topleft-self.offset
        display_surf.blit(self.baseFloorImg,baseFloor_offset)

        #Draw the visible sprites after considering offset
        self.enemy_sprites.update(display_surf,self.offset,self)
        self.visible_sprites.update(display_surf,self.offset)
        # self.draw_visible_sprites()
        
        self.player_attack()
        if(self.player.health<=0):
            SaveGameScreen()
            return 10
        # self.player.draw(display_surf)
        self.player.display_ui(display_surf)
        # debug_print(self.player.status,(10,10),display_surf)

        #Displaying the weapon selection.
        self.display_selection(display_surf,10,SCREEN_HEIGHT-ITEM_BOX_SIZE,not self.player.can_switch_weapon,self.curr_selected_weapon)

        #Displaying the magic selection.
        self.display_selection(display_surf,10,SCREEN_HEIGHT-2*ITEM_BOX_SIZE - 20, not self.player.can_switch_magic, self.curr_selected_magic)

        #Displaying the level information if any.
        # self.level_information.update(display_surf)
        # debug_print('(0,0)',-self.offset)
        
        
        # SaveGameScreen(display_surf,"Before_playing_dialog_box.png")
        # debug_print(self.player.rect.topleft,(500,500))

        # debug_print(self.GameSettings.PLAYER_SPEED,(300,300))
        # debug_print(f'weapon damage: {self.GameSettings.WEAPON_INFO[self.player.weapon_name]["damage"]}',(500,300))
        # debug_print(self.enemy_counter,(600,500))
        # self.GameSettings.display_settings(can_change_values=1)
        #Blitting the detection tiles.
        # self.draw_map_detection_tiles(display_surf)
        return 0
    
    def draw_map_detection_tiles(self,display_surf):
        for row_index,row in enumerate(self.detection_tiles):
            for col_index,val in enumerate(row):
                pos=(col_index*BASE_SIZE,row_index*BASE_SIZE)
                newpos=pos-self.offset
                debug_print(val,newpos,display_surf)