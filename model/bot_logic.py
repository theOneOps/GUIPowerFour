import copy

from .game_logic import peek
from .game_types import Grid_t, Pos_t, StackPos_t


def get_random_position(tab: Grid_t, height: int,
                        width: int) -> Pos_t:
    for i in range(height):
        for j in range(width):
            if tab[i][j] == -1:
                return [i, j]
    return None


def get_possible_positions(tab: Grid_t, height: int, width: int,
                           player: int) -> list:
    possible_positions = []  # list of grid, to get all possible
    # positions played for a player
    positions_play = []  # list of all positions played

    for i in range(width):
        # if the column is empty
        if tab[i][height - 1] == -1:
            copie_grid = copy.deepcopy(tab)
            copie_grid[i][height - 1] = player
            possible_positions.append(copie_grid)
            positions_play.append([i, height - 1])

        # if the column is full
        elif tab[i][0] != -1:
            pass

        # if the column is not full and empty either...
        else:
            copie_grid = copy.deepcopy(tab)
            k: int = height - 1
            while k != -1:
                if copie_grid[i][k] == -1:
                    copie_grid[i][k] = player
                    possible_positions.append(copie_grid)
                    positions_play.append([i, k])
                    break
                k -= 1

    return possible_positions, positions_play


def match_null(height: int, width: int, nbsquarefilled: int) -> bool:
    if height * width == nbsquarefilled:
        return True
    return False


def evaluates(grid, player):
    # This is a simple evaluation function that you can expand.
    # Currently, it just counts the player's tokens.

    player_tokens = sum(row.count(player) for row in grid)
    return player_tokens


def minimax_with_move(grid: Grid_t, depth: int, is_maximizing_player: int,
                      alpha: int, beta, player,
                      height: int, width: int, nb_tokens: int,
                      nb_square_filled: int,
                      stack: StackPos_t):
    fst = peek(stack)
    if depth == 0 or match_null(height, width,
                                nb_square_filled):
        return evaluates(grid, player), None

    best_move = None

    if is_maximizing_player:
        max_eval = float('-inf')
        child, position = get_possible_positions(grid, height, width, player)
        for i in range(len(child)):
            new_pile = stack[:]
            new_pile.append(position[i])
            eval, _ = minimax_with_move(child[i], depth - 1,
                                        False,
                                        alpha,
                                        beta, 1 - player, height, width,
                                        nb_tokens, nb_square_filled + 1,
                                        new_pile)
            if eval > max_eval:
                max_eval = eval
                best_move = position[i]
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        child, position = get_possible_positions(grid, height, width, player)
        for i in range(len(child)):
            new_pile = stack[:]
            new_pile.append(position[i])
            eval, _ = minimax_with_move(child[i], depth - 1,
                                        True,
                                        alpha, beta,
                                        1 - player, height, width, nb_tokens,
                                        nb_square_filled + 1,
                                        new_pile)
            if eval < min_eval:
                min_eval = eval
                best_move = position[i]
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def evaluate(grid, player, max_player, max_length):
    score = 0
    # Define weights for different sequence lengths
    weights = {i: 10 * i for i in range(2, max_length + 1)}

    # Evaluate sequences of various lengths
    for length in range(2, max_length + 1):
        score += evaluate_horizontal(grid, player, length) * weights[length]
        score += evaluate_vertical(grid, player, length) * weights[length]
        score += evaluate_diagonal(grid, player, length) * weights[length]
        # Add evaluations for vertical, diagonal (both directions) here with
        # same length

    # Adjust the score for the minimizing player
    if not max_player:
        score *= -1

    return score


def evaluate_horizontal(grid, player, length):
    count = 0
    for row in grid:
        for i in range(len(row) - length + 1):
            sequence = row[i:i + length]
            if (sequence.count(player) == length and
                    sequence.count(None) == 0):
                count += 1
            elif (sequence.count(player) == length - 1 and
                  sequence.count(None) == 1):
                # This is an open-ended sequence with potential to win
                count += 0.5
    return count


def evaluate_vertical(grid, player, length):
    count = 0
    for col in range(len(grid[0])):
        for i in range(len(grid) - length + 1):
            sequence = [grid[i + n][col] for n in range(length)]
            if (sequence.count(player) == length and
                    sequence.count(None) == 0):
                count += 1
            elif (sequence.count(player) == length - 1 and
                  sequence.count(None) == 1):
                # This is an open-ended sequence with potential to win
                count += 0.5
    return count


def evaluate_diagonal(grid, player, length):
    count = 0
    for col in range(len(grid[0]) - length + 1):
        for row in range(len(grid) - length + 1):
            sequence = [grid[row + n][col + n] for n in range(length)]
            if (sequence.count(player) == length and
                    sequence.count(None) == 0):
                count += 1
            elif (sequence.count(player) == length - 1 and
                  sequence.count(None) == 1):
                # This is an open-ended sequence with potential to win
                count += 0.5
    return count
