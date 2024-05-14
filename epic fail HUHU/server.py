import pygame
import enchant
import random
import socket
import threading

HOST = '192.168.100.102'  # Replace with server IP if needed
PORT = 5555        # Choose an open port number

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

EN_dictionary = enchant.Dict("en_US")

def handle_client(conn, addr):
    global bigram
    while True:
        # Send bigram to client
        conn.sendall(bigram.encode())

        # Receive submitted word
        data = conn.recv(1024).decode()
        if not data:
            break

        # Check word validity
        if ... (check word validity using dictionary and bigram):
            # Send valid word message and update bigram
            ...
        else:
            # Send invalid word message

        # Manage turn changes (send message indicating whose turn)
        ...

    conn.close()

while True:
    conn, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
