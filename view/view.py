from tkinter.colorchooser import askcolor

from PIL import Image, ImageTk

from .grid_view import *
from .widgets_utils import *

height: int = 5
width: int = 5
nb_tokens: int = 5
level = 1
BOT_COLOR = "red"
HUMAN_COLOR = "yellow"
ComeBackTrump: int = 0
BestPositionTrump: int = 0
ReverseTrump: int = 0


def init_config_frame(window) -> Frame:
    for widget in window.winfo_children():
        widget.destroy()

    global width
    global height
    global nb_tokens
    global level

    container_frame: Frame = define_frame(window, 0, 0, WINDOWWIDTH,
                                          WINDOWHEIGHT)
    nothing = Label(container_frame, text="", bg=PINK)
    nothing.grid(column=0, row=0)
    label_title: Label = define_label(
        container_frame, "Welcome dear User !", 15,
        0, 1, True
    )
    canvas: Canvas = Canvas(
        container_frame, width=220, height=210, highlightthickness=0, bg=PINK
    )
    canvas.grid(column=0, row=2, columnspan=2)

    try:
        power_image = Image.open("../Images/power.png")
        power_image_canvas = ImageTk.PhotoImage(power_image)
        canvas.create_image(110, 110, image=power_image_canvas)
        canvas.grid(column=0, row=2, columnspan=2)
        # canvas.config(bg="black")
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

    label_options: Label = define_label(container_frame,
                                        "Options",
                                        15, 0, 3,
                                        True)

    fst_frame: Frame = define_frame(container_frame, 0, 5)

    width_var: IntVar = IntVar()
    height_var: IntVar = IntVar()
    nb_tokens_var: IntVar = IntVar()
    level_var: IntVar = IntVar()

    width_var.set(width)
    height_var.set(height)
    nb_tokens_var.set(nb_tokens)
    level_var.set(level)

    def change_value_height():
        height_var.set(int(spinbox_height.get()))
        global height
        height = height_var.get()

    def change_value_level():
        level_var.set(int(spinbox_level.get()))
        global level
        level = level_var.get()

    def change_value_width():
        width_var.set(int(spinbox_width.get()))
        global width
        width = width_var.get()

    def change_value_tokens():
        nb_tokens_var.set(int(spinbox_nb_tokens.get()))
        global nb_tokens
        nb_tokens = nb_tokens_var.get()

    def colorChoose(entry: Entry, player: str) -> None:
        global BOT_COLOR
        global HUMAN_COLOR
        color_tuple = askcolor(title=f"Choose the color of the {player}")

        entry.delete(0, "end")
        if color_tuple is None:  # Check if the user canceled
            # the color selection
            if player == "Bot":
                entry.insert(0, BOT_COLOR)
                entry.config(bg=BOT_COLOR)
            else:
                entry.insert(0, HUMAN_COLOR)
                entry.config(bg=HUMAN_COLOR)
        else:
            color = str(color_tuple[1])  # Get the color string
            entry.insert(0, str(color))
            entry.config(bg=str(color))
            if player == "Bot":
                BOT_COLOR = str(color)
            else:
                HUMAN_COLOR = str(color)

    spinbox_width: Spinbox = define_spinbox(
        fst_frame, change_value_width,
        0, 10,
        0, 0, value_var=width_var
    )
    label_width: Label = define_label(fst_frame, "width",
                                      10, 1,
                                      0, False)

    scd_frame: Frame = define_frame(container_frame, 1, 5)
    spinbox_height: Spinbox = define_spinbox(
        scd_frame, change_value_height,
        0, 10, 10,
        0, value_var=height_var
    )
    label_height: Label = define_label(scd_frame,
                                       "height", 10, 1,
                                       0, False)

    trd_frame: Frame = define_frame(container_frame, 0, 6)
    spinbox_level: Spinbox = define_spinbox(
        trd_frame, change_value_level, 0,
        10, 0, 0, value_var=level_var
    )
    label_level: Label = define_label(trd_frame, "level",
                                      10, 1, 0,
                                      False)

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

    sth_frame: Frame = define_frame(container_frame, 0, 9)
    label_bot_color: Label = define_label(sth_frame, "Bot's color",
                                          10,
                                          0, 0,
                                          False)
    entry_bot_color: Entry = define_entry(sth_frame, 8,
                                          f"{BOT_COLOR}",
                                          1, 0)
    entry_bot_color.config(bg=BOT_COLOR)
    btn_bot_color = define_button(
        sth_frame,
        lambda entry=entry_bot_color, player="Bot": colorChoose(entry, player),
        "Bot color",
        0,
        1,
        width=10,
        columnspan=True,
    )

    sevth_frame: Frame = define_frame(container_frame, 1, 9)
    label_human_color: Label = define_label(
        sevth_frame, "Human's color", 10,
        0, 0, False
    )
    entry_human_color: Entry = define_entry(sevth_frame, 8,
                                            f"{HUMAN_COLOR}", 1,
                                            0)
    entry_human_color.config(bg=HUMAN_COLOR)
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

    quitBtn: Button = define_button(
        container_frame, lambda: window.quit(), "Quit", 0, 10
    )
    helpBtn: Button = define_button(
        container_frame, lambda: print("Help"), "Help",
        0, 10, True
    )
    startBtn: Button = define_button(
        container_frame, lambda: define_game_play(window),
        "Start", 1, 10
    )

    return container_frame


