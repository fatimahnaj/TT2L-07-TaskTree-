import pygame
pygame.init()

screen_size = (1540,800)
screen_width = screen_size[0]
screen_height = screen_size[1]
screen = pygame.display.set_mode(screen_size)

black = (0,0,0)

class TEXT:
    def __init__(self,text,x,y,size,normal_color,hover_color=None,font="I-pixel-u.ttf"):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.font = font

    def display_text(self):
        font = pygame.font.Font(self.font,self.size)
        self.rect = font.render(f"{self.text}", True, self.normal_color)
        self.rect_text = self.rect.get_rect(center=(self.x,self.y))
        screen.blit(self.rect, self.rect_text)

    def hover_color_change(self):
        font = pygame.font.Font(self.font,self.size)
        self.rect = font.render(f"{self.text}", True, self.normal_color)
        self.rect_text = self.rect.get_rect(center=(self.x,self.y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect_text.collidepoint(mouse_x, mouse_y):
            self.rect = font.render(f"{self.text}", True, self.hover_color)
        screen.blit(self.rect, self.rect_text)

    def update_text(self, new_text):
        self.text = new_text

    def is_clicked(self,position):
        self.rect = self.rect.get_rect(center=(self.x,self.y))
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def check_text_length(self,input):
        font = pygame.font.Font("I-pixel-u.ttf",self.size)
        self.rect = font.render(f"{self.text}", True, self.normal_color)
        text_width, text_height = font.size(input)
        return text_width
    
class BUTTON:
    def __init__(self, x, y, width=0, height=0, color=black, circle_width=3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.center_x = self.x - self.width // 2
        self.center_y = self.y - self.height // 2
        self.circle_width = circle_width
        self.disabled = False

    def draw_button(self):
        if not self.disabled:
            set_button = pygame.Rect(self.x,self.y, self.width, self.height)
            pygame.draw.rect(screen, self.color, set_button)
        else:
            disabled_button = pygame.Rect(self.x,self.y, self.width, self.height)
            pygame.draw.rect(screen, (200, 200, 200), disabled_button)

    def draw_hoverbutton(self,position,hover_color):
        set_button = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, set_button)
        if position[0] in range(set_button.left, set_button.right) and position[1] in range(set_button.top, set_button.bottom):
            set_button = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, hover_color, set_button)

    def draw_circle(self):
        circle_center = (self.x,self.y)
        pygame.draw.circle(screen, self.color, circle_center, 10, self.circle_width)

    def fill_circle(self,position):
        if not self.disabled:
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if position[0] in range(rect.left, rect.right) and position[1] in range(rect.top, rect.bottom):
                self.circle_width = 0
            else:
                self.circle_width = 3
    
    def image_button(self,image_link):
        if not self.disabled:
            image = pygame.image.load(image_link)
            rect_2 = image.get_rect()
            rect_2.topleft = (self.x, self.y)
            screen.blit(image, (self.center_x,self.center_y))

    def update_color(self, new_color):
        self.color = new_color

    def is_clicked(self,position):
        if not self.disabled:
            rect = pygame.Rect(self.center_x, self.center_y, self.width, self.height)
            if position[0] in range(rect.left, rect.right) and position[1] in range(rect.top, rect.bottom):
                return True
        return False
    
    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False
    
def bg(image_link):
    load_image = pygame.image.load(image_link)
    screen.blit(load_image, (0,0))

def convert_time(time,x,y,size):
    display_minutes = int(time / 60)
    display_time = TEXT(f"{display_minutes:02}",x,y,size,black)
    display_time.display_text()

#Ummu Level Bar
class LevelBar():
    def __init__(self, x, y, w, h, level):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xp = 0
        self.max_xp = 30
        self.level = level
    
    def draw(self, surface):
        #calculate level ratio
        ratio = self.xp / self.max_xp
        pygame.draw.rect(surface, "white", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "orange", (self.x, self.y, self.w * ratio, self.h))

    def addXP(self, increment):
        self.xp += increment
        if self.xp >= self.max_xp:
            excess = self.xp - self.max_xp 
            self.max_xp += 10
            self.level += 1
            self.xp = 0 + excess

    
class Coins():
    def __init__(self, coins):
        self.coins = coins
    
    def addCoins(self, increment):
        self.coins +=increment
        
class POPUP:
    def __init__(self,image,max_duration,pos=(0,0)):
        self.show_popup = False
        self.start_time = 0
        self.max_duration = max_duration  
        self.x = pos[0]
        self.y = pos[1]
        if image == None:
            self.image = ""
        else:
            self.image = image

    #used when the reuirements are met
    def trigger(self):
        self.show_popup = True
        self.start_time = pygame.time.get_ticks()

    def show_img(self):
        if self.show_popup:
                current_time = pygame.time.get_ticks()
                if current_time - self.start_time < self.max_duration:
                    # Load the image
                    image = pygame.image.load(self.image).convert_alpha()
                    # Calculate its position to center it on the screen
                    rect = image.get_rect()
                    screen.blit(image, (self.x,self.y))
                else:
                    self.show_popup = False

    def show_text(self,text,x,y,size,color=black):
            if self.show_popup:
                current_time = pygame.time.get_ticks()
                if current_time - self.start_time < self.max_duration:
                    #load the texts
                    font = pygame.font.Font("DePixelHalbfett.ttf",size)
                    rect = font.render(f"{text}", True, color)
                    rect_text = rect.get_rect(center=(x,y))
                    screen.blit(rect, rect_text)
                else:
                    self.show_popup = False

#anisah sounds
def play_music(music_file):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)

#comment
class Comment:
    def __init__(self, x, y, font_size=20, color=(255, 0, 0), duration=2000, font='DePixelHalbfett.ttf'):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color
        self.duration = duration
        self.font = font
        self.text = ''
        self.last_update_time = 0

    def update_text(self, new_text):
        self.text = new_text

    def update_color(self, new_color):
        self.color = new_color

    def update_font_size(self, new_size):
        self.font_size = new_size

    def display(self, screen):
        if self.text and pygame.time.get_ticks() - self.last_update_time < self.duration:
            text = TEXT(self.text, self.x, self.y, self.font_size, self.color, font=self.font)
            text.display_text()
        else:
            self.text = ''

    def show(self, screen):
        self.display(screen)

    def show_for_duration(self, new_text, screen):
        self.update_text(new_text)
        self.last_update_time = pygame.time.get_ticks()
        self.display(screen)
