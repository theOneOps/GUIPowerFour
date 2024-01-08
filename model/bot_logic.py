## @file: bot_logic.py
## This file contains all the funtions to determine the best move for the bot
## or the random move's one
"""
@package model
@file: bot_logic.py
@desc: This file contains all the funtions to determine
the best move for the bot or the random move's one

"""

import copy
import secrets
import numpy as np

# from .game_logic import finish_range_in_all_directions
from .game_types import Grid_t, Pos_t, StackPos_t


def get_random_position(tab: Grid_t, height: int,
                        width: int) -> Pos_t:
    """
    @brief get a random position in the grid
    :param tab: the 2D array representing the grid
    :param height: the height of the grid
    :param width: the width of the grid
    :return: the random position among the empty positions unless None
    """
    l: StackPos_t = []
    for i in range(height):
        for j in range(width):
            if tab[i][j] == -1:
                l.append([i, j])

    if len(l) != 0:
        # secrets.randbelow is used to generate secure random numbers
        x = secrets.randbelow(len(l))
        return l[x]
    return None


def match_null(height: int, width: int, nbsquarefilled: int) -> bool:
    """
    @brief check if the grid is full
    :param height: the height of the grid
    :param width: the width of the grid
    :param nbsquarefilled: the number of square filled
    :return: True if the grid is full, False otherwise
    """
    if height * width == nbsquarefilled:
        return True
    return False


def Position_possible(grid: Grid_t, player: int):
    n = len(grid[0])
    L: list[Grid_t] = []
    for i in range(n):
        if grid[n - 1][i] == -1:
            # cas quand la colonne est vide
            Pos: Grid_t = copy.deepcopy(grid)
            Pos[n - 1][i] = player
            L.append(Pos)
            # ajoute la grid avec la position_possible
        elif grid[0][i] == -1:
            # cas contraire
            j = 1
            while grid[j][i] != -1:
                j += 1
            if j != 0:
                Pos = copy.deepcopy(grid)
                Pos[j + 1][i] = player
                L.append(Pos)
                # ajoute la grid avec la position_possible
    return L


def evaluate(grid: Grid_t, player: int, max_player: int, max_length: int) \
        -> int:
    """
    @brief evaluate the grid
    :param grid: the 2D array representing the grid
    :param player: the player to check (0 or 1)
    :param max_player: the player to maximize
    :param max_length: the maximum length of
     a sequence (the number of tokens to check)
    :return: return the score of the grid
    """
    score = 0
    # Define weights for different sequence lengths
    weights = {i: 10 * i for i in range(3, max_length + 1)}

    # Evaluate sequences of various lengths
    for length in range(3, max_length + 1):
        score += evaluate_horizontal(grid, player, length) * weights[length]
        score += evaluate_vertical(grid, player, length) * weights[length]
        # Add evaluations for vertical, diagonal (both directions) here with
        score += evaluate_diagonal(grid, player, length) * weights[length]
        # same length

    # Adjust the score for the minimizing player
    if not max_player:
        score *= -1

    return score


def minimax(grid: Grid_t, depth: int, player: int, max_player: int, nb_tokens: int):
    L: list[Grid_t] = Position_possible(grid, player)
    # Cas de base : profondeur atteinte ou jeu terminé
    if depth == 0 or len(L) == 0:
        # Renvoie le score de la position et aucune position (None)
        return evaluate(grid, 1 - player, 1 - max_player, nb_tokens), grid

    if max_player:
        # Joueur max (la personne qui joue)
        value = float('-inf')
        best_grid = None
        for current_grid in L:
            # Récursivement évalue la position suivante
            print(np.array(current_grid))
            score, _ = minimax(current_grid, depth - 1, 1-player, 1-max_player, nb_tokens)
            # Met à jour la meilleure position et le score
            if score > value:
                value = score
                best_grid = current_grid
    else:
        # Joueur min (adversaire)
        value = float('inf')
        best_grid = None
        for current_grid in L:
            # Récursivement évalue la position suivante
            score, _ = minimax(current_grid, depth - 1, 1-player, max_player, nb_tokens)
            # Met à jour la meilleure position et le score
            if score < value:
                value = score
                best_grid = current_grid

    # Renvoie le score et la meilleure position
    return value, best_grid


