import curses
import curses.ascii
import itertools
from platform import system
from pynput import keyboard
import threading

from cursor import Cursor
from keybinds import Keybinds

text = [[0, 0, {}, "coucou :)"], [0, 1, {"1" : 2}, "voici mon petit programme"], [0, 2, {"1" : 0, "2" : 2}, "xD"]]

class Screen:
    def __init__(self, doc):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        self.doc = doc
        self.loop = True
        self.mode = "edit"
        curses.noecho()

        ymax, xmax = self.screen.getmaxyx()
        if len(self.doc) == 0:
            self.doc = [[0, 0, ""]]
        x = len(self.doc[-1][-1])+self.doc[-1][0]
        y = len(self.doc)-1
        self.cursor = Cursor(self.screen, x, y, xmax, ymax)


    def keybinds(self):
        k = Keybinds(self.screen, self.doc, self.cursor, self.loop, self.mode)
        with keyboard.GlobalHotKeys({
                "<right>" : k.on_activate_right,
                "<left>" : k.on_activate_left,
                "<down>" : k.on_activate_down,
                "<up>" : k.on_activate_up,
                "<home>" : k.on_activate_home,
                "<end>" : k.on_activate_end,

                "<enter>" : k.on_activate_enter,
                "<backspace>" : k.on_activate_delete,
                "<tab>" : k.on_activate_tab,

                "<alt>+<left>" : k.on_activate_alt_left,
                "<alt>+<right>" : k.on_activate_alt_right,

                "<alt>+q": k.on_activate_alt_q,
                "<alt>+e": k.on_activate_alt_e,
                "<alt>+v": k.on_activate_alt_v,
                }) as h:
            h.join()

        #elif key == curses.KEY_RESIZE:
        #    self.cursor.ymax, self.cursor.xmax = self.screen.getmaxyx()
        #else:
        #    self.doc = self.cursor.add_text(self.doc, chr(key))


    def refresh_pagination(self):
        add_paging = {}
        for line in self.doc[::-1]:
            paging = line[2]
            if line != self.doc[-1] and add_paging != {}:
                for i in range(len(paging)-1):
                    if add_paging.get(str(i+1), None) is None:
                        add_paging[str(i+1)] = 0
                    paging[str(i+1)] = add_paging[str(i+1)]
            else:
                for p in paging.items():
                    if p[1] == 1:
                        paging[p[0]] = 0

            for p in paging.items():
                if p[1] == 2: #if it's an arrow
                    add_paging[p[0]] = 1
                    add_paging = dict(itertools.islice(add_paging.items(), int(p[0])))
                else:
                    if add_paging.get(p[0], None) is None:
                        add_paging[p[0]] = 0
                    else:
                        add_paging[p[0]] = p[1]
                    
            self.doc[line[1]][2] = paging


    def refresh(self):
        while self.loop:
            self.screen.clear()
            self.refresh_pagination()
            for line in self.doc:
                pagination = ""
                if len(line[2]) != 0:
                    for i in line[2].items():
                        if i[1] == 0:
                            pagination = pagination + "      "
                        elif i[1] == 1:
                            pagination = pagination + "  |   "
                        elif i[1] == 2:
                            pagination = pagination + "  |-> "
                            
                self.screen.addstr(line[1], line[0], pagination + line[-1])
            self.screen.move(self.cursor.y, self.cursor.x + 6*len(self.doc[self.cursor.y][2]))
            self.screen.refresh()


    def main(self):
        refresh_thread = threading.Thread(target = self.refresh)
        keybinds_thread = threading.Thread(target = self.keybinds)
        
        refresh_thread.start()
        keybinds_thread.start()

        refresh_thread.join()
        keybinds_thread.join()


        self.screen.clear()
        curses.endwin()

        print(self.cursor.x, self.cursor.y, self.cursor.xmax, self.cursor.ymax)
        print(self.doc)

        with open("output.txt", "w") as f:
            text = []
            for line in self.doc:
                pagination = ""
                if len(line[2]) != 0:
                    for i in line[2].items():
                        if i[1] == 0:
                            pagination = pagination + "      "
                        elif i[1] == 1:
                            pagination = pagination + "  |   "
                        elif i[1] == 2:
                            pagination = pagination + "  |-> "
                        
                text.append(pagination + line[-1])
            f.write("\n".join(text))


Screen(text).main()
