import pygame
pygame.init()

screen_size = (1540,800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('TaskTree')

run = True
while run:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip() #updates the display

pygame.quit()