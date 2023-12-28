from tkinter import *
from tkinter import messagebox

from model.core import *

# globals' variables

tab: Grid_t
nbSquareFilled: int
tourJeu: int
stack: StackPos_t
finishG: bool

PINK: str = "#F8E5E5"
frameWidth: int = 100
frameHeight: int = 50
framePad: int = 10
CELL_SIZE = 40

WINDOWWIDTH: int = 300
WINDOWHEIGHT: int = 530


def defineSpinBox(frameparent: Frame, func, from_: int,
                  to: int, col: int, row: int, valueVar: IntVar, wrap_:
        bool = True) -> Spinbox:
    spin = Spinbox(frameparent, from_=from_, to=to, wrap=wrap_, width=5,
                   command=func, textvariable=valueVar)
    spin.grid(column=col, row=row)
    return spin


def defineFrame(root: Tk, col: int, row: int,
                h: int = frameHeight, w: int = frameWidth,
                pad: int = framePad, columnspan: bool = False) -> Frame:
    frame = Frame(root, height=h, width=w, bg=PINK)
    frame.config(padx=pad, pady=pad)

    if columnspan:
        frame.grid(column=col, row=row, columnspan=2)
    else:
        frame.grid(column=col, row=row)
    return frame


def defineLabel(parent, text: str, fontSize: int,
                col: int, row: int, columnspan: bool,
                fill: str = "black") -> Label:
    label = Label(parent, text=text, font=("arial", fontSize, "bold"), bg=PINK,
                  fg=fill)
    if columnspan:
        label.grid(column=col, row=row, columnspan=2)
    else:
        label.grid(column=col, row=row)
    return label


def defineEntry(parent, width: int, string: str,
                col: int, row: int, disable: bool = True) -> Entry:
    entry: Entry = Entry(parent, width=width)
    # if disable:
    #     entry.config(state="disabled")
    entry.insert(END, string=string)
    entry.grid(column=col, row=row)

    return entry


def defineRadio(parent, function, string: str, variable: IntVar,
                value: int, col: int, row: int) -> Radiobutton:
    radioBtn: Radiobutton = Radiobutton(parent, text=string, variable=variable,
                                        value=value,
                                        bg=PINK,
                                        command=lambda: function(variable))
    radioBtn.grid(column=col, row=row)
    return radioBtn


# function for the radioButton's function (This will change later)
def changeRadioValue(value: IntVar):
    print(value.get())


def defineButton(parent, function, string: str, col: int, row: int,
                 columnspan: bool = False, width: int = 5) -> Button:
    btn: Button = Button(parent, text=string, command=function, width=width)
    if columnspan:
        btn.grid(column=col, row=row, columnspan=2, pady=20)
    else:
        btn.grid(column=col, row=row, pady=20)
    return btn


def createBoard(parent, width: int, height: int, cell_size: int, humanColor:
str, botColor: str, tokens: int) -> (
        Canvas):
    global tab
    global stack
    global nbSquareFilled
    global tourJeu
    global finishG

    nbSquareFilled = 0
    tourJeu = 0
    finishG = True
    tab = [[-1 for _ in range(height)] for _ in range(width)]
    stack = []
    # Create circles and labels
    X = 0
    Y = 0
    canvas: Canvas = Canvas(parent, width=width * cell_size,
                            height=height * cell_size,
                            borderwidth=0, highlightthickness=0)

    for row in range(height):
        for col in range(width):
            x1 = X
            y1 = Y
            x2 = X + cell_size
            y2 = Y + cell_size

            circle = canvas.create_oval(x1, y1, x2, y2, outline="black",
                                        fill="white",
                                        tags=f"circle_{row}_{col}")
            # bind the circle with the fill's function so that If I click on a oval, it fill in
            # black or whatever color that I choose
            canvas.tag_bind(circle, "<Button-1>", lambda event, r=row,
                                                         c=col: fill_cell(
                canvas, r, c, humanColor, botColor,
                height, width, tokens))
            X += cell_size
        X = 0
        Y += cell_size

    return canvas


