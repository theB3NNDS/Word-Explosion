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

def draw_screen():
    #screen outlines
    pygame.draw.rect(screen, (40, 60, 82), [0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100])

run = True
    
while run:
    screen.fill("gray")
    timer.tick(fps)
    draw_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()

