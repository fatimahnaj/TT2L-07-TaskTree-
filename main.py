import pygame
import json
import os
from classes_functions import *

pygame.init()
pygame.mixer.init()

screen_size = (1540,800)
screen_width = screen_size[0]
screen_height = screen_size[1]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('TaskTree')

clock = pygame.time.Clock()
clock.tick(60)  # Limit frame rate to 60 FPS

#colors
black = (0,0,0)
grey = (231,231,245)
dark_grey = (94,99,122)
blue = (39, 39, 89)

#in seconds
#pomodoro_length = 1800
#break_length = 300
pomodoro_length = 1
break_length = 3
timer = 0

lap_length = 4
current_lap = 1
current_seconds = pomodoro_length
pygame.time.set_timer(pygame.USEREVENT, 1000)

started = False
stopwatch = False
pomodoro = True

settings = BUTTON(0,0)
settings_button = BUTTON((screen_width-74),67,72,69)
back = BUTTON(0,0)
back_button = BUTTON((screen_width-115),75,110,100)

#Level Points
point_per_second = 1/60
level_xp_increment = 10
level_bar = LevelBar(60, 80, 200, 30, 0)

#Coins 
coins_per_task = 30
coins_bar = Coins(0)
coins_text = TEXT("Coins: " + str(coins_bar.coins), 200, 150, 50, black)

ambience_level_required = {
    'sunny' : 0,
    'night' : 1,
    'snow' : 2,
}

start = BUTTON(20, 20)
start_button = BUTTON(790, 440, 400, 170)

#ambience
sunny_bg = BUTTON(1200, 330, 50, 50)
night_bg = BUTTON(1350, 330, 50, 50)
snow_bg = BUTTON(1450, 330, 50, 50)

plant = BUTTON(0, 0)
plant_button = BUTTON(90, 290, 70, 70)
garden = BUTTON(0, 0)
garden_button = BUTTON(90, 490, 70, 70)

shop = BUTTON(0, 0)
shop_button = BUTTON(60, 290, 100, 80)
shop_back = BUTTON(345, 300, 100,80)

#music
music_1 = BUTTON(670, 450, 60, 60)
music_2 = BUTTON(770, 450, 60, 60)
music_3 = BUTTON(870, 450, 60, 60)

#user input for todo list
user_input = ""
input_text = TEXT(user_input, 780,350,20, grey, grey,"DePixelHalbfett.ttf")
add_task_button = BUTTON(screen_width-70, screen_height-80, 50, 50, black)
add_task_text = TEXT("Todo list :", 1250, 525, 20, dark_grey, dark_grey,"DePixelHalbfett.ttf")
checklist_1_button = BUTTON(1020, 570, 20, 20, grey)
checklist_2_button = BUTTON(1020, 620, 20, 20, grey)
checklist_3_button = BUTTON(1020, 670, 20, 20, grey)
input_your_text = TEXT("Enter your task for today !", 800, 200, 30, blue, blue,"DePixelHalbfett.ttf")
todo_lists = [""]
todo1 = ""
todo2 = ""
todo3 = ""
todo1_text = TEXT(todo1, 1250, 570, 18, black, black,"DePixelHalbfett.ttf")
todo2_text = TEXT(todo2, 1250, 620, 18, black, black,"DePixelHalbfett.ttf")
todo3_text = TEXT(todo3, 1250, 670, 18, black, black,"DePixelHalbfett.ttf")

def finish_task_3(button):
    if button == 1:
        todo_lists.remove(todo_lists[1])
        todo1_text.update_text(todo_lists[1])
        todo2_text.update_text(todo_lists[2])
        todo3 = ""
        todo3_text.update_text(todo3)
    elif button == 2:
        todo_lists.remove(todo_lists[2])
        todo2_text.update_text(todo_lists[2])
        todo3 = ""
        todo3_text.update_text(todo3)
    elif button == 3:
        todo_lists.remove(todo_lists[3])
        todo3 = ""
        todo3_text.update_text(todo3)
    checklist_3_button.update_color(grey)

def finish_task_2(button):
    if button == 1:
        todo_lists.remove(todo_lists[1])
        todo1_text.update_text(todo_lists[1])
        todo2 = ""
        todo2_text.update_text(todo2)
    elif button == 2:
        todo_lists.remove(todo_lists[2])
        todo2 = ""
        todo2_text.update_text(todo2)
    checklist_2_button.update_color(grey)

#save & load data
def save_game_state():
    game_state = {
        'level': level_bar.level,
        'coins': coins_bar.coins,
        'todo_lists': todo_lists,
        'todo1': todo1,
        'todo2': todo2,
        'todo3': todo3,
        
    }
    with open('game_state.txt', 'w') as f:
        json.dump(game_state, f)

def load_game_state():
    global level_bar, coins_bar, todo_lists, todo1, todo2, todo3
    if os.path.exists('game_state.txt'):
        with open('game_state.txt', 'r') as f:
            game_state = json.load(f)
            level_bar.level = game_state['level']
            coins_bar.coins = game_state['coins']
            todo_lists = game_state['todo_lists']
            todo1 = game_state['todo1']
            todo2 = game_state['todo2']
            todo3 = game_state['todo3']

        todo1_text.update_text(todo1)
        todo2_text.update_text(todo2)
        todo3_text.update_text(todo3)
    else:
        # Initialize game state to default values
        level_bar.level = 1
        coins_bar.coins = 0
        todo_lists = [""]
        todo1 = ""
        todo2 = ""
        todo3 = ""

