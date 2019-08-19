__author__ = 'Marcus T Taylor'


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


class TreeView(ttk.Treeview):

    def __init__(self, master, database):
        ttk.Treeview.__init__(self, master)
        xsb = ttk.Scrollbar(orient=tk.HORIZONTAL, command=self.xview)
        ysb = ttk.Scrollbar(orient=tk.VERTICAL, command=self.yview)
        self.configure(xscroll=xsb.set)
        self.configure(yscroll=ysb.set)
        self['columns'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                           '13', '14', '15', '16', '17', '18', '19', '20', '21', '22')
        self.column('#0', width=DEFAULT_HEAD_WIDTH_2, stretch=tk.NO, anchor=tk.CENTER)
        for _ in self['columns']:
            if _ in '1':
                width = DEFAULT_HEAD_WIDTH_3
            elif _ in ('11', '21', '22'):
                width = DEFAULT_HEAD_WIDTH_2
            else:
                width = DEFAULT_HEAD_WIDTH_1
            self.column(_, width=width, stretch=tk.NO, anchor=tk.CENTER)
        self.heading('#0', text='Hole')
        for _ in self['columns']:
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
            self.heading(_, text=text)
        connect = db.connect(database)
        cursor = connect.cursor()
        cursor.execute('SELECT course, hole01, hole02, hole03, hole04, hole05, '
                       'hole06, hole07, hole08, hole09, front, hole10, '
                       'hole11, hole12, hole13, hole14, hole15, hole16, '
                       'hole17, hole18, back, total FROM game_stats '
                       'ORDER BY GID DESC')
        for row in cursor.fetchall():
            self.insert('', 'end', values=row)
        connect.close()
        self.grid(row=5, column=0, columnspan=10)


class Gui(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Disc Golfer Keeper')
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
        self.course = ttk.Combobox(data, values=parks)
        self.course.set(parks[0])
        self.course.grid(row=0, column=1)
        holes = FrameRow(self, 1)
        for index in range(0, 9):
            hole = index + 1
            label = f'Hole {hole}'
            LabelText(holes, (0, index), label, DEFAULT_LABEL_WIDTH)
        LabelText(holes, (0, 9), 'Front', DEFAULT_LABEL_WIDTH)
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
        ButtonTotal(buttons, self.total_score)
        ButtonSave(buttons, self.save_game)
        # Scorecard Frame
        scorecard = FrameRow(self, 3)
        self.scorecard = TreeView(scorecard, self.database)

    def save_game(self):
        connect = db.connect(self.database)
        cursor = connect.cursor()
        sql = 'INSERT INTO game_stats ' \
              '(course, hole01, hole02, hole03, hole04, hole05, ' \
              'hole06, hole07, hole08, hole09, front, ' \
              'hole10, hole11, hole12, hole13, hole14, ' \
              'hole15, hole16, hole17, hole18, back, total) ' \
              'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        scores = [self.hole1.get(),
                  self.hole2.get(),
                  self.hole3.get(),
                  self.hole4.get(),
                  self.hole5.get(),
                  self.hole6.get(),
                  self.hole7.get(),
                  self.hole8.get(),
                  self.hole9.get(),
                  self.total_front(),
                  self.hole10.get(),
                  self.hole11.get(),
                  self.hole12.get(),
                  self.hole13.get(),
                  self.hole14.get(),
                  self.hole15.get(),
                  self.hole16.get(),
                  self.hole17.get(),
                  self.hole18.get(),
                  self.total_back(),
                  self.total_front() + self.total_back()]
        scores = [int(x) for x in scores]
        scores.insert(0, self.course.get())
        cursor.execute(sql, tuple(scores))
        connect.commit()
        connect.close()
        self.scorecard.insert('', 0, values=scores)

    def total_back(self):
        row = [self.hole10.get(),
               self.hole11.get(),
               self.hole12.get(),
               self.hole13.get(),
               self.hole14.get(),
               self.hole15.get(),
               self.hole16.get(),
               self.hole17.get(),
               self.hole18.get()]
        row = [int(x) for x in row]
        return sum(row)

    def total_front(self):
        row = [self.hole1.get(),
               self.hole2.get(),
               self.hole3.get(),
               self.hole4.get(),
               self.hole5.get(),
               self.hole6.get(),
               self.hole7.get(),
               self.hole8.get(),
               self.hole9.get()]
        row = [int(x) for x in row]
        return sum(row)

    def total_score(self):
        self.set_total(self.front, self.total_front())
        self.set_total(self.back, self.total_back())
        return self.total_front() + self.total_back()

    @staticmethod
    def set_total(master, value):
        master.configure(state=tk.NORMAL)
        master.delete(0, tk.END)
        master.insert(tk.END, value)
        master.configure(state=tk.DISABLED)


if __name__ == '__main__':
    Gui().mainloop()
