## @file grid_functions.py
## This file contains all the functions that are used to create the
## grid and to fill it in and all trumps functions (come back, best position,
# reverse board)

"""!
@file grid_functions.py
@description This file contains all the functions that are used to create the
grid and to fill it in
@details This file contains all the functions that are used to play on the
board, and all trumps functions (come back, best position, reverse board)

"""

from tkinter import *
from tkinter import messagebox

from model.bot_logic import *
from model.game_logic import *

# globals' variables

## the grid variable : it's a 2D array that contains the value of each cell of
# the grid
tab: Grid_t
## the nbSquareFilled variable : it's an int that indicates the number of cell
# filled in the grid
nbSquareFilled: int
## the tourJeu variable : it's an int that indicates the number of turn to play
tourJeu: int
## the stack variable : it's a stack that contains all positions played during
# the game
stack: StackPos_t
## the finishG variable : it's a boolean that indicates if the game is over
# or not
finishG: bool

# constants variables

## the cell size : it's the size of each cell of the grid
CELL_SIZE: int = 40
## the window's width
WINDOWWIDTH: int = 300
## the window's height
WINDOWHEIGHT: int = 530


def vie_create_board(
        parent,
        width: int,
        height: int,
        cell_size: int,
        human_color: str,
        bot_color: str,
        tokens: int,
        who_starts: int,
        padding: int = 5,  # Adjust this value for padding
        depth: int = 4,
) -> Canvas:
    """!
    @brief Create a canvas with a grid of circles
    :param parent: the parent of the canvas
    :param width: the width of the board
    :param height: the height of the board
    :param cell_size: the size of each cell of the board
    :param human_color: the color of the human player
    :param bot_color: the color of the bot player
    :param tokens: the number of tokens to align to win
    :param padding: the padding of the board and for each cell of the board
    :param depth: the depth of the minimax algorithm
    :param who_starts: the first player to play
    :return: the canvas
    """
    global tab
    global stack
    global nbSquareFilled
    global tourJeu
    global finishG

    # we initialize all the global variables
    nbSquareFilled = 0
    tourJeu = 0
    finishG = True
    # Creation of the 2D array to store the circles
    tab = [[-1 for _ in range(width)] for _ in range(height)]
    stack = []

    x: int = 0
    y: int = 0
    canvas: Canvas = Canvas(
        parent,
        width=width * (cell_size + padding) + 2,
        height=height * (cell_size + padding) + 4,
        borderwidth=0,
        highlightthickness=0,
        bg='#8CB9BC',
    )

    for row in range(height):
        for col in range(width):
            x1 = x + padding
            y1 = y + padding
            x2 = x + cell_size + padding
            y2 = y + cell_size + padding

            circle = canvas.create_oval(
                x1,
                y1,
                x2,
                y2,
                outline="black",
                fill="white",
                tags=f"circle_{row}_{col}",
            )

            # bind the circle with the fill's function so that
            # If I click on a circle, it fills in
            # black or whatever color that the human chooses

            canvas.tag_bind(
                circle,
                "<Button-1>",
                lambda event, c=col: vie_fill_cell(
                    canvas, c, human_color, bot_color, height, width, tokens,
                    depth
                ),
            )
            x += cell_size + padding
        x = 0
        y += cell_size + padding

    # if who_starts == 2 at the beginning: then we need to pick
    # a random value to know who starts
    if who_starts == 2:
        # we pick a random value between 0 and 1
        rand_value: int = secrets.randbelow(2)
        # if the value is 0, then the bot starts
        if rand_value == 0:
            # we get the best position for the bot
            best_grid = mod_minimax(tab, depth, depth, BOTVALUE, 1,
                                    tokens, width, height, nbSquareFilled)
            pos = vie_get_the_best_position(best_grid[1], tab, BOTVALUE)
            # we check if the position is not None, because if it is None,
            # then it means that the board is full or there is a problem with
            # the minimax algorithm... so we need to stop the game
            if pos is not None:
                vie_update_game_state(
                    canvas, pos[1], 0, bot_color, width, height, tokens
                )

    # if the value is 0 at the beginning, then the bot starts
    elif who_starts == 0:
        # so, we will just call the minimax algorithm to get the best position
        # for the bot
        best_grid = mod_minimax(tab, depth, depth, BOTVALUE, 1, tokens,
                                width, height, nbSquareFilled)
        pos = vie_get_the_best_position(best_grid[1], tab, BOTVALUE)
        # and again, we just check to determine if the board is full or not
        # and if there is a problem with the minimax algorithm
        if pos is not None:
            vie_update_game_state(
                canvas, pos[1], 0, bot_color, width, height, tokens
            )

    return canvas


