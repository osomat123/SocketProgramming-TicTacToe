# constants
EMPTY_SPACE = "-"


class Board:
    # Public Methods
    def __init__(self, size):
        self.size = size
        self.state = [EMPTY_SPACE for _ in range(size * size)]

    def add_to_state(self, pos_i, pos_j, symbol):
        index_in_state = self.__get_index_in_state(pos_i, pos_j)
        self.state[index_in_state] = symbol

    def is_cell_empty(self, pos_i, pos_j):
        index_in_state = self.__get_index_in_state(pos_i, pos_j)
        return self.state[index_in_state] == EMPTY_SPACE

    def find_winner(self):
        patterns = self.__get_all_patterns_in_state()
        for pattern in patterns:
            if self.__is_winning_pattern(pattern):
                winner = pattern[0]
                return winner

        if EMPTY_SPACE in self.state:
            return None

        return "Draw"

    def print_board(self):
        formatted_state = ""

        for i in range(len(self.state)):
            formatted_state += self.state[i]
            formatted_state += "  "

            if (i+1) % self.size == 0:
                formatted_state += "\n"

        print(formatted_state)

    # Private Methods
    def __is_winning_pattern(self, pattern):
        for i in range(1, self.size):
            if EMPTY_SPACE in pattern:
                return False

            if pattern[i] != pattern[i - 1]:
                return False

        return True

    def __get_pattern(self, symbol_index_lambda):
        pattern = ""
        for i in range(self.size):
            symbol_index = symbol_index_lambda(i)
            pattern += self.state[symbol_index]

        return pattern

    def __get_row_pattern(self, row_index):
        assert row_index < self.size
        pattern = self.__get_pattern(lambda i: (row_index * self.size) + i)
        return pattern

    def __get_column_pattern(self, col_index):
        assert col_index < self.size
        pattern = self.__get_pattern(lambda i: col_index + (i * self.size))
        return pattern

    def __get_left_diag_pattern(self):
        pattern = self.__get_pattern(lambda i: (i * self.size) + i)
        return pattern

    def __get_right_diag_pattern(self):
        pattern = self.__get_pattern(lambda i: (i * self.size) + (self.size - i - 1))
        return pattern

    def __get_all_patterns_in_state(self):
        patterns = []

        # Get all row patterns
        for i in range(self.size):
            patterns.append(self.__get_row_pattern(i))

        # Get all column patterns
        for i in range(self.size):
            patterns.append(self.__get_column_pattern(i))

        # Get diagonal patterns
        patterns.append(self.__get_left_diag_pattern())
        patterns.append(self.__get_right_diag_pattern())

        return patterns

    def __get_index_in_state(self, pos_i, pos_j):
        index_i = pos_i - 1
        index_j = pos_j - 1
        return (index_i * self.size) + index_j
