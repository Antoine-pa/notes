from cursor import Cursor
from paging import Paging
from tools import Tools

class Screen:
    def __init__(self, screen, doc):
        self.screen = screen
        
        self.paging = Paging()
        self.tools = Tools()

        self.mode = "edit"
        ymax, xmax = screen.getmaxyx()
        self.y_start_stop = [0, ymax]
        if len(doc) == 0:
            doc = [[0, 0, ""]]
        x = self.paging.len_text(doc, len(doc) - 1, self)
        y = len(doc)-1


        self.cursor = Cursor(screen, x, y, xmax, ymax, self.paging)
