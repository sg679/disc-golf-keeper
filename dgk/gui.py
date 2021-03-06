from dgk.version import __version__
from tkinter import font, messagebox, ttk
import os
import tkinter as tk
import getpass as gp
import sqlite3 as db


APP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_COURSES = os.path.join(APP_DIR, "config/courses.ini")
APP_DATABASE = os.path.join(APP_DIR, "database/dgk.db")
APP_FONT = "Helvetica Neue"
LABEL_WIDTH = 8
TV_COLUMN_WIDTH_1 = 35
TV_COLUMN_WIDTH_2 = 60
TV_COLUMN_WIDTH_3 = 130
WIDGET_BACKGROUND = "gray91"


class DGKApplication(tk.Tk):
    def __init__(self):
        # Required file checking.
        if not os.path.exists(APP_COURSES):
            raise FileNotFoundError(
                "Cannot find the specified course list at '{}'".format(APP_COURSES)
            )
        if not os.path.exists(APP_DATABASE):
            raise FileNotFoundError(
                "Cannot find the specified database at '{}'".format(APP_DATABASE)
            )
        super().__init__()
        s = ttk.Style()
        s.configure("TButton", foreground="green", relief=tk.GROOVE)
        s.configure("TCombobox", foreground="gray30")
        s.configure("TEntry", foreground="blue")
        s.configure("TLabel", foreground="gray10")
        s.map("TButton", foreground=[("disabled", WIDGET_BACKGROUND)])
        self.title("Disc Golfer Keeper v{} - {}".format(__version__, gp.getuser()))
        self.resizable(False, False)
        form_font = font.nametofont("TkDefaultFont")
        form_font.configure(family=APP_FONT, size=13)
        self.option_add("*Font", form_font)
        self["background"] = WIDGET_BACKGROUND
        self["bd"] = 1
        self["relief"] = tk.RAISED
        self["takefocus"] = True

    def execute(self):
        self.mainloop()


class DGKButton(ttk.Button):
    def __init__(self, master, command):
        super().__init__(master)
        self["command"] = command
        self["text"] = "Save Game"
        self["width"] = 10
        self.grid(row=5, column=0, columnspan=11, pady=(15, 0))


class DGKCombo(ttk.Combobox):
    def __init__(self, master, options):
        super().__init__(master)
        self["height"] = 6
        self["justify"] = "center"
        self["state"] = "readonly"
        self["value"] = options
        self["width"] = 20
        self.set(options[0])
        self.grid(row=0, column=1)


class DGKField(ttk.Label):
    def __init__(self, master, text):
        super().__init__(master)
        self["anchor"] = tk.CENTER
        self["text"] = text
        self["width"] = 20
        self.grid(row=0, column=0)


