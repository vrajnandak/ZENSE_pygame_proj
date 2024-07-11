from Settings import *

#A separate class for ui as we have to do player_ui, enemy_ui, show the weapons, show the attacks, show the heals etc.
class UI:
    def __init__(self):
        #Font
        self.font=pygame.font.Font(None,30)

        pass

    def display(self,display_surf,player):
        player.display_ui(display_surf)
        pass