import pygame
import json
from datetime import date, timedelta
import os
from classes_functions import *
from pygame.locals import *

pygame.init()
pygame.mixer.init()

screen_size = (1540,800)
screen_width = screen_size[0]
screen_height = screen_size[1]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('TaskTree')

clock = pygame.time.Clock()
clock.tick(60)  # Limit frame rate to 60 FPS

CLEAR_NOTIFICATION_EVENT = pygame.USEREVENT + 1

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
seed = BUTTON(0, 0)
seed_button = BUTTON(90, 390, 70, 70)
quit = BUTTON(1067, 190, 50, 50)

shop = BUTTON(0, 0)
shop_button = BUTTON(60, 290, 100, 80)
shop_back = BUTTON(345, 300, 100,80)
transfer_to_garden = BUTTON (150, 300)
transfer_to_garden_button = BUTTON(990,599, 80, 80)

#music
music_1 = BUTTON(670, 450, 60, 60)
music_2 = BUTTON(770, 450, 60, 60)
music_3 = BUTTON(870, 450, 60, 60)

play_music('Songs/music_1.MP3')

#sounds
mute = BUTTON(680, 360, 60, 60)
unmute = BUTTON(830, 360, 60, 60)

#streak
streak_count = 0
last_completed_date = date.today().isoformat()

streak_text = TEXT("Streaks: " + str(streak_count), 200, 250, 50, black)

#plant growth 
plant_stage = 1
water_count = 0
fertilizer_count = 0
water_required = 2
fertilizer_required = 2
selected_plant_background = 'Design/plant1.png'

#garden
flower_x = []
flower_y = []
flower_width = []
flower_height = []
selected_flower_img = ''
fully_grown_flower = []
locked_flowers_img = []
locked_flowers_rect = []

#store the seed
chosen_seed = 0
seed_chosen = False

#user input for todo list
user_input = ""
input_text = TEXT(user_input, 780,350,20, grey, grey,"DePixelHalbfett.ttf")
add_task_button = BUTTON(screen_width-120, screen_height-80, 112, 50, black)
add_task_text = TEXT("Todo list :", 1250, 525, 20, dark_grey, dark_grey,"DePixelHalbfett.ttf")

input_your_text = TEXT("Enter your task for today !", 800, 200, 30, blue, blue,"DePixelHalbfett.ttf")

uparrow = BUTTON(screen_width-500, screen_height-70, 16, 16, black)
downarrow = BUTTON(screen_width-480, screen_height-70, 16, 16, black)

# Create a list of tasks
tasks = ["Task {}".format(i + 1) for i in range(21)]

# Initialize taskboard visibility
taskboard_visible = True

# Create toggle button
toggle_button = BUTTON(screen_width-70, screen_height-350, 50, 50, black)


#save & load data
def save_game_state():
    game_state = {
        'level': level_bar.level,
        'level_xp': level_bar.xp,
        'coins': coins_bar.coins,
        'tasks': tasks,
        'plant_stage': plant_stage,
        'water_count': water_count,
        'fertilizer_count': fertilizer_count,
        'streak_count': streak_count,
        'last_completed_date': last_completed_date,
        'seed_chosen': seed_chosen,
        'chosen_seed': chosen_seed,
        'locked_flowers_img': locked_flowers_img,
        'flower_x' : flower_x,
        'flower_y' : flower_y,
        'flower_width': flower_width,
        'flower_height': flower_height
    }
    with open('game_state.json', 'w') as f:
        json.dump(game_state, f)

