from Board import *


class Game:
    game_symbols = ["X", "O"]

    # Public Methods
    def __init__(self, server, board_size, player_symbol, first_turn_symbol):
        self.server = server
        self.board = Board(board_size)
        self.player_symbol = player_symbol

        for symbol in Game.game_symbols:
            if symbol != self.player_symbol:
                self.opponent_symbol = symbol

        self.cur_turn_symbol = first_turn_symbol

    def play_game(self):
        winner = None

        while winner is None:
            self.board.print_board()

            if self.cur_turn_symbol == self.player_symbol:
                pos_i, pos_j = self.__get_input()
                self.board.add_to_state(pos_i, pos_j, self.cur_turn_symbol)
                self.__send_data_to_server(pos_i, pos_j)
                self.cur_turn_symbol = self.opponent_symbol
            else:
                pos_i, pos_j = self.__receive_data_from_server()
                self.board.add_to_state(pos_i, pos_j, self.cur_turn_symbol)
                self.cur_turn_symbol = self.player_symbol

            winner = self.board.find_winner()

        self.__print_winner(winner)

    # Private Methods
    def __print_winner(self, winner):
        if winner == "Draw":
            print("Draw!")
        if winner == self.player_symbol:
            print("You win :)")
        if winner == self.opponent_symbol:
            print("Opponent wins :(")

    def __validate_user_input(self, user_input):
        if len(user_input) < 2:
            print("Enter two coordinates!")
            return False

        if not (user_input[0].isdigit() and user_input[1].isdigit()):
            print("You should enter numbers!")
            return False

        for data in user_input:
            if not data.isdigit():
                print("You should enter numbers!")
                return False

            if int(data) not in range(4):
                print("Coordinates should be from 1 to 3!")
                return False

        pos_i = int(user_input[0])
        pos_j = int(user_input[1])
        if not self.board.is_cell_empty(pos_i, pos_j):
            print("This cell is occupied! Choose another one!")
            return False

        return True

    def __get_input(self):
        while True:
            user_input = [i for i in input("Enter the coordinates: ").split(maxsplit=1)]
            is_input_valid = self.__validate_user_input(user_input)

            if is_input_valid:
                return int(user_input[0]), int(user_input[1])

    def __send_data_to_server(self, pos_i, pos_j):
        data = bytes(f"{pos_i} {pos_j}", encoding="utf-8")
        self.server.sendall(data)

    def __receive_data_from_server(self):
        received_data = self.server.recv(50).decode().split()
        pos_i = int(received_data[0])
        pos_j = int(received_data[1])
        return pos_i, pos_j


