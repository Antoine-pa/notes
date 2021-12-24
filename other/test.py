import curses

screen = curses.initscr()
screen.keypad(True)
curses.noecho()
max_y, max_x = screen.getmaxyx()
#screen.border()

box1 = curses.newwin(max_y, round((max_x)//2), 0, 0)
box1.box()
#box1.addstr()

box2 = curses.newwin(max_y, max_x-round(max_x/2), 0, max_x//2)
box2.box()
#box2.addstr()
box1.addstr(1, 1, "okzef")


while True:
    #key = screen.getch()
    screen.move(2, 1)

    screen.refresh()

    box1.refresh()  
    box2.refresh()
    


curses.endwin()