# def minimax_with_move(grid: Grid_t, depth: int, is_maximizing_player: int,
#                       player,
#                       height: int, width: int, nb_tokens: int,
#                       nb_square_filled: int,
#                       stack: StackPos_t):
#     """
#     @brief minimax algorithm with alpha-beta pruning
#     :param grid: the 2D array representing the grid
#     :param depth: the depth of the tree
#     :param is_maximizing_player: the player to maximize
#     :param player: the player to check (0 or 1)
#     :param height: the height of the grid
#     :param width: the width of the grid
#     :param nb_tokens: the number of tokens to check
#     :param nb_square_filled: the number of square filled
#     :param stack: the stack of positions played
#     :return: the best move
#     """
#     if depth == 0:
#         return evaluate(grid, player, is_maximizing_player, nb_tokens), None
#
#     # Check if the last move won the game
#     fst = peek(stack)
#     if fst and finish_range_in_all_directions(player, fst[0], fst[1], grid,
#                                               nb_tokens, width, height):
#         return evaluate(grid, player, is_maximizing_player, nb_tokens), None
#
#     # Check for a draw
#     if match_null(height, width, nb_square_filled):
#         return evaluate(grid, player, is_maximizing_player, nb_tokens), None
#
#     best_move = None
#
#     if is_maximizing_player:
#         max_eval = float('-inf')
#         for i in range(len(grid)):
#             copie_grid = copy.deepcopy(grid)
#             new_pile = stack[:]
#             k: int = height - 1
#             while k != -1:
#                 if copie_grid[i][k] == -1:
#                     copie_grid[i][k] = player
#                     print(np.array(copie_grid))
#                     new_pile.append([i, k])
#                     break
#                 k -= 1
#             if k != -1:
#                 eval, _ = minimax_with_move(copie_grid, depth - 1,
#                                             False,
#                                             1 - player, height, width,
#                                             nb_tokens, nb_square_filled + 1,
#                                             new_pile)
#
#                 if eval > max_eval:
#                     max_eval = eval
#                     best_move = [i, k]
#         return max_eval, best_move
#     else:
#         min_eval = float('inf')
#         for i in range(len(grid)):
#             copie_grid = copy.deepcopy(grid)
#             new_pile = stack[:]
#             k: int = height - 1
#             while k != -1:
#                 if copie_grid[i][k] == -1:
#                     copie_grid[i][k] = player
#                     new_pile.append([i, k])
#                     break
#                 k -= 1
#             if k != -1:
#                 eval, _ = minimax_with_move(copie_grid, depth - 1,
#                                             True,
#                                             1 - player, height, width,
#                                             nb_tokens, nb_square_filled + 1,
#                                             new_pile)
#
#                 if eval < min_eval:
#                     min_eval = eval
#                     best_move = [i, k]
#         return min_eval, best_move


def evaluate_horizontal(grid: Grid_t, player: int, length: int) -> int:
    """
    @brief evaluate the grid in horizontal
    :param grid: the 2D array representing the grid
    :param player: the player to check (0 or 1)
    :param length: the length of the sequence (the number of tokens to check)
    :return: the score of the sequence
    """
    count = 0
    for row in grid:
        for i in range(len(row) - length + 1):
            sequence = row[i:i + length]

            if sequence.count(1 - player) == length and sequence.count(
                    None) == 0:
                count += 2  # Blocking an almost complete sequence by the
                # opponent

            if sequence.count(1 - player) == length - 1 and sequence.count(
                    None) == 1:
                count += 1.5  # Blocking an almost complete sequence by
                # the opponent

            elif sequence.count(player) == length:
                count += 1  # Completed sequence by the player

            elif sequence.count(player) == length - 1 and sequence.count(
                    None) == 1:
                count += 0.5  # Potential winning sequence for the
                # player

    return count


def evaluate_vertical(grid: Grid_t, player: int, length: int) -> int:
    """
    @brief evaluate the grid in vertical
    :param grid: the 2D array representing the grid
    :param player: the player to check (0 or 1)
    :param length: the length of the sequence (the number of tokens to check)
    :return: the score of the sequence
    """
    count = 0
    for col in range(len(grid[0])):
        for i in range(len(grid) - length + 1):
            sequence = [grid[i + n][col] for n in range(length)]

            if sequence.count(1 - player) == length and sequence.count(
                    None) == 0:
                count += 2  # Blocking an almost complete sequence by the
                # opponent

            if sequence.count(1 - player) == length - 1 and sequence.count(
                    None) == 1:
                count += 1.5  # Blocking an almost complete sequence by
                # the opponent

            elif sequence.count(player) == length:
                count += 1  # Completed sequence by the player

            elif sequence.count(player) == length - 1 and sequence.count(
                    None) == 1:
                count += 0.5  # Potential winning sequence for the player
    return count


def evaluate_diagonal(grid: Grid_t, player: int, length: int) -> int:
    """
    @brief evaluate the grid in diagonal
    :param grid: the 2D array representing the grid
    :param player: the player to check (0 or 1)
    :param length: the length of the sequence (the number of tokens to check)
    :return: the score of the sequence
    """
    count = 0
    # Check diagonals from top-left to bottom-right
    for col in range(len(grid[0]) - length + 1):
        for row in range(len(grid) - length + 1):
            sequence = [grid[row + n][col + n] for n in range(length)]
            count += evaluate_sequence(sequence, player, length)

    # Check diagonals from bottom-left to top-right
    for col in range(len(grid[0]) - length + 1):
        for row in range(length - 1, len(grid)):
            sequence = [grid[row - n][col + n] for n in range(length)]
            count += evaluate_sequence(sequence, player, length)

    return count


def evaluate_sequence(sequence, player, length):
    """
    Evaluate a sequence of tokens.
    """
    count = 0
    if sequence.count(1 - player) == length and sequence.count(None) == 0:
        count += 2  # Blocking an almost complete sequence by the opponent

    if sequence.count(1 - player) == length - 1 and sequence.count(None) == 1:
        count += 1.5  # Blocking an almost complete sequence by the opponent

    elif sequence.count(player) == length:
        count += 1  # Completed sequence by the player

    elif sequence.count(player) == length - 1 and sequence.count(None) == 1:
        count += 0.5  # Potential winning sequence for the player

    return count
