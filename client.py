from tkinter import *
from backend import Database

db = Database()


def delete_lb1(func):
    def inner(*args, **kwargs):
        lb1.delete(0, END)
        return func(*args, **kwargs)

    return inner


@delete_lb1
def view_all():
    for record in db.view_all():
        lb1.insert(END, record)


@delete_lb1
def search():
    # print(*tuple(t.get() for t in [title_text, author_text, year_text, isbn_text]))
    for record in db.search(*inputs()):
        lb1.insert(END, record)


def add():
    db.populate_table([inputs()])
    lb1.insert(END, inputs())


def inputs():
    return tuple(t.get() for t in [title_text, author_text, year_text, isbn_text])


def get_selected_row(event):
    try:
        global selected_row
        global selected_index
        selected_index = lb1.curselection()[0]
        selected_row = lb1.get(selected_index)

        for entry, attr in zip(entries, selected_row[1:]):
            entry.delete(0, END)
            entry.insert(END, attr)
    except IndexError:
        pass

    return selected_row


def delete():
    db.delete(selected_row[0])
    lb1.delete(selected_index, selected_index)
    return


def update():
    db.update(selected_row[0], *inputs())
    view_all()


window = Tk()
window.wm_title("Book Store")

config = {
    "labels": [
        {"grid": {"row": 0, "column": 0}, "params": {"text": "Title"}},
        {"grid": {"row": 0, "column": 2}, "params": {"text": "Author"}},
        {"grid": {"row": 1, "column": 0}, "params": {"text": "Year"}},
        {"grid": {"row": 1, "column": 2}, "params": {"text": "ISBN"}},
    ],
    "entries": [
        {"grid": {"row": 0, "column": 1}, "params": {"textvariable": StringVar()}},
        {"grid": {"row": 0, "column": 3}, "params": {"textvariable": StringVar()}},
        {"grid": {"row": 1, "column": 1}, "params": {"textvariable": StringVar()}},
        {"grid": {"row": 1, "column": 3}, "params": {"textvariable": StringVar()}},
    ],
    "buttons": [
        {
            "grid": {"row": 2, "column": 3},
            "params": {"text": "View all", "width": 12, "command": view_all},
        },
        {
            "grid": {"row": 3, "column": 3},
            "params": {"text": "Search Entry", "width": 12, "command": search},
        },
        {
            "grid": {"row": 4, "column": 3},
            "params": {"text": "Add Entry", "width": 12, "command": add},
        },
        {
            "grid": {"row": 5, "column": 3},
            "params": {"text": "Update Selected", "width": 12, "command": update},
        },
        {
            "grid": {"row": 6, "column": 3},
            "params": {"text": "Delete Selected", "width": 12, "command": delete},
        },
        {
            "grid": {"row": 7, "column": 3},
            "params": {"text": "Close", "width": 12, "command": window.destroy},
        },
    ],
    "listboxes": [
        {
            "grid": {"row": 2, "column": 0, "rowspan": 6, "columnspan": 2},
            "params": {"height": 6, "width": 35},
        }
    ],
}

for grid, params in [c.values() for c in config["labels"]]:
    l = Label(window, **params)
    l.grid(**grid)

textvars = [c["params"]["textvariable"] for c in config["entries"]]
title_text, author_text, year_text, isbn_text = textvars

entries = []

for grid, params in [c.values() for c in config["entries"]]:
    entry = Entry(window, **params)
    entry.grid(**grid)
    entries.append(entry)

e1, e2, e3, e4 = entries

for grid, params in [c.values() for c in config["buttons"]]:
    b = Button(window, **params)
    b.grid(**grid)

grid, params = config["listboxes"][0].values()
lb1 = Listbox(window, **params)
lb1.grid(**grid)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

lb1.configure(yscrollcommand=sb1.set)
sb1.configure(command=lb1.yview)
lb1.bind("<<ListboxSelect>>", get_selected_row)

window.mainloop()
