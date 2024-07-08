from Settings import *

class CollisionHelper:
    def __init__(self,level):
        self.the_level=level
        pass

    def update_detection_tiles_horizontal(self,entity,distance_moved):
        #Getting the entity's positions.
        top_row=int(entity.rect.top//BASE_SIZE)
        bottom_row=int(top_row+(entity.rect.height//BASE_SIZE))
        left_col_old=int((entity.rect.x-distance_moved)//BASE_SIZE)
        left_col_curr=int((entity.rect.x)//BASE_SIZE)

        #Setting the loop iterator val, level's vals.
        step_val=1 if distance_moved >0 else -1
        val1=1 if distance_moved > 0 else 0
        val2=0 if distance_moved > 0 else 1

        #The for loop.
        for i in range(left_col_old,left_col_curr,step_val):
            for j in range(top_row,bottom_row,1):
                self.the_level.detection_tiles[j][i]=val1
                self.the_level.detection_tiles[j][i+entity.width_tiles]=val2
        pass

    #A method to update the detection tiles of the level whenever the sprite moves horizontally.
    # def old_update_detection_tiles_horizontal(self,entity,distance_moved):
    #     top_row=int(entity.rect.top//BASE_SIZE)
    #     bottom_row=int(top_row+(entity.rect.height//BASE_SIZE))
    #     entity_width=entity.width_tiles
    #     left_col_old=int((entity.rect.x-distance_moved)//BASE_SIZE)
    #     left_col_curr=int((entity.rect.x)//BASE_SIZE)
    #     if(distance_moved>0):
    #         # left_col_old=int((entity.rect.x-distance_moved)//BASE_SIZE)
    #         # left_col_curr=int((entity.rect.x)//BASE_SIZE)
    #         # print(f'moved right, entity_width: {entity_width}, left old: {left_col_old} and left curr: {left_col_curr}')
    #         # print(f'left old:{left_col_old} and left curr:{left_col_curr}')
    #         # right_col_old=(entity.rect.right-distance_moved)//32
    #         # right_col_curr=(entity.rect.right)//32
    #         for i in range(left_col_old,left_col_curr,1):
    #             for j in range(top_row,bottom_row,1):
    #                 # print(f'before updation, self.the_level[{j}][{i}]: {self.the_level.detection_tiles[j][i]}')
    #                 self.the_level.detection_tiles[j][i]=1
    #                 # print(f'after having updated, self.the_level[{j}][{i}]: {self.the_level.detection_tiles[j][i]}')
    #                 self.the_level.detection_tiles[j][i+entity_width]=0
    #                 # print('updated',end='')
    #         pass
    #     elif(distance_moved<0):
    #         # left_col_old=int((entity.rect.x-distance_moved)//BASE_SIZE)
    #         # left_col_curr=int((entity.rect.x)//BASE_SIZE)
    #         # print(f'moved left, entity_width: {entity_width}, left old: {left_col_old} and left curr: {left_col_curr}')
    #         for i in range(left_col_old,left_col_curr,-1):
    #             for j in range(top_row,bottom_row,1):
    #                 self.the_level.detection_tiles[j][i]=0
    #                 self.the_level.detection_tiles[j][i+entity_width]=1
    #         pass
    #     pass

    def update_detection_tiles_vertical(self,entity,distance_moved):
        pass

    #A method to update the detection tiles of the level. This function is called only if the entity has moved.
    # def update_level_detection_tiles(self,entity,direction,old_pos,new_pos):
    #     movement=1 if (new_pos-old_pos) > 0 else -1         #We don't need to check for if there has been no movement as this function is called only if there has been movement.
    #     entity_cols=entity.rect.width//32           #The number of cols that the entity covers
    #     entity_rows=entity.rect.height//32          #The number of rows that the entity covers
    #     print('in the function')
    #     if direction=="Horizontal":
    #         old_col=old_pos//32                     #The old left position.
    #         new_col=new_pos//32                     #The new left position.
    #         cols_changed=abs(new_col-old_col)
    #         if(cols_changed>0):
    #             top_row=entity.rect.top//32
    #             if(movement==1):
    #                 for i in range(cols_changed):
    #                     for j in range(top_row,top_row+entity_rows,1):
    #                         self.the_level.detection_tiles[j][i+old_col]=1              #Changing the left portion to be set to 1
    #                         self.the_level.detection_tiles[j][new_col+entity_cols-i]=0
    #                         print('heylskfj')
    #                     # self.the_level.detection_tiles[i][old_col]=1
    #                     # self.the_level.detection_tiles[i][new_col]=1
    #                     pass
    #                 pass
    #         pass
    #     elif direction=="Vertical":
    #         pass
    #     pass

    #A method to get the max number of pixels that the player can move without having collision.
    def get_pixel_counter(self,entity,sprite,movement,distance_moved,is_horizontal,is_vertical):
        lower_lim=0
        upper_lim=abs(int(distance_moved))
        left=lower_lim
        right=upper_lim
        while left<=right:
            mid=left+(right-left)//2
            #If you were to calculate the offset for only horizontal movement then you would'nt want to consider the movement for y-axis and similarily vice-versa. So, this variable offest term that we're adding would be the same if written separately for horizontal, vertical collisions but since we've wrote them in one function, we set them to 0 appropriately.
            offset_x=sprite.rect.left-entity.rect.left-mid*movement*is_horizontal      #Considering only to add horizontal movement.
            offset_y=sprite.rect.top-entity.rect.top-mid*movement*is_vertical          #Considering only to add vertical movement.
            offset=(offset_x,offset_y)
            if entity.mask.overlap(sprite.mask,offset):
                right=mid-1
            else:
                left=mid+1
                pass
        return right
    
    #A method to set the entity as close as possible to the sprite in question, without having collision.
    def handle_horizontal_collision(self,entity,sprite,speed):
        movement= 1 if entity.direction.x > 0 else -1
        distance_moved=entity.direction.x*speed
        entity.rect.x-=distance_moved        #Undoing the added direction in x-axis as this caused mask collision.
        can_move_pixel=self.get_pixel_counter(entity,sprite,movement,distance_moved,1,0)
        new_distance_moved=movement*can_move_pixel
        entity.rect.x+=new_distance_moved
        return new_distance_moved
        # if(can_move_pixel!=0):
        #     print('should go to new function')
        #     self.update_level_detection_tiles(entity,"Horizontal",entity.rect.x-movement*can_move_pixel,entity.rect.x)
        pass

    def handle_vertical_collision(self,entity,sprite,speed):
        movement=1 if entity.direction.y > 0 else -1
        distance_moved=entity.direction.y*speed
        entity.rect.y-=distance_moved        #Undoing the added direction in y-axis as this caused the mask collision.
        can_move_pixel=self.get_pixel_counter(entity,sprite,movement,distance_moved,0,1)
        new_distance_moved=movement*can_move_pixel
        entity.rect.y+=new_distance_moved
        return new_distance_moved
        # if(can_move_pixel):
        #     print('should go to new function verticcally')
        # self.update_level_detection_tiles(entity,"Vertical",entity.rect.y-movement*can_move_pixel,entity.rect.y)
        pass

    #Returns whether or not a collision with the transportation portal has occured.
    def handle_spritegroup_collision(self,entity,speed,direction, spriteGroup, is_transportation_portal):
        has_entity_moved=0
        for sprite in spriteGroup:
            if sprite.rect.colliderect(entity.rect) and entity.rect.topleft!=sprite.rect.topleft:       #The 2nd condition is to eliminate an enemy sprite checking collision against itself. This is quite important because without this, an enemy sprite would trigger movement by itself when the player is in the attack radius, leading to absurd movement.
                if(is_transportation_portal):
                    #Transport the player
                    return 1
                elif(entity.mask.overlap(sprite.mask,(sprite.rect.left-entity.rect.left, sprite.rect.top-entity.rect.top))):
                    distance_moved=0
                    if(direction=="Horizontal"):
                        distance_moved=self.handle_horizontal_collision(entity,sprite,speed)
                        if(distance_moved!=0):
                            self.update_detection_tiles_horizontal(entity,distance_moved)
                    elif(direction=="Vertical"):
                        distance_moved=self.handle_vertical_collision(entity,sprite,speed)
                        if(distance_moved!=0):
                            self.update_detection_tiles_vertical(entity,distance_moved)
                    has_entity_moved+=distance_moved
        # if(speed==PLAYER_SPEED):
        #     print('player has_entity_moved: ',has_entity_moved)
        if(has_entity_moved!=0):
            return 2                    #Indicates that the entity has moved and tiles have been updated already.
        else:
            return 0                    #Indicates that the tiles have not been updated by the collision detector.