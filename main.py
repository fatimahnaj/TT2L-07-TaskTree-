import pygame
from classes_functions import *

pygame.init()

screen_size = (1540,800)
screen_width = screen_size[0]
screen_height = screen_size[1]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('TaskTree')

#colors
black = (0,0,0)
grey = (231,231,245)
dark_grey = (94,99,122)
blue = (39, 39, 89)

#in seconds
pomodoro_length = 300
break_length = 10
timer = 0

lap_length = 3
current_lap = 1
current_seconds = pomodoro_length
pygame.time.set_timer(pygame.USEREVENT, 1000)

started = False
stopwatch = False
pomodoro = True

pomodoro_button = TEXT("pomodoro",675,120,20,black,blue)
break_button = TEXT("break",790,120,20,black,blue)
stopwatch_button = TEXT("stopwatch",905,120,20,black,blue)
start_stop_button = TEXT("START",775,270,30,black)

settings = BUTTON(0,0)
settings_button = BUTTON((screen_width-74),67,72,69)
back = BUTTON(0,0)
back_button = BUTTON((screen_width-115),75,110,100)

increase_pomodoro = BUTTON(245, 325, 40, 20)
decrease_pomodoro = BUTTON(245, 350, 40, 20)
increase_break = BUTTON(245, 487, 40, 20)
decrease_break = BUTTON(245, 510, 40, 20)


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

        global current_seconds,started,timer,stopwatch,pomodoro,lap_length,current_lap,pomodoro_length,break_length

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #pomodoro setup
            if event.type == pygame.MOUSEBUTTONDOWN:
                #check if start/stop button is clicked, toggle the pomodoro
                if start_stop_button.check_for_input(pygame.mouse.get_pos()): 
                    if started:
                        started = False
                        start_stop_button.update_text("START")
                    else:
                        started = True
                        start_stop_button.update_text("STOP")
                #display pomodoro, stop the break/stopwatch
                if pomodoro_button.check_for_input(pygame.mouse.get_pos()):
                    if started == False:
                        started = False
                        current_seconds = pomodoro_length
                        start_stop_button.update_text("START")
                        stopwatch = False
                        pomodoro = True
                    else:
                        current_seconds = current_seconds
                #display break time, stop the pomodoro/stopwatch
                if break_button.check_for_input(pygame.mouse.get_pos()):
                    if started == False:
                        started = False
                        current_seconds = break_length
                        start_stop_button.update_text("START")
                        stopwatch = False
                        pomodoro = False
                    else:
                        current_seconds = current_seconds
                #display stopwatch, stop the pomodoro
                if stopwatch_button.check_for_input(pygame.mouse.get_pos()):
                    if started == False:
                        started = False
                        current_seconds = timer
                        start_stop_button.update_text("START")
                        stopwatch = True
                        pomodoro = False
                    else:
                        current_seconds = current_seconds
                #settings button
                if settings_button.check_for_input(pygame.mouse.get_pos()):
                    screen_settings()
                    print("Switching to settings screen.")
            #counting the time
            if event.type == pygame.USEREVENT and started:
                if stopwatch:
                    current_seconds += 1
                else:
                    if current_lap < lap_length:
                        if current_seconds > 0:
                            current_seconds -= 1
                        elif current_seconds == 0:
                                if pomodoro:
                                    current_seconds = break_length
                                    pomodoro = False
                                else:
                                    current_seconds = pomodoro_length
                                    pomodoro = True
                                    current_lap += 1
                                    print(current_lap)
                    elif current_lap == lap_length:
                        if current_seconds > 0:
                            current_seconds -= 1
                        elif current_seconds == 0:
                                if pomodoro:
                                    current_seconds = break_length
                                    pomodoro = False
                                else:
                                    current_seconds = pomodoro_length
                                    pomodoro = True
                                    started = False
                                    start_stop_button.update_text("START")
                                    print("finish lap")


        bg('Design/main room.png')
        settings.image_button('Design/setting-button1.png')
        pomodoro_button.hover_color_change()
        break_button.hover_color_change()
        stopwatch_button.hover_color_change()
        start_stop_button.display_text()
        
        if current_seconds >= 0:
            display_seconds = current_seconds % 60
            display_minutes = int(current_seconds / 60) % 60
            display_hour = int(current_seconds / 3600) % 60
        countdown_text = TEXT(f"{display_hour:02}:{display_minutes:02}",755,190,90,black)
        sec_countdown_text = TEXT(f"{display_seconds:02}",930,210,45,black)
        countdown_text.display_text()
        sec_countdown_text.display_text()

        pygame.display.flip()

    pygame.quit()

def screen_settings():
    run = True
    while run:

        global pomodoro_length,break_length,lap_length,current_seconds


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #pomodoro settings
                if increase_pomodoro.check_for_input(pygame.mouse.get_pos()):
                    if pomodoro_length == 3600:
                        pomodoro_length = pomodoro_length
                    else:
                        pomodoro_length = pomodoro_length + 300
                        print(pomodoro_length)
                if decrease_pomodoro.check_for_input(pygame.mouse.get_pos()):
                    if pomodoro_length > 300:
                        pomodoro_length = pomodoro_length - 300
                        print(pomodoro_length)
                    else:
                        pomodoro_length = pomodoro_length
                #break settings
                if increase_break.check_for_input(pygame.mouse.get_pos()):
                    if break_length == 3310:
                        break_length = break_length
                    else:
                        break_length = break_length + 300
                        print(break_length)
                if decrease_break.check_for_input(pygame.mouse.get_pos()):
                    if break_length > 300:
                        break_length = break_length - 300
                        print(break_length)
                    else:
                        break_length = break_length
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    screen_home()
                    print("Returning to homescreen")

        
        bg('Design/setting page.png')
        back.image_button('Design/back-button.png')
        convert_time(pomodoro_length,180,330,60)
        convert_time(break_length,180,495,60)

        pygame.display.flip()

    pygame.quit()

screen_home()
