# Power4++ Project

## Brief Description

A program that plays Power/ Connect 4 in python-Tkinter

### Detailed Description

The goal of this project is to develop a computerized version of the Connect
Four game using the Python programming language with the Tkinter graphical
interface. In this game, a player has the opportunity to challenge a robot whose
difficulty level is customizable. The main features of the game include:

- A game grid with variable dimensions, determined by the player's choice.
- The option for the player to define the number of tokens required to align in
  order to win the game.
- Customization of token colors, allowing the player to choose the color of
  their own tokens as well as the robot's.
- The inclusion of power-ups designed to assist the player in winning against
  the robot.
- The player's action involves clicking on an unfilled column to place a token.
  The robot uses the Minimax algorithm to choose the position of a token.

In summary, this project aims to create an interactive and customizable version
of the Connect Four game, offering a degree of freedom to the player. This
includes the ability to personalize game sessions as they wish, and the option
to use bonuses/power-ups during gameplay when competing against a bot with
significant analytical capability, depending on the depth parameter set by the
user.

### Authors

- Selly MEDEWOU
- Jeremie YANG

### Import

This program uses the following external modules:

- `tkinter` as `tk`
- `random`
- `copy`
- `tkinter.messagebox`
- `askcolor` from `tkinter.colorchooser`

### Installation

There are two ways to install the program:

#### First : Clone it from GitHub

To install the program, you can clone the repository using the following
command:

`git clone https://github.com/theOneOps/GUIPowerFour.git`

Then go to the directory where the file `main.py` is located, and install
the `requirements.txt` using the following command:

`pip install -r requirements.txt`

##### Run

To run the program, you can use the following command:

`python main.py`

#### Second : Run with a shell script or a batch file

You can also run the program using a shell script or a bash file. To do this,
use the following command:

##### On Windows : just execute this line of code:
Firstly go to the directory where the `install.bat` is located, and then run this command : 

`.\install.bat`

##### On Linux : just execute this line of code:
Firstly, go to the directory where the `install.sh` is located, and then run this command : 

`sh install.sh`

The program will install the required modules and then run the program.

To understand how the program works, you can read the documentation of the
program. Here is some information about the program's naming convention: all the
variables, and functions are in camelCase, and the constants are in
CAPITAL_LETTERS.

### Convention Naming

#### Variables:

- `name_frame`: for the frame's variable
- `name_btn`: for the button's variable
- `label_name`: for the label's variable
- `canvas_name`: for the canvas's variable
- `spin_name`: for the spinbox's variable
- `name_lb_frame`: for the labelframe's variable
- `name_var`: for the Invar's variable
- `radio_name`: for the radiobutton's variable

#### Functions:

Functions have a trigam representing the first three letters of the package
where the function is. There are 3 types of trigams:

- `mod`: for functions in the model package
- `con`: for functions in the controller package (no functions in this package,
  so no trigam's function for this package)
- `vie`: for functions in the view package
