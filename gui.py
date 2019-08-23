from tkinter import ttk
import sqlite3 as db
import tkinter as tk

DEFAULT_LABEL_WIDTH = 7
DEFAULT_HEAD_WIDTH_1 = 35
DEFAULT_HEAD_WIDTH_2 = 55
DEFAULT_HEAD_WIDTH_3 = 120


class ButtonSave(ttk.Button):

    def __init__(self, master, command):
        ttk.Button.__init__(self, master)
        self['command'] = command
        self['text'] = 'Save'
        self.grid(row=0, column=1)


class ButtonTotal(ttk.Button):

    def __init__(self, master, command):
        ttk.Button.__init__(self, master)
        self['command'] = command
        self['text'] = 'Total'
        self.grid(row=0, column=0)


class EntryThrows(ttk.Entry):

    def __init__(self, master, index):
        ttk.Entry.__init__(self, master)
        self['justify'] = 'center'
        self['width'] = 2
        self.insert(tk.END, 0)
        self.grid(row=index[0], column=index[1])


class EntryTotal(ttk.Entry):

    def __init__(self, master, index):
        ttk.Entry.__init__(self, master)
        self['justify'] = 'center'
        self['state'] = tk.DISABLED
        self['width'] = 2
        self.insert(tk.END, 0)
        self.grid(row=index[0], column=index[1])


class FrameRow(ttk.Frame):

    def __init__(self, master, row):
        ttk.Frame.__init__(self, master)
        self.grid(row=row, column=0, padx=10, pady=10)


class LabelText(ttk.Label):

    def __init__(self, master, index, text, width):
        ttk.Label.__init__(self, master)
        self['anchor'] = tk.CENTER
        self['text'] = text
        self['width'] = width
        self.grid(row=index[0], column=index[1], pady=10)


class ScorecardTable(ttk.Frame):

    def __init__(self, master, database):
        self.database = database
        ttk.Frame.__init__(self, master)
        self.grid(row=3, column=0, padx=10, pady=10)
        self.score_card = ttk.Treeview(self)
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.score_card.yview)
        self.score_card.configure(yscroll=ysb.set)
        ysb.grid(row=0, column=1, sticky=tk.NE + tk.SE)
        self.score_card['show'] = 'headings'
        self.score_card['columns'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                                      '13', '14', '15', '16', '17', '18', '19', '20', '21', '22')
        for _ in self.score_card['columns']:
            if _ in '1':
                width = DEFAULT_HEAD_WIDTH_3
            elif _ in ('11', '21', '22'):
                width = DEFAULT_HEAD_WIDTH_2
            else:
                width = DEFAULT_HEAD_WIDTH_1
            self.score_card.column(_, width=width, stretch=tk.NO, anchor=tk.CENTER)
        for _ in self.score_card['columns']:
            if _ == '1':
                text = 'Course'
            elif _ == '11':
                text = 'Front'
            elif _ == '21':
                text = 'Back'
            elif _ == '22':
                text = 'Total'
            else:
                header = int(_)
                if header > 10:
                    text = header - 2
                else:
                    text = header - 1
            self.score_card.heading(_, text=text)
        self.score_card.grid(row=0, column=0)
        self.score_card.after(1000, self.load)

    def load(self):
        children = self.score_card.get_children()
        if children:
            for _ in children:
                self.score_card.delete(_)
        connect = db.connect(self.database)
        cursor = connect.cursor()
        try:
            cursor.execute('SELECT course, hole01, hole02, hole03, hole04, hole05, '
                           'hole06, hole07, hole08, hole09, front, hole10, '
                           'hole11, hole12, hole13, hole14, hole15, hole16, '
                           'hole17, hole18, back, total FROM game_stats '
                           'ORDER BY GID DESC')
        except db.OperationalError as OPError:
            exit(OPError)
        except db.ProgrammingError as PROError:
            exit(PROError)
        else:
            for row in cursor.fetchall():
                self.score_card.insert('', 'end', values=row)
        finally:
            connect.close()
            self.score_card.after(300000, self.load)


