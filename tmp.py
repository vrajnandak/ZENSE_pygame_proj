import pygame
pygame.init()

Window=pygame.display.set_mode((550,550),pygame.RESIZABLE)
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    Window.fill('black')
    surf=pygame.image.load('graphics/Player/idle.png')
    Window.blit(surf,(300,300))
    pygame.display.flip()
    