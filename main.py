import pygame
from classes_functions import *

pygame.init()

screen_size = (1540,800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('TaskTree')

#colors
black = (0,0,0)
grey = (231,231,245)
dark_grey = (94,99,122)
blue = (94, 69, 178)

pomodoro_length = 10000
break_length = 300
timer = 0

current_seconds = pomodoro_length
pygame.time.set_timer(pygame.USEREVENT, 1000)
started = False
stopwatch = False

pomodoro_button = TEXT("pomodoro",675,120,20,black,blue)
break_button = TEXT("break",775,120,20,black,blue)
timer_button = TEXT("timer",855,120,20,black,blue)
start_stop_button = TEXT("START",755,260,20,grey)

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

        global current_seconds,started,timer,stopwatch

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_stop_button.check_for_input(pygame.mouse.get_pos()):
                    if started:
                        started = False
                        start_stop_button.update_text("START")
                    else:
                        started = True
                        start_stop_button.update_text("STOP")
                if pomodoro_button.check_for_input(pygame.mouse.get_pos()):
                    started = False
                    current_seconds = pomodoro_length
                    stopwatch = False
                if break_button.check_for_input(pygame.mouse.get_pos()):
                    started = False
                    current_seconds = break_length
                    stopwatch = False
                if timer_button.check_for_input(pygame.mouse.get_pos()):
                    started = False
                    current_seconds = timer
                    stopwatch = True
            if event.type == pygame.USEREVENT and started:
                if stopwatch == False:
                    current_seconds -= 1
                else:
                    current_seconds += 1

        bg('Design/main room.png')
        pomodoro_button.hover_color_change()
        break_button.hover_color_change()
        timer_button.hover_color_change()
        start_stop_button.display_text()

        
        if current_seconds >= 0:
            display_seconds = current_seconds % 60
            display_minutes = int(current_seconds / 60) % 60
            display_hour = int(display_minutes / 60) % 60
        countdown_text = TEXT(f"{display_hour:02}:{display_minutes:02}",755,165,80,black)
        sec_countdown_text = TEXT(f"{display_seconds:02}",910,180,40,black)
        countdown_text.display_text()
        sec_countdown_text.display_text()

        pygame.display.flip()

    pygame.quit()

def screen_settings() :
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((64, 64, 64))
        if pygame.mouse.get_pressed()[0] == 1: 
            screen_settings()
        
        pygame.display.flip()

    pygame.quit()

def screen_tree() :
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((0, 128, 0))
        if pygame.mouse.get_pressed()[0] == 1: 
            screen_tree()
        
        pygame.display.flip()

    pygame.quit()
        

screen_startup()