def load_game_state():
    global level_bar, coins_bar, plant_stage, water_count, fertilizer_count, tasks, streak_count, last_completed_date, seed_chosen, chosen_seed, locked_flowers_img,flower_x, flower_y, flower_width, flower_height
    if os.path.exists('game_state.json'):
        with open('game_state.json', 'r') as f:
            game_state = json.load(f)
            level_bar.level = game_state.get('level', 0)
            level_bar.xp = game_state.get('level_xp', 0)
            coins_bar.coins = game_state.get('coins', 0)
            tasks = game_state.get('tasks', [])
            plant_stage = game_state.get('plant_stage', 1)
            water_count = game_state.get('water_count', 0)
            fertilizer_count = game_state.get('fertilizer_count', 0)
            streak_count = game_state.get('streak_count', 0)
            last_completed_date = game_state.get('last_completed_date', date.today().isoformat())
            seed_chosen = game_state.get('seed_chosen', False)
            chosen_seed = game_state.get('chosen_seed', 0)
            locked_flowers_img = game_state.get('locked_flowers_img', [])
            flower_x = game_state.get('flower_x', [])
            flower_y = game_state.get('flower_y', [])
            flower_width = game_state.get('flower_width', [])
            flower_height = game_state.get('flower_height', [])
    else:
        #set game state to default values
        level_bar.level = 0
        level_bar.xp = 0
        coins_bar.coins = 0
        tasks = []
        plant_stage = 1
        water_count = 0
        fertilizer_count = 0
        streak_count = 0
        last_completed_date = date.today().isoformat()
        seed_chosen = False
        chosen_seed = 0
        locked_flowers_img = []
        flower_x = []
        flower_y = []
        flower_width = []
        flower_height = []

#update streak count
def update_streak_count():
    global streak_count, last_completed_date
    
    today = date.today()
    last_completed_date = date.fromisoformat(last_completed_date)

    if (today - last_completed_date) == timedelta(days=1):
        streak_count += 1
    else:
        streak_count = 0

    last_completed_date = today.isoformat()
    save_game_state()


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

#internal function (coins)
def spend_coins(cost):
    if coins_bar.coins >= cost:
        coins_bar.coins -= cost
        print("You have spent", cost, "coins.")
        return True
    else:
        print("You do not have enough coins to spend.")
        return False
    


def growth_plant():
    global plant_stage, water_count, fertilizer_count, water_required, fertilizer_required, selected_plant_background

    plant_stage += 1
    water_count = 0
    fertilizer_count = 0
    water_required += 2
    fertilizer_required += 2

def saving_rect(rect):
    global flower_x, flower_y, flower_width, flower_height
    flower_x.append(rect.x)
    flower_y.append(rect.y)
    flower_width.append(rect.width)
    flower_height.append(rect.height)

