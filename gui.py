from tkinter import ttk
import getpass as gp
import os
import sqlite3 as db
import tkinter as tk

DEFAULT_FONT_ENTRY = ('Helvetica', 13)
DEFAULT_FONT_LABEL = ('Helvetica', 12)
DEFAULT_LABEL_WIDTH = 7
DEFAULT_TV_WIDTH_1 = 35
DEFAULT_TV_WIDTH_2 = 55


class ButtonSave(ttk.Button):

    def __init__(self, master, command):
        ttk.Button.__init__(self, master)
        self['command'] = command
        self['text'] = 'Save'
        self['width'] = 10
        self.grid(row=4, column=0, columnspan=11, pady=(15, 0))


class CreateGameForm(ttk.Frame):

    def __init__(self, master, database):
        self.database = database
        ttk.Frame.__init__(self, master)
        self.grid(row=0, column=0, padx=10, pady=10)
        for index in range(0, 9):
            hole = index + 1
            label = hole
            LabelText(self, (0, index), label, DEFAULT_LABEL_WIDTH)
        LabelText(self, (0, 9), 'Front', DEFAULT_LABEL_WIDTH)
        LabelText(self, (0, 10), 'Total', 14)
        self.hole1 = EntryHole(self, (1, 0), self.update_score)
        self.hole2 = EntryHole(self, (1, 1), self.update_score)
        self.hole3 = EntryHole(self, (1, 2), self.update_score)
        self.hole4 = EntryHole(self, (1, 3), self.update_score)
        self.hole5 = EntryHole(self, (1, 4), self.update_score)
        self.hole6 = EntryHole(self, (1, 5), self.update_score)
        self.hole7 = EntryHole(self, (1, 6), self.update_score)
        self.hole8 = EntryHole(self, (1, 7), self.update_score)
        self.hole9 = EntryHole(self, (1, 8), self.update_score)
        self.front = EntryTotalSub(self, (1, 9))
        self.total = EntryTotalMain(self, (1, 10))
        for index in range(10, 19):
            hole = index
            label = f'{hole}'
            LabelText(self, (2, index - 10), label, DEFAULT_LABEL_WIDTH)
        LabelText(self, (2, 9), 'Back', DEFAULT_LABEL_WIDTH)
        self.hole10 = EntryHole(self, (3, 0), self.update_score)
        self.hole11 = EntryHole(self, (3, 1), self.update_score)
        self.hole12 = EntryHole(self, (3, 2), self.update_score)
        self.hole13 = EntryHole(self, (3, 3), self.update_score)
        self.hole14 = EntryHole(self, (3, 4), self.update_score)
        self.hole15 = EntryHole(self, (3, 5), self.update_score)
        self.hole16 = EntryHole(self, (3, 6), self.update_score)
        self.hole17 = EntryHole(self, (3, 7), self.update_score)
        self.hole18 = EntryHole(self, (3, 8), self.update_score)
        self.back = EntryTotalSub(self, (3, 9))
        ButtonSave(self, self.save_game)

    def save_game(self):
        connect = db.connect(self.database)
        cursor = connect.cursor()
        sql = 'INSERT INTO game_stats ' \
              '(hole01, hole02, hole03, hole04, hole05, ' \
              'hole06, hole07, hole08, hole09, front, ' \
              'hole10, hole11, hole12, hole13, hole14, ' \
              'hole15, hole16, hole17, hole18, back, total) ' \
              'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        scores = [self.hole1.get(), self.hole2.get(), self.hole3.get(),
                  self.hole4.get(), self.hole5.get(), self.hole6.get(),
                  self.hole7.get(), self.hole8.get(), self.hole9.get(),
                  self.total_sub('front'), self.hole10.get(), self.hole11.get(),
                  self.hole12.get(), self.hole13.get(), self.hole14.get(),
                  self.hole15.get(), self.hole16.get(), self.hole17.get(),
                  self.hole18.get(), self.total_sub('back'), self.total_score()]
        scores = [int(x) for x in scores]
        try:
            cursor.execute(sql, tuple(scores))
        except db.OperationalError as OPError:
            print(OPError)
        except db.ProgrammingError as PROError:
            print(PROError)
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

    def total_score(self):
        return self.total_sub('back') + self.total_sub('front')

    def total_sub(self, side):
        row = []
        if side == 'back':
            row = [self.hole10.get(), self.hole11.get(), self.hole12.get(),
                   self.hole13.get(), self.hole14.get(), self.hole15.get(),
                   self.hole16.get(), self.hole17.get(), self.hole18.get()]
        if side == 'front':
            row = [self.hole1.get(), self.hole2.get(), self.hole3.get(),
                   self.hole4.get(), self.hole5.get(), self.hole6.get(),
                   self.hole7.get(), self.hole8.get(), self.hole9.get()]
        row = [int(x) for x in row]
        return sum(row)

    def update_score(self, event):
        print(event)
        self.set_total(self.front, self.total_sub('front'))
        self.set_total(self.back, self.total_sub('back'))
        self.set_total(self.total, self.total_score())


