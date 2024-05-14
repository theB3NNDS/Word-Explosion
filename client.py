import socket
import pygame
import threading

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Explosion")
timer = pygame.time.Clock()
fps = 60

# Game variables
active_string = ''
running = True
letters = [chr(i) for i in range(97, 123)]
submit = ''
bigram = ''
message = ''
my_turn = False
play_again = False
game_result = None  # Variable to store the game result

# Load in assets here
title_font = pygame.font.Font('assets/BebasNeue-Regular.ttf', 50)
bigram_font = pygame.font.Font('assets/BebasNeue-Regular.ttf', 100)
typing_font = pygame.font.Font('assets/VT323-Regular.ttf', 50)
system_font = pygame.font.Font('assets/Teko-VariableFont_wght.ttf', 30)

# Network configuration
HOST = '192.168.100.102'
PORT = 5555

# Function to handle receiving messages from the server
def receive_messages(sock):
    global bigram, message, my_turn, running, play_again, game_result

    while running:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break

            if data.startswith("BIGRAM"):
                bigram = data.split()[1]
            elif data.startswith("VALID"):
                message = f'Valid word: {data.split()[1]}'
            elif data.startswith("INVALID"):
                message = f'INVALID WORD!'
            elif data == "TURN":
                my_turn = True
                message = 'Your turn!'
            elif data == "WAIT":
                message = 'Wait for your turn...'
            elif data == "WIN":
                game_result = "You Win!"
            elif data == "LOSE":
                game_result = "You Lose!"
            elif data == "PLAY_AGAIN?":
                play_again = True
        except Exception as e:
            print(f"Error: {e}")
            break

# Connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

def draw_screen():
    screen.fill((209, 204, 197))
    pygame.draw.rect(screen, (48, 55, 69), [0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100])
    screen.blit(title_font.render(f'WORD EXPLOSION', True, 'black'), (270, 10))
    screen.blit(typing_font.render(f'"{active_string}"', True, 'white'), (270, SCREEN_HEIGHT -75))
    screen.blit(bigram_font.render(f'{bigram}', True, 'black'), (350, 100))
    screen.blit(system_font.render(message, True, 'black'), (350, 200))
    if game_result:
        screen.blit(system_font.render(game_result, True, 'black'), (350, 300))

def main():
    global active_string, submit, message, my_turn, running, play_again, game_result

    while running:
        timer.tick(fps)
        draw_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if my_turn:
                    if event.unicode.lower() in letters:
                        active_string += event.unicode.lower()
                    if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                        active_string = active_string[:-1]
                    if event.key == pygame.K_RETURN:
                        submit = active_string
                        sock.sendall(f"SUBMIT {submit}".encode())
                        active_string = ''
                        my_turn = False
                        message = 'Waiting for response...'
                if play_again:
                    if event.key == pygame.K_y:
                        sock.sendall("PLAY_AGAIN".encode())
                        play_again = False
                        message = 'Waiting for the other player...'
                    elif event.key == pygame.K_n:
                        running = False

        pygame.display.flip()
    pygame.quit()
    sock.close()

main()
