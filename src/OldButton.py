import pygame

class Button:
    def __init__(self,pos,button_width,button_height,text,font,text_color,background_color,hover_color,click_color):
        self.pos=pos                    #We're going to let this be a tuple.
        self.button_width=button_width
        self.button_height=button_height
        self.text=text
        self.font=font
        self.text_color=text_color
        self.background_color=background_color
        self.hover_color=hover_color
        self.click_color=click_color


        #For animation purposes. The idea is to make the button appear from the left side of the screen. The second button appears only when the first button has come to final position.
        self.animation_speed=0.1
        self.final_left_pos=self.pos[0]
        self.curr_left_pos=0

        # #For animation purposes. The idea is to inflate the button when the mouse hovers on the screen.
        # self.hover_stat="Forward"           #Set to 'Forward' when mouse hovers on button, else it is set to 'Backward'.
        # self.inflate_width=0.1
        # self.inflate_height=0.1
        # self.hover_width=self.button_width + 50
        # self.hover_height=(self.hover_width*self.button_height)//self.button_width          #This is to try to maintain the aspect ratio.
        # self.inflate_counter=0
        # self.inflate_max_count=self.inflate_width*(self.hover_width-self.button_width)
        # self.new_width=self.button_width
        # self.new_height=self.button_height


        #Top rectangle.
        self.top_rect=pygame.Rect((self.curr_left_pos,self.pos[1]),(self.button_width,self.button_height))
        self.top_color=self.background_color

        #Text
        self.text_surf=self.font.render(text,True,self.text_color)          #The text to be rendered, antialias, color_of_text, bg=none. The documentation says newline characters not allowed so we'd have to physically place the text on the button surface. When anti-aliasing is enabled (True), Pygame applies techniques to blend the edges of the text pixels with the background pixels, making the text appear smoother and more readable, especially at smaller font sizes or when the text is displayed against complex backgrounds.
            #The below text_rect is to get the rectangle to place the text surface. From this rectangle, we get the width and height of the surface. Now, we use these along with the center position of the top_rect inorder to display the text properly and be able to move it as well.
        self.text_rect=self.text_surf.get_rect(center=self.top_rect.center)
        self.text_rect_width=self.text_rect.right-self.text_rect.left
        self.text_rect_height=self.text_rect.bottom-self.text_rect.top
        # self.img=pygame.Surface((self.button_width,self.button_height),pygame.SRCALPHA)
        # self.rect=self.image.get_rect(topleft=self.pos)
        pass

    def chk_mousepos(self):
        mouse_pos=pygame.mouse.get_pos()
        # if 
        #If mouse hovers i.e., self.hover_stat=='Forward'.
            #if(self.inflate_counter<self.):
                #self.
        #When mouse is not hovering on the button, inflate_ip again but only if the rect was inflate previously.
        pass

    def animate(self):          #We could add like a linear equation and decide how fast the animation should by setting the self.curr_left_pos based on the current number of ticks and set this value to self.curr_left_pos(This would be only to smoothen the animation)
        if(self.curr_left_pos<self.final_left_pos):
            self.curr_left_pos+=self.animation_speed
            self.top_rect.left=self.curr_left_pos
        
        #The below code doesn't work as top_rect cannot be a decimal i think.
        # if(self.top_rect.left<self.final_left_pos):
        #     self.top_rect.left+=self.animation_speed
        #     print(self.top_rect.left)
        pass

    def draw(self,display_surf):
        self.animate()
        pygame.draw.rect(display_surf, self.top_color, self.top_rect)           #Drawing the top rectangle on the screen.
        display_surf.blit(self.text_surf,(self.top_rect.centerx-self.text_rect_width//2,self.top_rect.centery-self.text_rect_height//2))
        # print('self.top_rect.centery: ', self.top_rect.centery)
        # print('top of the text: ',self.top_rect.centery - self.text_rect_height)
        # display_surf.blit(self.text_surf, self.text_rect)