# background
selected_background = 'Design/sunny.png'

#internal function (ambience)
def can_change_ambience(ambience):

    level = level_bar.level  
 
    if ambience in ambience_level_required:
        # Compare the required level with your current level
        required_level = ambience_level_required[ambience]
        if level >= required_level:
            print("You are eligible for", ambience, "ambience.")
            return True
        else:
            print("You need to reach level", required_level, "to access", ambience, "ambience.")
            return False
    else:
        print("Ambience not found in the requirements.")  
        return False
    
#plant growth 
plant_stage = 1
water_count = 0
fertilizer_count = 0
water_required = 2
fertilizer_required = 2
selected_plant_background = 'Design/plant1.png'

def growth_plant():
    global plant_stage, water_count, fertilizer_count, water_required, fertilizer_required, selected_plant_background

    plant_stage += 1
    water_count = 0
    fertilizer_count = 0
    water_required += 2
    fertilizer_required += 2

    #update plant image
    if plant_stage == 2:
        selected_plant_background = 'Design/plant2.png'
    elif plant_stage == 3:
        selected_plant_background = 'Design/plant3.png' 
    elif plant_stage == 4:
        selected_plant_background = 'Design/plant4.png'

#screen functions
def screen_startup():
    run = True

    load_game_state()

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #start button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_for_input(pygame.mouse.get_pos()):
                    screen_home(selected_background)
                    print("Switching to home screen.")

        bg('Design/frontpage.png')
        start.image_button('Design/frontpage-button1.png')
        
        pygame.display.flip()

    pygame.quit()

def screen_home(new_selected_background):
    global selected_background 
    selected_background = new_selected_background
    pomodoro_button = TEXT("pomodoro",675,120,20,black,blue)
    break_button = TEXT("break",790,120,20,black,blue)
    stopwatch_button = TEXT("stopwatch",905,120,20,black,blue)
    start_stop_button = TEXT("START",775,270,30,black)

    run = True
    while run:

        global current_seconds,started,timer,stopwatch,pomodoro,lap_length,current_lap,pomodoro_length,break_length,todo3

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
                    #todo list cannot exceed 3 tasks
                    if len(todo_lists) < 4:
                        screen_user_input()
                #checked/finish our task
                if checklist_1_button.check_for_input(pygame.mouse.get_pos()):
                    if len(todo_lists) == 3+1:
                        finish_task_3(1)
                    elif len(todo_lists) == 2+1:
                        finish_task_2(1)
                    elif len(todo_lists) == 1+1:
                        todo_lists.remove(todo_lists[1])
                        todo1 = ""
                        todo1_text.update_text(todo1)
                        checklist_1_button.update_color(grey)
                if checklist_2_button.check_for_input(pygame.mouse.get_pos()):
                    if len(todo_lists) == 3+1:
                        finish_task_3(2)
                    elif len(todo_lists) == 2+1:
                        finish_task_2(2)
                if checklist_3_button.check_for_input(pygame.mouse.get_pos()):
                    if len(todo_lists) == 3+1:
                        finish_task_3(3)
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
                                    coins_bar.addCoins(30)
                                    coins_text = TEXT("Coins: " + str(coins_bar.coins), 200, 150, 50, black)
                                    coins_text.display_text()

                                    level_bar.addXP(20)
                                    level_bar.draw(screen)
                                    current_seconds = break_length
                                    pomodoro = False
                                    save_game_state()

                                
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
                                    save_game_state()
                                   
                                else:
                                    current_seconds = pomodoro_length
                                    pomodoro = True
                                    started = False
                                    start_stop_button.update_text("START")
                                    print("finish lap")

        bg(selected_background)
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
        add_task_button.image_button('Design/add_task_button.png')
        todo1_text.display_text()
        todo2_text.display_text()
        todo3_text.display_text()
        checklist_1_button.draw_circle()
        checklist_2_button.draw_circle()
        checklist_3_button.draw_circle()
        checklist_1_button.fill_circle(pygame.mouse.get_pos())
        checklist_2_button.fill_circle(pygame.mouse.get_pos())
        checklist_3_button.fill_circle(pygame.mouse.get_pos())


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

        level_text = TEXT("Level " + str(level_bar.level), 200, 50, 50, black)
        level_text.display_text()

        
        #Coins
        coins_image = BUTTON(10, 105)
        coins_image.image_button('Design/coin.png')
        
        coins_text = TEXT("Coins: " + str(coins_bar.coins), 200, 150, 50, black)
        coins_text.display_text()

        pygame.display.flip()

    pygame.quit()

