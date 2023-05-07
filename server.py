import socket
import time
from tictactoe import *

HOST = "127.0.0.1"
PORT = 12346
clients = []


def init_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.listen(2)
    establish_clients(s)
    return s


def establish_clients(s):
    print("Waiting for connections...")

    while len(clients) != 2:
        conn, addr = s.accept()
        print(f"Connected to {addr}")
        # conn.sendall(bytes("Connected to server\nWaiting for opponent...", encoding="utf-8"))
        clients.append(conn)


def send_data(data, client_index):
    encoded_data = bytes(data, encoding="utf-8")
    conn = clients[client_index]
    conn.sendall(encoded_data)


def broadcast_data(data):
    encoded_data = bytes(data, encoding="utf-8")
    for conn in clients:
        conn.sendall(encoded_data)


def assign_symbol():
    send_data("3 X X", 0)
    send_data("3 O X", 1)
    time.sleep(0.5)

def play_game():
    global cells
    sender_id = 0
    receiver_id = 1
    # broadcast_data(f"{cells}|1")
    while True:
        move = clients[sender_id].recv(50).decode()
        send_data(move, receiver_id)

        sender_id = (sender_id * -1) + 1
        receiver_id = (receiver_id * -1) + 1



def close_server(s):
    for conn in clients:
        conn.close()
    s.close()


if __name__ == "__main__":
    try:
        s = init_server()
        assign_symbol()
        play_game()
        close_server(s)
    except KeyboardInterrupt:
        close_server(s)