def update_game_state(canvas: Canvas, row: int, col: int, player: int,
                      color: str, width: int, height: int, tokens: int) -> None:
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
                    finishG = launchGame(tab, width, height, tourJeu=tourJeu,
                                         tokens=tokens, pile=stack,
                                         finishGame=finishG, thePos=[row, col])
                    canvas.itemconfig(f"circle_{row}_{col}", fill=color)
                    nbSquareFilled += 1
                    if not finishG:
                        if player == 1:
                            messagebox.showinfo("victoire", "Vous avez gagné !")
                        else:
                            messagebox.showinfo("victoire", "Le bot a gagné !")
                        return
                    break
        else:
            messagebox.showinfo("match nul", "pas de gagnant")
            return


def fill_cell(canvas, row, col, humanColor: str, botColor: str, height: int,
              width: int, tokens: int) -> None:
    global tab
    global nbSquareFilled
    global tourJeu
    global stack
    global finishG

    if finishG:
        update_game_state(canvas, row, col, 1, humanColor, width, height,
                          tokens)
        tourJeu += 1
    else:
        messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
        return

    if tourJeu % 2 != 0:
        if finishG:
            position = getRandomPosition(tab, width, height)
            if position is not None:
                update_game_state(canvas, position[0], position[1], 0, botColor,
                                  width, height, tokens)
                tourJeu += 1


def comeBackFunc(canvas: Canvas) -> None:
    global stack
    global tourJeu
    global nbSquareFilled
    global finishG
    oldPosition = peek(stack)
    if oldPosition is not None:
        canvas.itemconfig(f"circle_{oldPosition[0]}_{oldPosition[1]}",
                          fill="white")
        tab[oldPosition[0]][oldPosition[1]] = -1
        stack.pop()
        tourJeu -= 1
        nbSquareFilled -= 1
        finishG = True


def bestPositionFunc(canvas: Canvas, width: int, height: int, tokens: int,
                     humanColor: str, botColor: str) -> None:
    global tab
    global nbSquareFilled
    global tourJeu
    global stack
    global finishG

    if finishG:
        update_game_state(canvas, getRandomPosition(tab, width, height)[0],
                          getRandomPosition(tab, width, height)[1], 1,
                          humanColor, width, height, tokens)
        tourJeu += 1
    else:
        messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
        return


    if tourJeu % 2 != 0:
        if finishG:
            position = getRandomPosition(tab, width, height)
            if position is not None:
                update_game_state(canvas, position[0], position[1], 0, botColor,
                                  width, height, tokens)
            else:
                # Handle the case when getRandomPosition returns None
                print("Error: getRandomPosition returned None")

def reverseBoard(canvas: Canvas, height: int, width: int, humanColor: str,
                 botColor: str) -> None:
    global stack
    global tab
    stack = refresh_stack_for_reversed_board(stack, height)
    tab = refresh_grid_for_reversed_board(tab, height)
    tab = refresh_grid_for_reversed_boardSecond(tab,height)
    modifyBoard(canvas, height, width, humanColor,
                botColor)


def refresh_stack_for_reversed_board(pile: StackPos_t,
                                     height: int) -> StackPos_t:
    refreshed_stack = []
    for position in pile:
        row, col = position
        refreshed_row = height - 1 - row  # Calculate the new row on the reversed board
        refreshed_stack.append([refreshed_row, col])
    return refreshed_stack


def refresh_grid_for_reversed_board(grid: Grid_t, height:int) -> Grid_t:
    return grid[::-1]

def modifyBoard(canvas: Canvas, height: int, width: int, humanColor: str,
                botColor: str) -> None:
    global tab
    for row in range(height):
        for col in range(width):
            if tab[row][col] == -1:
                canvas.itemconfig(f"circle_{row}_{col}",
                                  fill="white")
            elif tab[row][col] == 1:
                canvas.itemconfig(f"circle_{row}_{col}",
                                  fill=f"{humanColor}")
            else:
                canvas.itemconfig(f"circle_{row}_{col}",
                               fill=f"{botColor}")

def refresh_grid_for_reversed_boardSecond(grid: Grid_t, height: int) -> Grid_t:
    reversed_grid = [[-1] * len(grid[0]) for _ in range(height)]

    for col in range(len(grid[0])):
        filled_row = height - 1
        for row in range(height - 1, -1, -1):
            if grid[row][col] != -1:
                reversed_grid[filled_row][col] = grid[row][col]
                filled_row -= 1

    return reversed_grid