def screen_user_input():
    run = True
    while run:

        global user_input,todo1,todo2,todo3
        user_input_limit = 300
        user_input_length = input_text.check_text_length(user_input)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    screen_home(selected_background)
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
                    if len(todo_lists) >= 3+1:
                        todo1 = todo_lists[1]
                        todo2 = todo_lists[2]
                        todo3 = todo_lists[3]
                        todo1_text.update_text(todo1)
                        todo2_text.update_text(todo2)
                        todo3_text.update_text(todo3)
                        checklist_1_button.update_color(blue)
                        checklist_2_button.update_color(blue)
                        checklist_3_button.update_color(blue)
                    elif len(todo_lists) == 2+1:
                        todo1 = todo_lists[1]
                        todo2 = todo_lists[2]
                        todo1_text.update_text(todo1)
                        todo2_text.update_text(todo2)
                        checklist_1_button.update_color(blue)
                        checklist_2_button.update_color(blue)
                    else: 
                        todo1 = todo_lists[1]
                        todo1_text.update_text(todo1)
                        checklist_1_button.update_color(blue)
                    save_game_state()
                    user_input = ""
                    input_text.update_text(user_input)
                    screen_home(selected_background)
        
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
    minute_text1 = TEXT("minute",313,370,15,grey,grey,"DePixelHalbfett.ttf")
    minute_text2 = TEXT("minute",313,530,15,grey,grey,"DePixelHalbfett.ttf")
    increase_pomodoro = BUTTON(245, 325, 40, 20)
    decrease_pomodoro = BUTTON(245, 350, 40, 20)
    increase_break = BUTTON(245, 487, 40, 20)
    decrease_break = BUTTON(245, 510, 40, 20)

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
                #ambience buttons
                if sunny_bg.check_for_input(pygame.mouse.get_pos()):
                     
                    res = can_change_ambience('sunny')

                    if res == True:
                        new_selected_background = 'Design/sunny.png'
                        screen_home(new_selected_background)
                        print("Switching to homescreen")
                            
                if night_bg.check_for_input(pygame.mouse.get_pos()):
                    res = can_change_ambience('night')

                    if res == True:
                        new_selected_background = 'Design/night.png'
                        screen_home(new_selected_background)
                        print("Switching to homescreen")

                if snow_bg.check_for_input(pygame.mouse.get_pos()):
                    res = can_change_ambience('snow')

                    if res == True:
                        new_selected_background = 'Design/snow.png'
                        screen_home(new_selected_background)
                        print("Switching to homescreen")

                if music_1.check_for_input(pygame.mouse.get_pos()):
                    play_music('Songs/music_1.MP3')
                if music_2.check_for_input(pygame.mouse.get_pos()):
                    play_music('Songs/music_2.MP3')
                if music_3.check_for_input(pygame.mouse.get_pos()):
                    play_music('Songs/music_3.MP3')

                #back button
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = pomodoro_length
                    screen_home(selected_background)
                    print("Returning to homescreen")

        
        bg('Design/setting page.png')
        back.image_button('Design/back-button.png')
        minute_text1.display_text()
        minute_text2.display_text()
        convert_time(pomodoro_length,180,330,60)
        convert_time(break_length,180,495,60)

        if can_change_ambience('sunny'):
            sunny_bg.image_button('Design/nothing.png')
            # true, unlocked
        else: 
            sunny_bg.image_button('Design/lock.png')
             # false, locked

        if can_change_ambience('night'):
            night_bg.image_button('Design/nothing.png')
            # true, unlocked
        else: 
            night_bg.image_button('Design/lock.png')
             # false, locked
        
        if can_change_ambience('snow'):
            snow_bg.image_button('Design/nothing.png')
            # true, unlocked
        else: 
            snow_bg.image_button('Design/lock.png')
             # false, locked

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
                    screen_home(selected_background)
                    print("Returning to homescreen")
                #shop button
                if shop_button.check_for_input(pygame.mouse.get_pos()):
                    screen_shop()
                    print("Switching to shop screen.")

        bg(selected_plant_background)
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
                    screen_home(selected_background)
                    print("Returning to homescreen")

        bg('Design/garden.png')
        back.image_button('Design/back-button.png')

        pygame.display.flip()

    pygame.quit()

def screen_shop():
    global water_count, fertilizer_count, water_required, fertilizer_required
    run = True
    water_plant = BUTTON(120, 400, 120, 50)
    fertilizer = BUTTON(120, 570, 120, 50)
    watering_can = POPUP('Design/watering-can.png',800)
    fertilize = POPUP('Design/fertilizer.png',800)
    
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_back.check_for_input(pygame.mouse.get_pos()):
                    screen_plant()
                    print("Returning to plant screen")
                if water_plant.check_for_input(pygame.mouse.get_pos()):
                    water_count += 1
                    watering_can.trigger() # Record the start time
                if fertilizer.check_for_input(pygame.mouse.get_pos()):
                    fertilizer_count += 1
                    fertilize.trigger()  # Record the start time
                
                #check if plant should grow
                if water_count >= water_required and fertilizer_count >= fertilizer_required:
                    growth_plant()

        bg(selected_plant_background)
        bg('Design/shop-page.png')
        # Check if we need to show the watering can image
        watering_can.show()
        fertilize.show()


        pygame.display.flip()

    pygame.quit()


screen_startup() 