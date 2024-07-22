from Settings import *

#This map contains the information related to each level that has to be displayed or shown.

#This is used only when the game is started.
game_lore=[
    "In a world with advanced technology, evil organizations, adventurers and more, 3 scientists are curious about the recently discovered ruins which are rumored to hold an ancient device, capable of travelling through space and time.", "Intrigued by these rumors, the scientists decide to explore the ruins before anyone else and try to unlock the secrets to time-travelling. They bring with them a famous adventurer, who has survived all by himself in many islands and discovered hidden treasures.", "To their surprise however, they lose each other while exploring the island and each gets sent to a different ruin entrance. The protagonist, an old friend of theirs and the number one adventurer in the world(who's now retired), gets a call from one of these scientist's colleagues asking him to rescue to them.", "The protagonist, with no hesitation, sets out to the island in hopes of rescuing them."
]
game_info=[
    "Player Movement Controls: [w,a,s,d] or [up,left,down,right arrow keys]",
    "Player attack: [space bar]\n Player magic: [left_control]",
    "Switch weapon: [n,p] for next and previous weapon\nSwitch magic: [m,o] for next and previous magic",
    "Camera Movement: [b] for box camera, [i,j,k,l] for keyboard camera movement, hover mouse close to screen end for mouse camera movement",
    "Pause screen: [esc] for pause screen. Another esc to go back to the game from pause screen",
    "Settings: Current weapon, magic information is displayed. Can purchase upgrades only if you have sufficient exp."
]


EVENT_CODES=['BeforeKillingAnyEnemy','AfterKillingAllEnemy','PortalCollision','FoundKeyPressingE']
RUIN0_ENTRY_CODE=106

start_msg={         #The key is the level id.
    '0':["Find the code to save the scientist.\n'To the one who explores this island, the key shall reveal itself'\nPress '9' near the portal to type the code."],              #Have to constantly check if the player is colliding with a particular rect and pressing 9.
    '1':["Save the Scientist by unlocking the cage.\nTalk with the scientist to get a clue where the key is."],                                                                 #Event handled when level's enemy counter reaches 0.
    '2':["Save the scientist from the ruins.\nTalk with the scientist to help him escape."],
    '3':["Save the scientist and leave these ruins."],
}

Scientist1={    #Is Stuck in Ruin1
    'dialog':{ EVENT_CODES[0]: ['Please Find the key to this cell.',
                                'I Think the key should be somewhere here. Can you check around',
                                'Hmmm, Maybe the cage will unlock if you destroy all the enemies in this room.',
                                'Can you please help me.'
                            ],
                EVENT_CODES[1]: ['Thank you so much for saving me.',
                                'Can you also save the other 2.',
                                'I think each of us got taken into different ruins',
                                'I wish you best of luck'
                            ]
            }
}

Scientist2={
    'dialog':{
        EVENT_CODES[0]:['Please save me from these Ruins.',
                        'I Think you need to find the hidden Key.',
                        "I don't know the exact location but press 'E' when near it."
        ],
        EVENT_CODES[1]:['Wow, You have already killed all the zombies.'],
        EVENT_CODES[3]:['Finally, You have found the key.',
                        'Thank you so much for saving me'
        ]
    }
}

#Conditions to display the messages.
#->Ruin0    ==> Start_msg,


