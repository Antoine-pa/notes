from screen import Screen
from logs.logs import log

from platform import system
from os import remove
import curses
import json

#text = [[0, 0, {}, "coucou"], [0, 1, {"1" : 1}, ""], [0, 2, {"1" : 2}, "test"]]
text = [[0, 0, {}, "01234567890123456789012345678901234567890123456789012345678901234567890123456789"]]

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

dict_special_char = {169 : "é", 160 : "à", 168 : "è", 167 : "ç", 170 : "ê", 174 : "î"}

class Window:
    def __init__(self, doc):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        self.doc = doc
        self.file = "./../output/output"
        self.loop = True
        curses.noecho()
        self._keybinds = dict_keybinds_os[system()]
        self.screen = Screen(self.screen, self.doc)
        self.screen.edit_box.keypad(True)


    def keybinds(self, key):
        if key == 259:
            self.screen.cursor.up(self.doc, self.screen)
        elif key == 258:
            self.screen.cursor.down(self.doc, self.screen)
        elif key == 260:
            self.screen.cursor.left(self.doc, self.screen)
        elif key == 261:
            self.screen.cursor.right(self.doc, self.screen)
        elif key == 262: #retour au début
            self.screen.cursor.x = 0
            self.screen.refresh_x_interval(self.doc, 0)
        elif key == 360: #retour à la fin
            self.screen.cursor.x = self.screen.paging.get_end_line(self.doc, self.screen.cursor.y, self.screen)
        elif key == 410: #resize
            self.screen.resize(self.doc)
        elif key == 15: #ctrl+o
            self.doc = self.screen.tools.open_file(self.screen)
        elif key == 195: #accent circonflexe
            key = self.screen.screen.getch()
            char = dict_special_char.get(key, None)
            if char is None:
                char = chr(key)
            self.doc = self.screen.cursor.add_text(self.doc, char, self.screen)
        elif key == self._keybinds["ctrl+alt+q"]:
            self.loop = False
        elif key == 10: #saut à la ligne
            self.doc = self.screen.cursor.add_line(self.doc, self.screen)
        elif key == self._keybinds["del"]: #suppression
            self.doc = self.screen.cursor.del_text(self.doc, self.screen)
        elif key == 9: #tab
            self.doc = self.screen.cursor.add_text(self.doc, "    ", self.screen)
        elif key == self._keybinds["ctrl+left-arrow"]:
            self.doc[self.screen.cursor.y][2] = self.screen.paging.move_left_pagination(self.screen.paging.get_pagination(self.doc, self.screen.cursor.y), self.screen.cursor.y, self.screen)
        elif key == self._keybinds["ctrl+right-arrow"]:
            if self.screen.paging.len_pagination(self.doc, self.screen.cursor.y) + 6 < self.screen.cursor.box_xmax:
                self.doc[self.screen.cursor.y][2] = self.screen.paging.move_right_pagination(self.screen.paging.get_pagination(self.doc, self.screen.cursor.y), self.screen.cursor.y, self.screen)
        else:
            self.doc = self.screen.cursor.add_text(self.doc, chr(key), self.screen)


    def refresh(self):
        self.doc = self.screen.paging.refresh_pagination(self.doc, self.screen)
        self.screen.tools.output(self.doc, "screen", screen = self.screen)
        self.screen.screen.refresh()
        self.screen.view_box.refresh()
        self.screen.cursor.move_cursor(self.screen, self.doc)
        self.screen.edit_box.refresh()



    def main(self):
        try:
            while self.loop:
                self.refresh()

                key = self.screen.screen.getch()
                self.keybinds(key)
                
        except KeyboardInterrupt:
            pass
        self.screen.screen.clear()
        self.screen.screen.refresh()
        curses.endwin()

        print(self.screen.cursor.x, self.screen.cursor.y, self.screen.cursor.xmax, self.screen.cursor.ymax, self.screen.cursor.box_xmax, self.screen.cursor.box_ymax)
        print(self.doc)

        self.screen.tools.save(self.doc, self.file)

        try: remove("debug.txt")
        except: pass


if len(text) == 0:
    text = [[0, 0, ""]]
"""
with open(f'/home/antoine/Desktop/lectures-lineaires/Spleen_Laforgue/fiche.json', "r") as file:
	text = json.load(file)
"""
Window(text).main()
