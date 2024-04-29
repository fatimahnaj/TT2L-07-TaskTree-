import pygame
pygame.init()

screen_size = (1540,800)
screen = pygame.display.set_mode(screen_size)

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

    def button(self,width, height, rect_color):
        set_button = pygame.Rect(self.x, self.y, width, height)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.rect(screen, rect_color, set_button)
        if set_button.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

def draw_rectangle(x, y, width, height, color):
    center_x = x - width // 2
    center_y = y - height // 2
    set_box = pygame.Rect(center_x, center_y, width, height)
    pygame.draw.rect(screen, color, set_box)

def bg(image_link):
    load_image = pygame.image.load(image_link)
    screen.blit(load_image, (0,0))