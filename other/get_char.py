import curses

screen = curses.initscr()
screen.keypad(True)
curses.noecho()

for line in range(screen.getmaxyx()[0]):
    key = screen.getch()
    screen.addstr(line, 0, str(key) + " : " + chr(key))
    screen.refresh()