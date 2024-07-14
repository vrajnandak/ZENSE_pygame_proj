from Settings import *

#This map contains the information related to each level that has to be displayed or shown.

class LEVEL_INFO:
    def __init__(self,level_id,has_displayed_basic_game_info):
        # self.start_msg=[]
        # if(not has_displayed_basic_game_info):
            # self.start_msg="Player Movement Controls."
        if(level_id==0):
            self.start_msg='Find the code to save the scientist. \n"To the one who explores this island, the key shall reveal itself"\nFind the portal and press "9" to enter the code.\n(Enter "Enter" to return to game).'
            pass
        elif(level_id==1):
            pass
        elif(level_id==2):
            pass
        elif(level_id==3):
            pass
        

        self.has_displayed_start_msg=False
        #FOR SHOWING THE MESSAGE AS A TIMER BASED THING, USE THESE VARIABLES.
        self.display_start_msg_timer=10000
        self.display_start_msg_time=None
        pass
    
    #A method to get the inputs.
    def inputs(self):
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_RETURN]):
            self.has_displayed_start_msg=True
        pass

    #A method to apply cooldowns.
    def apply_cooldown(self):
        curr_time=pygame.time.get_ticks()
        if curr_time-self.display_start_msg_time>=self.display_start_msg_timer:
            self.has_displayed_start_msg=True
        pass

    def display_start_msg(self):
        if not self.has_displayed_start_msg:
            if(self.display_start_msg_time==None):
                self.display_start_msg_time=pygame.time.get_ticks()
            DISPLAY_MSG(self.start_msg,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2))
            # self.apply_cooldown()
        pass

    def update(self):
        self.inputs()
        self.display_start_msg()