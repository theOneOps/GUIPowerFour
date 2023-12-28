from type import *

humanValue = 1
botValue = 0


# Variables constantes
# ------------------------------- DEBUT principles types -------------------------------

# ------------------------------- DEBUT principles Functions -------------------------------


# vérifier si la position joué est valide ou pas ...
def valid_coord(x: int, y: int, width: int, height: int) -> bool:
    return ((x >= 0 and x < width) and (y >= 0 and y < height))


# vérifier si un quintuplet en horizontal(si nb_tokens == 5) est atteint
def finishRangeHorizontal(player: int, posx: int, posy: int, tab: Grid_t,
                          nb_tokens: int, width: int, height: int
                          ) -> bool:
    x = posx
    y = posy
    count = 0
    for i in range(x - nb_tokens - 1, x + nb_tokens):
        if valid_coord(i, y, width, height):
            if tab[i][y] == player:
                count += 1
            else:
                count = 0
        if count == nb_tokens:
            break
    return True if count == nb_tokens else False


# vérifier si un quintuplet en vertical(si nb_tokens == 5) est atteint
def finishRangeVertical(player: int, posx: int, posy: int, tab: Grid_t,
                        nb_tokens: int, width: int, height: int
                        ) -> bool:
    x = posx
    y = posy
    count = 0
    for i in range(y - nb_tokens - 1, y + nb_tokens):
        if valid_coord(i, y, width, height):
            if tab[i][y] == player:
                count += 1
            else:
                count = 0
        if count == nb_tokens:
            break
    return True if count == nb_tokens else False


# vérifier si un quintuplet dans le diagonale gauche(si nb_tokens == 5) est atteint
def finishRangeHautGauche(player: int, posx: int, posy: int, tab: Grid_t,
                          nb_tokens: int, width: int, height: int
                          ) -> (bool):
    x = posx
    y = posy - nb_tokens - 1
    count = 0
    for i in range(x - nb_tokens - 1, x + nb_tokens):
        if valid_coord(i, y, width, height):
            if tab[i][y] == player:
                count += 1
            else:
                count = 0
        if count == nb_tokens:
            break
        y += 1
    return True if count == nb_tokens else False


# vérifier si un quintuplet dans le diagonale droit(si nb_tokens == 5) est atteint
def finishRangeBasGauche(player: int, posx: int, posy: int, tab: Grid_t,
                         nb_tokens: int, width: int, height: int) -> (
        bool):
    x = posx
    y = posy + nb_tokens - 1
    count = 0
    for i in range(x - nb_tokens - 1, x + nb_tokens):
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
def finishRangeInAllDirections(player: int, x: int, y: int,
                               tab: Grid_t, token: int, width: int,
                               height: int) -> bool:
    return (finishRangeVertical(player, x, y, tab, token, width, height) or
            finishRangeHorizontal(player, x, y, tab, token, width, height) or
            finishRangeHautGauche(player, x, y, tab, token, width, height) or
            finishRangeBasGauche(player, x, y, tab, token, width, height))


# à faire...
# fonction permettant de vérifier si la case sur laquelle on veut jouer est valide en vérifiant la colonne de la case joué... si il y a encore de la place...
# def isColumnClickedValid(tab: Grid_t, thePosition: Pos_t) -> bool:
#     res: bool = False
#     # à faire
#     x = thePosition[0]
#
#     return res


# fonction à lancer lors du tour du joueur bot
def play_bot(tab: Grid_t, player: int, pile: StackPos_t, finishGame: bool,
             token: int, width: int, height: int, thePos: Pos_t) -> bool:
    # best_position: Pos_t = best_positionToPlay(tab, player)
    if finishRangeInAllDirections(player, thePos[0], thePos[1],
                                  tab, token, width, height):
        print("le joueur bot a gagné")
        finishGame = False
    return finishGame


# fonction à lancer lors du tour du joueur humain
def play_human(tab: Grid_t, player: int, thePosition: Pos_t,
               pile: StackPos_t, finishGame: bool, token: int, width: int,
               height: int) -> bool:
    if finishRangeInAllDirections(player, thePosition[0], thePosition[1],
                                  tab, token, width, height):
        print("le joueur humain a gagné")
        finishGame = False
    return finishGame


# fonction pour poser le token du joueur dont c'est le tour sur le board du jeu
# avec ajout de la position joué dans la pile

# à faire...
# fonction qui utilisera le min_max pour déterminer la meilleure position possible à jouer...
def best_positionToPlay(tab: Grid_t, player: int) -> Pos_t:
    position: Pos_t = {}
    # À faire... minmax
    return position


# Fonction principale qui fera avancer le jeu et qui appelera toutes les autres...
# def play(tab: Grid_t, tourJeu: int, pile: StackPos_t) -> None:
#     global finishGame
#     if tourJeu % 2 == 0:
#         play_bot(tab, botValue, pile)
#         tourJeu += 1
#     else:
#         thePosition: Pos_t = getPositionPlayHuman(tab)
#         play_human(tab, humanValue, thePosition, pile)
#         tourJeu += 1
#

def getRandomPosition(tab: Grid_t, height: int, width: int) -> Pos_t:
    position: Pos_t
    for i in range(height):
        for j in range(width):
            if tab[i][j] == -1:
                return [i, j]
    return None


# à faire...
# fonction pour récupérer la position joué par le joueur human depuis l'interface graphique

# à faire...
# fonction pour mettre à jour l'interface du jeu lorsqu'un joueur jouer

def launchGame(tab: Grid_t, width: int, height: int, tourJeu: int, tokens:
int, pile: StackPos_t, finishGame: bool, thePos: Pos_t) -> bool:
    res: bool = True

    if tourJeu % 2 == 0:
        res = play_human(tab, humanValue, thePos, pile, finishGame, tokens,
                         width,
                         height)
    else:
        res = play_bot(tab, botValue, pile, finishGame, tokens, width, height,
                       thePos)
    print(f"tour de jeu: {tourJeu} | finishGame : {res}")

    return res


def peek(stack: StackPos_t) -> Pos_t:
    if not stack:
        return None  # Retourne None si la pile est vide
    return stack[-1]