def vie_update_game_state(
        canvas: Canvas,
        col: int,
        player: int,
        color: str,
        width: int,
        height: int,
        tokens: int,
) -> None:
    """!
    @brief This function update the game state
    :param canvas: the canvas where the game is played on
    :param col: the column where the player has played
    :param player: variable for the player who plays | 1 for the human | 0 for
    the bot
    :param color: the color of the player
    :param width: the width of the board
    :param height: the height of the board
    :param tokens: the number of tokens to align to win
    :return: None
    """
    global tab
    global nbSquareFilled
    global tourJeu
    global stack
    global finishG

    # If the game is not over
    if finishG:
        # if there is still a place to play

        for row in range(height - 1, -1, -1):
            # if the cell is empty
            if tab[row][col] == -1:
                tab[row][col] = player
                # print(f"best_position joué : {[row, col]}")
                # add the position to the stack
                stack.append([row, col])
                # check if the game is over (if there is a winner)
                finishG = mod_launch_game(
                    tab,
                    width,
                    height,
                    tour_jeu=tourJeu,
                    tokens=tokens,
                    finishgame=finishG,
                    the_pos=[row, col],
                )
                # fill the cell with the color of the player
                canvas.itemconfig(f"circle_{row}_{col}", fill=color)
                # increment the number of cell filled
                nbSquareFilled += 1
                # if the game is over, and there is a winner
                if not finishG:
                    # if the player is the human
                    if player == 1:
                        messagebox.showinfo("victoire",
                                            "Vous avez gagné !")
                    else:
                        # the player is the bot
                        messagebox.showinfo("victoire",
                                            "Le bot a gagné !")
                    return
                break


def vie_fill_cell(
        canvas,
        col,
        human_color: str,
        bot_color: str,
        height: int,
        width: int,
        tokens: int,
        depth: int,
) -> None:
    """!
    @brief This function fill the cell
    :param canvas: the canvas where the game is played on
    :param col: the column where the player has played
    :param human_color: the color of the human player
    :param bot_color: the color of the bot player
    :param height: the height of the game's board
    :param width: the width of the game's board
    :param tokens: the number of tokens to align to win
    :param depth: the depth of the minimax algorithm
    :return: None
    """
    global tab
    global nbSquareFilled
    global tourJeu
    global stack
    global finishG

    # if the game is not over
    if finishG:
        # if there is not a place to play
        if nbSquareFilled == height * width:
            messagebox.showinfo("fin du jeu", "pas de gagnant, "
                                              "match nul")
            return

        # if there is still a place to play
        if tab[0][col] == -1:
            # update the game's board with the human's position
            vie_update_game_state(canvas, col, 1, human_color, width,
                                  height, tokens)
            tourJeu += 1
        else:
            return
    else:
        # if the game is already over
        pos: Pos_t = stack[-1]
        if pos is not None:
            if tab[pos[0]][pos[1]] == 1:
                messagebox.showinfo("fin du jeu",
                                    "vous avez déjà gagné !")
            else:
                messagebox.showinfo("fin du jeu",
                                    "le bot a déjà gagné !")
        # messagebox.showinfo("fin du jeu",
        #                     "on a déjà un gagnant !")
        return

    # if it's the bot's turn
    if tourJeu % 2 != 0:
        # if the game is not over
        if finishG:

            # get the best position for the bot

            # position = minimax_with_move(tab, depth, True,
            #                              BOTVALUE, height, width, tokens,
            #                              nbSquareFilled, stack)
            best_grid = mod_minimax(tab, depth, depth, BOTVALUE, 1,
                                    tokens, width, height, nbSquareFilled)
            position = vie_get_the_best_position(best_grid[1], tab, BOTVALUE)
            # print(f"best_grid calculé : \n{np.array(best_grid[1])}")
            # print(f"best_position calculé : {position}")
            # print(f"stack  :  {stack}")

            # print(f"score {position[0]} |position joué par le bot : "
            #       f" {position[1]}")
            # if the position is not None
            if position is not None:
                # actualize the game's board with the bot's position
                vie_update_game_state(
                    canvas, position[1], 0, bot_color, width, height,
                    tokens
                )
                # print(f"grid  :  {tab}")
                # increment the number of turn for the next player: the human
                tourJeu += 1


