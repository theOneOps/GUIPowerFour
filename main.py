"""!
  @brief A program that plays Power/ Connect 4
  @mainpage Power4++ Project
    @section description_main Description

    The goal of this project is to develop a computerized version of the
    Connect Four game using the Python programming language with the Tkinter
    graphical
    interface. In this game, a player has the opportunity to challenge a robot
    whose difficulty level is customizable. The main features of the game
    include:

    A game grid with variable dimensions, determined by the player's choice.
    The option for the player to define the number of tokens required to align
    in order to win the game.
    Customization of token colors, allowing the player to choose the color of
    their own tokens as well as the robot's.
    The inclusion of power-ups designed to assist the player in winning against
    the robot.
    The player's action involves clicking on an unfilled column to place
     a token. The robot uses the Minimax algorithm to choose the position of
     a token.

    In summary, this project aims to create an interactive and customizable
    version of the Connect Four game, offering a degree of freedom to the
    player.
    This includes the ability to personalize game sessions as they wish,
    and the option to use bonuses/power-ups during gameplay when competing
    against a bot with significant analytical capability, depending on the
    depth parameter set
    by the user.

    @section author_main Authors
    - @subpage Selly MEDEWOU
    - @subpage Jeremie YANG

    @section import_section Import
    This program uses the following external modules :
    - tkinter as tk
    - random
    - copy
    - tkinter.messagebox
    - askcolor from tkinter.colorchooser

    @section install_section Installation
    There is two ways to install the program:
    @subsection install_subsection First Clone it from GitHub
    To install the program, you can clone the repository using the following
    command:
    @code
    git clone https://github.com/theOneOps/GUIPowerFour.git
    @endcode

    and then you go the directory where there is the file main.py, and you
    install the requirements.txt using the following command:
    @code
    pip install -r requirements.txt
    @endcode

    @section run_section Run
    To run the program, you can use the following command:
    @code
    python main.py
    @endcode

    @subsection installsecond_subsection Run with a shell script or a batch
    file

    You can also run the program using a shell script on linux or a batch file.
    To do this, you can use the following command:
    @code
    install.bat on windows
    @endcode
    or
    @code
    sh install.sh on linux
    @endcode

    And the program will install the required modules and then run the program.

    To understand how the program works, you can read the documentation of the
    program.
    But here some information about the program's naming convention:
    all the variables, and functions are in camelCase
    the constants are in CAPITAL_LETTERS.
    now the conventions :

    @section convention_section Convention naming

    @subsection convention_dubsection The variables:

    - name_frame : for the frame's variable
    - name_btn : for the button's variable
    - label_name : for the label's variable
    - canvas_name : for the canvas's variable
    - spin_name : for the spinbox's variable
    - name_lb_frame : for the labelframe's variable
    - name_var : for the Invar's variable
    - radio_name : for the radiobutton's variable

    @subsection convention_subsection The functions:

    A trigam : that represent the first three letters of the package
    where the function is.
    there is 3 types of trigams:

    - mod : for the functions in the model package
    - con : for the functions in the controller package (in this package,
    there is no functions) so there is NO TRIGAM's function for this package
    - vie : for the functions in the view package

"""

## @file: main.py
## This file is responsible for launching the program

from controller.motor import init_game

init_game()
