## @file bot_logic.py
## This file contains all the funtions to determine the best move for the bot
## and the random move's one
"""!
@package model
@file: bot_logic.py
@desc This file contains all the funtions to determine
the best move for the bot or the random move's one

"""
import copy
import secrets

from .game_logic import mod_finish_range_in_all_directions
from .game_types import Grid_t, Pos_t, StackPos_t


def mod_get_random_position(tab: Grid_t, height: int,
                            width: int) -> Pos_t:
    """!
    @brief get a random position in the grid
    :param tab: the 2D array representing the grid
    :param height: the height of the grid
    :param width: the width of the grid
    :return: the random position among the empty positions unless None
    """
    l: StackPos_t = []
    # loop to get all the empty positions
    for i in range(height):
        for j in range(width):
            if tab[i][j] == -1:
                l.append([i, j])

    # check if the list is not empty
    if len(l) != 0:
        # secrets.randbelow is used to generate secure random numbers
        # if not empty, get a random position in the list
        x = secrets.randbelow(len(l))
        return l[x]
    # unless we return None which means the grid is full
    return None


def mod_match_null(height: int, width: int, nbsquarefilled: int) -> bool:
    """!
    @brief check if the grid is full
    :param height: the height of the grid
    :param width: the width of the grid
    :param nbsquarefilled: the number of square filled
    :return: True if the grid is full, False otherwise
    """
    if height * width == nbsquarefilled:
        return True
    return False


def mod_positions_possibles(grid: Grid_t) -> list[Pos_t]:
    """!
    @brief get all the possible positions
    :param grid: the 2D array representing the grid
    :return: the list of all the possible positions
    """
    rows: int = len(grid)
    cols: int = len(grid[0])
    l: list[Pos_t] = []

    # the idea is to loop through the grid to get the first empty position in
    # each column

    # so we loop through the columns
    for i in range(cols):
        # and then through the rows by starting from the bottom until we find
        # the first empty position
        for j in range(rows - 1, -1, -1):
            if grid[j][i] == -1:
                l.append([j, i])
                break
                # we break the loop to get the first empty position
            # and then we go to the next column

    return l


def mod_evaluate(grid: Grid_t, player: int, max_player: int, max_length: int) \
        -> int:
    """!
    @brief evaluate the grid
    :param grid: the 2D array representing the grid
    :param player: the player to check (0 or 1)
    :param max_player: the player to maximize
    :param max_length: the maximum length of
     a sequence (the number of tokens to check)
    :return: return the score of the grid
    """
    # here the idea is to evaluate the grid by checking the sequences of
    # different lengths and then to multiply the score by a weight

    # so first, we initialize the score to 0
    score: int = 0
    # Define weights for different sequence lengths
    weights: dict = {
        3: 30,  # Sequence of 3
        4: 100,  # Sequence of 4
        5: 400,  # Sequence of 5
        6: 600,  # Sequence of 6
        7: 900,  # Sequence of 7
        8: 1500,  # Sequence of 8
        9: 3000,  # Sequence of 9
        10: 7000  # Sequence of 10
    }
    # Evaluate sequences of various lengths
    for length in range(3, max_length + 1):
        # we add the score of the sequence of length 'length' to the score
        # the evaluation is done in horizontal, vertical and diagonal
        score += ((mod_evaluate_horizontal(grid, player, length) +
                   mod_evaluate_vertical(grid, player, length) +
                   mod_evaluate_diagonal(grid, player, length)) * weights[
                      length])

    # Adjust the score for the minimizing player
    if not max_player:
        score *= -1

    return score