def vie_come_back_func(canvas: Canvas, human_color: str,
                       bot_color: str, height: int) -> None:
    """!
    @brief This function come back to the previous position
    :param canvas:  the canvas where the game is played on
    :param human_color: the color of the human player
    :param bot_color: the color of the bot player
    :param height: the height of the game's board
    :return: None
    """
    global stack
    global tab
    global tourJeu
    global nbSquareFilled
    global finishG
    # get the last position played
    old_position: Pos_t = mod_peek(stack)

    if old_position is not None:
        # we actualize the game's board by deleting the last position played
        canvas.itemconfig(f"circle_{old_position[0]}_{old_position[1]}",
                          fill="white")
        tab[old_position[0]][old_position[1]] = -1
        # we delete the last position played from the stack
        stack.pop()
        tourJeu -= 2
        # we decrement the number of cell filled
        nbSquareFilled -= 1
        # we actualize the game's state by setting the game's state to True
        # so that the game can continue even if the game was over
        finishG = True
        # we actualize the game's board (I mean the grid)

        # we push the values of the grid in the reversed grid at the bottom of
        # each column of the grid... hence the start at the bottom of the grid

        tab = vie_gravity_fall_func(tab, height)

        # we actualize the game's board based on the modified grid

        vie_modify_board(canvas, len(tab), len(tab[0]), human_color, bot_color)


def vie_best_position_func(
        canvas: Canvas,
        width: int,
        height: int,
        tokens: int,
        human_color: str,
        bot_color: str,
        depth: int,
) -> None:
    """!
    @brief This function get the best position for the bot
    :param canvas: the canvas where the game is played on
    :param width: the width of the game's board
    :param height: the height of the game's board
    :param tokens: the number of tokens to align to win
    :param human_color: the color of the human player
    :param bot_color: the color of the bot player
    :param depth: the depth of the minimax algorithm
    :return: None
    """
    global tab
    global nbSquareFilled
    global tourJeu
    global stack
    global finishG

    if finishG:
        if nbSquareFilled == height * width:
            messagebox.showinfo("fin du jeu", "pas de gagnant, "
                                              "match nul")
            return

        best_grid = mod_minimax(tab, depth, depth, HUMANVALUE, 1,
                                tokens, width, height, nbSquareFilled)
        # print(f"la grille de la best position : {best_grid[1]}")
        pos = vie_get_the_best_position(best_grid[1], tab, HUMANVALUE)
        if pos is not None:
            # update the game's board with the best position for the human
            vie_update_game_state(
                canvas,
                pos[1],
                1,
                human_color,
                width,
                height,
                tokens,
            )
            tourJeu += 1
    else:
        pos: Pos_t = stack[-1]
        if pos is not None:
            if tab[pos[0]][pos[1]] == 1:
                messagebox.showinfo("fin du jeu",
                                    "vous avez déjà gagné !")
            else:
                messagebox.showinfo("fin du jeu",
                                    "le bot a déjà gagné !")
        # messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
        return

    # the bot's turn
    if finishG:
        if nbSquareFilled < height * width:

            best_grid = mod_minimax(tab, depth, depth, BOTVALUE,
                                    1, tokens,
                                    width, height, nbSquareFilled)
            pos = vie_get_the_best_position(best_grid[1], tab, BOTVALUE)
            if pos is not None:
                vie_update_game_state(
                    canvas, pos[1], 0, bot_color, width, height, tokens
                )
            tourJeu += 1


