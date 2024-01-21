## @file motor.py
## The motor file contains the main function to launch the program


"""
@file motor.py
@desc This file contains the main function to launch the program

"""

import view.main_view as vue
from view.grid_functions import *

# globals' variables
## window's width
WINDOWWIDTH: int = 300

## window's height
WINDOWHEIGHT: int = 500

## background's color of the window
PINK: str = "#255369"


def init_game():
    """
    @brief This function initializes the game
    :return:
    """
    # Create the window
    window = Tk()

    # Set the window's size
    window.minsize(width=WINDOWWIDTH, height=WINDOWHEIGHT)
    game_config_frame = vue.vie_init_config_frame(window)

    # Calculate the position of the window on the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = int((screen_width - window.winfo_reqwidth()) // 2.5)
    y_position = (screen_height - window.winfo_reqheight()) // 9

    # Positioning the window on the screen

    window.geometry(f"+{x_position}+{y_position}")

    # can't resize the window anymore
    window.resizable(False, False)

    # Set the background's color of the window
    window.config(bg=PINK, padx=20)
    # Set the title of the window
    window.title("Power 4 ++")

    # we maintain the window open until the user closes it
    window.mainloop()
