import pygame
from Settings import *
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
# from pathfinding.core.diagonal_movement import DiagonalMovement     #To allow the enemies to move diagonally as well while searching the path.

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.pos=pos

        # ***************************************HAS TO BE REPLACED BY THE PROPER STARTING IMAGE***********************************
        self.img=pygame.Surface((BASE_SIZE,BASE_SIZE))
        self.img.fill('red')
        # self.img=pygame.image.load(
        #     os.path.join(
        #         os.path.join(
        #             GRAPHICS_DIR_PATH,"Enemy"
        #             ),
        #             "tmpENEMY.png"
        #     )
        # )
        self.mask=pygame.mask.from_surface(self.img)        #This will be used by the player for collision detection.
        self.rect=self.img.get_rect(topleft=self.pos)

        #Enemy Dimensions - Used for updating the tiles
        self.width_tiles=int(self.rect.width//BASE_SIZE)
        self.height_tiles=int(self.rect.height//BASE_SIZE)

        #Variables to move towards player.
        self.direction=pygame.math.Vector2()
        self.attack_radius=ENEMY_ATTACK_RADIUS*BASE_SIZE

        #The max size of the submatrix, centered around self( i.e., enemy sprite).
        self.SUBMATRIX_SIZE=12
        self.SUBMATRIX_HALF_SIZE=int(self.SUBMATRIX_SIZE//2)

    def update_direction(self,player,level):
        #The default direction of the enemy.
        self.direction.x=player.rect.centerx-self.rect.centerx
        self.direction.y=player.rect.centery-self.rect.centery
        
        #Make the grid
            #Getting the small matrix around the enemy as it is a waste to use the entire level's detection tiles for making the grid.
        small_submatrix=[]
        start_row=max(0,int((self.rect.y//BASE_SIZE)-self.SUBMATRIX_HALF_SIZE))
        end_row=min(len(level.detection_tiles),start_row+self.SUBMATRIX_SIZE)
        start_col=max(0,int((self.rect.x//BASE_SIZE)-self.SUBMATRIX_HALF_SIZE))
        end_col=min(len(level.detection_tiles[0]), start_col+self.SUBMATRIX_SIZE)
        for i in range(start_row,end_row,1):
            submatrix_row=level.detection_tiles[i][start_col:end_col]
            small_submatrix.append(submatrix_row)
        grid=Grid(matrix=small_submatrix)
        # print(small_submatrix)
        # for row in small_submatrix:
        #     print(row)
        # print('')
        #Set the start and end cell to be topleft of the self and the player respectively.
        start_x=int(self.rect.x//BASE_SIZE)-start_col
        start_y=int(self.rect.y//BASE_SIZE)-start_row
        end_x=min(max(int(player.rect.x//BASE_SIZE)-start_col, 0),end_col-start_col-1)
        end_y=min(max(int(player.rect.y//BASE_SIZE)-start_row, 0),end_row-start_row-1)
        self.start_x=start_x
        self.start_y=start_y
        self.end_x=end_x
        self.end_y=end_y
        # print('The cell indices: ',end_x, end_y)
        start_cell=grid.node(start_x,start_y)
        end_cell=grid.node(end_x,end_y)
        # start_cell=grid.node(int(self.rect.x//BASE_SIZE),int(self.rect.y//BASE_SIZE))
        # end_cell=grid.node(int(player.rect.x//BASE_SIZE),int(player.rect.y//BASE_SIZE))
        
        #Find the path to the player.
        path,runs=level.finder.find_path(start_cell,end_cell,grid)
        self.path=path
        # self.path,runs=level.finder.find_path(start_cell,end_cell,grid)
        # print(path)
        #Put the direction towards the next cell in the path.
        # if(len(self.path)>2):
        if(len(path)>2):            #As we only need to move if there is an intermediate node between the start and end node.
            # next_cell=self.path[1]
            next_cell=path[1]       #This node only contains the indices w.r.t submatrix, so we've to add the starting number of rows/columns, multiply by BASE_SIZE for actual positions.
            next_cell_col=(start_col+next_cell.x)*BASE_SIZE
            next_cell_row=(start_row+next_cell.y)*BASE_SIZE

            #Variables to check if the next cell to move to differ from the current cell that the sprite is on.
            cell_cols_different=1 if (int(self.rect.x//BASE_SIZE)!=int(next_cell_col//BASE_SIZE)) else 0
            cell_rows_different=1 if (int(self.rect.y//BASE_SIZE)!=int(next_cell_row//BASE_SIZE)) else 0

            #Prioritizing the horizontal movement of the sprite over the vertical movement. Sprite can move either in horizontal or vertical only
            self.direction.x=next_cell_col-self.rect.x
            self.direction.y=next_cell_row-self.rect.y
            print('before updating the directions,next direction: ', self.direction)
            if(self.direction.x<0):
                if(path[1].y<path[0].y):
                    if(self.rect.bottom//BASE_SIZE!=self.rect.top//BASE_SIZE):
                        self.direction.x=0
                        self.direction.y=-1
                    pass
                elif(path[1].y>path[0].y):
                    if(self.rect.bottom//BASE_SIZE!=self.rect.top//BASE_SIZE):
                        self.direction.x=0
                        self.direction.y=1
                    pass
                pass
            # if(cell_cols_different):
            #     self.direction.y=0
            # elif(cell_rows_different):
            #     self.direction.x=0
            print('next direction: ', self.direction)
        pass

    def handle_collisions(self,direction,level):
        ret_val1=level.collision_detector.handle_spritegroup_collision(self,ENEMY_SPEED,direction,level.transport_sprites,1,collision_type="rect_collision")
        ret_val2=level.collision_detector.handle_spritegroup_collision(self,ENEMY_SPEED,direction,level.obstacle_sprites,0,collision_type="rect_collision")
        ret_val3=level.collision_detector.handle_spritegroup_collision(self,ENEMY_SPEED,direction,level.enemy_sprites,0,collision_type="rect_collision")
        ret_val4=level.collision_detector.handle_spritegroup_collision(self,ENEMY_SPEED,direction,[level.player],0,collision_type="rect_collision")
        if(ret_val3==1):
            return 1
        elif(ret_val1==2 or ret_val2==2 or ret_val3==2 or ret_val4==2):
            return 2
        else:
            return 0
        pass

    def update(self,display_surf,offset,level):

        #Moving the enemy sprite if player within range.
        # if(self.direction.magnitude()<=self.attack_radius):
        if(pygame.math.Vector2(level.player.rect.left-self.rect.left, level.player.rect.top-self.rect.top).magnitude()<=self.attack_radius):
            self.update_direction(level.player,level)
            # print(f'starting cell: ', self.start_x,self.start_y)
            # print(f'ending cell: ', self.end_x,self.end_y)
            print(self.path)
            if(self.direction.magnitude()!=0):
                self.direction=self.direction.normalize()
            self.rect.x+=self.direction.x*ENEMY_SPEED
            ret_val=self.handle_collisions("Horizontal",level)
            if(ret_val==0):
                level.collision_detector.update_detection_tiles_horizontal(self,self.direction.x*ENEMY_SPEED)
            self.rect.y+=self.direction.y*ENEMY_SPEED
            ret_val=self.handle_collisions("Vertical",level)
            if(ret_val==0):
                level.collision_detector.update_detection_tiles_horizontal(self,self.direction.y*ENEMY_SPEED)
            pass
        else:   #If there is even a bit of residual movement or a lag, there should still be collision detection done.
            # ret_val=self.handle_collisions("horizontal",level)
            # if(ret_val==0):
                # level.collision_detector.update_detection_tiles_horizontal(self,self.direction.x*ENEMY_SPEED)
                # pass
            # ret_val=self.handle_collisions("Vertical",level)
            # if(ret_val==0):
                # level.collision_detector.update_detection_tiles_vertical(self,self.direction.y*ENEMY_SPEED)
                # pass
            pass

        self.draw(display_surf,offset)
        pass

    def draw(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)
        pass

    # class ToPlayerPathFinder:
    #     def __init__(self,map_matrix):
    #         self.matrix=map_matrix
    #         self.grid=Grid(matrix=map_matrix)
    #         self.img=pygame.Surface((BASE_SIZE,BASE_SIZE))
    #         self.img.fill('black')

    #     def draw_active_cell(self,display_surf):
    #         mouse_pos=pygame.mouse.get_pos()
    #         col=mouse_pos[0]//BASE_SIZE
    #         row=mouse_pos[1]//BASE_SIZE
    #         display_surf.blit(self.img,(col,row))

    #     def update(self):
    #         self.draw_active_cell()