from tkinter import *

PINK: str = "#F8E5E5"
frameWidth: int = 100
frameHeight: int = 50
framePad: int = 10


def define_spinbox(
        frameparent: Frame,
        func,
        from_: int,
        to: int,
        col: int,
        row: int,
        value_var: IntVar,
        wrap_: bool = True,
) -> Spinbox:
    spin = Spinbox(
        frameparent,
        from_=from_,
        to=to,
        wrap=wrap_,
        width=5,
        command=func,
        textvariable=value_var,
    )
    spin.grid(column=col, row=row)
    return spin


def define_frame(
        root: Tk,
        col: int,
        row: int,
        h: int = frameHeight,
        w: int = frameWidth,
        pad: int = framePad,
        columnspan: bool = False,
) -> Frame:
    frame = Frame(root, height=h, width=w, bg=PINK)
    frame.config(padx=pad, pady=pad)

    if columnspan:
        frame.grid(column=col, row=row, columnspan=2)
    else:
        frame.grid(column=col, row=row)
    return frame


def define_label(
        parent,
        text: str,
        font_size: int,
        col: int,
        row: int,
        columnspan: bool,
        fill: str = "black",
) -> Label:
    label = Label(
        parent, text=text, font=("arial", font_size, "bold"), bg=PINK, fg=fill
    )
    if columnspan:
        label.grid(column=col, row=row, columnspan=2)
    else:
        label.grid(column=col, row=row)
    return label


def define_entry(parent, width: int, string: str, col: int, row: int) -> Entry:
    entry: Entry = Entry(parent, width=width)
    entry.insert(END, string=string)
    entry.grid(column=col, row=row)

    return entry


def define_radio(
        parent, function, string: str, variable: IntVar, value: int, col: int,
        row: int
) -> Radiobutton:
    radio_btn: Radiobutton = Radiobutton(
        parent,
        text=string,
        variable=variable,
        value=value,
        bg=PINK,
        command=lambda: function(variable),
    )
    radio_btn.grid(column=col, row=row)
    return radio_btn


# function for the radioButton's function (This will change later)
def change_radio_value(value: IntVar):
    print(value.get())


def define_button(
        parent,
        function,
        string: str,
        col: int,
        row: int,
        columnspan: bool = False,
        width: int = 5,
) -> Button:
    btn: Button = Button(parent, text=string, command=function, width=width)
    if columnspan:
        btn.grid(column=col, row=row, columnspan=2, pady=20)
    else:
        btn.grid(column=col, row=row, pady=20)
    return btn
