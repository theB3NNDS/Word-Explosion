import pygame
import enchant
EN_dictionary = enchant.Dict("en_US")

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Explosion")
timer = pygame.time.Clock()
fps = 60

#game variables
active_string = 'test string'
running = False
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
           'y', 'z']
submit = ''

#load in assets here
title_font = pygame.font.Font('assets/BebasNeue-Regular.ttf', 50)
typing_font = pygame.font.Font('assets/VT323-Regular.ttf', 50)
system_font = pygame.font.Font('assets/Teko-VariableFont_wght.ttf', 30)

class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)


def draw_screen():
    #screen outlines
    pygame.draw.rect(screen, (40, 60, 82), [0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100])
    screen.blit(typing_font.render(f'"{active_string}"', True, 'white'), (270, SCREEN_HEIGHT -75))


run = True
    
while run:
    screen.fill("gray")
    timer.tick(fps)
    draw_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if not running:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN:
                    submit = active_string
                    active_string = ''
            

    pygame.display.flip()
pygame.quit()

