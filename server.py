import socket
import threading
import random
import enchant

EN_dictionary = enchant.Dict("en_US")

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Generate a bigram
def generate_bigram():
    bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'nd', 'on', 'en', 'at', 'ou',
               'ed', 'ha', 'to', 'or', 'it', 'is', 'hi', 'es', 'ng', 'the', 'and',
               'ing', 'her', 'hat', 'his', 'tha', 'ere', 'for', 'ent', 'ion', 'ter',
               'was', 'you', 'ith', 'ver', 'all', 'wit', 'thi', 'tio']
    return random.choice(bigrams)

# Game state
bigram = generate_bigram()
players = []
current_turn = 0
game_over = False
play_again_votes = 0

# Handle client connection
def handle_client(conn, addr):
    global current_turn, game_over, bigram, play_again_votes

    print(f"Connected by {addr}")
    conn.sendall(f"BIGRAM {bigram}".encode())

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data.startswith("PLAY_AGAIN"):
                play_again_votes += 1
                if play_again_votes == 2:
                    play_again_votes = 0
                    bigram = generate_bigram()
                    game_over = False
                    current_turn = 0
                    for player in players:
                        player.sendall(f"BIGRAM {bigram}".encode())
                    players[current_turn].sendall(f"TURN".encode())
            elif players[current_turn] == conn:
                command, word = data.split(maxsplit=1)
                if command == "SUBMIT":
                    if bigram in word and EN_dictionary.check(word):
                        conn.sendall(f"VALID {word}".encode())
                        bigram = generate_bigram()
                        current_turn = 1 - current_turn  # Switch turn
                        for player in players:
                            player.sendall(f"BIGRAM {bigram}".encode())
                        players[current_turn].sendall(f"TURN".encode())
                    else:
                        conn.sendall(f"INVALID {word}".encode())
                        game_over = True
                        players[1 - current_turn].sendall(f"WIN".encode())
                        conn.sendall(f"LOSE".encode())
                        for player in players:
                            player.sendall("PLAY_AGAIN?".encode())
            else:
                conn.sendall("WAIT".encode())
        except Exception as e:
            print(f"Error: {e}")
            break

    conn.close()
    players.remove(conn)
    if not players:
        game_over = False
        bigram = generate_bigram()
        current_turn = 0
        play_again_votes = 0

# Server setup
def start_server():
    global players

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print("Server started. Waiting for players to connect...")
        while len(players) < 2:
            conn, addr = s.accept()
            players.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr)).start()
            if len(players) == 2:
                players[current_turn].sendall(f"TURN".encode())

start_server()
