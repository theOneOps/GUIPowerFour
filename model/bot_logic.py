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
    rows = len(grid)
    cols = len(grid[0])
    L: list[Grid_t] = []

    for i in range(cols):
        for j in range(rows - 1, -1, -1):
            if grid[j][i] == -1:
                Pos: Grid_t = copy.deepcopy(grid)
                Pos[j][i] = player
                L.append(Pos)
                break  # Sort de la boucle interne une fois qu'un coup
                # est trouvé
    return L


# def evaluate(grid: Grid_t, player: int, max_player: int, max_length: int) \
#         -> int:
#     """
#     @brief evaluate the grid
#     :param grid: the 2D array representing the grid
#     :param player: the player to check (0 or 1)
#     :param max_player: the player to maximize
#     :param max_length: the maximum length of
#      a sequence (the number of tokens to check)
#     :return: return the score of the grid
#     """
#     score = 0
#     # Define weights for different sequence lengths
#     weights = {i: 10 * i for i in range(3, max_length + 1)}
#
#     # Evaluate sequences of various lengths
#     for length in range(3, max_length + 1):
#         score += evaluate_horizontal(grid, player, length) * weights[length]
#         score += evaluate_vertical(grid, player, length) * weights[length]
#         # Add evaluations for vertical, diagonal (both directions) here with
#         score += evaluate_diagonal(grid, player, length) * weights[length]
#         # same length
#
#     # Adjust the score for the minimizing player
#     if not max_player:
#         score *= -1


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
    # weights = {i: 10 * i for i in range(3, max_length + 1)}
    # weights = {3: 5, 4: 50, 5: 100}  # Exemple de poids ajustés
    weights = {
        3: 10,  # Séquences de 3
        4: 50,  # Séquences de 4
        5: 100,  # Séquences de 5
        6: 200,  # Séquences de 6
        7: 500,  # Séquences de 7
        8: 1000,  # Séquences de 8
        9: 2000,  # Séquences de 9
        10: 5000  # Séquences de 10
    }
    # Evaluate sequences of various lengths
    for length in range(3, max_length + 1):
        score += (evaluate_horizontal(grid, player, length) +
                  evaluate_vertical(grid, player, length) +
                  evaluate_diagonal(grid, player, length)) * weights[length]

        # same length

    # Adjust the score for the minimizing player
    if not max_player:
        score *= -1

    return score


def minimax(grid: Grid_t, depth: int, player: int, max_player: int,
            nb_tokens: int):
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
            print(f"joueur max\n {np.array(current_grid)}\n")
            score, _ = minimax(current_grid, depth - 1, 1 - player,
                               1 - max_player, nb_tokens)
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
            print(f"joueur min\n {np.array(current_grid)}\n")
            score, _ = minimax(current_grid, depth - 1, 1 - player,
                               1 - max_player,
                               nb_tokens)
            # Met à jour la meilleure position et le score
            if score < value:
                value = score
                best_grid = current_grid

    # Renvoie le score et la meilleure position
    return value, best_grid


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
            if sequence.count(player) == length:
                count += 1
            elif sequence.count(player) == length - 1 and sequence.count(
                    -1) == 1:
                if i > 0 and row[i - 1] == -1 or i + length < len(row) and \
                        row[
                            i + length] == -1:  # Vérifie si la séquence est
                    # ouverte
                    count += 0.5

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


def evaluate_diagonal(grid: Grid_t, player: int, length: int) -> int:
    count = 0
    # Diagonales de haut gauche à bas droite
    for col in range(len(grid[0]) - length + 1):
        for row in range(len(grid) - length + 1):
            sequence = [grid[row + n][col + n] for n in range(length)]
            count += evaluate_sequence_diagonal(grid, sequence, player, row,
                                                col, 1)

    # Diagonales de bas gauche à haut droite
    for col in range(len(grid[0]) - length + 1):
        for row in range(length - 1, len(grid)):
            sequence = [grid[row - n][col + n] for n in range(length)]
            count += evaluate_sequence_diagonal(grid, sequence, player, row,
                                                col, -1)

    return count


def evaluate_sequence_diagonal(grid: Grid_t, sequence: list, player: int,
                               start_row: int, start_col: int,
                               direction: int):
    count = 0
    if sequence.count(player) == len(sequence):
        count += 1
    elif sequence.count(player) == len(sequence) - 1 and sequence.count(
            -1) == 1:
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
