"""
! @brief A program that plays Power/ Connect 4
  @mainpage P4++ Project
    @section description_main Description
    A program that plays Power 4 with board of variable size,
    variable number to win, game levels, asset , undo

    @section author_main Author
    - @subpage Selly MEDEWOU
    - @subpage Jeremie YANG

    @section import_section Import

    This program uses the following external modules :
    - tkinter as tk
    - random
    - copy
    -tkinter.messagebox
    -from tkinter.colorchooser import askcolor
    -from PIL import Image, ImageTk
"""

import controller.motor as game

game.init_game()
