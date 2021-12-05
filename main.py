from screen import Screen
from platform import system
import curses

text = [[0, 0, {}, "coucou"]]

dict_keybinds_os = {
    "Linux" : {
        "ctrl+alt+q" : 27,
        "del" : 127,
        "ctrl+left-arrow" : 546,
        "ctrl+right-arrow" : 561},
    "Windows" : {
        "ctrl+alt+q" : 17,
        "del" : 8,
        "ctrl+left-arrow" : 443,
        "ctrl+right-arrow" : 444},
    "Darwin" : {
        "ctrl+alt+q" : 0,
        "del" : 0,
        "ctrl+left-arrow" : 0,
        "ctrl+right-arrow" : 0}}

class Window:
    def __init__(self, doc):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        self.doc = doc
        self.file = "output.txt"
        self.loop = True
        curses.noecho()
        self._keybinds = dict_keybinds_os[system()]
        self.screen = Screen(self.screen, self.doc)


    def keybinds(self, key):
        if key == 259:
            self.screen.cursor.up(self.doc, self.screen)
        elif key == 258:
            self.screen.cursor.down(self.doc, self.screen)
        elif key == 260:
            self.screen.cursor.left(self.doc, self.screen)
        elif key == 261:
            self.screen.cursor.right(self.doc, self.screen)
        elif key == 262:
            self.screen.cursor.x = 0
        elif key == 360:
            self.screen.cursor.x = self.screen.paging.get_end_line(self.doc, self.screen)
        elif key == 410:
            self.screen.cursor.ymax, self.screen.cursor.xmax = self.screen.getmaxyx()
        elif key == self._keybinds["ctrl+alt+q"]:
            self.loop = False
        elif key == 10:
            self.doc = self.screen.cursor.add_line(self.doc, self.screen)
        elif key == self._keybinds["del"]:
            self.doc = self.screen.cursor.del_text(self.doc, self.screen)
        elif key == 9:
            self.doc = self.screen.cursor.add_text(self.doc, "    ", self.screen)
        elif key == self._keybinds["ctrl+left-arrow"]:
            self.doc[self.screen.cursor.y][2] = self.screen.paging.move_left_pagination(self.screen.paging.get_pagination(self.doc, self.screen.cursor.y), self.screen.cursor.y)
        elif key == self._keybinds["ctrl+right-arrow"]:
            if self.screen.paging.len_pagination(self.doc, self.screen.cursor.y) + 6 < self.screen.cursor.xmax:
                self.doc[self.screen.cursor.y][2] = self.screen.paging.move_right_pagination(self.screen.paging.get_pagination(self.doc, self.screen.cursor.y), self.screen.cursor.y)
        else:
            self.doc = self.screen.cursor.add_text(self.doc, chr(key), self.screen)



    def refresh(self):
        self.screen.screen.clear()
        self.doc = self.screen.paging.refresh_pagination(self.doc)
        self.screen.tools.output(self.doc, "screen", screen = self.screen)
        self.screen.tools.move_cursor(self.screen, self.doc)
        self.screen.screen.refresh()



    def main(self):
        while self.loop:
            self.refresh()

            key = self.screen.screen.getch()
            self.keybinds(key)

        self.screen.screen.clear()
        curses.endwin()

        print(self.screen.cursor.x, self.screen.cursor.y, self.screen.cursor.xmax, self.screen.cursor.ymax)
        print(self.doc)

        self.screen.tools.save(self.doc, self.file)


if len(text) == 0:
    text = [[0, 0, ""]]

Window(text).main()
