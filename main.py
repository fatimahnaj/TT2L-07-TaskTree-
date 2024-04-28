import pygame
from classes_functions import *
pygame.init()

screen_size = (1540,800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('TaskTree')

black = (0,0,0)
grey = (231,231,245)
dark_grey = (94,99,122)
blue = (94, 69, 178)

pomodoro_length = 14
break_length = 5

current_seconds = pomodoro_length
pygame.time.set_timer(pygame.USEREVENT, 1000)

pomodoro_text = TEXT("pomodoro",675,120,20,black,blue)
break_text = TEXT("break",775,120,20,black,blue)
timer_text = TEXT("timer",855,120,20,black,blue)
pomodoro_timer_text = TEXT(current_seconds,755,165,80,black,black)

#screen functions
def screen_startup():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bg('Design/frontpage.png')
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
            if event.type == pygame.USEREVENT and current_seconds >0 :
                current_seconds -= 1
            else:
                current_seconds = 0

        bg('Design/main room.png')
        pomodoro_text.hover_color_change()
        break_text.hover_color_change()
        timer_text.hover_color_change()
        pomodoro_timer_text.display_text()
        pygame.display.flip()
        
    pygame.quit()

screen_startup()