def vie_reverse_board(
        canvas: Canvas, height: int, width: int, humancolor: str, botcolor: str
) -> None:
    """!
    @brief This function reverse the board
    :param canvas: the canvas where the game is played on
    :param height: the height of the game's board
    :param width: the width of the game's board
    :param humancolor: the color of the human player
    :param botcolor: the color of the bot player
    :return: None
    """
    global stack
    global tab
    # we reverse the stack
    stack = vie_refresh_stack_for_reversed_board(stack, height)
    # we reverse the grid
    tab = vie_refresh_grid_for_reversed_board(tab, height)
    # we actualize the game's board based on the reversed grid
    vie_modify_board(canvas, height, width, humancolor, botcolor)


def vie_refresh_grid_for_reversed_board(grid: Grid_t, height: int) -> Grid_t:
    """!
    @brief This function refresh the grid for the reversed board
    :param grid: the grid to refresh
    :param height: the height of the game's board
    :return: the reversed grid
    """
    grid = grid[::-1]

    # We call the gravity_fall_func function to push the values in the bottom,
    # like we were applying a gravity on the grid

    reversed_grid = vie_gravity_fall_func(grid, height)

    return reversed_grid


def vie_refresh_stack_for_reversed_board(pile: StackPos_t,
                                         height: int) -> StackPos_t:
    """!
    @brief This function refresh the stack for the reversed board
    :param pile: the stack to refresh
    :param height: the height of the game's board
    :return: the reversed stack
    """
    # we create a new stack that will be the reversed stack
    refreshed_stack = []
    for position in pile:
        row, col = position
        refreshed_row = height - 1 - row  # Calculate the new
        # row on the reversed board
        refreshed_stack.append([refreshed_row, col])
    return refreshed_stack


def vie_modify_board(
        canvas: Canvas, height: int, width: int, human_color: str,
        bot_color: str
) -> None:
    """!
    @brief This function modify the game's board
    :param canvas: the canvas where the game is played on
    :param height: the height of the game's board
    :param width: the width of the game's board
    :param human_color: the color of the human player
    :param bot_color: the color of the bot player
    :return: None
    """
    global tab
    for row in range(height):
        for col in range(width):
            if tab[row][col] == -1:
                canvas.itemconfig(f"circle_{row}_{col}",
                                  fill="white")
            elif tab[row][col] == 1:
                canvas.itemconfig(f"circle_{row}_{col}",
                                  fill=f"{human_color}")
            else:
                canvas.itemconfig(f"circle_{row}_{col}",
                                  fill=f"{bot_color}")


def vie_get_the_best_position(best_board: Grid_t, board: Grid_t,
                              player: int) -> Pos_t:
    """!
    @brief This function get the best position for the bot
    :param best_board: the board that contains the current game's state with
    the best position possible for the player
    :param board: the current game's state
    :param player: the player we want to get the best position for
    :return: the best position for the player
    """
    for row in range(len(best_board)):
        for col in range(len(best_board[row])):
            ## we check if the value of the best board is different from the
            # value of the board

            if best_board[row][col] != board[row][col]:
                # if the value of the best board is equal to the player
                if best_board[row][col] == player:
                    # then we have found the best position for the player,
                    # so we return it
                    return [row, col]


def vie_gravity_fall_func(old_grid: Grid_t, height: int) -> Grid_t:
    """!
    @brief This function apply a gravity on the grid
    :param old_grid: the grid to apply the gravity on
    :param height: the height of the game's board
    :return: the grid with the gravity applied on
    """
    # we create a new grid that will be the reversed grid
    reversed_grid = [[-1] * len(old_grid[0]) for _ in range(height)]

    # we push the values of the grid in the reversed grid at the bottom of
    # each column of the grid... hence the start at the bottom of the grid

    for col in range(len(old_grid[0])):
        filled_row = height - 1
        for row in range(height - 1, -1, -1):
            if old_grid[row][col] != -1:
                reversed_grid[filled_row][col] = old_grid[row][col]
                filled_row -= 1

    return reversed_grid
