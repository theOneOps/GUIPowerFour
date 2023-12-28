from type import *

# Variables constantes

humanValue: int = 1
botValue: int = 0


# vérifier si la position jouée est valide ou pas ...
def valid_coord(x: int, y: int, width: int, height: int) -> bool:
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
    x: int = posx
    y: int = posy
    count: int = 0

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
    x: int = posx
    y: int = posy - nb_tokens - 1
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
    player: int, x: int, y: int, tab: Grid_t, token: int, width: int, height: int
) -> bool:
    return (
        finish_range_vertical(player, x, y, tab, token, width, height)
        or finish_range_horizontal(player, x, y, tab, token, width, height)
        or finish_range_haut_gauche(player, x, y, tab, token, width, height)
        or finish_range_bas_gauche(player, x, y, tab, token, width, height)
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
    if finish_range_in_all_directions(
        player, theposition[0], theposition[1], tab, token, width, height
    ):
        print("le joueur humain a gagné")
        finishgame = False
    return finishgame


# à faire...
# fonction qui utilisera le min_max pour déterminer
# la meilleure position possible à jouer...
# def best_position_to_play(tab: Grid_t, player: int) -> Pos_t:
#     position: Pos_t = {}
#     # À faire... minmax
#     return position
#


def get_random_position(tab: Grid_t, height: int, width: int) -> Pos_t:
    position: Pos_t
    for i in range(height):
        for j in range(width):
            if tab[i][j] == -1:
                return [i, j]
    return None


def launch_game(
    tab: Grid_t,
    width: int,
    height: int,
    tour_jeu: int,
    tokens: int,
    finishgame: bool,
    the_pos: Pos_t,
) -> bool:
    res: bool

    if tour_jeu % 2 == 0:
        res = play_human(tab, humanValue, the_pos, finishgame, tokens, width, height)
    else:
        res = play_bot(tab, botValue, finishgame, tokens, width, height, the_pos)
    print(f"tour de jeu: {tour_jeu} | finishGame : {res}")

    return res


def peek(stack: StackPos_t) -> Pos_t:
    if not stack:
        return None  # Retourne None si la pile est vide
    return stack[-1]