def mod_minimax(grid: Grid_t, truly_depth: int, depth: int, player: int,
                max_player: int, nb_tokens: int, width: int,
                height: int, nbsquarefilled: int, previous_player: int = -1,
                pos: Pos_t
                = None) -> (int, Grid_t):
    """!
    @brief minimax algorithm
    :param grid: the 2D array representing the grid
    :param truly_depth: the depth of the tree
    :param depth: the depth of the tree
    :param player: the player to check (0 for the bot or 1 for the human)
    :param max_player: the player to maximize
    :param nb_tokens: the number of tokens to align to win the game
    :param width: the width of the grid
    :param height: the height of the grid
    :param nbsquarefilled: the number of square filled
    :param previous_player: the player who played the previous move
    :param pos: the position to check for the player who plays that position
    :return: the score of the best position and the best grid according to the
    minimax algorithm
    """
    # we get all the possible positions from the current grid
    l: list[Pos_t] = mod_positions_possibles(grid)

    # we check if the position is not None
    # if it is not None, it means a player has played a move
    # so we check if the player who played that move has won the game
    if pos is not None:
        # if the player who has played is the maximizing player and he has won
        if (mod_finish_range_in_all_directions(previous_player, pos[0], pos[1],
                                               grid,
                                               nb_tokens, width, height) and
                max_player == 1):
            # we return minus infinity and the grid (basically, it means the
            # minimizing player has won the game)
            # we return minus inf because it's the worst case for the
            # maximizing player (and although, it's the turn of the
            # maximizing player)
            # so we want the max player to not play that move
            return float('-inf'), grid
        # if the player who has played is the minimizing player and he has won
        elif (mod_finish_range_in_all_directions(previous_player, pos[0],
                                                 pos[1],
                                                 grid,
                                                 nb_tokens, width, height) and
              max_player == 0):
            # we return plus infinity and the grid (basically, it means the
            # maximizing player has won the game)
            # we return plus inf because it's the worst case for the
            # minimizing player (and although, it's the turn of the
            # minimizing player)
            # so we want the min player to bring up this move to the top for
            # the maximizing player
            return float('inf'), grid

    if mod_match_null(height, width, nbsquarefilled):
        # if it is a draw, then we return 0 for the score to mean that it is a
        # way to not lose the game and to not win the game (because again ,
        # when we win, the score is positive and when we lose, the score is
        # negative)
        return 0, grid  # 5000

    # (truly_depth is initialized with the same value as depth)
    # case when the truly depth is even
    if (depth == 0 or len(l) == 0) and truly_depth % 2 == 0:
        # Renvoie le score de la position et aucune position (None)
        return mod_evaluate(grid, 1 - player, 1 - max_player, nb_tokens), grid

    # case when the truly depth is odd
    if (depth == 0 or len(l) == 0) and truly_depth % 2 != 0:
        # Renvoie le score de la position et aucune position (None)
        return mod_evaluate(grid, player, max_player, nb_tokens), grid

    # if the player is the maximizing player
    if max_player:
        # we initialize the value to minus infinity because we want to
        # maximize the score for this player
        value: float = float('-inf')
        # we initialize the best grid to None because we want to get the best
        # grid for the maximizing player
        best_grid: Grid_t = None
        # we loop through all the possible positions to get the best position
        # ever
        for current_pos in l:
            # we first copy the grid to not modify the original one
            new_grid: Grid_t = copy.deepcopy(grid)
            # we play the move for the current player
            new_grid[current_pos[0]][current_pos[1]] = player

            # we recursively evaluate the next position
            score, _ = mod_minimax(new_grid, truly_depth, depth - 1,
                                   1 - player, 1 - max_player, nb_tokens,
                                   width, height, nbsquarefilled + 1,
                                   player, current_pos)

            # we update the best position and the score
            if score > value:
                value = score
                best_grid = new_grid

            # if the score is the same, we update the best grid
            # in this case, we want to get the best grid for the maximizing
            # player
            if score == value:
                best_grid = new_grid

    else:
        # we initialize the value to plus infinity because we want to
        # minimize the score for this player
        value: float = float('inf')
        best_grid: Grid_t = None
        for current_pos in l:
            new_grid: Grid_t = copy.deepcopy(grid)
            new_grid[current_pos[0]][current_pos[1]] = player

            # we recursively evaluate the next position
            score, _ = mod_minimax(new_grid, truly_depth, depth - 1,
                                   1 - player, 1 - max_player, nb_tokens,
                                   width, height, nbsquarefilled + 1,
                                   player, current_pos)

            # we update the best position and the score
            if score < value:
                value = score
                best_grid = new_grid

            # if the score is the same, we update the best grid
            # in this case, we want to get the best grid for the minimizing
            # player
            if score == value:
                best_grid = new_grid

    # we return the value of the best grid and the grid 'itself'
    return value, best_grid


def mod_evaluate_horizontal(grid: Grid_t, player: int, length: int) -> int:
    """!
    @brief evaluate the grid in horizontal
    :param grid: the 2D array representing the grid
    :param player: the player to check (0 or 1)
    :param length: the length of the sequence (the number of tokens to check)
    :return: the score value of the sequence
    """
    # basically, the idea is to loop through the grid and to check the
    # sequences of length 'length' in horizontal
    # and to check if the sequence is open or not
    # if the sequence is open, we add 0.5 to the score
    # if the sequence is closed, we add 1 to the score (it's a winning
    # sequence for the player)

    count: int = 0
    for row in grid:
        # for each row, we loop through the columns
        for i in range(len(row) - length + 1):
            # we get the sequence of length 'length'
            # so we stop at len(row) - length + 1 because we don't want to
            # exceed the length of the row while trying to get the sequence
            # of length 'length'
            sequence = row[i:i + length]
            # then we check if the sequence is open or not with the good length
            if sequence.count(player) == length:
                count += 1
            # if the sequence is open and the sequence contains only one empty
            # only one empty square because we want to check if that
            # sequence, particularly, is open
            elif sequence.count(player) == length - 1 and sequence.count(
                    -1) == 1:
                # first we check checks if there's room to the left
                # of the sequence. If i is greater than 0, it means there
                # are cells to the left of the sequence.
                # checks if the cell immediately to the left
                # of the sequence is empty (represented as -1).

                # the condition after the 'or' is where we check if it is the
                # same manner as the left for the right
                if i > 0 and row[i - 1] == -1 or i + length < len(row) and \
                        row[
                            i + length] == -1:
                    # if the sequence is open, we add 0.5 to the score
                    count += 0.5

    return count


