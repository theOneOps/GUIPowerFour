## @file game_logic.py
## This file contains all the funtions needed to play the game
## except the bot's logic

"""
@package model
@file: game_logic.py
@desc: This file contains all the funtions needed to play the game
except the bot's logic

"""

from .game_types import Grid_t, Pos_t, StackPos_t

# constants variables

## the value of the human player
HUMANVALUE: int = 1

## the value of the bot player
BOTVALUE: int = 0


# vérifier si la position jouée est valide ou pas ...
def valid_coord(x: int, y: int, width: int, height: int) -> bool:
    """
    @brief Verify if the position played is valid or not
    :param x: the x position to check between 0 and width
    :param y: the y position to check between 0 and height
    :param width: the width of the grid
    :param height: the height of the grid
    :return: the result of the check (a boolean)
    """
    return (0 <= x < width) and (0 <= y < height)


# vérifier si un quintuplet en horizontal(si nb_tokens == 5) est atteint
def finish_range_horizontal(
        player: int,
        posx: int,
        posy: int,
        tab: Grid_t,
        nb_tokens: int,
        width: int,
        height: int,
) -> bool:
    """
    @brief check if a range of 5 tokens is reached in horizontal
    :param player: the player to check (0 or 1)
    :param posx: the x position to check
    :param posy: the y position to check
    :param tab: the grid
    :param nb_tokens: the number of tokens to check
    :param width: the width of the grid
    :param height: the height of the grid
    :return: the result of the check
    """
    x: int = posx
    y: int = posy
    count: int = 0

    # we starts the check from the position x - nb_tokens + 1
    for i in range(x - nb_tokens + 1, x + nb_tokens):
        if valid_coord(i, y, width, height):
            if tab[i][y] == player:
                count += 1
            else:
                count = 0
        if count == nb_tokens:
            break
    return True if count == nb_tokens else False


# vérifier si un quintuplet en vertical(si nb_tokens == 5) est atteint
def finish_range_vertical(
        player: int,
        posx: int,
        posy: int,
        tab: Grid_t,
        nb_tokens: int,
        width: int,
        height: int,
) -> bool:
    """
    @brief check if a range of 5 tokens is reached in vertical
    :param player: the player to check (0 or 1)
    :param posx: the x position to check
    :param posy: the y position to check
    :param tab: the 2D array
    :param nb_tokens: the number of tokens to check
    :param width: the width of the grid
    :param height: the height of the grid
    :return: the result of the check
    """
    x: int = posx
    y: int = posy
    count: int = 0
    for i in range(y - nb_tokens + 1, y + nb_tokens):
        if valid_coord(x, i, width, height):
            if tab[x][i] == player:
                count += 1
            else:
                count = 0
        if count == nb_tokens:
            break
    return True if count == nb_tokens else False


# vérifier si un quintuplet dans le diagonale gauche(si nb_tokens == 5)
# est atteint
def finish_range_haut_gauche(
        player: int,
        posx: int,
        posy: int,
        tab: Grid_t,
        nb_tokens: int,
        width: int,
        height: int,
) -> bool:
    """
    @brief check if a range of 5 tokens is reached in left diagonal
    :param player: the player to check (0 or 1)
    :param posx: the x position to check
    :param posy: the y position to check
    :param tab: the 2D array
    :param nb_tokens: the number of tokens to check
    :param width: the width of the grid
    :param height: the height of the grid
    :return: the result of the check
    """
    x: int = posx
    y: int = posy - nb_tokens + 1
    count: int = 0
    for i in range(x - nb_tokens + 1, x + nb_tokens):
        if valid_coord(i, y, width, height):
            if tab[i][y] == player:
                count += 1
            else:
                count = 0
        if count == nb_tokens:
            break
        y += 1
    return True if count == nb_tokens else False


