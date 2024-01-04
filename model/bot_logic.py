import copy

from .game_logic import valid_coord, peek, finish_range_in_all_directions
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


def evaluate(grid: Grid_t, width: int, height: int, x: int, y: int,
             player: int, nb_tokens: int) -> [int, Pos_t]:
    return (
        evaluate_horizontal(grid, width, height, x, y, player, nb_tokens) +
        evaluate_vertical(grid, width, height, x, y, player, nb_tokens) +
        evaluate_haut_gauche(grid, width, height, x, y, player, nb_tokens) +
        evaluate_bas_gauche(grid, width, height, x, y, player, nb_tokens),
        [x, y]
    )


def minimax_with_move(grid: Grid_t, depth: int, is_maximizing_player: int,
                      alpha: int, beta: int, player: int, height: int,
                      width: int, nbsquarefilled: int,

                      nb_tokens: int, pile: StackPos_t):
    next_player = 1 - player
    move = peek(pile)

    if depth == 0 or match_null(height, width, nbsquarefilled) or not (
            finish_range_in_all_directions(player, move[0], move[1], grid,
                                           nb_tokens, width, height)):
        last_move = peek(pile)
        return evaluate(grid, width, height, last_move[0], last_move[1],
                        player, nb_tokens)[0], last_move

    if is_maximizing_player:
        max_eval = float('-inf')
        best_move = None
        child, position = get_possible_positions(grid, height, width, player)
        for i in range(len(child)):
            new_pile = pile[:]  # Create a copy of the pile
            new_pile.append(position[i])
            eval, _ = minimax_with_move(child[i], depth - 1,
                                        False, alpha, beta,
                                        next_player, height, width,
                                        nbsquarefilled + 1,
                                        nb_tokens, new_pile)
            if eval > max_eval:
                max_eval = eval
                best_move = position[i]
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        child, position = get_possible_positions(grid, height, width, player)
        for i in range(len(child)):
            new_pile = pile[:]  # Create a copy of the pile
            new_pile.append(position[i])
            eval, _ = minimax_with_move(child[i], depth - 1,
                                        True,
                                        alpha, beta, next_player,
                                        height, width,
                                        nbsquarefilled + 1,
                                        nb_tokens, new_pile)
            if eval < min_eval:
                min_eval = eval
                best_move = position[i]
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def evaluate_n_u_plets(grid: Grid_t, x: int, y: int, player: int) -> int:
    value: int = 0
    if grid[x][y] == player:
        value += 6
    elif grid[x][y] == -1:
        value += 0
    else:
        value += 1

    return value


def calculate_score(value_max: bool, n: int):
    if value_max:
        return int(5. * pow(10, (n / 6) - 1))
    else:
        return int(5. * pow(10, n - 1) - pow(10, n - 2))


def evaluate_direction(code: int, code_max: int) -> int:
    if code == 0:
        code_max += 1
    elif code <= 5:
        code_max += calculate_score(False, code)
    elif code % 6 == 0:
        code_max += calculate_score(True, code)
    return code_max


def evaluate_horizontal(grid: Grid_t, width: int, height: int, x: int, y: int,
                        player: int, nb_tokens: int) -> int:
    code_max: int = 0
    tmp_x: int = x - nb_tokens + 1

    while tmp_x <= x:
        if not (valid_coord(tmp_x, y, width, height)):
            tmp_x += 1
        else:
            code = 0
            for i in range(tmp_x, tmp_x + nb_tokens):
                if not (valid_coord(i, y, width, height)):
                    code += 13
                else:
                    code += evaluate_n_u_plets(grid, i, y, player)
            code_max += evaluate_direction(code, code_max)
            tmp_x += 1
    return code_max


def evaluate_vertical(grid: Grid_t, width: int, height: int, x: int, y: int,
                      player: int, nb_tokens: int) -> int:
    code_max: int = 0
    tmp_y: int = y - nb_tokens + 1

    while tmp_y <= y:
        if not (valid_coord(x, tmp_y, width, height)):
            tmp_y += 1
        else:
            code = 0
            for i in range(tmp_y, tmp_y + nb_tokens):
                if not (valid_coord(x, i, width, height)):
                    code += 13
                else:
                    code += evaluate_n_u_plets(grid, x, i, player)
            code_max += evaluate_direction(code, code_max)
            tmp_y += 1

    return code_max


def evaluate_haut_gauche(grid: Grid_t, width: int, height: int, x: int, y: int,
                         player: int, nb_tokens: int) -> int:
    code_max: int = 0
    tmp_x: int = x - nb_tokens + 1
    tmp_y: int = y - nb_tokens + 1

    while tmp_x <= x:
        if not (valid_coord(tmp_x, tmp_y, width, height)):
            tmp_x += 1
            tmp_y += 1
        else:
            code = 0
            i: int = tmp_x
            for j in range(tmp_y, tmp_y + nb_tokens):
                if not (valid_coord(i, j, width, height)):
                    code += 13
                else:
                    code += evaluate_n_u_plets(grid, i, j, player)
                i += 1

            code_max += evaluate_direction(code, code_max)
            tmp_x += 1
            tmp_y += 1

    return code_max


def evaluate_bas_gauche(grid: Grid_t, width: int, height: int, x: int, y: int,
                        player: int, nb_tokens: int) -> int:
    code_max: int = 0
    tmp_x: int = x - nb_tokens + 1
    tmp_y: int = y + nb_tokens - 1

    while tmp_x <= x:
        if not (valid_coord(tmp_x, tmp_y, width, height)):
            tmp_x += 1
            tmp_y -= 1
        else:
            code = 0
            i: int = tmp_x
            for j in range(tmp_y, tmp_y - nb_tokens, -1):
                if not (valid_coord(i, j, width, height)):
                    code += 13
                else:
                    code += evaluate_n_u_plets(grid, i, j, player)
                i += 1

            code_max += evaluate_direction(code, code_max)
            tmp_x += 1
            tmp_y -= 1

    return code_max
