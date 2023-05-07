import socket
from Game import *

HOST = "127.0.0.1"
PORT = 12345


def get_game_info(server):
    game_info = server.recv(50).decode().split()
    board_size = int(game_info[0])
    player_symbol = game_info[1]
    first_turn_symbol = game_info[2]
    return board_size, player_symbol, first_turn_symbol


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    # print(server.recv(1024).decode())
    while True:
        board_size, player_symbol, first_turn_symbol = get_game_info(server)
        g = Game(server, board_size, player_symbol, first_turn_symbol)
        g.play_game()


if __name__ == "__main__":
    main()
