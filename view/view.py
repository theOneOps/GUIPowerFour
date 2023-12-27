from tkinter.colorchooser import askcolor

from PIL import Image, ImageTk

from .miscelleanous import *

height: int = 5
width: int = 5
nb_tokens: int = 5
level = 1
BOT_COLOR = "red"
HUMAN_COLOR = "yellow"
ComeBackTrump: int = 0
BestPositionTrump: int = 0
ReverseTrump: int = 0


def initConfigFrame(window) -> Frame:
    for widget in window.winfo_children():
        widget.destroy()

    containerFrame: Frame = defineFrame(window, 0, 0, WINDOWWIDTH, WINDOWHEIGHT)
    nothing = Label(containerFrame, text="", bg=PINK)
    nothing.grid(column=0, row=0)
    label_Title: Label = defineLabel(containerFrame, "Welcome dear User !", 15,
                                     0, 1, True)
    canvas: Canvas = Canvas(window, width=220, height=210,
                            highlightthickness=0, bg=PINK)

    try:
        power_image = Image.open("../Images/power.png")
        powerImageCanvas = ImageTk.PhotoImage(power_image)
        canvas.create_image(110, 110, image=powerImageCanvas)
        canvas.grid(column=0, row=2, columnspan=2)
        # canvas.config(bg="black")
    except Exception as e:
        print(f"Error loading image: {e}")

    LabelOptions: Label = defineLabel(containerFrame, "Options", 15, 0, 3, True)
    # LabelOptions.grid(column=0, row=3, columnspan=2)
    fstFrame: Frame = defineFrame(containerFrame, 0, 5)

    widthVar: IntVar = IntVar()
    heightVar: IntVar = IntVar()
    nb_tokensVar: IntVar = IntVar()
    levelVar: IntVar = IntVar()

    widthVar.set(width)
    heightVar.set(height)
    nb_tokensVar.set(nb_tokens)
    levelVar.set(level)

    def changeValueHeight():
        heightVar = int(spinboxHeight.get())
        global height
        height = heightVar

    def changeValueLevel():
        levelVar = int(spinboxLevel.get())
        global level
        level = levelVar

    def changeValueWidth():
        widthVar = int(spinboxWidth.get())
        global width
        width = widthVar

    def changeValueTokens():
        nb_tokensVar = int(spinboxNb_tokens.get())
        global nb_tokens
        nb_tokens = nb_tokensVar

    def colorChoose(entry: Entry, player: str) -> None:
        global BOT_COLOR
        global HUMAN_COLOR
        color_tuple = askcolor(title=f"Choose the color of the {player}")

        entry.delete(0, 'end')
        if color_tuple is None:  # Check if the user canceled the color selection
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

    spinboxWidth: Spinbox = defineSpinBox(fstFrame, changeValueWidth,
                                          0, 10, 0, 0, valueVar=widthVar)
    LabelWidth: Label = defineLabel(fstFrame, "width", 10, 1, 0, False)

    scdFrame: Frame = defineFrame(containerFrame, 1, 5)
    spinboxHeight: Spinbox = defineSpinBox(scdFrame, changeValueHeight, 0, 10,
                                           10, 0, valueVar=heightVar)
    labelHeight: Label = defineLabel(scdFrame, "height", 10, 1, 0, False)

    trdFrame: Frame = defineFrame(containerFrame, 0, 6)
    spinboxLevel: Spinbox = defineSpinBox(trdFrame, changeValueLevel, 0, 10, 0,
                                          0,
                                          valueVar=levelVar)
    labelLevel: Label = defineLabel(trdFrame, "level", 10, 1, 0, False)

    fthFrame: Frame = defineFrame(containerFrame, 1, 6)
    spinboxNb_tokens: Spinbox = defineSpinBox(fthFrame, changeValueTokens, 0,
                                              10, 0, 0, valueVar=nb_tokensVar)

    labelNb_Tokens: Label = defineLabel(fthFrame, "tokens", 10, 1, 0, False)

    labelWhoStart: Label = defineLabel(containerFrame, "who start first ?", 10,
                                       0, 7, True,
                                       fill="red")
    radioState: IntVar = IntVar()
    radioBot: Radiobutton = defineRadio(containerFrame, changeRadioValue, "Bot",
                                        radioState, 0, 0,
                                        8)
    radioHuman: Radiobutton = defineRadio(containerFrame, changeRadioValue,
                                          "Human", radioState, 1,
                                          1, 8)

    sthFrame: Frame = defineFrame(containerFrame, 0, 9)
    labelBotColor: Label = defineLabel(sthFrame, "Bot's color", 10,
                                       0, 0, False)
    entryBotColor: Entry = defineEntry(sthFrame, 8, f"{BOT_COLOR}", 1, 0)
    btnBotColor = defineButton(sthFrame,
                               lambda entry=entryBotColor,
                                      player="Bot":
                               colorChoose(entry, player), "Bot color", 0,
                               1, width=10, columnspan=True)

    sevthFrame: Frame = defineFrame(containerFrame, 1, 9)
    labelHumanColor: Label = defineLabel(sevthFrame, "Human's color", 10, 0, 0,
                                         False)
    entryHumanColor: Entry = defineEntry(sevthFrame, 8, f"{HUMAN_COLOR}", 1, 0)
    btnHumanColor = defineButton(sevthFrame,
                                 lambda entry=entryHumanColor,
                                        player="Human":
                                 colorChoose(entry, player), "Human color", 0,
                                 1, width=10, columnspan=True)

    quitBtn: Button = defineButton(containerFrame, lambda: window.quit(),
                                   "Quit", 0, 10)
    helpBtn: Button = defineButton(containerFrame, lambda: print("Help"),
                                   "Help", 0, 10, True)
    startBtn: Button = defineButton(containerFrame,
                                    lambda: defineGamePlay(window), "Start", 1,
                                    10)

    return containerFrame


