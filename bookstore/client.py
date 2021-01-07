from tkinter import *
from backend import Database


class Client:
    def delete_lb1(func):
        def inner(self, *args, **kwargs):
            self.lb1.delete(0, END)
            return func(self, *args, **kwargs)

        return inner

    @delete_lb1
    def view_all(self):
        for record in self.db.view_all():
            self.lb1.insert(END, record)

    @delete_lb1
    def search(self):
        # print(*tuple(t.get() for t in [title_text, author_text, year_text, isbn_text]))
        for record in self.db.search(*self.inputs()):
            self.lb1.insert(END, record)

    def add(self):
        self.db.populate_table([self.inputs()])
        self.lb1.insert(END, self.inputs())

    def inputs(self):
        return tuple(t.get() for t in self.textvars)

    def get_selected_row(self, event):
        try:
            selected_index = self.lb1.curselection()[0]
            selected_row = self.lb1.get(selected_index)
            self.selected_index = selected_index
            self.selected_row = selected_row

            for entry, attr in zip(self.entries, selected_row[1:]):
                entry.delete(0, END)
                entry.insert(END, attr)
        except IndexError:
            pass

        return self.selected_row

    def delete(self):
        self.db.delete(self.selected_row[0])
        self.lb1.delete(self.selected_index, self.selected_index)
        return

    def update(self):
        self.db.update(self.selected_row[0], *self.inputs())
        self.view_all()

    def __init__(self, db):
        self.db = db
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
                {
                    "grid": {"row": 0, "column": 1},
                    "params": {"textvariable": StringVar()},
                },
                {
                    "grid": {"row": 0, "column": 3},
                    "params": {"textvariable": StringVar()},
                },
                {
                    "grid": {"row": 1, "column": 1},
                    "params": {"textvariable": StringVar()},
                },
                {
                    "grid": {"row": 1, "column": 3},
                    "params": {"textvariable": StringVar()},
                },
            ],
            "buttons": [
                {
                    "grid": {"row": 2, "column": 3},
                    "params": {
                        "text": "View all",
                        "width": 12,
                        "command": self.view_all,
                    },
                },
                {
                    "grid": {"row": 3, "column": 3},
                    "params": {
                        "text": "Search Entry",
                        "width": 12,
                        "command": self.search,
                    },
                },
                {
                    "grid": {"row": 4, "column": 3},
                    "params": {"text": "Add Entry", "width": 12, "command": self.add},
                },
                {
                    "grid": {"row": 5, "column": 3},
                    "params": {
                        "text": "Update Selected",
                        "width": 12,
                        "command": self.update,
                    },
                },
                {
                    "grid": {"row": 6, "column": 3},
                    "params": {
                        "text": "Delete Selected",
                        "width": 12,
                        "command": self.delete,
                    },
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

        self.textvars = [c["params"]["textvariable"] for c in config["entries"]]

        entries = []

        for grid, params in [c.values() for c in config["entries"]]:
            entry = Entry(window, **params)
            entry.grid(**grid)
            entries.append(entry)

        self.entries = entries

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
        lb1.bind("<<ListboxSelect>>", self.get_selected_row)

        self.lb1 = lb1
        self.sb1 = sb1

        window.mainloop()


client = Client(Database("books.db"))