class LEVEL_INFO:
    def __init__(self,level_id):
        self.level_id=level_id
        self.start_msg=start_msg[str(level_id)]

        self.codeEnterImg=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Code_Enter_image.png"))
        self.codeEnterImg_rect=self.codeEnterImg.get_rect(topleft=(200,200))
        pass

    #A method to get the correct code from the player.
    def getCorrectCodeFromPlayer(self):
        # SaveGameScreen(filename=os.path.join(GRAPHICS_DIR_PATH,"GameScreen.png"))
        # bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"GameScreen.png"))
        bg=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        bg.fill('black')
        bg.blit(self.codeEnterImg,self.codeEnterImg_rect.topleft)
        display_surf=pygame.display.get_surface()
        rectangles=[]
        rectangles_left=[278,568,860]
        rectangle_top=[325,413,499]
        rectangle_sizes=60
        for top in rectangle_top:
            for left in rectangles_left:
                rectangle=pygame.rect.Rect(left,top,rectangle_sizes,rectangle_sizes)
                rectangles.append(rectangle)
        rectangles.append(pygame.rect.Rect(568,582,rectangle_sizes,rectangle_sizes))

        enter_button=pygame.rect.Rect(860,582,rectangle_sizes,rectangle_sizes)
        clear_button=pygame.rect.Rect(278,582,rectangle_sizes,rectangle_sizes)
        pass_code=""
        font=pygame.font.Font(None,60)

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        if(pass_code==""):
                            return 1
                        return int(pass_code)
                    elif event.key==pygame.K_BACKSPACE:
                        pass_code=pass_code[:-1]
                    elif event.key>=pygame.K_0 and event.key<=pygame.K_9:
                        num_entered=str(event.key-pygame.K_0)
                        pass_code+=num_entered
                if event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    for index,rect in enumerate(rectangles):
                        if rect.collidepoint(mouse_pos):
                            index+=1
                            if(index==10):
                                index=0
                            pass_code+=str(index)
                    if clear_button.collidepoint(mouse_pos):
                        pass_code=pass_code[:-1]
                    if enter_button.collidepoint(mouse_pos):
                        if(pass_code==""):
                            return 1
                        return int(pass_code)
                    pass
            display_surf.blit(bg,(0,0))
            # print(pygame.mouse.get_pos())
            pass_code_surf=font.render(pass_code,True,'black')
            pass_code_rect=pass_code_surf.get_rect(topright=(932,228)) #pygame.rect.Rect(932,228,pass)
            display_surf.blit(pass_code_surf,pass_code_rect.topleft)
            pygame.display.flip()
            
        pass

    #A method to handle the different events that happen in the game.
    def handle_event(self,event_code,level=None):
        if event_code==EVENT_CODES[0]:
            pass
        elif event_code==EVENT_CODES[1]:
            if level:
                if level.level_id==1 and not level.player.has_killed_all_enemies_in_ruin1_and_unlocked_gate:
                    #Display the message
                    SaveGameScreen()
                    bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Curr_Screen.png"))
                    DISPLAY_DIALOGS(["Hurray, You have Saved the Scientist1!!!!!",],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
                    if level.unlockable_gate_sprites:
                        for sprite in level.unlockable_gate_sprites:
                            sprite.kill()
                        
                    level.player.has_killed_all_enemies_in_ruin1_and_unlocked_gates=True
                    # level.level_scientist=
            pass
        elif event_code==EVENT_CODES[2]:
            if self.level_id==0 and level!=None and level.player.has_entered_correct_code==False:
                # if level:
                SaveGameScreen()
                bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Curr_Screen.png"))
                if level.player.rect.colliderect(Ruin0_rect_enterCode) and pygame.key.get_pressed()[pygame.K_9]:
                    # SaveGameScreen()
                    # bg_image=pygame.image.load(os.path.join())
                    code=self.getCorrectCodeFromPlayer()
                    if(code!=RUIN0_ENTRY_CODE):
                        # bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Curr_Screen.png"))
                        DISPLAY_DIALOGS(["You have entered the Wrong Code. Dash into the portal while pressing '9' and try again\n(The code is a 3-digit code.)","Hint: The Seas are vast and have yet to be explored."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                        return 0
                    else:
                        level.player.has_entered_correct_code=True
                        # print('You have successfully crossed over to Ruin1')
                        return 1        #Indicates that the map should be changed. The map will be chosen in Game.py
                elif not level.player.rect.colliderect(Ruin0_rect_enterCode):
                    # SaveGameScreen()
                    DISPLAY_DIALOGS(["Please Clear Ruin1 Before entering this Ruin."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                    return 0
                # pass
            return 1
        else:
            pass
        pass

    def update(self,display_surf):
        pass
        # if (not self.has_displayed_basic_game_info) or (self.has_displayed_start_msg):
        # self.inputs()
        # self.display_game_info(display_surf)
        # self.display_start_msg(display_surf)
        # self.apply_cooldown()


class Scientist(pygame.sprite.Sprite):
    def __init__(self,pos,groups,scientist_id):
        super().__init__(groups)
        self.pos=pos
        self.scientist_id=scientist_id
        self.graphics_path=os.path.join(GRAPHICS_DIR_PATH,"SCIENTISTS",f'Scientist{self.scientist_id}')

        self.img=pygame.image.load(os.path.join(self.graphics_path,f'Scientist{self.scientist_id}.png'))
        self.rect=self.img.get_rect(topleft=pos)

        self.dialogs={}
        # self.dialog_index=0
        self.initialize_dialogs()
        pass

    def initialize_dialogs(self):
        if self.scientist_id==1:
            self.dialogs=Scientist1["dialog"]
        elif self.scientist_id==2:
            pass
        elif self.scientist_id==3:
            pass
        pass

    def draw(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)

    def update(self,display_surf,offset):
        #If player within proximity, play the EVENT_CODES[0] messages.
        self.draw(display_surf,offset)
        pass
    pass