def delete_rect():
    global flower_x, flower_y, flower_width, flower_height
    flower_x.pop()
    flower_y.pop()
    flower_width.pop()
    flower_height.pop()

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
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    #preload the flower rect
                    for i in range(len(flower_x)):
                        rect = pygame.Rect(flower_x[i], flower_y[i], flower_width[i], flower_height[i])
                        locked_flowers_rect.append(rect)
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

    # Create a font
    font = pygame.freetype.Font(None, 24)

    # Create a variable to store the current page
    current_page = 0

    # Create a taskboard
    taskboard = pygame.Rect(1000, 500, 500, 250)

    maximum_task_per_page = 5

    comment1 = Comment(260, 380)
    comment1.update_color((255, 219, 108))
    comment2 = Comment(290, 410)
    comment2.update_color((255, 219, 88))

    run = True
    while run:

        global current_seconds,started,timer,stopwatch,pomodoro,lap_length,current_lap,pomodoro_length,break_length,taskboard_visible
        
        if seed_chosen:
            plant_button.enable()
        else:
            plant_button.disable()
            comment1.show_for_duration('<<<  Please choose', screen)
            comment2.show_for_duration('your seed first!', screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #pomodoro setup
            if event.type == pygame.MOUSEBUTTONDOWN:
                #check if start/stop button is clicked, toggle the pomodoro
                if start_stop_button.is_clicked(pygame.mouse.get_pos()): 
                    if started:
                        started = False
                        start_stop_button.update_text("START")
                    else:
                        started = True
                        start_stop_button.update_text("STOP")
                #display pomodoro, stop the break/stopwatch
                if pomodoro_button.is_clicked(pygame.mouse.get_pos()):
                    if started == False:
                        started = False
                        current_seconds = pomodoro_length
                        start_stop_button.update_text("START")
                        stopwatch = False
                        pomodoro = True
                    else:
                        current_seconds = current_seconds
                #display break time, stop the pomodoro/stopwatch
                if break_button.is_clicked(pygame.mouse.get_pos()):
                    if started == False:
                        started = False
                        current_seconds = break_length
                        start_stop_button.update_text("START")
                        stopwatch = False
                        pomodoro = False
                    else:
                        current_seconds = current_seconds
                #display stopwatch, stop the pomodoro
                if stopwatch_button.is_clicked(pygame.mouse.get_pos()):
                    if started == False:
                        started = False
                        current_seconds = timer
                        start_stop_button.update_text("START")
                        stopwatch = True
                        pomodoro = False
                    else:
                        current_seconds = current_seconds
                #add to do list button
                if add_task_button.is_clicked(pygame.mouse.get_pos()):
                    screen_user_input()
                #settings button
                if settings_button.is_clicked(pygame.mouse.get_pos()):
                    screen_settings()
                    print("Switching to settings screen.")
                #plant button
                if plant_button.is_clicked(pygame.mouse.get_pos()):
                    if not plant_button.disabled:
                        screen_plant()
                        print("Switching to plant screen.")
                #garden button
                if garden_button.is_clicked(pygame.mouse.get_pos()):
                    screen_garden()
                    print("Switching to garden screen.")
                #seed button
                if seed_button.is_clicked(pygame.mouse.get_pos()):
                    screen_seed()
                    print("Switching to seed screen.")

                if uparrow.is_clicked(pygame.mouse.get_pos()):
                    print("Up")
                    current_page = max(0, current_page - 1)

                if downarrow.is_clicked(pygame.mouse.get_pos()):
                    print("Down")
                    if current_page * maximum_task_per_page < len(tasks) - maximum_task_per_page: 
                        current_page += 1

                if toggle_button.is_clicked(pygame.mouse.get_pos()):
                    taskboard_visible = not taskboard_visible


                mouse_pos = pygame.mouse.get_pos()

                # Check if the mouse click position is within a task
                for i in range(maximum_task_per_page):
                    task_index = current_page * maximum_task_per_page + i
                    if task_index < len(tasks):
                        task_rect = pygame.Rect(taskboard.x + 10, taskboard.y + 50 + i * 30, taskboard.width - 20, 30)
                        if task_rect.collidepoint(mouse_pos):
                            # Click to remove task
                            tasks.pop(task_index)
                            save_game_state()
                            break

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
                                    coins_bar.addCoins(30)
                                    coins_text = TEXT("Coins: " + str(coins_bar.coins), 200, 150, 50, black)
                                    coins_text.display_text()
                                    
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
            
            #mute/unmute alternative
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:

                    pygame.mixer.music.pause()
                if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()

                if event.key == pygame.K_UP:
                    # Go to the previous page when the up arrow key is pressed
                    current_page = max(0, current_page - 1)

                if event.key == pygame.K_DOWN:
                    # Go to the next page when the down arrow key is pressed
                    if current_page * maximum_task_per_page < len(tasks) - maximum_task_per_page:  # Check if there is at least one more task to display
                        current_page += 1

                if event.key == pygame.K_y:
                    taskboard_visible = not taskboard_visible


        bg(selected_background)
        settings.image_button('Design/setting-button1.png')
        plant.image_button('Design/plant-button.png')
        garden.image_button('Design/garden-button.png')
        seed.image_button('Design/seed-button.png')
        comment1.show(screen)
        comment2.show(screen)
        pomodoro_button.hover_color_change()
        break_button.hover_color_change()
        stopwatch_button.hover_color_change()
        start_stop_button.display_text()
        toggle_button.image_button('Design/add_task_button.png')


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

        #streak
        streak_image = BUTTON(0, 0)
        streak_image.image_button('Design/streak.png')
        streak_text = TEXT("Streaks: " + str(streak_count), 270, 730, 50, black)
        streak_text.display_text()

        # Task bar
        if taskboard_visible:
            # Draw the taskboard
            pygame.draw.rect(screen, grey, taskboard)

            # draw the tasks for the current page
            for i in range(maximum_task_per_page):
                task_index = current_page * maximum_task_per_page + i
                if task_index < len(tasks):
                    task = tasks[task_index]
                    # circle
                    circle_pos = (taskboard.x + 15, taskboard.y + 70 + i * 30)
                    text_pos = (taskboard.x + 30, taskboard.y + 65 + i * 30)
                    text_rect = font.get_rect(task)
                    text_size = text_rect.size
                    # rect covers the circle and text
                    task_rect = pygame.Rect(circle_pos[0] - 5, circle_pos[1] - 5, 20 + text_size[0], text_size[1])
                    if task_rect.collidepoint(pygame.mouse.get_pos()):
                        #filled circle
                        pygame.draw.circle(screen, (0, 0, 0), circle_pos, 5)
                    else:
                        #hollow circle
                        pygame.draw.circle(screen, (0, 0, 0), circle_pos, 5, 1)
                    font.render_to(screen, text_pos, task, (0, 0, 0))

            # Add task button
            add_task_text.display_text()
            add_task_button.image_button('Design/task_button.png')

            #Task Up & Down Button
            uparrow.image_button('Design/up.png')
            downarrow.image_button('Design/down.png')

        update_streak_count()    
        pygame.display.flip()

    pygame.quit()

def screen_user_input():
    run = True
    while run:

        global user_input, tasks
        user_input_limit = 300
        user_input_length = input_text.check_text_length(user_input)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(pygame.mouse.get_pos()):
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
                    tasks.append(user_input)
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
    notification = TEXT("", 1320, 450, 30, blue)

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

    while run:

        global pomodoro_length,break_length,lap_length,current_seconds


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                #pomodoro settings
                if increase_pomodoro.is_clicked(pygame.mouse.get_pos()):
                    if pomodoro_length == 3600:
                        pomodoro_length = pomodoro_length
                    else:
                        pomodoro_length = pomodoro_length + 300
                        print(pomodoro_length)
                if decrease_pomodoro.is_clicked(pygame.mouse.get_pos()):
                    if pomodoro_length > 300:
                        pomodoro_length = pomodoro_length - 300
                        print(pomodoro_length)
                    else:
                        pomodoro_length = pomodoro_length
                #break settings
                if increase_break.is_clicked(pygame.mouse.get_pos()):
                    if break_length == 3310:
                        break_length = break_length
                    else:
                        break_length = break_length + 300
                        print(break_length)
                if decrease_break.is_clicked(pygame.mouse.get_pos()):
                    if break_length > 300:
                        break_length = break_length - 300
                        print(break_length)
                    else:
                        break_length = break_length
                #ambience buttons
                if sunny_bg.is_clicked(pygame.mouse.get_pos()):
                     
                    res = can_change_ambience('sunny')

                    if res == True:
                        new_selected_background = 'Design/sunny.png'
                        screen_home(new_selected_background)
                        print("Switching to homescreen")

                    else:
                        print("Not enough level")
                        notification.update_text("Level up some more :(")
                        
                        pygame.time.set_timer(CLEAR_NOTIFICATION_EVENT, 3000)  # 3000 milliseconds = 3 seconds
                            
                if night_bg.is_clicked(pygame.mouse.get_pos()):
                    res = can_change_ambience('night')

                    if res == True:
                        new_selected_background = 'Design/night.png'
                        screen_home(new_selected_background)
                        print("Switching to homescreen")

                    else:
                        print("Not enough level")
                        notification.update_text("Level up some more :(")
                        
                        pygame.time.set_timer(CLEAR_NOTIFICATION_EVENT, 3000)  # 3000 milliseconds = 3 seconds

                if snow_bg.is_clicked(pygame.mouse.get_pos()):
                    res = can_change_ambience('snow')

                    if res == True:
                        new_selected_background = 'Design/snow.png'
                        screen_home(new_selected_background)
                        print("Switching to homescreen")

                    else:
                        print("Not enough level")
                        notification.update_text("Level up some more :(")
                        
                        pygame.time.set_timer(CLEAR_NOTIFICATION_EVENT, 3000)  # 3000 milliseconds = 3 seconds

                if music_1.is_clicked(pygame.mouse.get_pos()):
                    play_music('Songs/music_1.MP3')
                if music_2.is_clicked(pygame.mouse.get_pos()):
                    play_music('Songs/music_2.MP3')
                if music_3.is_clicked(pygame.mouse.get_pos()):
                    play_music('Songs/music_3.MP3')

                if mute.is_clicked(pygame.mouse.get_pos()):
                    print("Mute")
                    pygame.mixer.music.pause()

                if unmute.is_clicked(pygame.mouse.get_pos()):
                    print("Unmute")
                    pygame.mixer.music.unpause()

                #back button
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    current_seconds = pomodoro_length
                    screen_home(selected_background)
                    print("Returning to homescreen")
            if event.type == CLEAR_NOTIFICATION_EVENT:
                notification.update_text("")
        
        bg('Design/setting page.png')
        back.image_button('Design/back-button.png')
        minute_text1.display_text()
        minute_text2.display_text()
        convert_time(pomodoro_length,180,330,60)
        convert_time(break_length,180,495,60)
        notification.display_text()

        pygame.display.flip()

    pygame.quit()

def screen_plant() :
    global plant_stage, chosen_seed, fully_grown_flower, selected_flower_img
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    screen_home(selected_background)
                #shop button
                if shop_button.is_clicked(pygame.mouse.get_pos()):
                    screen_shop()
                    print("Switching to shop screen.")
                if transfer_to_garden_button.is_clicked(pygame.mouse.get_pos()):
                    fully_grown_flower.append(selected_flower_img)
                    save_game_state()
                    screen_garden()

        # Update plant image based on the chosen seed
        if chosen_seed == 1:
            selected_flower_img = 'Design/flower1.png'
            if plant_stage == 1:
                selected_plant_background = 'Design/plant1.png'
            elif plant_stage == 2:
                selected_plant_background = 'Design/plant2.png'
            elif plant_stage == 3:
                selected_plant_background = 'Design/plant3.png'
            elif plant_stage == 4:
                selected_plant_background = 'Design/plant4.png'
        elif chosen_seed == 2:
            selected_flower_img = 'Design/flower2.png'
            if plant_stage == 1:
                selected_plant_background = 'Design/plant1.png'
            elif plant_stage == 2:
                selected_plant_background = 'Design/plant2.png'
            elif plant_stage == 3:
                selected_plant_background = 'Design/plant5.png'
            elif plant_stage == 4:
                selected_plant_background = 'Design/plant6.png'
        elif chosen_seed == 3:
            selected_flower_img = 'Design/flower3.png'
            if plant_stage == 1:
                selected_plant_background = 'Design/plant1.png'
            elif plant_stage == 2:
                selected_plant_background = 'Design/plant2.png'
            elif plant_stage == 3:
                selected_plant_background = 'Design/plant7.png'
            elif plant_stage == 4:
                selected_plant_background = 'Design/plant8.png'


        bg(selected_plant_background)
        back.image_button('Design/back-button.png')
        shop.image_button('Design/shop-button.png')

        #Coins text
        coins_image = BUTTON(10, 105)
        coins_image.image_button('Design/coin.png')
        
        coins_text = TEXT("Coins: " + str(coins_bar.coins), 200, 150, 50, black)
        coins_text.display_text()

        if plant_stage == 4:
            transfer_to_garden.image_button('Design/next_arrow.png')

        pygame.display.flip()

    pygame.quit()

def screen_garden() :
    global flower_x, flower_y, flower_width, flower_height, fully_grown_flower, locked_flowers_img, locked_flowers_rect, seed_chosen
    run = True
    zoom_level = 1.0
    dragging = False
    movable_flowers = []
    finish_placement_button = BUTTON(screen_width-100, screen_height-80, 50, 50, dark_grey)
    selected_flower = ''

    #receive flower image from fully_grown_flower, store flower's rect into movable flowers (used for further codings)
    for flower in fully_grown_flower:
        flower_img = pygame.image.load(fully_grown_flower[0])
        flower_rect = flower_img.get_rect()
        movable_flowers.append(flower_rect)

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Cannot zoom in out if we're still placing a flower
                if len(movable_flowers) != 0:
                    zoom_level = zoom_level
                # Zoom in out will be triggered
                else:
                    if event.button == 4:  # Mouse wheel up
                        zoom_level += 0.1
                        if zoom_level > 2.6:
                            zoom_level = 2.6
                    if event.button == 5:  # Mouse wheel down
                        zoom_level -= 0.1
                        if zoom_level < 1.0:  # Prevent zooming out too much
                            zoom_level = 1.0
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    screen_home(selected_background)
                # Repeat for each flower in movable flowers
                for flower in movable_flowers:
                    # Check whether any flower is clicked
                    if flower.collidepoint(event.pos):
                        dragging = True
                        selected_flower = flower
                        print(f"Selected flower = {selected_flower}")
                    # Check if the player has finish the flower placement
                    if finish_placement_button.is_clicked(pygame.mouse.get_pos()):
                        finish_placement_button.update_color(blue)
                        locked_flowers_rect.append(selected_flower)
                        locked_flowers_img.append(fully_grown_flower[0]) #move the selected flower into locked_flowers; the flower now can't be move
                        saving_rect(selected_flower)
                        new_pos = pygame.Rect(flower_x[-1], flower_y[-1], flower_width[-1], flower_height[-1])
                        locked_flowers_rect.append(new_pos)
                        movable_flowers.remove(selected_flower)
                        fully_grown_flower.pop()
                        print(f"Selected flower has been locked at {locked_flowers_rect[-1]}")
                        seed_chosen = False
                        save_game_state()
                        screen_home(selected_background)

                # Player cannot move it anymore flower from locked_flowers
                for flower in locked_flowers_rect:
                    if flower.collidepoint(event.pos):
                        dragging = False
                        break
            # Stop the flower movement if mousebuttonup
            elif event.type == pygame.MOUSEBUTTONUP:
                for flower in movable_flowers:
                    dragging = False
                    print(f"Flower dropped at {movable_flowers}")
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    selected_flower.x = mouse_x - 20
                    selected_flower.y = mouse_y - 18


        screen.fill((85, 174, 78))  # Fill the screen with green color
        bg = pygame.image.load('Design/garden_zoom.png')
        back.image_button('Design/back-button.png')

        main_surface = pygame.Surface((1540, 800))  # Crop/frame and make it center
        main_surface.blit(bg, (0, 0))
        new_width = int(main_surface.get_width() * zoom_level)
        new_height = int(main_surface.get_height() * zoom_level)
        zoomed_main_surface = pygame.transform.smoothscale(main_surface, (new_width, new_height))

        # Center the main surface on the screen
        screen_rect = screen.get_rect()
        zoomed_main_surface_rect = zoomed_main_surface.get_rect(center=screen_rect.center)

        # Blit the scaled main surface to the screen
        screen.blit(zoomed_main_surface, zoomed_main_surface_rect.topleft)

        back.image_button('Design/back-button.png')

        # If flower hasn't been locked, the lock button will display
        if movable_flowers != []:
            finish_placement_button.image_button('Design/locked.png')

        # Blit the flowers that have been locked to their permanent position
        for i, flower in enumerate(locked_flowers_img):
            flower_img = pygame.image.load(locked_flowers_img[i])
            scaled_width = int(flower_width[i] * zoom_level)
            scaled_height = int(flower_height[i] * zoom_level)
            scaled_flower_img = pygame.transform.smoothscale(flower_img, (scaled_width, scaled_height))
            scaled_x = int((flower_x[i] * zoom_level) + zoomed_main_surface_rect.x)
            scaled_y = int((flower_y[i] * zoom_level) + zoomed_main_surface_rect.y)
            scaled_flower_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
            screen.blit(scaled_flower_img, scaled_flower_rect.topleft)

        # Blit the flowers (these flowers can be moved)
        for i, flower in enumerate(movable_flowers):
            flower_img = pygame.image.load(fully_grown_flower[0])
            screen.blit(flower_img, flower)

        # Update the display
        pygame.display.flip()

    pygame.quit()

def screen_seed() :
    run = True
    global chosen_seed, seed_chosen
    seed1 = BUTTON(600, 430, 90, 100)
    seed2 = BUTTON(800, 430, 90, 100)
    seed3 = BUTTON(1000, 430, 90, 100)
    
    while run :

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if seed1.is_clicked(pygame.mouse.get_pos()):
                    chosen_seed = 1
                    seed_chosen = True
                    save_game_state()
                    screen_plant()
                    print("Seed 1 chosen. Switching to plant screen.")
                elif seed2.is_clicked(pygame.mouse.get_pos()):
                    chosen_seed = 2
                    seed_chosen = True
                    save_game_state()
                    screen_plant()
                    print("Seed 2 chosen. Switching to plant screen.")               
                elif seed3.is_clicked(pygame.mouse.get_pos()):
                    chosen_seed = 3
                    seed_chosen = True
                    save_game_state()
                    screen_plant()
                    print("Seed 3 chosen. Switching to plant screen.")
                if quit.is_clicked(pygame.mouse.get_pos()):
                    screen_home(selected_background)
                    print("Returning to homescreen")


        bg('Design/seed-page.png')

        pygame.display.flip()

    pygame.quit()

def screen_shop():
    global water_count, fertilizer_count, water_required, fertilizer_required
    run = True
    water_plant = BUTTON(120, 400, 120, 50)
    fertilizer = BUTTON(120, 570, 120, 50)
    watering_can = POPUP('Design/watering-can.png',800)
    fertilize = POPUP('Design/fertilizer.png',800)
    textcoins = TEXT("5", 140, 400, 30, black)
    textsoil = TEXT("10", 140, 565, 30, black)

    #comment
    comment = Comment(screen_width / 2, 100)
    notification = Comment(screen_width / 2, 100)
    notification.update_color(black)
    notification.update_font_size(35)
    
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_back.is_clicked(pygame.mouse.get_pos()):
                    screen_plant()
                    print("Returning to plant screen")
                if water_plant.is_clicked(pygame.mouse.get_pos()):
                    if water_count < water_required:
                        #spend coins(30) to proceed with the action
                        if spend_coins(5):
                            water_count += 1
                            watering_can.trigger()
                            coins_text = TEXT("Coins: " + str(coins_bar.coins), 200, 150, 50, black)
                            coins_text.display_text()
                            save_game_state()
                        else:
                            notification.show_for_duration('Not Enough Coins !', screen)

                    else:
                        comment.show_for_duration('Your soil is already moist!  No need to water right now.', screen)

                if fertilizer.is_clicked(pygame.mouse.get_pos()):
                    if fertilizer_count < fertilizer_required:
                        #spend coins(30) to proceed with the action
                        if spend_coins(10):
                            fertilizer_count += 1
                            fertilize.trigger()
                            coins_text = TEXT("Coins: " + str(coins_bar.coins), 200, 150, 50, black)
                            coins_text.display_text()
                            save_game_state()

                        else:
                            notification.show_for_duration('Not Enough Coins !', screen)

                    else:
                        comment.show_for_duration('Your plant looks vibrant and healthy!  No need for more fertilizer now.', screen)
                                        
                #check if plant should grow
                if water_count >= water_required and fertilizer_count >= fertilizer_required:
                    growth_plant()

        # Update plant image based on the chosen seed
        if chosen_seed == 1:
            if plant_stage == 1:
                selected_plant_background = 'Design/plant1.png'
            elif plant_stage == 2:
                selected_plant_background = 'Design/plant2.png'
            elif plant_stage == 3:
                selected_plant_background = 'Design/plant3.png'
            elif plant_stage == 4:
                selected_plant_background = 'Design/plant4.png'
        elif chosen_seed == 2:
            if plant_stage == 1:
                selected_plant_background = 'Design/plant1.png'
            elif plant_stage == 2:
                selected_plant_background = 'Design/plant2.png'
            elif plant_stage == 3:
                selected_plant_background = 'Design/plant5.png'
            elif plant_stage == 4:
                selected_plant_background = 'Design/plant6.png'
        elif chosen_seed == 3:
            if plant_stage == 1:
                selected_plant_background = 'Design/plant1.png'
            elif plant_stage == 2:
                selected_plant_background = 'Design/plant2.png'
            elif plant_stage == 3:
                selected_plant_background = 'Design/plant7.png'
            elif plant_stage == 4:
                selected_plant_background = 'Design/plant8.png'
        
        
        bg(selected_plant_background)
        bg('Design/shop-page.png')
        # Check if we need to show the watering can image
        watering_can.show()
        fertilize.show()
        #display comment
        comment.show(screen)
        notification.show(screen)
        textsoil.display_text()
        textcoins.display_text()    
        
        pygame.display.flip()

    pygame.quit()

screen_startup() 