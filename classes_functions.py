import pygame
pygame.init()

screen_size = (1540,800)
screen = pygame.display.set_mode(screen_size)

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