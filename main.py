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
pomodoro_length = 10
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

#Level Points
point_per_second = 1/60
level_xp_increment = 10
level_bar = LevelBar(60, 80, 200, 30, 0)

start = BUTTON(20, 20)
start_button = BUTTON(790, 440, 400, 170) 

plant = BUTTON(0, 0)
plant_button = BUTTON(90, 290, 70, 70)
garden = BUTTON(0, 0)
garden_button = BUTTON(90, 490, 70, 70)

shop = BUTTON(0, 0)
shop_button = BUTTON(60, 290, 100, 80)
shop_back = BUTTON(345, 300, 100,80)

water_plant = BUTTON(120, 400, 120, 50)
fertilizer = BUTTON(120, 570, 120, 50)


#user input for todo list
user_input = ""
input_text = TEXT(user_input, 780,350,20, grey, grey,"DePixelHalbfett.ttf")
add_task_text = TEXT("Todo list :", 1250, 525, 20, dark_grey, dark_grey,"DePixelHalbfett.ttf")
add_task_button = BUTTON(screen_width-70, screen_height-80, 50, 50, black)
input_your_text = TEXT("Enter your task for today !", 800, 200, 30, blue, blue,"DePixelHalbfett.ttf")
todo_lists = [""]
todo1 = ""
todo1_text = TEXT(todo1, 1250, 570, 18, grey, grey,"DePixelHalbfett.ttf")


#screen functions
def screen_startup():
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #start button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_for_input(pygame.mouse.get_pos()):
                    screen_home()
                    print("Switching to home screen.")

        bg('Design/frontpage.png')
        start.image_button('Design/frontpage-button1.png')
        
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
                #add to do list button
                if add_task_button.check_for_input(pygame.mouse.get_pos()):
                    screen_user_input()
                #settings button
                if settings_button.check_for_input(pygame.mouse.get_pos()):
                    screen_settings()
                    print("Switching to settings screen.")
                #plant button
                if plant_button.check_for_input(pygame.mouse.get_pos()):
                    screen_plant()
                    print("Switching to plant screen.")
                #garden button
                if garden_button.check_for_input(pygame.mouse.get_pos()):
                    screen_garden()
                    print("Switching to garden screen.")
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
                                    print("pomodoro completed")
                                    # level_bar.addXP(pomodoro_length * point_per_second)
                                    level_bar.addXP(20)
                                    level_bar.draw(screen)
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
                                    print("pomodoro completed")
                                    # level_bar.addXP(pomodoro_length * point_per_second)
                                    level_bar.addXP(20)
                                    level_bar.draw(screen)
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
        plant.image_button('Design/plant-button.png')
        garden.image_button('Design/garden-button.png')
        pomodoro_button.hover_color_change()
        break_button.hover_color_change()
        stopwatch_button.hover_color_change()
        start_stop_button.display_text()
        taskboard = pygame.Rect(1000, 500, 500, 250)
        pygame.draw.rect(screen, grey, taskboard)
        add_task_text.display_text()
        add_task_button.draw_button()
        todo1_text.display_text()
        
        if current_seconds >= 0:
            display_seconds = current_seconds % 60
            display_minutes = int(current_seconds / 60) % 60
            display_hour = int(current_seconds / 3600) % 60
        countdown_text = TEXT(f"{display_hour:02}:{display_minutes:02}",755,190,90,black)
        sec_countdown_text = TEXT(f"{display_seconds:02}",930,210,45,black)
        countdown_text.display_text()
        sec_countdown_text.display_text()


        #draw level bar
        level_bar.draw(screen)

        level_text = TEXT("Level " + str(level_bar.level), 110, 50, 50, black)
        level_text.display_text()

        pygame.display.flip()

    pygame.quit()

def screen_user_input():
    run = True
    while run:

        global user_input,todo1
        user_input_limit = 300
        user_input_length = input_text.check_text_length(user_input)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    screen_home()
                    print("Returning to homescreen")
            #input_text
            if event.type == pygame.TEXTINPUT:
                if user_input_length < user_input_limit:
                    user_input += event.text
                else:
                    user_input = user_input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                if event.key == pygame.K_RETURN:
                    todo_lists.append(user_input)
                    todo1 = todo_lists[1]
                    todo1_text.update_text(todo1)
                    todo1_text.update_color(black)
                    user_input = ""
                    input_text.update_text(user_input)
                    screen_home()
        
        screen.fill(grey)
        back.image_button('Design/back-button.png')
        input_your_text.display_text()
        input_box = pygame.Rect(500,280, 600, 150)
        pygame.draw.rect(screen, blue, input_box)
        input_text.display_text()
        input_text.update_text(user_input)

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

def screen_plant() :
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    screen_home()
                    print("Returning to homescreen")
                #shop button
                if shop_button.check_for_input(pygame.mouse.get_pos()):
                    screen_shop()
                    print("Switching to shop screen.")

        bg('Design/plant1.png')
        back.image_button('Design/back-button.png')
        shop.image_button('Design/shop-button.png')

        pygame.display.flip()

    pygame.quit()

def screen_garden() :
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    screen_home()
                    print("Returning to homescreen")

        bg('Design/garden.png')
        back.image_button('Design/back-button.png')

        pygame.display.flip()

    pygame.quit()

def screen_shop():
    run = True
    clock = pygame.time.Clock()
    show_watering_can = False
    watering_can_start_time = 0
    watering_can_duration = 800  
    show_fertilizer = False
    fertilizer_start_time = 0
    fertilizer_duration = 800  
    background_image = pygame.image.load('Design/shop-page.png').convert()

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_back.check_for_input(pygame.mouse.get_pos()):
                    screen_plant()
                    print("Returning to plant screen")
                if water_plant.check_for_input(pygame.mouse.get_pos()):
                    show_watering_can = True
                    watering_can_start_time = pygame.time.get_ticks()  # Record the start time
                if fertilizer.check_for_input(pygame.mouse.get_pos()):
                    show_fertilizer = True
                    fertilizer_start_time = pygame.time.get_ticks()  # Record the start time

        # Blit the background image
        screen.blit(background_image, (0, 0))

        # Check if we need to show the watering can image
        if show_watering_can:
            current_time = pygame.time.get_ticks()
            if current_time - watering_can_start_time < watering_can_duration:
                # Load the watering can image
                watering_can_image = pygame.image.load('Design/watering-can.png').convert_alpha()
                # Calculate its position to center it on the screen
                watering_can_rect = watering_can_image.get_rect(center=(screen_width / 2, screen_height / 2))
                # Blit the watering can image
                screen.blit(watering_can_image, watering_can_rect)
            else:
                show_watering_can = False
                
        if show_fertilizer:
            current_time = pygame.time.get_ticks()
            if current_time - fertilizer_start_time < fertilizer_duration:
                # Load the watering can image
                fertilizer_image = pygame.image.load('Design/fertilizer.png').convert_alpha()
                # Calculate its position to center it on the screen
                fertilizer_rect = fertilizer_image.get_rect(center=(screen_width / 2, screen_height / 2))
                # Blit the watering can image
                screen.blit(fertilizer_image, fertilizer_rect)
            else:
                show_fertilizer = False


        pygame.display.flip()
        clock.tick(60)  # Limit frame rate to 60 FPS

    pygame.quit()

screen_startup()
