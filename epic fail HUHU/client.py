import pygame
import enchant
import random


EN_dictionary = enchant.Dict("en_US")

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Explosion")
timer = pygame.time.Clock()
fps = 60

#game variables
active_string = ''
running = False
letters = [chr(i) for i in range(97, 123)]
submit = ''
bigram = ''
message = ''

#load in assets here
title_font = pygame.font.Font('assets/BebasNeue-Regular.ttf', 50)
bigram_font = pygame.font.Font('assets/BebasNeue-Regular.ttf', 100)
typing_font = pygame.font.Font('assets/VT323-Regular.ttf', 50)
system_font = pygame.font.Font('assets/Teko-VariableFont_wght.ttf', 30)

def generate_bigram():
    bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'nd', 'on', 'en', 'at', 'ou',
               'ed', 'ha', 'to', 'or', 'it', 'is', 'hi', 'es', 'ng', 'the', 'and',
               'ing', 'her', 'hat', 'his', 'tha', 'ere', 'for', 'ent', 'ion', 'ter',
               'was', 'you', 'ith', 'ver', 'all', 'wit', 'thi', 'tio']
    return random.choice(bigrams)
bigram = generate_bigram()

def draw_screen():
    screen.fill((209, 204, 197))
    pygame.draw.rect(screen, (48, 55, 69), [0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100])
    screen.blit(title_font.render(f'WORD EXPLOSION', True, 'black'), (270, 10))
    screen.blit(typing_font.render(f'"{active_string}"', True, 'white'), (270, SCREEN_HEIGHT -75))
    screen.blit(bigram_font.render(f'{bigram}', True, 'black'), (350, 100))
    screen.blit(system_font.render(message, True, 'black'), (350, 200))

def main():
    global active_string, submit, bigram, message, running

    run = True
    while run:
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
                        # Check if the submitted word contains the bigram and is a valid word
                        if bigram in submit and EN_dictionary.check(submit):
                            if submit != bigram:
                                message = f'Valid word: {submit}'
                                bigram = generate_bigram()
                            else:
                                message = f'INVALID WORD!'
                        else:
                            message = f'INVALID WORD!'
                        active_string = ''
            
        pygame.display.flip()
    pygame.quit()

main()