class Gui(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        import getpass
        self.title(f'Disc Golfer Keeper - {getpass.getuser()}')
        self['background'] = 'gray91'
        self['bd'] = 1
        self['relief'] = tk.GROOVE
        self['takefocus'] = True
        # Database checking.
        import os
        data_dir = os.path.abspath(__file__)
        database = data_dir.replace(os.path.basename(__file__), 'database/dgk.sqlite')
        try:
            if not os.path.exists(database):
                raise FileNotFoundError
            else:
                self.database = database
        except FileNotFoundError:
            exit('Database file not found! Exiting...')
        # Holes Frame
        data = FrameRow(self, 0)
        LabelText(data, (0, 0), 'Course', 10)
        parks = ['Mary Rutan Park', 'Mill Valley Park']
        self.course = ttk.Combobox(data)
        self.course['height'] = 4
        self.course['justify'] = 'center'
        self.course['values'] = parks
        self.course.set(parks[0])
        self.course.grid(row=0, column=1)
        holes = FrameRow(self, 1)
        for index in range(0, 9):
            hole = index + 1
            label = f'Hole {hole}'
            LabelText(holes, (0, index), label, DEFAULT_LABEL_WIDTH)
        LabelText(holes, (0, 9), 'Front', DEFAULT_LABEL_WIDTH)
        LabelText(holes, (0, 10), 'Total', 14)
        self.hole1 = EntryThrows(holes, (1, 0))
        self.hole2 = EntryThrows(holes, (1, 1))
        self.hole3 = EntryThrows(holes, (1, 2))
        self.hole4 = EntryThrows(holes, (1, 3))
        self.hole5 = EntryThrows(holes, (1, 4))
        self.hole6 = EntryThrows(holes, (1, 5))
        self.hole7 = EntryThrows(holes, (1, 6))
        self.hole8 = EntryThrows(holes, (1, 7))
        self.hole9 = EntryThrows(holes, (1, 8))
        self.front = EntryTotal(holes, (1, 9))
        self.total = ttk.Entry(holes)
        self.total['font'] = ('Arial', 74)
        self.total['justify'] = 'center'
        self.total['state'] = tk.DISABLED
        self.total['width'] = 3
        self.total.grid(row=1, column=10, rowspan=3)
        for index in range(10, 19):
            hole = index
            label = f'Hole {hole}'
            LabelText(holes, (2, index - 10), label, DEFAULT_LABEL_WIDTH)
        LabelText(holes, (2, 9), 'Back', DEFAULT_LABEL_WIDTH)
        self.hole10 = EntryThrows(holes, (3, 0))
        self.hole11 = EntryThrows(holes, (3, 1))
        self.hole12 = EntryThrows(holes, (3, 2))
        self.hole13 = EntryThrows(holes, (3, 3))
        self.hole14 = EntryThrows(holes, (3, 4))
        self.hole15 = EntryThrows(holes, (3, 5))
        self.hole16 = EntryThrows(holes, (3, 6))
        self.hole17 = EntryThrows(holes, (3, 7))
        self.hole18 = EntryThrows(holes, (3, 8))
        self.back = EntryTotal(holes, (3, 9))
        # Button Frame
        buttons = FrameRow(self, 2)
        ButtonTotal(buttons, self.update_score)
        ButtonSave(buttons, self.save_game)
        # Scorecard Frame
        ScorecardTable(self, self.database)

    def save_game(self):
        connect = db.connect(self.database)
        cursor = connect.cursor()
        sql = 'INSERT INTO game_stats ' \
              '(course, hole01, hole02, hole03, hole04, hole05, ' \
              'hole06, hole07, hole08, hole09, front, ' \
              'hole10, hole11, hole12, hole13, hole14, ' \
              'hole15, hole16, hole17, hole18, back, total) ' \
              'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        scores = [self.hole1.get(), self.hole2.get(), self.hole3.get(),
                  self.hole4.get(), self.hole5.get(), self.hole6.get(),
                  self.hole7.get(), self.hole8.get(), self.hole9.get(),
                  self.total_front(), self.hole10.get(), self.hole11.get(),
                  self.hole12.get(), self.hole13.get(), self.hole14.get(),
                  self.hole15.get(), self.hole16.get(), self.hole17.get(),
                  self.hole18.get(), self.total_back(),
                  self.total_front() + self.total_back()]
        scores = [int(x) for x in scores]
        scores.insert(0, self.course.get())
        try:
            cursor.execute(sql, tuple(scores))
        except db.OperationalError as OPErr:
            print(OPErr)
        except db.ProgrammingError as PROErr:
            print(PROErr)
        else:
            connect.commit()
        finally:
            connect.close()

    @staticmethod
    def set_total(master, value):
        master.configure(state=tk.NORMAL)
        master.delete(0, tk.END)
        master.insert(tk.END, value)
        master.configure(state=tk.DISABLED)

    def total_back(self):
        row = [self.hole10.get(), self.hole11.get(), self.hole12.get(),
               self.hole13.get(), self.hole14.get(), self.hole15.get(),
               self.hole16.get(), self.hole17.get(), self.hole18.get()]
        row = [int(x) for x in row]
        return sum(row)

    def total_front(self):
        row = [self.hole1.get(), self.hole2.get(), self.hole3.get(),
               self.hole4.get(), self.hole5.get(), self.hole6.get(),
               self.hole7.get(), self.hole8.get(), self.hole9.get()]
        row = [int(x) for x in row]
        return sum(row)

    def total_score(self):
        return self.total_front() + self.total_back()

    def update_score(self):
        self.set_total(self.front, self.total_front())
        self.set_total(self.back, self.total_back())
        self.set_total(self.total, self.total_score())


if __name__ == '__main__':
    Gui().mainloop()
