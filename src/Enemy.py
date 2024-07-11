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
        # self.img=pygame.Surface((BASE_SIZE,BASE_SIZE))
        # self.img.fill('red')
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

        #Enemy Dimensions - Used for updating the tiles
        self.width_tiles=int(self.rect.width//BASE_SIZE)
        self.height_tiles=int(self.rect.height//BASE_SIZE)

        #Variables to move towards player.
        self.direction=pygame.math.Vector2()
        self.attack_radius=ENEMY_ATTACK_RADIUS*BASE_SIZE

        #The max size of the submatrix, centered around self( i.e., enemy sprite).
        self.SUBMATRIX_SIZE=12
        self.SUBMATRIX_HALF_SIZE=int(self.SUBMATRIX_SIZE//2)

        #Enemy UI.
        self.health=ENEMY_HEALTH

    def update_direction(self,player,level):
        #The default direction of the enemy.
        self.direction.x=player.rect.centerx-self.rect.centerx
        self.direction.y=player.rect.centery-self.rect.centery
        
        #Making the grid(A small submatrix of the level's matrix), centered about the enemy sprite. There is no need to do a grid.cleanup() as we create a new grid each time.
        small_submatrix=[]
        start_row=max(0,int((self.rect.y//BASE_SIZE)-self.SUBMATRIX_HALF_SIZE))
        end_row=min(len(level.detection_tiles),start_row+self.SUBMATRIX_SIZE)
        start_col=max(0,int((self.rect.x//BASE_SIZE)-self.SUBMATRIX_HALF_SIZE))
        end_col=min(len(level.detection_tiles[0]), start_col+self.SUBMATRIX_SIZE)
        for i in range(start_row,end_row,1):
            submatrix_row=level.detection_tiles[i][start_col:end_col]
            small_submatrix.append(submatrix_row)
        grid=Grid(matrix=small_submatrix)

        #Finding the start and end cells.
        start_x=int(self.rect.x//BASE_SIZE)-start_col
        start_y=int(self.rect.y//BASE_SIZE)-start_row
        end_x=min(max(int(player.rect.x//BASE_SIZE)-start_col, 0),end_col-start_col-1)
        end_y=min(max(int(player.rect.y//BASE_SIZE)-start_row, 0),end_row-start_row-1)
        start_cell=grid.node(start_x,start_y)
        end_cell=grid.node(end_x,end_y)
        
        #Finding the path to the player and updating the direction of the enemy sprite.
        path,runs=level.finder.find_path(start_cell,end_cell,grid)
        if(len(path)>2):
            # print(path)
            next_cell=path[1]       #This cell contains the indices in the submatrix, so we find the actual position in map. BASE_SIZE//2 is added to give a bit of diagonal movement.
            next_cell_col=(start_col+next_cell.x)*BASE_SIZE + BASE_SIZE//2
            next_cell_row=(start_row+next_cell.y)*BASE_SIZE + BASE_SIZE//2
            #Prioritizing the horizontal movement of the sprite over the vertical movement. Sprite can move either in horizontal or vertical only
            self.direction.x=next_cell_col-self.rect.x
            self.direction.y=next_cell_row-self.rect.y
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
        if(pygame.math.Vector2(level.player.rect.left-self.rect.left, level.player.rect.top-self.rect.top).magnitude()<=self.attack_radius):
            self.update_direction(level.player,level)
            if(self.direction.magnitude()!=0):
                self.direction=self.direction.normalize()
            self.rect.x+=self.direction.x*ENEMY_SPEED
            ret_val=self.handle_collisions("Horizontal",level)
            self.rect.y+=self.direction.y*ENEMY_SPEED
            ret_val=self.handle_collisions("Vertical",level)
            pass

        self.draw(display_surf,offset)
        pass

    def draw(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)
        pass