# SECOND PAGE
def define_game_play(window) -> Frame:
    # need to change the widget's positions
    global ComeBackTrump
    global BestPositionTrump
    global ReverseTrump

    ComeBackTrump = 0
    BestPositionTrump = 0
    ReverseTrump = 0

    for widget in window.winfo_children():
        widget.destroy()

    gamePlay: Frame = define_frame(window, 0, 0,
                                   WINDOWHEIGHT, WINDOWWIDTH, 10)
    return_btn = define_button(
        gamePlay, lambda: init_config_frame(window),
        "Return", 0,
        0
    )
    help_btn = define_button(gamePlay, lambda: print("Help"),
                             "Help", 0, 0,
                             True)
    quit_btn = define_button(gamePlay, lambda: window.quit(),
                             "Quit", 1, 0)

    # number of tokens to win (label)

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
    canvas_bot_color: Canvas = Canvas(
        color_of_the_bot_frame,
        width=CELL_SIZE,
        height=CELL_SIZE,
        borderwidth=0,
        highlightthickness=0,
    )
    canvas_bot_color.grid(row=0, column=1)

    circle = canvas_bot_color.create_oval(
        0, 0, CELL_SIZE, CELL_SIZE, outline=f"{BOT_COLOR}", fill=f"{BOT_COLOR}"
    )

    # frame to print the human's color

    color_of_the_human_frame: Frame = define_frame(gamePlay, 1, 2)
    label_color_human = define_label(
        color_of_the_human_frame, "Human's color  ", 10,
        0, 0, False
    )
    canvas_human_color: Canvas = Canvas(
        color_of_the_human_frame,
        width=CELL_SIZE,
        height=CELL_SIZE,
        borderwidth=0,
        highlightthickness=0,
    )
    canvas_human_color.grid(row=0, column=1)
    circle = canvas_human_color.create_oval(
        0, 0, CELL_SIZE, CELL_SIZE, outline=f"{HUMAN_COLOR}",
        fill=f"{HUMAN_COLOR}"
    )

    print(f"bot's color ! {BOT_COLOR}\n")
    print(f"human's color ! {HUMAN_COLOR}\n")

    # label to print who's turn it is...

    print(f"width is : {width}\n")

    print(f"height is : {height}\n")

    grid_tab: Canvas = create_board(
        gamePlay, width, height, CELL_SIZE, HUMAN_COLOR, BOT_COLOR,
        tokens=nb_tokens
    )
    grid_tab.grid(row=3, column=0, columnspan=2)

    label_all_trumps: Label = define_label(gamePlay,
                                           "All trumps Card",
                                           15, 0,
                                           4, True)
    label_all_trumps.config(pady=5)

    # the trump 's frame

    trump_frame: Frame = define_frame(gamePlay, 0, 5, columnspan=True)

    # the section for the comeback Button

    come_back_btn: Button = define_button(
        trump_frame, lambda: increment_count("comeback"),
        "come back",
        0, 0,
        width=12
    )

    label_come_back_count: Label = define_label(trump_frame,
                                                "used:0", 10,
                                                1, 0,
                                                False)

    # the section for the reverse board's Button

    def increment_count(string: str) -> None:
        global ReverseTrump
        global ComeBackTrump
        global BestPositionTrump

        if string == "reverse":
            ReverseTrump += 1
            label_reverse_board_count.config(text=f"used: {ReverseTrump}")
            print("Reverse the " "board")
            reverse_board(grid_tab, height, width, HUMAN_COLOR, BOT_COLOR)

        elif string == "best":
            BestPositionTrump += 1
            label_best_pos_count.config(text=f"used: {BestPositionTrump}")
            print("best Position " "launched")
            best_position_func(
                grid_tab, width, height, nb_tokens, HUMAN_COLOR, BOT_COLOR
            )

        else:
            ComeBackTrump += 1
            label_come_back_count.config(text=f"used: {ComeBackTrump}")
            print("come back")
            come_back_func(grid_tab)

    btn_reverse_board: Button = define_button(
        trump_frame, lambda: increment_count("reverse"),
        "reverse board", 0, 1,
        width=12
    )

    label_reverse_board_count: Label = define_label(
        trump_frame, "used:0", 10, 1, 1, False
    )

    # the section for the best Position Button

    btn_best_pos: Button = define_button(
        trump_frame, lambda: increment_count("best"),
        "best position", 0, 2,
        width=12
    )

    label_best_pos_count: Label = define_label(trump_frame,
                                               "used:0", 10,
                                               1, 2,
                                               False)

    reset_btn = define_button(gamePlay, lambda: define_game_play(window),
                              "Reset", 1, 6)

    return gamePlay