def mod_evaluate_vertical(grid: Grid_t, player: int, length: int) -> int:
    """!
    @brief evaluate the grid in vertical
    :param grid: the 2D array representing the grid
    :param player: the player to check (0 or 1)
    :param length: the length of the sequence (the number of tokens to check)
    :return: the score value of the sequence
    """
    count: int = 0

    for col in range(len(grid[0])):
        for row in range(len(grid) - length + 1):
            sequence = [grid[row + n][col] for n in range(length)]
            if sequence.count(player) == length:
                count += 1
            elif sequence.count(player) == length - 1 and sequence.count(
                    -1) == 1:
                if row > 0 and grid[row - 1][
                    col] == -1 or row + length < len(grid) and \
                        grid[row + length][col] == -1:
                    count += 0.5
    return count


def mod_evaluate_diagonal(grid: Grid_t, player: int, length: int) -> int:
    """!
    @brief evaluate the grid in diagonal
    :param grid: the 2D array representing the grid
    :param player: the player to check (0 or 1)
    :param length: the length of the sequence (the number of tokens to check)
    :return: the score value of the sequence
    """
    count: int = 0
    # The function starts by checking diagonal sequences from the top-left
    # corner to the bottom-right corner (col and row loops).

    for col in range(len(grid[0]) - length + 1):
        for row in range(len(grid) - length + 1):
            # For each starting position within this loop, it extracts
            # a sequence
            # of tokens of the specified length from the grid using
            # a list comprehension.
            # It then calls the evaluate_sequence_diagonal function to evaluate
            # the specific diagonal sequence.
            # so the 1 argument for direction indicates that it's checking
            # diagonal sequences from the top-left to the bottom-right.
            sequence = [grid[row + n][col + n] for n in range(length)]
            count += mod_evaluate_sequence_diagonal(grid, sequence,
                                                    player, row, col,
                                                    1)

    # The function starts by checking diagonal sequences from the bottom-left
    # corner to the top-right corner (col and row loops).
    for col in range(len(grid[0]) - length + 1):
        # And it is basically the same thing as the previous loop
        # except that it checks diagonal sequences from the bottom-left to the
        # top-right, but the principle is the same
        for row in range(length - 1, len(grid)):
            sequence = [grid[row - n][col + n] for n in range(length)]
            count += mod_evaluate_sequence_diagonal(grid, sequence, player,
                                                    row, col, -1)

    return count


def mod_evaluate_sequence_diagonal(grid: Grid_t, sequence: list, player: int,
                                   start_row: int, start_col: int,
                                   direction: int):
    """!
    @brief evaluate the sequence in diagonal
    :param grid: the 2D array representing the grid
    :param sequence:
    :param player:
    :param start_row: the row to start from
    :param start_col: the column to start from
    :param direction:the direction to check (1 for top-left to bottom-right
    and -1 for bottom-left to top-right)
    :return: the score value of the sequence
    """
    count: int = 0
    if sequence.count(player) == len(sequence):
        count += 1
    elif sequence.count(player) == len(sequence) - 1 and sequence.count(
            -1) == 1:
        # Depending on the direction, it checks for the empty cell either
        # on the top-left or top-right side (or bottom-left or bottom-right,
        # depending on the direction).

        # start_row > 0 and start_col > 0: This checks if the sequence
        # has enough room on the top-left side to potentially complete the
        # sequence with an empty cell. It ensures that start_row and
        # start_col are not at the top or left edge of the grid.
        # grid[start_row - 1][start_col - 1] == -1:
        # This condition checks if the cell immediately above and to the left
        # of the sequence is an empty
        # cell (-1).

        # OR

        # start_row + len(sequence) < len(grid) and start_col
        # + len(sequence) < len(grid[0]):
        # These conditions check if the sequence has enough room on the
        # bottom-right side to potentially complete the sequence with
        # an empty cell. It ensures that the sequence doesn't extend
        # beyond the bottom or right edge of the grid.

        # or

        # grid[start_row + len(sequence)][start_col + len(sequence)] == -1:
        # This condition checks if the cell immediately below and to the right
        # of the sequence is an empty cell (-1).

        # then we verify the same thing for the other direction
        # and finally, if the sequence is open, we add 0.5 to the score
        if (direction == 1 and (
                start_row > 0 and start_col > 0 and
                grid[start_row - 1][start_col - 1] == -1) or
            (start_row + len(sequence) < len(grid) and start_col + len(
                sequence) < len(grid[0]) and grid[start_row + len(sequence)][
                 start_col + len(sequence)] == -1)) or \
                (direction == -1 and (
                        start_row < len(grid) - 1 and start_col > 0 and
                        grid[start_row + 1][start_col - 1] == -1) or
                 (start_row - len(sequence) >= 0 and start_col + len(
                     sequence) < len(grid[0]) and
                  grid[start_row - len(sequence)][
                      start_col + len(sequence)] == -1)):
            count += 0.5
    return count
