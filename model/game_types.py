# -------------------- DEBUT principles variables ------------------

# variables fictifs juste pour pouvoir définir les prototypes voir contenus
# de mes fonctions...

# principles types

# type of each square of the grid
Pos_t = tuple(list[int, int])

# stack of Pos to be aware of every token put on the grid in time
StackPos_t = list[Pos_t]

# grid type is for the grid of the board
Grid_t = list[list[int]]

# the dictionary would be use for trump
# so for each trump(key), we will have acess to number of times it has been
# use by a player (user or bot)
# Trump_t = {str: int}
