from tkinter import *
from tkinter import messagebox

from model.core import *
from model.minmax import *

# globals' variables

tab: Grid_t
nbSquareFilled: int
tourJeu: int
stack: StackPos_t
finishG: bool
CELL_SIZE: int = 40

WINDOWWIDTH: int = 300
WINDOWHEIGHT: int = 530


def create_board(
        parent,
        width: int,
        height: int,
        cell_size: int,
        human_color: str,
        bot_color: str,
        tokens: int,
        padding: int = 5,  # Adjust this value for padding
) -> Canvas:
    global tab
    global stack
    global nbSquareFilled
    global tourJeu
    global finishG

    nbSquareFilled = 0
    tourJeu = 0
    finishG = True
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
        bg='blue',
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
            # If I click on a oval, it fill in
            # black or whatever color that I choose

            canvas.tag_bind(
                circle,
                "<Button-1>",
                lambda event, c=col: fill_cell(
                    canvas, c, human_color, bot_color, height, width, tokens
                ),
            )
            x += cell_size + padding
        x = 0
        y += cell_size + padding

    return canvas


def update_game_state(
        canvas: Canvas,
        col: int,
        player: int,
        color: str,
        width: int,
        height: int,
        tokens: int,
) -> None:
    global tab
    global nbSquareFilled
    global tourJeu
    global stack
    global finishG

    if finishG:
        if nbSquareFilled < height * width:
            for row in range(height - 1, -1, -1):
                if tab[row][col] == -1:
                    tab[row][col] = player
                    stack.append([row, col])
                    finishG = launch_game(
                        tab,
                        width,
                        height,
                        tour_jeu=tourJeu,
                        tokens=tokens,
                        finishgame=finishG,
                        the_pos=[row, col],
                    )
                    canvas.itemconfig(f"circle_{row}_{col}", fill=color)
                    nbSquareFilled += 1
                    if not finishG:
                        if player == 1:
                            messagebox.showinfo("victoire",
                                                "Vous avez gagné !")
                        else:
                            messagebox.showinfo("victoire",
                                                "Le bot a gagné !")
                        return
                    break
        else:
            messagebox.showinfo("match nul", "pas de gagnant")
            return


def fill_cell(
        canvas,
        col,
        human_color: str,
        bot_color: str,
        height: int,
        width: int,
        tokens: int,
) -> None:
    global tab
    global nbSquareFilled
    global tourJeu
    global stack
    global finishG

    if finishG:
        update_game_state(canvas, col, 1, human_color, width, height, tokens)
        tourJeu += 1
    else:
        messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
        return

    if tourJeu % 2 != 0:
        if finishG:
            position = get_random_position(tab, width, height)
            if position is not None:
                update_game_state(
                    canvas, position[1], 0, bot_color, width, height, tokens
                )
                tourJeu += 1


def come_back_func(canvas: Canvas) -> None:
    global stack
    global tourJeu
    global nbSquareFilled
    global finishG
    old_position: Pos_t = peek(stack)
    if old_position is not None:
        canvas.itemconfig(f"circle_{old_position[0]}_{old_position[1]}",
                          fill="white")
        tab[old_position[0]][old_position[1]] = -1
        stack.pop()
        tourJeu -= 1
        nbSquareFilled -= 1
        finishG = True


def best_position_func(
        canvas: Canvas,
        width: int,
        height: int,
        tokens: int,
        human_color: str,
        bot_color: str,
) -> None:
    global tab
    global nbSquareFilled
    global tourJeu
    global stack
    global finishG

    if finishG:
        update_game_state(
            canvas,
            get_random_position(tab, width, height)[1],
            1,
            human_color,
            width,
            height,
            tokens,
        )
        tourJeu += 1
    else:
        messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
        return

    if tourJeu % 2 != 0:
        if finishG:
            position = get_random_position(tab, width, height)
            if position is not None:
                update_game_state(
                    canvas, position[1], 0, bot_color, width, height, tokens
                )


def reverse_board(
        canvas: Canvas, height: int, width: int, humancolor: str, botcolor: str
) -> None:
    global stack
    global tab
    stack = refresh_stack_for_reversed_board(stack, height)
    tab = refresh_grid_for_reversed_board(tab, height)
    modify_board(canvas, height, width, humancolor, botcolor)


def refresh_grid_for_reversed_board(grid: Grid_t, height: int) -> Grid_t:
    grid = grid[::-1]
    reversed_grid = [[-1] * len(grid[0]) for _ in range(height)]

    for col in range(len(grid[0])):
        filled_row = height - 1
        for row in range(height - 1, -1, -1):
            if grid[row][col] != -1:
                reversed_grid[filled_row][col] = grid[row][col]
                filled_row -= 1

    return reversed_grid


def refresh_stack_for_reversed_board(pile: StackPos_t,
                                     height: int) -> StackPos_t:
    refreshed_stack = []
    for position in pile:
        row, col = position
        refreshed_row = height - 1 - row  # Calculate the new
        # row on the reversed board
        refreshed_stack.append([refreshed_row, col])
    return refreshed_stack


def modify_board(
        canvas: Canvas, height: int, width: int, human_color: str,
        bot_color: str
) -> None:
    global tab
    for row in range(height):
        for col in range(width):
            if tab[row][col] == -1:
                canvas.itemconfig(f"circle_{row}_{col}", fill="white")
            elif tab[row][col] == 1:
                canvas.itemconfig(f"circle_{row}_{col}", fill=f"{human_color}")
            else:
                canvas.itemconfig(f"circle_{row}_{col}", fill=f"{bot_color}")
