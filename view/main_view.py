## @file main_view.py
## This file is the main view of the program with all the widgets linked

"""

## @package view
## @file main_view.py
## @description The main view of the game
## @brief This file is the main view of the program with all the widgets linked
"""
from tkinter.colorchooser import askcolor

from PIL import Image, ImageTk

from .grid_functions import *
from .widgets_functions import *

# GLOBAL VARIABLES

## the game's board height
height: int = 6
## the game's board width
width: int = 6
## the number of tokens to win
nb_tokens: int = 6
## the level of the bot
level = 2
## the color of the bot on the game's board
bot_color = "red"
## the color of the human on the game's board
human_color = "yellow"
## variable to keep track of the number of comeback trump used
comebacktrump: int = 0
## variable to keep track of the number of best position trump used
bestpositiontrump: int = 0
## variable to keep track of the number of reverse trump used
reversetrump: int = 0


def init_config_frame(window) -> Frame:
    """
    @brief This function initialize create the first page of the game, the
    configuration page
    :param window:  the window where the frame will be displayed
    :return: a frame with all the widgets needed
    """

    # destroy all the widgets of the window
    for widget in window.winfo_children():
        widget.destroy()

    global width
    global height
    global nb_tokens
    global level

    # the main frame that will contain all the widgets of the page
    container_frame: Frame = define_frame(window, 0, 0, WINDOWWIDTH,
                                          WINDOWHEIGHT)
    # this widget is used to initialize the grid property for the rest
    # of the widgets
    nothing = Label(container_frame, text="", bg=PINK)
    nothing.grid(column=0, row=0)

    # the title of the game
    label_title: Label = define_label(
        container_frame, "Welcome dear User !", 15,
        0, 1, True
    )

    # the canvas that will contain the image of the game or a text if the
    # image is not found
    canvas: Canvas = Canvas(
        container_frame, width=220, height=210, highlightthickness=0, bg=PINK
    )
    canvas.grid(column=0, row=2, columnspan=2)
    # try to open the image of the game and display it on the canvas
    try:
        power_image = Image.open("../Images/power.png")
        power_image_canvas = ImageTk.PhotoImage(power_image)
        canvas.create_image(110, 110, image=power_image_canvas)
        canvas.grid(column=0, row=2, columnspan=2)
        # canvas.config(bg="black")

    # if the image is not found, display a text on the canvas

    except Exception as e:
        print(f"We got a problem : {e}")
        # Display colored text on the canvas with a border
        text = "Power Po\nPower Pow\nPower Power\nPower 4++"

        # Border attributes
        border_width = 2.
        border_relief = "solid"

        # Create a rectangle to serve as the border
        canvas.create_rectangle(
            border_width,
            border_width,
            canvas.winfo_reqwidth() - border_width,
            canvas.winfo_reqheight() - border_width,
            outline="black",
            width=border_width,
            fill="light grey"
        )

        # Create colored text lines on the canvas
        lines = text.split("\n")
        line_height = canvas.winfo_reqheight() // len(lines)

        for i, line in enumerate(lines):
            y_position = i * line_height + line_height // 2
            color = "gray" if i % 2 == 0 else "blue"
            # Change color based on line index
            canvas.create_text(
                canvas.winfo_reqwidth() // 2,
                y_position,
                text=line,
                font=("Helvetica", 12 + 6 * i),
                anchor="center",
                fill=color
            )

    # the label that will be displayed to show the users options that they
    # can change for the game

    label_options: Label = define_label(container_frame,
                                        "Options",
                                        15, 0, 3,
                                        True)

    # the frame that will contain the spinbox for the width
    fst_frame: Frame = define_frame(container_frame, 0, 5)

    # initialization of the spinboxes' values
    width_var: IntVar = IntVar()
    height_var: IntVar = IntVar()
    nb_tokens_var: IntVar = IntVar()
    level_var: IntVar = IntVar()

    # set the spinboxes their corresponding values
    width_var.set(width)
    height_var.set(height)
    nb_tokens_var.set(nb_tokens)
    level_var.set(level)

    # the function that will be called when the height's spinbox value will
    # change
    def change_value_height() -> None:
        """
        @brief This function will be called when the height's spinbox value
        :return:None
        """
        height_var.set(int(spinbox_height.get()))
        global height
        height = height_var.get()

    # the function that will be called when the level's spinbox value will
    # change
    def change_value_level() -> None:
        """
        @brief This function will be called when the level's spinbox value
        :return:
        """
        level_var.set(int(spinbox_level.get()))
        global level
        level = level_var.get()

    # the function that will be called when the width's spinbox value will
    # change
    def change_value_width() -> None:
        """
        @brief This function will be called when the width's spinbox value
        :return: None
        """
        width_var.set(int(spinbox_width.get()))
        global width
        width = width_var.get()

    # the function that will be called when the width's spinbox value will
    # change
    def change_value_tokens() -> None:
        nb_tokens_var.set(int(spinbox_nb_tokens.get()))
        global nb_tokens
        nb_tokens = nb_tokens_var.get()

    # the function that will be called when we click on a button color to
    # change the color of the bot or the human

    def colorChoose(entry: Entry, player: str) -> None:
        global bot_color
        global human_color
        color_tuple = askcolor(title=f"Choose the color of the {player}")

        entry.delete(0, "end")
        if color_tuple is None:  # Check if the user canceled the askcolor
            # the color selection
            if player == "Bot":
                entry.insert(0, bot_color)
                entry.config(bg=bot_color)
            else:
                entry.insert(0, human_color)
                entry.config(bg=human_color)
        else:
            color = str(color_tuple[1])  # Get the color string
            entry.insert(0, str(color))
            entry.config(bg=str(color))
            if player == "Bot":
                bot_color = str(color)
            else:
                human_color = str(color)

    # the spinbox for the width and the label that will be displayed next to
    # the spinbox's width
    spinbox_width: Spinbox = define_spinbox(
        fst_frame, change_value_width,
        0, 10,
        0, 0, value_var=width_var
    )

    label_width: Label = define_label(fst_frame, "width",
                                      10, 1,
                                      0, False)

    # the second frame that will contain the spinbox for the height and the
    # label that will be displayed next to the spinbox's height
    scd_frame: Frame = define_frame(container_frame, 1, 5)
    spinbox_height: Spinbox = define_spinbox(
        scd_frame, change_value_height,
        0, 10, 10,
        0, value_var=height_var
    )

    label_height: Label = define_label(scd_frame,
                                       "height", 10, 1,
                                       0, False)

    # the third frame that will contain the spinbox for the level and the
    # label that will be displayed next to the spinbox's level
    trd_frame: Frame = define_frame(container_frame, 0, 6)
    spinbox_level: Spinbox = define_spinbox(
        trd_frame, change_value_level, 0,
        10, 0, 0, value_var=level_var
    )

    label_level: Label = define_label(trd_frame, "level",
                                      10, 1, 0,
                                      False)

    # the fourth frame that will contain the spinbox for the number of
    # tokens and the label that will be displayed next to the spinbox's number
    fth_frame: Frame = define_frame(container_frame, 1,
                                    6)
    spinbox_nb_tokens: Spinbox = define_spinbox(
        fth_frame, change_value_tokens, 0,
        10, 0, 0, value_var=nb_tokens_var
    )

    label_nb_tokens: Label = define_label(fth_frame, "tokens",
                                          10, 1,
                                          0, False)

    label_who_start: Label = define_label(
        container_frame, "who start first ?", 10, 0,
        7, True, fill="red"
    )
    radio_state: IntVar = IntVar()
    radio_bot: Radiobutton = define_radio(
        container_frame, change_radio_value, "Bot", radio_state,
        0, 0, 8
    )
    radio_human: Radiobutton = define_radio(
        container_frame, change_radio_value, "Human", radio_state,
        1, 1, 8
    )

    # the frame that will contain the color of the bot(entry), the color of
    # the bot, and the button to change the color of the bot

    sth_frame: Frame = define_frame(container_frame, 0, 9)

    label_bot_color: Label = define_label(sth_frame, "Bot's color",
                                          10,
                                          0, 0,
                                          False)

    entry_bot_color: Entry = define_entry(sth_frame, 8,
                                          f"{bot_color}",
                                          1, 0)
    entry_bot_color.config(bg=bot_color)

    btn_bot_color = define_button(
        sth_frame,
        lambda entry=entry_bot_color, player="Bot": colorChoose(entry, player),
        "Bot color",
        0,
        1,
        width=10,
        columnspan=True,
    )

    # the frame that will contain the color of the human(entry), the color
    # of the human, and the button to change the color of the human
    sevth_frame: Frame = define_frame(container_frame, 1, 9)

    label_human_color: Label = define_label(
        sevth_frame, "Human's color", 10,
        0, 0, False
    )
    entry_human_color: Entry = define_entry(sevth_frame, 8,
                                            f"{human_color}", 1,
                                            0)

    entry_human_color.config(bg=human_color)
    btn_human_color = define_button(
        sevth_frame,
        lambda entry=entry_human_color, player="Human": colorChoose(entry,
                                                                    player),
        "Human color",
        0,
        1,
        width=10,
        columnspan=True,
    )

    # the button to quit the game
    quitBtn: Button = define_button(
        container_frame, lambda: window.quit(), "Quit", 0, 10
    )
    # the button to see the help of the config page, helps about the options

    helpBtn: Button = define_button(
        container_frame, lambda: print("Help"), "Help",
        0, 10, True
    )
    # the button to launch the game
    startBtn: Button = define_button(
        container_frame, lambda: define_game_play(window),
        "Start", 1, 10
    )

    return container_frame


