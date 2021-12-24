from cursor import Cursor
from paging import Paging
from tools import Tools
import curses

class Screen:
    def __init__(self, screen, doc):
        self.screen = screen

        ymax, xmax = screen.getmaxyx()

        self.line_reload = None

        self.edit_box = curses.newwin(ymax, round((xmax)//2), 0, 0)
        self.view_box = curses.newwin(ymax, xmax-round(xmax/2), 0, xmax//2)
        self.edit_box.box()
        self.view_box.box()
        box_ymax, box_xmax = self.edit_box.getmaxyx()
        
        self.paging = Paging()
        self.tools = Tools()

        self.mode = "edit"

        self.x_interval = [0, box_xmax]
        self.y_interval = [0, box_ymax - 2]

        x = self.paging.len_text(doc, len(doc) - 1, self)
        y = len(doc)-1

        self.cursor = Cursor(screen, x, y, xmax, ymax, box_xmax, box_ymax, self.paging)
        self.refresh_x_interval(doc, y)
    

    def resize(self, doc):
        self.line_reload = None
        self.cursor.ymax, self.cursor.xmax = self.screen.getmaxyx()
        self.edit_box = curses.newwin(self.cursor.ymax, round((self.cursor.xmax)//2), 0, 0)
        self.view_box = curses.newwin(self.cursor.ymax, self.cursor.xmax-round(self.cursor.xmax/2), 0, self.cursor.xmax//2)
        self.edit_box.box()
        self.view_box.box()
        self.cursor.box_ymax, self.cursor.box_xmax = self.edit_box.getmaxyx()
        self.refresh_x_interval(doc, self.cursor.y)
    
    def update_x_interval(self, num):
        self.x_interval[0] += num
        self.x_interval[1] += num
        self.line_reload = None

    def update_y_interval(self, num):
        self.y_interval[0] += num
        self.y_interval[1] += num
        self.line_reload = None
    
    def refresh_x_interval(self, doc, line):
        self.x_interval = [0, self.cursor.box_xmax]
        len_line = len(doc[line][-1]) + self.paging.len_pagination(doc, doc[line][1])
        if len_line - (len_line - self.cursor.x) > self.x_interval[1]:
            self.update_x_interval(len_line - (len_line - self.cursor.x) - self.x_interval[1] + 2)
        else:
            self.line_reload = None
    
    def refresh_y_interval(self, doc):
        self.y_interval = [0, self.cursor.box_ymax - 2]
        if len(doc) - (len(doc) - self.cursor.y) > self.y_interval[1]:
            self.update_y_interval(len(doc) - (len(doc) - self.cursor.y) - self.y_interval[1])
        else:
            self.line_reload = None