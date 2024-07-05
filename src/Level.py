import pygame
from Settings import *
from Obstacle import *
from Player import *

class Level:
    def __init__(self,level_id):
        self.level_id=level_id

        #Sprite groups of the level.
        self.enemy_sprites=pygame.sprite.Group()
        self.visible_sprites=pygame.sprite.Group()
        self.obstacle_sprites=pygame.sprite.Group()
        self.transport_sprites=pygame.sprite.Group()

        #Player of the level.
        self.player=None

        #Graphics of the level.
        self.graphics_path=os.path.join(MAPS_DIRECTORY_PATH,f'Ruin{self.level_id}')
        self.graphics={}            #Has 'elem_id' as key, and value is a list '[pygame_img,(imgwidth,imgheight)]
        self.loadGraphics()
        self.createMap()

        #Sizes for the Level. I am doing this in the hope that there will be less computations as these values are stored after __init__() is called.
        self.LEVEL_HEIGHT=self.baseFloorRect.bottom
        self.LEVEL_WIDTH=self.baseFloorRect.right
        self.player_based_offset=pygame.math.Vector2()
        #This and the below 3 variables are used for calculating offsets for a good experience of camera movement.
        self.RIGHT_OFFSET_BORDER=self.LEVEL_WIDTH-SCREEN_WIDTH_HALF
        self.LEFT_OFFSET_BORDER=SCREEN_WIDTH_HALF
        self.TOP_OFFSET_BORDER=SCREEN_HEIGHT_HALF
        self.BOTTOM_OFFSET_BORDER=self.LEVEL_HEIGHT-SCREEN_HEIGHT_HALF
        self.RIGHT_OFFSET_VAL=self.LEVEL_WIDTH-SCREEN_WIDTH
        self.BOTTOM_OFFSET_VAL=self.LEVEL_HEIGHT-SCREEN_HEIGHT


    #A function to simply store the unique graphics for this level.
    def loadGraphics(self):
        #There is no need to load 'ALL_BLOCKS' as we already have the id's and the things we're going to follow.
        # Loading the ALL_BLOCKS dictionary.
        # load_ALL_BLOCKS()

        #Load the different graphics in this folder. Since all the images have their id's, we can just parse the names of the files and then set the graphics.
        all_files_in_ruin=os.listdir(self.graphics_path)
        for file in all_files_in_ruin:
            if '.png' in file and BASEMAP_NAME not in file:
                use_file_name=file[:-4]
                ind_strings=use_file_name.split('_',4)     #The ind_strings will be <name_of_obstacle>
                ind_strings[1:]=[int(num) if num.isdigit() else num for num in ind_strings[1:]]
                # print(ind_strings)
                # split_list[1:] = [int(num) if num.isdigit() else num for num in split_list[1:]]
                self.graphics[ind_strings[1]]=[pygame.image.load(os.path.join(self.graphics_path,file)),(ind_strings[2],ind_strings[3])]
            pass
        pass

    #A function to create the map.
    def createMap(self):
        #Figure out the Base Map.
        self.baseFloorImg=pygame.image.load(os.path.join(self.graphics_path,BASEMAP_NAME))
        self.baseFloorRect=self.baseFloorImg.get_rect(topleft=(0,0))

        #Figure out the layout using csv. User 'self.graphics' to create the objects
        FloorinfoPath=os.path.join(self.graphics_path,FLOORINFO_DIR_NAME)
        floorinfo_files=os.listdir(FloorinfoPath)

        #You now have the .csv files. Iterate through all of them and then create the objects. Use the comments in the settings to figure out where to place enemies, player, invisible_blocks based on id's.
        for file in floorinfo_files:
            with open(os.path.join(FloorinfoPath,file)) as map:
                layout=reader(map,delimiter=',')
                for row_index,row in enumerate(layout):
                    for col_index,val in enumerate(row):
                        x=col_index*BASE_SIZE
                        y=row_index*BASE_SIZE
                        if(val!='-1'):
                            val=int(val)
                            img_pos=(x,y)
                            if(val<1000):
                                img=self.graphics[int(val)]
                                img=img[0]
                                Obstacle(img_pos,img,[self.visible_sprites,self.obstacle_sprites])      #The instance of this class created is added to the given spriteGroups.
                                pass
                            elif(val==1000):
                                Obstacle(img_pos,None,[self.obstacle_sprites])
                                pass
                            elif(val==1001):
                                self.player=Player(img_pos)
                                pass
                            elif(val==1002):
                                pass
                            elif(val==1003):
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
            self.player_based_offset.x=0
            self.player.offset.x=0
            pass
        elif(player_pos[0]>self.RIGHT_OFFSET_BORDER):
            # self.player_based_offset.x=self.LEVEL_WIDTH-SCREEN_WIDTH
            self.player_based_offset.x=self.RIGHT_OFFSET_VAL
            # self.player.offset.x=self.LEVEL_WIDTH-SCREEN_WIDTH
            self.player.offset.x=self.RIGHT_OFFSET_VAL
            pass
        else:
            self.player_based_offset.x=player_pos[0]-SCREEN_WIDTH_HALF
            self.player.offset.x=player_pos[0]-SCREEN_WIDTH_HALF
            pass

        #Gettings the y-offset.
        if(player_pos[1]<self.TOP_OFFSET_BORDER):
            self.player_based_offset.y=0
            self.player.offset.y=0
            pass
        elif(player_pos[1]>self.BOTTOM_OFFSET_BORDER):
            # self.player_based_offset.y=self.LEVEL_HEIGHT-SCREEN_HEIGHT
            self.player_based_offset.y=self.BOTTOM_OFFSET_VAL
            # self.player.offset.y=self.LEVEL_HEIGHT-SCREEN_HEIGHT
            self.player.offset.y=self.BOTTOM_OFFSET_VAL
            pass
        else:
            self.player_based_offset.y=player_pos[1]-SCREEN_HEIGHT_HALF
            self.player.offset.y=player_pos[1]-SCREEN_HEIGHT_HALF
            pass
        pass

    def run(self,keys):
        #Move the Player
        self.player.move(keys,self)
        #Get the Offset
        self.get_player_based_offset()

        #Draw the BaseMap Image after considering offset
        display_surf=pygame.display.get_surface()
        baseFloor_offset=self.baseFloorRect.topleft-self.player_based_offset
        display_surf.blit(self.baseFloorImg,baseFloor_offset)

        #Draw the visible sprites after considering offset
        self.visible_sprites.update(display_surf,self.player_based_offset)
        self.player.draw(display_surf)
        pass