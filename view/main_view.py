## @file main_view.py
## This file is the main view of the program with all the widgets linked

"""

## @package view
## @file main_view.py
## @description The main view of the game
## @brief This file is the main view of the program with all the widgets linked
"""
from tkinter.colorchooser import askcolor

from .grid_functions import *
from .widgets_functions import *

# GLOBAL VARIABLES

## the game's board height
height: int = 6
## the game's board width
width: int = 6
## the number of tokens to win
nb_tokens: int = 4
## the level of the bot
level = 2
## the color of the bot on the game's board
bot_color = "crimson"
## the color of the human on the game's board
human_color = "gold"
## variable to keep track of the number of comeback trump used
comebacktrump: int = 0
## variable to keep track of the number of best position trump used
bestpositiontrump: int = 0
## variable to keep track of the number of reverse trump used
reversetrump: int = 0
## variable to keep track of who start first
radio_state: IntVar


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
    global radio_state

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
        0, 1, True, fill="goldenrod"
    )

    # the canvas that will contain the image of the game or a text if the
    # image is not found
    canvas: Canvas = Canvas(
        container_frame, width=220, height=210, highlightthickness=0, bg=PINK
    )
    canvas.grid(column=0, row=2, columnspan=2)
    # try to open the image of the game and display it on the canvas
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
        fill="light grey")

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
            fill=color)

    # the label that will be displayed to show the users options that they
    # can change for the game

    label_options: Label = define_label(container_frame,
                                        "Options",
                                        15, 0, 3,
                                        True, fill="goldenrod")

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
        global height
        width = width_var.get()
        height = width_var.get()

    # the function that will be called when the width's spinbox value will
    # change
    def change_value_tokens() -> None:
        nb_tokens_var.set(int(spinbox_nb_tokens.get()))
        global nb_tokens
        nb_tokens = nb_tokens_var.get()

    # the function that will be called when we click on a button color to
    # change the color of the bot or the human

    def colorChoose(btn: Button, player: str) -> None:
        global bot_color
        global human_color
        color_tuple = askcolor(title=f"Choose the color of the {player}")

        # Check if the user canceled the askcolor selection
        if color_tuple is not None and color_tuple[1] is not None:
            color: str = str(color_tuple[1])  # Get the color string
            if player == "Bot":
                bot_color = color
                btn_bot_color.config(bg=bot_color)
            else:
                human_color = color
                btn_human_color.config(bg=human_color)

    # the spinbox for the width and the label that will be displayed next to
    # the spinbox's width
    spinbox_width: Spinbox = define_spinbox(
        fst_frame, change_value_width,
        1, 9,
        0, 0, value_var=width_var
    )

    label_width: Label = define_label(fst_frame, "width",
                                      10, 1,
                                      0, False)

    # the second frame that will contain the spinbox for the height and the
    # label that will be displayed next to the spinbox's height
    scd_frame: Frame = define_frame(container_frame, 1, 5)
    spinbox_height: Spinbox = define_spinbox(
        scd_frame, change_value_width,
        1, 9, 0,
        0, value_var=width_var
    )

    label_height: Label = define_label(scd_frame,
                                       "height", 10, 1,
                                       0, False)

    # the third frame that will contain the spinbox for the level and the
    # label that will be displayed next to the spinbox's level
    trd_frame: Frame = define_frame(container_frame, 0, 6)
    spinbox_level: Spinbox = define_spinbox(
        trd_frame, change_value_level, 1,
        5, 0, 0, value_var=level_var
    )

    label_level: Label = define_label(trd_frame, "level",
                                      10, 1, 0,
                                      False)

    # the fourth frame that will contain the spinbox for the number of
    # tokens and the label that will be displayed next to the spinbox's number
    fth_frame: Frame = define_frame(container_frame, 1,
                                    6)
    spinbox_nb_tokens: Spinbox = define_spinbox(
        fth_frame, change_value_tokens, 1,
        9, 0, 0, value_var=nb_tokens_var
    )

    label_nb_tokens: Label = define_label(fth_frame, "tokens",
                                          10, 1,
                                          0, False)

    label_who_start: Label = define_label(
        container_frame, "who start first ?", 10, 0,
        7, True, fill="goldenrod"
    )
    radio_state = IntVar()
    radio_state.set(2)
    radio_bot: Radiobutton = define_radio(
        container_frame, change_radio_value, "Bot", radio_state,
        0, 0, 8
    )

    radio_random: Radiobutton = define_radio(
        container_frame, change_radio_value, "Random", radio_state,
        2, 0, 8
    )
    radio_random.grid(column=0, row=8, columnspan=2)

    radio_human: Radiobutton = define_radio(
        container_frame, change_radio_value, "Human", radio_state,
        1, 1, 8
    )

    # the frame that will contain the color of the bot(entry), the color of
    # the bot, and the button to change the color of the bot

    sth_frame: Frame = define_frame(container_frame, 0, 9,
                                    columnspan=True)

    sth_frame.config(pady=0)

    bot_color_frame: Frame = define_frame(sth_frame, 0, 0)
    bot_color_frame.config(pady=0)

    label_bot_color: Label = define_label(bot_color_frame, "Bot's color",
                                          10,
                                          0, 0,
                                          False)

    btn_bot_color = define_button(
        bot_color_frame,
        lambda: colorChoose(btn_bot_color, "Bot"),
        " ",
        1,
        0,
        width=3,
        bg=bot_color
    )

    # the frame that will contain the color of the human(entry), the color
    # of the human, and the button to change the color of the human
    human_color_frame: Frame = define_frame(sth_frame, 1, 0)
    human_color_frame.config(pady=0)

    label_human_color: Label = define_label(
        human_color_frame, "Human's color", 10,
        0, 0, False
    )

    btn_human_color = define_button(
        human_color_frame,
        lambda: colorChoose(btn_human_color, "Human"),
        " ",
        1,
        0,
        width=3,
        bg=human_color
    )

    # the button to quit the game
    quitBtn: Button = define_button(
        container_frame, lambda: window.quit(), "Quit", 0, 10,
        font_size=12,
    )
    # the button to see the help of the config page, helps about the options

    helpBtn: Button = define_button(
        container_frame, lambda: help_function(1), "Help",
        0, 10, True,
        font_size=12,
    )
    # the button to launch the game
    startBtn: Button = define_button(
        container_frame, lambda: define_game_play(window),
        "Start", 1, 10,
        font_size=12,
    )

    container_frame.config(pady=0)

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
        0,
        font_size=12,
    )
    # the button to get helps about the game
    help_btn = define_button(gamePlay, lambda: help_function(0),
                             "Help", 0, 0,
                             True, font_size=12, )

    # the button to quit the game
    quit_btn = define_button(gamePlay, lambda: window.quit(),
                             "Quit", 1, 0, font_size=12, )

    # the label to print the number of tokens to align in effort to win
    label_print_nb_tokens = define_label(
        gamePlay, f"Number of tokens to win:" f" {nb_tokens}",
        20, 0,
        1, True
    )

    # frame to print the bot's color
    color_of_the_bot_frame: Frame = define_frame(gamePlay, 0, 2)
    color_of_the_bot_frame.config(pady=10)
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
    canvas_bot_color.config(bg="#255369")

    # the circle that will be displayed on the canvas to show the bot's color
    circle = canvas_bot_color.create_oval(
        0, 0, CELL_SIZE, CELL_SIZE, outline=f"{bot_color}", fill=f"{bot_color}"
    )

    # frame to print the human's color

    color_of_the_human_frame: Frame = define_frame(gamePlay, 1, 2)
    color_of_the_human_frame.config(pady=10)
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
    canvas_human_color.config(bg="#255369")

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

    board_frame: LabelFrame = define_lb_frame(gamePlay, 0, 3, columnspan=True)
    board_frame.config(relief="sunken", highlightcolor="black",
                       bg="#F8E5B5")
    global radio_state
    # canvas to print the game's board
    grid_tab: Canvas = create_board(
        board_frame, width, height, CELL_SIZE, human_color, bot_color,
        tokens=nb_tokens, who_starts=radio_state.get(), depth=level
    )
    grid_tab.grid(row=0, column=0, columnspan=2, padx=10)

    # the trump 's frame
    # the frame that will contain all the trump's buttons and labels that will
    # show the number of times the trump has been used

    all_trumps_frame: Frame = define_frame(board_frame, 2, 0)
    all_trumps_frame.config(bg="#9cc7d6")
    all_trumps_frame.config(padx=20)

    label_all_trumps: Label = define_label(all_trumps_frame,
                                           "All trumps Card",
                                           15, 0,
                                           0, bg="#9cc7d6",
                                           columnspan=True)
    label_all_trumps.config(pady=5, fg="black")

    trump_comeback_frame: Frame = define_frame(all_trumps_frame, 0, 1,
                                               columnspan=False)

    trump_comeback_frame.config(bg="#9cc7d6", padx=10)

    trump_comeback_frame.grid_rowconfigure(0, minsize=10)

    # the section for the comeback Button

    come_back_btn: Button = define_button(
        trump_comeback_frame, lambda: increment_count("comeback"),
        "come back",
        0, 0,
        width=8,
        font_size=15,
        bg="#696464",
        color="white"
    )

    come_back_btn.config(padx=5)

    label_come_back_count: Label = define_label(trump_comeback_frame,
                                                "used: 0", 8,
                                                1, 0,
                                                True, bg="#9cc7d6",
                                                fill="crimson")
    label_come_back_count.config(padx=5)

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
            # print("Reverse the " "board")
            reverse_board(grid_tab, height, width, human_color, bot_color)

        elif string == "best":
            bestpositiontrump += 1
            label_best_pos_count.config(text=f"used: {bestpositiontrump}")
            # print("best Position " "launched")
            best_position_func(
                grid_tab, width, height, nb_tokens, human_color, bot_color,
                depth=level
            )

        else:
            comebacktrump += 1
            label_come_back_count.config(text=f"used: {comebacktrump}")
            # print("come back")
            come_back_func(grid_tab, human_color, bot_color, height)

    # the section for the reverse board's Button

    trump_reverse_board_frame: Frame = define_frame(all_trumps_frame, 0,
                                                    2,
                                                    columnspan=True)
    trump_reverse_board_frame.config(bg="#9cc7d6")

    btn_reverse_board: Button = define_button(
        trump_reverse_board_frame, lambda: increment_count("reverse"),
        "reverse board", 0, 0,
        width=10, anchor="w",
        font_size=15,
        bg="#696464",
        color="white"
    )

    btn_reverse_board.config(padx=5)

    label_reverse_board_count: Label = define_label(
        trump_reverse_board_frame, "used:0", 10, 1,
        0, False, bg="#9cc7d6",
        fill="crimson"
    )

    label_reverse_board_count.config(padx=5)

    # the section for the best Position Button

    trump_btn_pos_frame: Frame = define_frame(all_trumps_frame, 0, 3,
                                              columnspan=False)
    trump_btn_pos_frame.config(bg="#9cc7d6")

    btn_best_pos: Button = define_button(
        trump_btn_pos_frame, lambda: increment_count("best"),
        "best position", 0, 0,
        width=10,
        font_size=15,
        bg="#696464",
        color="white"
    )

    btn_best_pos.config(padx=5)

    label_best_pos_count: Label = define_label(trump_btn_pos_frame,
                                               "used:0", 10,
                                               1, 0,
                                               False, bg="#9cc7d6",
                                               fill="crimson")

    label_best_pos_count.config(padx=5)

    # the reset button to reset the game's board
    reset_btn = define_button(gamePlay, lambda: define_game_play(window),
                              "Reset", 1, 6, font_size=12, )

    return gamePlay


