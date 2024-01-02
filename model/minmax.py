from .type import Grid_t, Pos_t


# à faire...
# fonction qui utilisera le min_max pour déterminer
# la meilleure position possible à jouer...
# def best_position_to_play(tab: Grid_t, player: int) -> Pos_t:
#     position: Pos_t = {}
#     # À faire... minmax
#     return position
#


def get_random_position(tab: Grid_t, height: int,
                        width: int) -> Pos_t:
    for i in range(height):
        for j in range(width):
            if tab[i][j] == -1:
                return [i, j]
    return None