# SECOND PAGE
def defineGamePlay(window) -> Frame:
    # need to change the widget's positions
    global ComeBackTrump
    global BestPositionTrump
    global ReverseTrump

    ComeBackTrump = 0
    BestPositionTrump = 0
    ReverseTrump = 0

    for widget in window.winfo_children():
        widget.destroy()

    gamePlay: Frame = defineFrame(window, 0, 0, WINDOWHEIGHT, WINDOWWIDTH, 10)
    returnBtn = defineButton(gamePlay, lambda: initConfigFrame(window),
                             "Return", 0, 0)
    help = defineButton(gamePlay, lambda: print("Help"), "Help", 0, 0, True)
    quit = defineButton(gamePlay, lambda: window.quit(), "Quit", 1, 0)

    # number of tokens to win (label)

    labelPrintNbTokens = defineLabel(gamePlay, f"Number of tokens to win:"
                                               f" {nb_tokens}",
                                     20, 0, 1, True)

    # frame to print the bot's color
    ColorOftheBotFrame: Frame = defineFrame(gamePlay, 0, 2)
    labelColorBot = defineLabel(ColorOftheBotFrame, "Bot's color  ", 10, 0, 0,
                                False)
    canvasBotColor: Canvas = Canvas(ColorOftheBotFrame, width=CELL_SIZE,
                                    height=CELL_SIZE,
                                    borderwidth=0, highlightthickness=0)
    canvasBotColor.grid(row=0, column=1)

    circle = canvasBotColor.create_oval(0, 0, CELL_SIZE, CELL_SIZE,
                                        outline=f"{BOT_COLOR}",
                                        fill=f"{BOT_COLOR}")

    # frame to print the human's color

    ColorOftheHumanFrame: Frame = defineFrame(gamePlay, 1, 2)
    labelColorHuman = defineLabel(ColorOftheHumanFrame, "Human's color  ",
                                  10, 0, 0,
                                  False)
    canvasHumanColor: Canvas = Canvas(ColorOftheHumanFrame, width=CELL_SIZE,
                                      height=CELL_SIZE,
                                      borderwidth=0, highlightthickness=0)
    canvasHumanColor.grid(row=0, column=1)
    circle = canvasHumanColor.create_oval(0, 0, CELL_SIZE, CELL_SIZE,
                                          outline=f"{HUMAN_COLOR}",
                                          fill=f"{HUMAN_COLOR}")

    print(f"bot's color ! {BOT_COLOR}\n")
    print(f"human's color ! {HUMAN_COLOR}\n")

    # label to print who's turn it is...

    print(f"width is : {width}\n")

    print(f"height is : {height}\n")

    gridTab: Canvas = createBoard(gamePlay, width, height, CELL_SIZE,
                                  HUMAN_COLOR, BOT_COLOR, tokens=nb_tokens)
    gridTab.grid(row=3, column=0, columnspan=2)

    LabelAllTrumps: Label = defineLabel(gamePlay, "All trumps Card", 15,
                                        0, 4,
                                        True)
    LabelAllTrumps.config(pady=5)

    # the trump 's frame

    TrumpFrame: Frame = defineFrame(gamePlay, 0, 5, columnspan=True)

    # the section for the comeback Button

    comeBackBtn: Button = defineButton(TrumpFrame, lambda: incrementCount(
        "comeback"),
                                       "come back", 0, 0, width=12)

    labelComeBackCount: Label = defineLabel(TrumpFrame, "used:0", 10, 1, 0,
                                            False)

    # the section for the reverse board's Button

    def incrementCount(string: str) -> None:
        global ReverseTrump
        global ComeBackTrump
        global BestPositionTrump

        if string == "reverse":
            ReverseTrump += 1
            labelReverseBoardCount.config(text=f"used: {ReverseTrump}")
            print("Reverse the "
                  "board")
            reverseBoard(gridTab, height, width, HUMAN_COLOR, BOT_COLOR)

        elif string == "best":
            BestPositionTrump += 1
            labelBestPosCount.config(text=f"used: {BestPositionTrump}")
            print("best Position "
                  "launched")
            bestPositionFunc(gridTab, width, height, nb_tokens, HUMAN_COLOR,
                             BOT_COLOR)

        else:
            ComeBackTrump += 1
            labelComeBackCount.config(text=f"used: {ComeBackTrump}")
            print("come back")
            comeBackFunc(gridTab)

    BtnReverseBoard: Button = defineButton(TrumpFrame, lambda:
    incrementCount("reverse"),
                                           "reverse board", 0, 1, width=12)

    labelReverseBoardCount: Label = defineLabel(TrumpFrame, "used:0", 10,
                                                1, 1,
                                                False)

    # the section for the best Position Button

    BtnBestPos: Button = defineButton(TrumpFrame, lambda: incrementCount(
        "best"),
                                      "best position", 0, 2, width=12)

    labelBestPosCount: Label = defineLabel(TrumpFrame, "used:0", 10, 1, 2,
                                           False)

    ResetBtn = defineButton(gamePlay, lambda: defineGamePlay(window), "Reset",
                            1, 6)

    return gamePlay