def help_function(number: int) -> None:
    """
    @brief This function display the help of the game
    :param number: the number of the help to display (0 for the game's rule
    and 1 for the game's configuration)
    :return: None
    """
    configuration_text = """\

    This page is where you configure the game, including settings such as \
board dimensions, player colors, starting player, and more.

    \t\t            Details:

    \b Board Dimensions:\nYou can adjust the width and height of the game
    board
    using the spinboxes. Note that they are LINKED, so changing one also \
changes the other to maintain a SQUARE board.

    \b Bot Difficulty LEVEL:\nChoose the bot's skill level. Higher levels
    result
    in a more challenging bot, but it may take more time to
    make moves (we recommend level LOWER THAN 4 for a good balance), for \
    a board of size over than 8.

    \b Tokens to Align (the spinbox's TOKENS):\nSet the number of tokens
    required for a player to win the game.

    \b Starting Player:\nFirst, select whether you or the bot will start the\
game using the radio buttons. \nYou can also customize the colors for each
player by clicking on the player's button and confirm the color choice
with the OK button.

    Finally, the three buttons at the bottom:

    \b Quit:\nUse this button to exit the game (close the program).

    \b Help:\nClick this button to access help on the configuration options.

    \b Start:\nLaunch the game with the current configuration settings.

    \t\t            Have fun !!!
    """

    game_rules_text = """\
    This page contains the game's description and rules:

    \t\t            Details:

    \b\bThe first three buttons:
    \b Return:\n Allows you to go back to the configuration page or the game \
settings.
    \b Help:\n Provides access to all the game's rule descriptions.
    \b Quit:\n Allows you to quit the game (close the program).

    Next, a reminder of the number of tokens required to align for a win \
(as previously set).

    \b\bPlayer Colors:\n
    Displays the colors of each player in the game, which you have set.

    \b\bGame Board:
    To play your token in a column, simply click on the desired column,\
and the token will be placed at the lowest available position. No need \
to click on individual cells to place your token.

    \b\bTrump Cards (on the right of the game board) :\n
    \b Comeback Trump:\n Allows you to revert to a previous turn.To return \
your turn, you'll need to click the button twice, as the first click takes \
you to the bot's turn.\n
    \b Reverse Board Trump:\n Reverses the entire game board.\n
    \b Best Position Trump:\n Places your token in the best available position\
based on the current state of the game.\n

    Finally, the Return button lets you reset the game, clearing the board of \
all tokens.

    \t        Have fun playing Our Connect 4++!
    """
    if number:

        messagebox.showinfo("Game settup help",
                            configuration_text)
    else:
        messagebox.showinfo("Game's rule", game_rules_text)