# vérifier si un quintuplet dans le diagonale droit(si nb_tokens == 5)
# est atteint
def finish_range_bas_gauche(
        player: int,
        posx: int,
        posy: int,
        tab: Grid_t,
        nb_tokens: int,
        width: int,
        height: int,
) -> bool:
    """
    @brief check if a range of 5 tokens is reached in right diagonal
    :param player: the player to check (0 or 1)
    :param posx: the x position to check
    :param posy: the y position to check
    :param tab: the 2D array
    :param nb_tokens: the number of tokens to check
    :param width: the width of the grid
    :param height: the height of the grid
    :return: the result of the check
    """
    x: int = posx
    y: int = posy + nb_tokens - 1
    count: int = 0
    for i in range(x - nb_tokens + 1, x + nb_tokens):
        if valid_coord(i, y, width, height):
            if tab[i][y] == player:
                count += 1
            else:
                count = 0
        if count == nb_tokens:
            break
        y -= 1
    return True if count == nb_tokens else False


# appeler tous les finishRange en les réunissant en une seule fonction...
def finish_range_in_all_directions(
        player: int, x: int, y: int, tab: Grid_t, token: int, width: int,
        height: int
) -> bool:
    """
    @brief check if a range of 5 tokens is reached in all directions
    :param player: the player to check (0 or 1)
    :param x: the x position to check
    :param y: the y position to check
    :param tab: the 2D array
    :param token: the number of tokens to check
    :param width: the width of the grid
    :param height: the height of the grid
    :return: the result of the check
    """
    return (
            finish_range_vertical(player, x, y, tab, token, width, height) or
            finish_range_horizontal(player, x, y, tab, token, width, height) or
            finish_range_haut_gauche(player, x, y, tab,
                                     token, width, height) or
            finish_range_bas_gauche(player, x, y, tab, token, width, height)
    )


# fonction à lancer lors du tour du joueur bot
def play_bot(
        tab: Grid_t,
        player: int,
        finishgame: bool,
        token: int,
        width: int,
        height: int,
        the_pos: Pos_t,
) -> bool:
    """
    @brief check if the bot has won
    :param tab: the 2D array of the board
    :param player: the bot value
    :param finishgame: the boolean that says if the game is finished or not
    :param token: the number of tokens to check
    :param width: the width of the grid
    :param height: the height of the grid
    :param the_pos: the position of the token played
    :return: the result of the check
    """
    # best_position: Pos_t = best_positionToPlay(tab, player)
    if finish_range_in_all_directions(
            player, the_pos[0], the_pos[1], tab, token, width, height
    ):
        print("le joueur bot a gagné")
        finishgame = False

    return finishgame


# fonction à lancer lors du tour du joueur humain
def play_human(
        tab: Grid_t,
        player: int,
        theposition: Pos_t,
        finishgame: bool,
        token: int,
        width: int,
        height: int,
) -> bool:
    """
    @brief check if the human has won
    :param tab: the 2D array of the board
    :param player: the human value
    :param theposition: the position the human played
    :param finishgame: the boolean that says if the game is finished or not
    :param token: the number of tokens to check
    :param width: the width of the grid
    :param height: the height of the grid
    :return: the result of the check
    """
    if finish_range_in_all_directions(
            player, theposition[0], theposition[1], tab, token, width, height
    ):
        print("le joueur humain a gagné")
        finishgame = False
    return finishgame


def launch_game(
        tab: Grid_t,
        width: int,
        height: int,
        tour_jeu: int,
        tokens: int,
        finishgame: bool,
        the_pos: Pos_t,
) -> bool:
    """
    @brief a boolean that says if the game is finished or
    not (if the bot wins or the human wins)
    :param tab: the 2D array of the board
    :param width: the width of the grid
    :param height: the height of the grid
    :param tour_jeu: the number of the turn
    :param tokens: the number of tokens to check
    :param finishgame: the boolean that says if the game is finished or not
    :param the_pos: the position the human played
    :return: the result of the check
    """
    res: bool

    if tour_jeu % 2 == 0:
        res = play_human(tab, HUMANVALUE, the_pos, finishgame, tokens, width,
                         height)
    else:
        res = play_bot(tab, BOTVALUE, finishgame, tokens, width, height,
                       the_pos)
    print(f"tour de jeu: {tour_jeu} | finishGame : {res}")

    return res


def peek(stack: StackPos_t) -> Pos_t:
    """
    @brief return the last element of the stack
    :param stack: the stack of positions played
    :return: the last element of the stack
    """
    if not stack:
        return None  # Retourne None si la pile est vide
    return stack[-1]
