import pygame
pygame.init()

screen_size = (1540,800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('TaskTree')


def screen_startup():
    run = True
    while run:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((200,200,200))
        if pygame.mouse.get_pressed()[0] == 1:
            screen_home()
        pygame.display.flip()

    pygame.quit()

def screen_home():
    run = True
    while run:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((150, 75, 0))
        pygame.display.flip()
        
    pygame.quit()

screen_startup()
#this is fatimah testing the push and pull feature
#lalamove
#whyoh
#aaa
#jaaa
#jaaa