class Cursor():
    def __init__(self, screen, x, y, xmax, ymax, box_xmax, box_ymax, paging):
        self.screen = screen
        self.x = x
        self.y = y
        self.xmax = xmax
        self.ymax = ymax
        self.box_xmax = box_xmax - 2
        self.box_ymax = box_ymax - 2
        self.paging = paging
    

    def up(self, doc, screen):
        if self.y != 0:
            self.y -= 1
            x_end_line = self.paging.get_end_line(doc, self.y, screen)
            if x_end_line < self.x:
                self.x = x_end_line
        elif self.x != 0:
            self.x = 0
            screen.x_interval = [0, self.box_xmax - 2]

        
        if self.y - screen.y_interval[0]+1 == 0 and screen.y_interval[0] != 0:
            screen.update_y_interval(-1)


    def down(self, doc, screen):
        if self.y != len(doc)-1:
            self.y += 1
            x_end_line = self.paging.get_end_line(doc, self.y, screen)
            if x_end_line < self.x:
                self.x = x_end_line
        elif self.x != self.paging.get_end_line(doc, self.y, screen):
            self.x = self.paging.get_end_line(doc, self.y, screen)
            len_line = len(doc[self.y][-1]) + screen.paging.len_pagination(doc, doc[self.y][1])
            screen.x_interval = [len_line-1-self.box_xmax, len_line+1]
        
        if self.box_ymax <= self.y and screen.y_interval[1] <= self.y:
            screen.update_y_interval(1)


    def left(self, doc, screen):
        if self.x != 0:
            self.x -= 1
            if self.x - screen.x_interval[0]+1 == 0 and screen.x_interval[0] != 0:
                screen.update_x_interval(-1)

        elif self.y != 0:
            self.y -= 1
            self.x = self.paging.get_end_line(doc, self.y, screen)


    def right(self, doc, screen):
        if self.x != self.paging.get_end_line(doc, self.y, screen):
            self.x += 1
            if self.box_xmax <= self.x and screen.x_interval[1] <= self.x:
                screen.update_x_interval(1)

        elif self.y != len(doc)-1:
            self.y += 1
            self.x = 0
    

    def add_text(self, doc, text, screen):
        screen.line_reload.append(self.y - screen.y_interval[0])
        text_doc = doc[self.y][-1]
        gap_x = doc[self.y][0]
        doc[self.y][-1] = text_doc[:self.x-gap_x] + text + text_doc[self.x-gap_x:]
        for _ in range(len(text)):
            self.right(doc, screen)
        return doc
    

    def del_text(self, doc, screen):
        screen.line_reload.append(self.y - screen.y_interval[0])
        text_doc = doc[self.y][-1]
        if len(text_doc) != 0 and self.x != 0:
            doc[self.y][-1] = text_doc[:self.x-1] + text_doc[self.x:]
            self.left(doc, screen)
        elif self.x != 0 or self.y != 0: #if we can supr a line or a pagination
            if self.paging.len_pagination(doc, self.y) != 0: #if we can supr a pagination
                doc[self.y][2] = self.paging.move_left_pagination(self.paging.get_pagination(doc, self.y), self.y, screen)
            else:
                doc = self.del_line(doc, screen)
                self.left(doc, screen)
        return doc


    def add_line(self, doc, screen):
        for i in range(self.y+1, len(doc)+1):
            screen.line_reload.append(i - screen.y_interval[0])
        text_line_after_cursor = doc[self.y][-1][self.x:]
        doc[self.y][-1] = doc[self.y][-1][:self.x]
        self.x = 0
        pagination = self.paging.pagination(doc, self.y, screen) #new paging
        doc = doc[:self.y+1] + [[0, self.y+1, pagination, text_line_after_cursor]] + doc[self.y+1:] #add the line in the doc

        for l in doc[self.y+2:]: #changement des numéros de lignes
            l[1] += 1
            doc[l[1]] = l

        self.down(doc, screen)

        screen.refresh_x_interval(doc, screen.cursor.y)

        return doc
    

    def del_line(self, doc, screen):
        text_line_after_cursor = doc[self.y][-1] #get rest
        doc[self.y-1][-1] += text_line_after_cursor #add rest
        doc = doc[:self.y] + doc[self.y+1:] #supr line

        for l in doc[self.y:]:
            l[1] -= 1
            doc[l[1]] = l

        self.y -= 1
        self.x = self.paging.get_end_line(doc, self.y, screen) - len(text_line_after_cursor) + 1
        for i in range(self.y-1, len(doc)):
            screen.line_reload.append(i - screen.y_interval[0])
            
        screen.refresh_x_interval(doc, screen.cursor.y)
        
        return doc


    def move_cursor(self, screen, doc):
        pos_y = self.y - screen.y_interval[0]
        if pos_y >= self.box_ymax:
            pos_y = self.box_ymax - 1

        pos_x = self.x - screen.x_interval[0] + screen.paging.len_pagination(doc, self.y)
        if pos_x >= self.box_xmax:
            pos_x = self.box_xmax - 1

        screen.edit_box.move(pos_y+1, pos_x+1)