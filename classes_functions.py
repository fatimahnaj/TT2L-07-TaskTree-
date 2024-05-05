import pygame
pygame.init()

screen_size = (1540,800)
screen = pygame.display.set_mode(screen_size)

black = (0,0,0)

class TEXT:
    def __init__(self,text,x,y,size,normal_color,hover_color=None):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.normal_color = normal_color
        self.hover_color = hover_color

    def display_text(self):
        font = pygame.font.Font("I-pixel-u.ttf",self.size)
        self.rect = font.render(f"{self.text}", True, self.normal_color)
        self.rect_text = self.rect.get_rect(center=(self.x,self.y))
        screen.blit(self.rect, self.rect_text)

    def hover_color_change(self):
        font = pygame.font.Font("I-pixel-u.ttf",self.size)
        self.rect = font.render(f"{self.text}", True, self.normal_color)
        self.rect_text = self.rect.get_rect(center=(self.x,self.y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect_text.collidepoint(mouse_x, mouse_y):
            self.rect = font.render(f"{self.text}", True, self.hover_color)
        screen.blit(self.rect, self.rect_text)

    def update_text(self, new_text):
        self.text = new_text

    def check_for_input(self,position):
        self.rect = self.rect.get_rect(center=(self.x,self.y))
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

class BUTTON:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.center_x = self.x - self.width // 2
        self.center_y = self.y - self.height // 2

    def draw_button(self):
        set_button = pygame.Rect(self.center_x, self.center_y, self.width, self.height)
        pygame.draw.rect(screen, self.color, set_button)

    def check_for_input(self,position):
        rect = pygame.Rect(self.center_x, self.center_y, self.width, self.height)
        if position[0] in range(rect.left, rect.right) and position[1] in range(rect.top, rect.bottom):
            return True
        return False

        
def bg(image_link):
    load_image = pygame.image.load(image_link)
    screen.blit(load_image, (0,0))

def convert_time(time,x,y,size):
    display_minutes = int(time / 60) % 60
    display_hour = int(time / 3600) % 60
    display_time = TEXT(f"{display_hour}h {display_minutes:02}min",x,y,size,black)
    display_time.display_text()
