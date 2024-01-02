import view.view as vue
from view.grid_view import *

# globals' variables
WINDOWWIDTH: int = 300
WINDOWHEIGHT: int = 530
PINK: str = "#F8E5E5"


def init_game():
    window = Tk()
    window.minsize(width=WINDOWWIDTH, height=WINDOWHEIGHT)
    game_config_frame = vue.init_config_frame(window)

    # Calculate the position of the window on the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = int((screen_width - window.winfo_reqwidth()) // 2.5)
    y_position = (screen_height - window.winfo_reqheight()) // 9

    # Positioning the window on the screen

    window.geometry(f"+{x_position}+{y_position}")

    # can't resize the window anymore
    window.resizable(False, False)
    window.config(bg=PINK, padx=20)
    window.title("Power 4 ++")

    window.mainloop()
