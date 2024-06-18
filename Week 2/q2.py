import copy  # use it for deepcopy if needed
import math
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variable to keep track of visited board positions. This is a dictionary with keys as self.boards as str and
# value represents the maxmin value. Use the get_boards_str function in History class to get the key corresponding to
# self.boards.
board_positions_val_dict = {}
board_positions_val_dict2 = {}

# Global variable to store the visited histories in the process of alpha beta pruning.
visited_histories_list = []
visited_histories_list2 = []


class History:
    def __init__(self, num_boards=2, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-(9n-1) representing the square in which the move will be played as shown
            below (n=2 is the number of boards).

             Board 1
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

             Board 2
              ____ ____ ____
             |_9_|_10_|_11_|
             |_12_|_13_|_14_|
             |_15_|_16_|_17_|

        # self.boards
            empty squares are represented using '0' and occupied squares are 'x'.
            Eg: [['x', '0', 'x', '0', 'x', 'x', '0', '0', '0'], ['0', 0', '0', 0', '0', 0', '0', 0', '0']]
            for two board game

            Board 1
              ___ ___ ____
             |_x_|___|_x_|
             |___|_x_|_x_|
             |___|___|___|

            Board 2
              ___ ___ ____
             |___|___|___|
             |___|___|___|
             |___|___|___|

        # self.player: 1 or 2
            Player whose turn it is at the current history/board

        :param num_boards: Number of boards in the game of Notakto.
        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        self.num_boards = num_boards
        if history is not None:
            self.history = history
            self.boards = self.get_boards()
        else:
            self.history = []
            self.boards = []
            for i in range(self.num_boards):
                # empty boards
                self.boards.append(['0', '0', '0', '0', '0', '0', '0', '0', '0'])
        # Maintain a list to keep track of active boards
        self.active_board_stats = self.check_active_boards()
        self.current_player = self.get_current_player()

    def get_boards(self):
        """ Play out the current self.history and get the boards corresponding to the history.

        :return: list of lists
                Eg: [['x', '0', 'x', '0', 'x', 'x', '0', '0', '0'], ['0', 0', '0', 0', '0', 0', '0', 0', '0']]
                for two board game

                Board 1
                  ___ ___ ____
                 |_x_|___|_x_|
                 |___|_x_|_x_|
                 |___|___|___|

                Board 2
                  ___ ___ ____
                 |___|___|___|
                 |___|___|___|
                 |___|___|___|
        """
        boards = []
        for i in range(self.num_boards):
            boards.append(['0', '0', '0', '0', '0', '0', '0', '0', '0'])
        for i in range(len(self.history)):
            board_num = math.floor(self.history[i] / 9)
            play_position = self.history[i] % 9
            boards[board_num][play_position] = 'x'
        return boards

    def check_active_boards(self):
        """ Return a list to keep track of active boards

        :return: list of int (zeros and ones)
                Eg: [0, 1]
                for two board game

                Board 1
                  ___ ___ ____
                 |_x_|_x_|_x_|
                 |___|_x_|_x_|
                 |___|___|___|

                Board 2
                  ___ ___ ____
                 |___|___|___|
                 |___|___|___|
                 |___|___|___|
        """
        active_board_stat = []
        for i in range(self.num_boards):
            if self.is_board_win(self.boards[i]):
                active_board_stat.append(0)
            else:
                active_board_stat.append(1)
        return active_board_stat

    @staticmethod
    def is_board_win(board):
        for i in range(3):
            if board[3 * i] == board[3 * i + 1] == board[3 * i + 2] != '0':
                return True

            if board[i] == board[i + 3] == board[i + 6] != '0':
                return True

        if board[0] == board[4] == board[8] != '0':
            return True

        if board[2] == board[4] == board[6] != '0':
            return True
        return False

    def get_current_player(self):
        """
        Get player whose turn it is at the current history/board
        :return: 1 or 2
        """
        total_num_moves = len(self.history)
        if total_num_moves % 2 == 0:
            return 1
        else:
            return 2

    def get_boards_str(self):
        boards_str = ""
        for i in range(self.num_boards):
            boards_str = boards_str + ''.join([str(j) for j in self.boards[i]])
        return boards_str

    def is_win(self):
        # Feel free to implement this in anyway if needed
        """
        0 - None
        1 - Player 1 wins
        -1 - Player 2 wins
        :return:
        """
        for status in self.active_board_stats:
            if status == 1:
                return 0
        if self.get_current_player() == 1:
            return 1
        else:
            return -1



    def get_valid_actions(self):
        # Feel free to implement this in anyway if needed
        actions = []
        for i in range(self.num_boards):
            if self.active_board_stats[i] == 0:
                pass
            else:
                # Center
                if self.boards[i][4] == '0':
                    actions.append(9*i+4)

            #Corners
                if self.boards[i][0] == '0':
                    actions.append(9*i)
                if self.boards[i][2] == '0':
                    actions.append(9*i+2)
                if self.boards[i][6] == '0':
                    actions.append(9*i+6)
                if self.boards[i][8] == '0':
                    actions.append(9*i+8)

            # Edges
                if self.boards[i][1] == '0':
                    actions.append(9*i+1)
                if self.boards[i][3] == '0':
                    actions.append(9*i+3)
                if self.boards[i][5] == '0':
                    actions.append(9*i+5)
                if self.boards[i][7] == '0':
                    actions.append(9*i+7)

        return actions


    def is_terminal_history(self):
        # Feel free to implement this in anyway if needed
        if self.is_win() == 0:
            return False
        return True


    def get_value_given_terminal_history(self):
        # Feel free to implement this in anyway if needed
        pass

    def update_history(self, action):
        child = copy.deepcopy(self)
        child.history.append(action)
        child.boards = child.get_boards()
        child.active_board_stats = child.check_active_boards()
        child.current_player = child.get_current_player()
        return child



i=0
def alpha_beta_pruning(history_obj, alpha, beta, max_player_flag):
    """
        Calculate the maxmin value given a History object using alpha beta pruning. Use the specific move order to
        speedup (more pruning, less memory).

    :param history_obj: History class object
    :param alpha: -math.inf
    :param beta: math.inf
    :param max_player_flag: Bool (True if maximizing player plays)
    :return: float
    """
    # These two already given lines track the visited histories.

    global visited_histories_list
    visited_histories_list.append(history_obj.history)
    # TODO implement
    if max_player_flag:
        max_eval = -math.inf
        if history_obj.is_terminal_history():
            if history_obj.history[0] != 4:
                print('yes', history_obj.is_win(), history_obj.is_terminal_history())
            return history_obj.is_win()
        else:
            actions = history_obj.get_valid_actions()
            board_str = history_obj.get_boards_str()
            if board_str not in board_positions_val_dict.keys():
                for action in actions:
                    child = history_obj.update_history(action)
                    eval = alpha_beta_pruning(child, -math.inf, beta, False)
                    if child.history[0] != 4:
                        print(child.history, eval, actions)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                board_positions_val_dict[board_str] = max_eval
            else:
                max_eval = board_positions_val_dict[board_str]
            return max_eval
    else:
        min_eval = math.inf
        if history_obj.is_terminal_history():
            if history_obj.history[0] != 4:
                print('yes', history_obj.is_win())
            return history_obj.is_win()
        else:
            actions = history_obj.get_valid_actions()
            board_str = history_obj.get_boards_str()
            if board_str not in board_positions_val_dict.keys():
                for action in actions:
                    child = history_obj.update_history(action)
                    eval = alpha_beta_pruning(child, alpha, math.inf, True)
                    if child.history[0] != 4:
                        print(child.history, eval)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                    board_positions_val_dict[board_str] = min_eval
            else:
                min_eval = board_positions_val_dict[board_str]
            return min_eval

    return -2
    # TODO implement



def maxmin(history_obj, max_player_flag):
    """
        Calculate the maxmin value given a History object using maxmin rule. Store the value of already visited
        board positions to speed up, avoiding recursive calls for a different history with the same board position.
    :param history_obj: History class object
    :param max_player_flag: True if the player is maximizing player
    :return: float
    """
    # Global variable to keep track of visited board positions. This is a dictionary with keys as str version of
    # self.boards and value represents the maxmin value. Use the get_boards_str function in History class to get
    # the key corresponding to self.boards.
    global visited_histories_list2
    visited_histories_list2.append(history_obj.history)
    # TODO implement
    if max_player_flag:
        max_eval = -math.inf
        if history_obj.is_terminal_history():
            return history_obj.is_win()
        else:
            actions = history_obj.get_valid_actions()
            board_str = history_obj.get_boards_str()
            if board_str not in board_positions_val_dict2.keys():
                for action in actions:
                    child = history_obj.update_history(action)
                    eval = maxmin(child, False)
                    max_eval = max(max_eval, eval)
                board_positions_val_dict2[board_str] = max_eval
            else:
                max_eval = board_positions_val_dict2[board_str]
            return max_eval
    else:
        min_eval = math.inf
        if history_obj.is_terminal_history():
            return history_obj.is_win()
        else:
            actions = history_obj.get_valid_actions()
            board_str = history_obj.get_boards_str()
            if board_str not in board_positions_val_dict2.keys():
                for action in actions:
                    child = history_obj.update_history(action)
                    eval = maxmin(child, True)
                    min_eval = min(min_eval, eval)
                    board_positions_val_dict2[board_str] = min_eval
            else:
                min_eval = board_positions_val_dict2[board_str]
            return min_eval
    return -2
    # TODO implement


def solve_alpha_beta_pruning(history_obj, alpha, beta, max_player_flag):
    global visited_histories_list
    val = alpha_beta_pruning(history_obj, alpha, beta, max_player_flag)
    return val, visited_histories_list


if __name__ == "__main__":
    logging.info("start")
    logging.info("alpha beta pruning")
    value, visited_histories = solve_alpha_beta_pruning(History(history=[], num_boards=3), -math.inf, math.inf, True)
    logging.info("maxmin value {}".format(value))
    logging.info("Number of histories visited {}".format(len(visited_histories)))
    logging.info("maxmin memory")
    # logging.info("maxmin value {}".format(maxmin(History(history=[], num_boards=2), True)))
    # logging.info("Number of histories visited {}".format(len(visited_histories_list2)))
    # logging.info("end")