class DGKForm(ttk.Frame):
    SIDE_BACK = 0
    SIDE_FRONT = 1

    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, padx=10, pady=10)
        table = ttk.Frame(self)
        table.grid(row=0, column=0, columnspan=11, pady=10)
        DGKField(table, "Course")
        self.course = DGKCombo(table, self._course())
        for index in range(0, 9):
            hole = index + 1
            label = hole
            DGKHole(self, (1, index), label, LABEL_WIDTH)
        DGKHole(self, (1, 9), "Front", LABEL_WIDTH)
        DGKHole(self, (1, 10), "Total", 14)
        self.hole1 = DGKScore(self, (2, 0), self._update)
        self.hole2 = DGKScore(self, (2, 1), self._update)
        self.hole3 = DGKScore(self, (2, 2), self._update)
        self.hole4 = DGKScore(self, (2, 3), self._update)
        self.hole5 = DGKScore(self, (2, 4), self._update)
        self.hole6 = DGKScore(self, (2, 5), self._update)
        self.hole7 = DGKScore(self, (2, 6), self._update)
        self.hole8 = DGKScore(self, (2, 7), self._update)
        self.hole9 = DGKScore(self, (2, 8), self._update)
        self.front = DGKSub(self, (2, 9))
        self.total = DGKTotal(self, (2, 10))
        for index in range(10, 19):
            hole = index
            label = "{}".format(hole)
            DGKHole(self, (3, index - 10), label, LABEL_WIDTH)
        DGKHole(self, (3, 9), "Back", LABEL_WIDTH)
        self.hole10 = DGKScore(self, (4, 0), self._update)
        self.hole11 = DGKScore(self, (4, 1), self._update)
        self.hole12 = DGKScore(self, (4, 2), self._update)
        self.hole13 = DGKScore(self, (4, 3), self._update)
        self.hole14 = DGKScore(self, (4, 4), self._update)
        self.hole15 = DGKScore(self, (4, 5), self._update)
        self.hole16 = DGKScore(self, (4, 6), self._update)
        self.hole17 = DGKScore(self, (4, 7), self._update)
        self.hole18 = DGKScore(self, (4, 8), self._update)
        self.back = DGKSub(self, (4, 9))
        DGKButton(self, self._save)
        self.after(500, self._update)

    def _clear(self):
        self._set(self.hole1, 0)
        self._set(self.hole2, 0)
        self._set(self.hole3, 0)
        self._set(self.hole4, 0)
        self._set(self.hole5, 0)
        self._set(self.hole6, 0)
        self._set(self.hole7, 0)
        self._set(self.hole8, 0)
        self._set(self.hole9, 0)
        self._set(self.front, 0)
        self._set(self.hole10, 0)
        self._set(self.hole11, 0)
        self._set(self.hole12, 0)
        self._set(self.hole13, 0)
        self._set(self.hole14, 0)
        self._set(self.hole15, 0)
        self._set(self.hole16, 0)
        self._set(self.hole17, 0)
        self._set(self.hole18, 0)
        self._set(self.back, 0)
        self._set(self.total, 0)

    @staticmethod
    def _course() -> list:
        with open(APP_COURSES, "r") as c:
            courses = c.read()
            c.close()
        course_list = courses.split("\n")
        course_list.remove("")
        return course_list

    def _save(self):
        scores = [
            self.hole1.get(),
            self.hole2.get(),
            self.hole3.get(),
            self.hole4.get(),
            self.hole5.get(),
            self.hole6.get(),
            self.hole7.get(),
            self.hole8.get(),
            self.hole9.get(),
            self._sub(self.SIDE_FRONT),
            self.hole10.get(),
            self.hole11.get(),
            self.hole12.get(),
            self.hole13.get(),
            self.hole14.get(),
            self.hole15.get(),
            self.hole16.get(),
            self.hole17.get(),
            self.hole18.get(),
            self._sub(self.SIDE_BACK),
            self._total(),
        ]
        scores = [int(x) for x in scores]
        for score in scores:
            if score <= 0:
                DGKInfoWindow("Save Error", "Not all values have been entered.")
                return
        connect = db.connect(APP_DATABASE)
        cursor = connect.cursor()
        sql = (
            "INSERT INTO game_stats "
            "(hole01, hole02, hole03, hole04, hole05, hole06, "
            "hole07, hole08, hole09, front, hole10, hole11, "
            "hole12, hole13, hole14, hole15, hole16, hole17, "
            "hole18, back, total, course) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        )
        scores.append(self.course.get())
        try:
            cursor.execute(sql, tuple(scores))
        except db.OperationalError as OPError:
            DGKInfoWindow("Database Error", OPError)
        except db.ProgrammingError as PROError:
            DGKInfoWindow("Database Error", PROError)
        else:
            connect.commit()
        finally:
            connect.close()
            self._clear()
            DGKInfoWindow("Save Successful", "Your scores were added to the database.")

    @staticmethod
    def _set(entry, value):
        entry["state"] = tk.NORMAL
        entry.delete(0, tk.END)
        entry.insert(tk.END, value)
        entry["state"] = tk.DISABLED

    def _sub(self, side) -> int:
        row = []
        if side is self.SIDE_BACK:
            row = [
                self.hole10.get(),
                self.hole11.get(),
                self.hole12.get(),
                self.hole13.get(),
                self.hole14.get(),
                self.hole15.get(),
                self.hole16.get(),
                self.hole17.get(),
                self.hole18.get(),
            ]
        if side is self.SIDE_FRONT:
            row = [
                self.hole1.get(),
                self.hole2.get(),
                self.hole3.get(),
                self.hole4.get(),
                self.hole5.get(),
                self.hole6.get(),
                self.hole7.get(),
                self.hole8.get(),
                self.hole9.get(),
            ]
        row = [int(x) for x in row]
        return sum(row)

    def _total(self) -> int:
        return self._sub(self.SIDE_BACK) + self._sub(self.SIDE_FRONT)

    def _update(self, event=None):
        self._set(self.front, self._sub(self.SIDE_FRONT))
        self._set(self.back, self._sub(self.SIDE_BACK))
        self._set(self.total, self._total())
        return event


class DGKHole(ttk.Label):
    def __init__(self, master, index, text, width):
        super().__init__(master)
        self["anchor"] = tk.CENTER
        self["text"] = text
        self["width"] = width
        self.grid(row=index[0], column=index[1])


class DGKInfoWindow:
    def __init__(self, title, message):
        messagebox.showinfo(title, message)


class DGKSub(ttk.Entry):
    def __init__(self, master, index):
        super().__init__(master)
        self["justify"] = "center"
        self["state"] = tk.DISABLED
        self["width"] = 3
        self.insert(tk.END, 0)
        self.grid(row=index[0], column=index[1])


class DGKTotal(ttk.Entry):
    def __init__(self, master, index):
        super().__init__(master)
        self["font"] = ("Helvetica", 52)
        self["justify"] = "center"
        self["state"] = tk.DISABLED
        self["width"] = 3
        self.grid(row=index[0], column=index[1], rowspan=3)


class DGKScore(ttk.Entry):
    def __init__(self, master, index, callback):
        super().__init__(master)
        self["justify"] = "center"
        self["width"] = 3
        self.insert(tk.END, 0)
        self.bind("<FocusIn>", self._reset)
        self.bind("<FocusOut>", callback)
        self.grid(row=index[0], column=index[1])

    def _reset(self, event):
        self.delete(0, tk.END)
        self.insert(tk.END, "")
        return event


class DGKScorecard(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=0, padx=10, pady=10)
        self.score_card = ttk.Treeview(self)
        xsb = ttk.Scrollbar(self)
        xsb["command"] = self.score_card.xview
        xsb["orient"] = tk.HORIZONTAL
        self.score_card["xscroll"] = xsb.set
        xsb.grid(row=1, column=0, sticky=tk.SW + tk.SE)
        ysb = ttk.Scrollbar(self)
        ysb["command"] = self.score_card.yview
        ysb["orient"] = tk.VERTICAL
        self.score_card["yscroll"] = ysb.set
        ysb.grid(row=0, column=1, sticky=tk.NE + tk.SE)
        self.score_card["columns"] = (
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
        )
        self.score_card["height"] = 10
        self.score_card["selectmode"] = "browse"
        self.score_card["show"] = "headings"
        for _ in self.score_card["columns"]:
            if _ in ("22",):
                width = TV_COLUMN_WIDTH_3
            elif _ in ("10", "20", "21"):
                width = TV_COLUMN_WIDTH_2
            else:
                width = TV_COLUMN_WIDTH_1
            self.score_card.column(_, width=width, stretch=tk.NO, anchor=tk.CENTER)
        for _ in self.score_card["columns"]:
            if _ == "10":
                text = "Front"
            elif _ == "20":
                text = "Back"
            elif _ == "21":
                text = "Total"
            elif _ == "22":
                text = "Course"
            else:
                header = int(_)
                if header > 10:
                    text = header - 1
                else:
                    text = header
            self.score_card.heading(_, text=text)
        self.score_card.grid(row=0, column=0)
        self.score_card.after(1000, self._reload)

    def _reload(self):
        # Depopulate old values from tree view.
        children = self.score_card.get_children()
        if children:
            for _ in children:
                self.score_card.delete(_)
        connect = db.connect(APP_DATABASE)
        cursor = connect.cursor()
        try:
            cursor.execute(
                "SELECT hole01, hole02, hole03, hole04, hole05, "
                "hole06, hole07, hole08, hole09, front, hole10, "
                "hole11, hole12, hole13, hole14, hole15, hole16, "
                "hole17, hole18, back, total, course FROM game_stats "
                "ORDER BY GID DESC"
            )
        except db.OperationalError as OPError:
            DGKInfoWindow("Database Error", OPError)
        except db.ProgrammingError as PROError:
            DGKInfoWindow("Database Error", PROError)
        else:
            # Repopulate tree view with updated values.
            for row in cursor.fetchall():
                self.score_card.insert("", "end", values=row)
        finally:
            connect.close()
            self.score_card.after(150000, self._reload)


class DGKWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        DGKForm(self)
        DGKScorecard(self)
