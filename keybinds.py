class Keybinds:
    def __init__(self, screen, doc, cursor, loop, mode):
        self.screen = screen
        self.doc = doc
        self.cursor = cursor
        self.loop = loop
        self.mode = mode


    def on_activate_right(self):
        self.cursor.right(self.doc)

    def on_activate_left(self):
        self.cursor.left(self.doc)

    def on_activate_down(self):
        self.cursor.down(self.doc)

    def on_activate_up(self):
        self.cursor.up(self.doc)
    
    def on_activate_home(self):
        self.cursor.x = 0
    
    def on_activate_end(self):
        self.cursor.x = self.cursor.get_end_line(self.doc)


    def on_activate_enter(self):
        self.doc = self.cursor.add_line(self.doc)
    
    def on_activate_delete(self):
        self.doc = self.cursor.del_text(self.doc)
    
    def on_activate_tab(self):
        self.doc = self.cursor.add_text(self.doc, "    ")
    
    
    def on_activate_alt_left(self):
        self.doc[self.cursor.y][2] = self.cursor.move_left_pagination(self.cursor.get_pagination(self.doc, self.cursor.y), self.cursor.y)
    
    def on_activate_alt_right(self):
        self.doc[self.cursor.y][2] = self.cursor.move_right_pagination(self.cursor.get_pagination(self.doc, self.cursor.y), self.cursor.y)


    def on_activate_alt_q(self):
        self.loop = False

    def on_activate_alt_e(self):
        self.mode = "edit"

    def on_activate_alt_v(self):
        self.mode = "view"