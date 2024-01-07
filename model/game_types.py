## @file game_types.py
## This file contains the special types that are created
"""
@package model
@file game_types.py
@desc This file contains the special types that are created
and used in the game

"""

# -------------------- DEBUT principles variables ------------------

# variables fictifs juste pour pouvoir définir les prototypes voir contenus
# de mes fonctions...

# principles types

## type of each square of the grid
Pos_t = tuple(list[int, int])

## stack of Pos to be aware of every token put on the grid in time
StackPos_t = list[Pos_t]

## grid type is for the grid of the board
Grid_t = list[list[int]]