# SECOND PAGE
def define_game_play(window) -> Frame:
    """
    @brief This function initialize create the second page of the game, the
    game's page, with the game's board, the trump's buttons and others widgets

    :param window: the window where the frame will be displayed
    :return: the frame with all the widgets needed
    """
    global comebacktrump
    global bestpositiontrump
    global reversetrump

    comebacktrump = 0
    bestpositiontrump = 0
    reversetrump = 0

    # destroy all the widgets of the window
    for widget in window.winfo_children():
        widget.destroy()

    # the main frame that will contain all the widgets of the page
    gamePlay: Frame = define_frame(window, 0, 0,
                                   WINDOWHEIGHT, WINDOWWIDTH, 10)

    # the button to return to the config page
    return_btn = define_button(
        gamePlay, lambda: init_config_frame(window),
        "Return", 0,
        0
    )
    # the button to get helps about the game
    help_btn = define_button(gamePlay, lambda: print("Help"),
                             "Help", 0, 0,
                             True)

    # the button to quit the game
    quit_btn = define_button(gamePlay, lambda: window.quit(),
                             "Quit", 1, 0)

    # the label to print the number of tokens to align in effort to win
    label_print_nb_tokens = define_label(
        gamePlay, f"Number of tokens to win:" f" {nb_tokens}",
        20, 0,
        1, True
    )

    # frame to print the bot's color
    color_of_the_bot_frame: Frame = define_frame(gamePlay, 0, 2)
    label_color_bot = define_label(
        color_of_the_bot_frame, "Bot's color  ",
        10, 0,
        0, False
    )
    # the canvas that will show the bot's color
    canvas_bot_color: Canvas = Canvas(
        color_of_the_bot_frame,
        width=CELL_SIZE,
        height=CELL_SIZE,
        borderwidth=0,
        highlightthickness=0,
    )
    canvas_bot_color.grid(row=0, column=1)

    # the circle that will be displayed on the canvas to show the bot's color
    circle = canvas_bot_color.create_oval(
        0, 0, CELL_SIZE, CELL_SIZE, outline=f"{bot_color}", fill=f"{bot_color}"
    )

    # frame to print the human's color

    color_of_the_human_frame: Frame = define_frame(gamePlay, 1, 2)
    label_color_human = define_label(
        color_of_the_human_frame, "Human's color  ", 10,
        0, 0, False
    )
    # the canvas that will show the human's color
    canvas_human_color: Canvas = Canvas(
        color_of_the_human_frame,
        width=CELL_SIZE,
        height=CELL_SIZE,
        borderwidth=0,
        highlightthickness=0,
    )
    canvas_human_color.grid(row=0, column=1)

    # the circle that will be displayed on the canvas to show the human's color
    circle = canvas_human_color.create_oval(
        0, 0, CELL_SIZE, CELL_SIZE, outline=f"{human_color}",
        fill=f"{human_color}"
    )

    print(f"bot's color ! {bot_color}\n")
    print(f"human's color ! {human_color}\n")

    # label to print who's turn it is...

    print(f"WIDTH is : {width}\n")

    print(f"HEIGHT is : {height}\n")

    # canvas to print the game's board
    grid_tab: Canvas = create_board(
        gamePlay, width, height, CELL_SIZE, human_color, bot_color,
        tokens=nb_tokens, depth=level
    )
    grid_tab.grid(row=3, column=0, columnspan=2)

    label_all_trumps: Label = define_label(gamePlay,
                                           "All trumps Card",
                                           15, 0,
                                           4, True)
    label_all_trumps.config(pady=5)

    # the trump 's frame
    # the frame that will contain all the trump's buttons and labels that will
    # show the number of times the trump has been used

    trump_comeback_frame: Frame = define_frame(gamePlay, 0, 5,
                                               columnspan=False)

    # the section for the comeback Button

    come_back_btn: Button = define_button(
        trump_comeback_frame, lambda: increment_count("comeback"),
        "come back",
        0, 0,
        width=11, anchor="w"
    )

    label_come_back_count: Label = define_label(trump_comeback_frame,
                                                "used:0", 10,
                                                0, 1,
                                                False)

    def increment_count(string: str) -> None:
        """
        @brief This function increment the number of times a trump has been
        :param string: the name of the trump
        :return: None
        """
        global reversetrump
        global comebacktrump
        global bestpositiontrump

        if string == "reverse":
            reversetrump += 1
            label_reverse_board_count.config(text=f"used: {reversetrump}")
            print("Reverse the " "board")
            reverse_board(grid_tab, height, width, human_color, bot_color)

        elif string == "best":
            bestpositiontrump += 1
            label_best_pos_count.config(text=f"used: {bestpositiontrump}")
            print("best Position " "launched")
            best_position_func(
                grid_tab, width, height, nb_tokens, human_color, bot_color,
                depth=level
            )

        else:
            comebacktrump += 1
            label_come_back_count.config(text=f"used: {comebacktrump}")
            print("come back")
            come_back_func(grid_tab, human_color, bot_color, height)

    # the section for the reverse board's Button

    trump_reverse_board_frame: Frame = define_frame(gamePlay, 0, 5,
                                                    columnspan=True)

    btn_reverse_board: Button = define_button(
        trump_reverse_board_frame, lambda: increment_count("reverse"),
        "reverse board", 0, 0,
        width=14, anchor="w"
    )

    label_reverse_board_count: Label = define_label(
        trump_reverse_board_frame, "used:0", 10, 0,
        1, False
    )

    # the section for the best Position Button

    trump_btn_pos_frame: Frame = define_frame(gamePlay, 1, 5,
                                              columnspan=False)

    btn_best_pos: Button = define_button(
        trump_btn_pos_frame, lambda: increment_count("best"),
        "best position", 0, 0,
        width=12
    )

    label_best_pos_count: Label = define_label(trump_btn_pos_frame,
                                               "used:0", 10,
                                               0, 1,
                                               False)

    # the reset button to reset the game's board
    reset_btn = define_button(gamePlay, lambda: define_game_play(window),
                              "Reset", 1, 6)

    return gamePlay
