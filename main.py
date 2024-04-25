import pygame
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

class TEXT:
    def __init__(self,text,x,y,size,normal_color,hover_color):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.normal_color = normal_color
        self.hover_color = hover_color

    def display_text(self):
        font = pygame.font.Font("I-pixel-u.ttf",self.size)
        set_text = font.render(f"{self.text}", True, self.normal_color)
        rect_text = set_text.get_rect(center=(self.x,self.y))
        screen.blit(set_text, rect_text)

    def hover_color_change(self):
        font = pygame.font.Font("I-pixel-u.ttf",self.size)
        set_text = font.render(f"{self.text}", True, self.normal_color)
        rect_text = set_text.get_rect(center=(self.x,self.y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if rect_text.collidepoint(mouse_x, mouse_y):
            set_text = font.render(f"{self.text}", True, self.hover_color)
        screen.blit(set_text, rect_text)

def button(x, y, width, height, normal_color, hover_color):
    set_button = pygame.Rect(x, y, width, height)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if set_button.collidepoint(mouse_x, mouse_y):
        color = hover_color
    else:
        color = normal_color
    pygame.draw.rect(screen, color, set_button)

def draw_rectangle(x, y, width, height, color):
    center_x = x - width // 2
    center_y = y - height // 2
    set_box = pygame.Rect(center_x, center_y, width, height)
    pygame.draw.rect(screen, color, set_box)

def bg(image_link):
    load_image = pygame.image.load(image_link)
    screen.blit(load_image, (0,0))

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

        screen.fill(grey)
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

        screen.fill(dark_grey)
        pomodoro_text.hover_color_change()
        break_text.hover_color_change()
        timer_text.hover_color_change()
        pomodoro_timer_text.display_text()
        pygame.display.flip()
        
    pygame.quit()

screen_startup()