class CreateScorecard(ttk.Frame):

    def __init__(self, master, database):
        self.database = database
        ttk.Frame.__init__(self, master)
        self.grid(row=1, column=0, padx=10, pady=10)
        self.score_card = ttk.Treeview(self)
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.score_card.yview)
        self.score_card.configure(yscroll=ysb.set)
        ysb.grid(row=0, column=1, sticky=tk.NE + tk.SE)
        self.score_card['columns'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9',
                                      '10', '11', '12', '13', '14', '15', '16', '17',
                                      '18', '19', '20', '21')
        self.score_card['height'] = 10
        self.score_card['selectmode'] = 'browse'
        self.score_card['show'] = 'headings'
        for _ in self.score_card['columns']:
            if _ in ('10', '20', '21'):
                width = DEFAULT_TV_WIDTH_2
            else:
                width = DEFAULT_TV_WIDTH_1
            self.score_card.column(_, width=width, stretch=tk.NO, anchor=tk.CENTER)
        for _ in self.score_card['columns']:
            if _ == '10':
                text = 'Front'
            elif _ == '20':
                text = 'Back'
            elif _ == '21':
                text = 'Total'
            else:
                header = int(_)
                if header > 10:
                    text = header - 1
                else:
                    text = header
            self.score_card.heading(_, text=text)
        self.score_card.grid(row=0, column=0)
        self.score_card.after(1000, self._load)

    def _load(self):
        children = self.score_card.get_children()
        if children:
            for _ in children:
                self.score_card.delete(_)
        connect = db.connect(self.database)
        cursor = connect.cursor()
        try:
            cursor.execute('SELECT hole01, hole02, hole03, hole04, hole05, '
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
            self.score_card.after(300000, self._load)


class EntryHole(ttk.Entry):

    def __init__(self, master, index, callback):
        ttk.Entry.__init__(self, master)
        self['font'] = DEFAULT_FONT_ENTRY
        self['justify'] = 'center'
        self['width'] = 3
        self.insert(tk.END, 0)
        self.bind('<FocusOut>', callback)
        self.grid(row=index[0], column=index[1])


class EntryTotalMain(ttk.Entry):

    def __init__(self, master, index):
        ttk.Entry.__init__(self, master)
        self['font'] = ('Helvetica', 52)
        self['justify'] = 'center'
        self['state'] = tk.DISABLED
        self['width'] = 3
        self.grid(row=index[0], column=index[1], rowspan=3)


class EntryTotalSub(ttk.Entry):

    def __init__(self, master, index):
        ttk.Entry.__init__(self, master)
        self['font'] = DEFAULT_FONT_ENTRY
        self['justify'] = 'center'
        self['state'] = tk.DISABLED
        self['width'] = 3
        self.insert(tk.END, 0)
        self.grid(row=index[0], column=index[1])


class LabelText(ttk.Label):

    def __init__(self, master, index, text, width):
        ttk.Label.__init__(self, master)
        self['anchor'] = tk.CENTER
        self['font'] = DEFAULT_FONT_LABEL
        self['text'] = text
        self['width'] = width
        self.grid(row=index[0], column=index[1])


class CreateGui(tk.Tk):

    def __init__(self):
        # Database checking.
        data_dir = os.path.abspath(__file__)
        database = data_dir.replace(os.path.basename(__file__), 'database/dgk.sqlite')
        try:
            if not os.path.exists(database):
                raise FileNotFoundError
            else:
                self.database = database
        except FileNotFoundError:
            exit('Database file not found! Exiting...')
        # Create application window
        tk.Tk.__init__(self)
        self.title(f'Disc Golfer Keeper - {gp.getuser()}')
        self.resizable(False, False)
        self['background'] = 'gray91'
        self['bd'] = 1
        self['relief'] = tk.GROOVE
        self['takefocus'] = True
        CreateGameForm(self, self.database)
        CreateScorecard(self, self.database)


if __name__ == '__main__':
    CreateGui().mainloop()
