import curses
from time import sleep
import curses 

screen = curses.initscr()

try:
    #screen.border(0)

    box1 = curses.newwin(20, 20, 5, 5)
    box1.box()    

    screen.refresh()
    box1.refresh()

    screen.getch()

finally:
    curses.endwin()

"""
pagination = ""
line = [0, 0]
text = ["", "d", ""]
i = 1
screen.addstr(line[1], line[0], pagination + text[i], curses.A_BOLD)
screen.refresh()
while True:
    pass

"""