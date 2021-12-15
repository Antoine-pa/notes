class Cursor():
    def __init__(self, screen, x, y, xmax, ymax, paging):
        self.screen = screen
        self.x = x
        self.y = y
        self.xmax = xmax
        self.ymax = ymax
        self.paging = paging
    

    def up(self, doc, screen):
        if self.y != 0:
            self.y -= 1
            x_end_line = self.paging.get_end_line(doc, self.y, screen)
            if x_end_line < self.x:
                self.x = x_end_line
        elif self.x != 0:
            self.x = 0
        
        if self.y - screen.y_start_stop[0]+1 == 0 and screen.y_start_stop[0] != 0:
            screen.y_start_stop[0] -= 1
            screen.y_start_stop[1] -= 1


    def down(self, doc, screen):
        if self.y != len(doc)-1:
            self.y += 1
            x_end_line = self.paging.get_end_line(doc, self.y, screen)
            if x_end_line < self.x:
                self.x = x_end_line
        elif self.x != self.paging.get_end_line(doc, self.y, screen):
            self.x = self.paging.get_end_line(doc, self.y, screen)
        
        if self.ymax <= self.y and screen.y_start_stop[1] <= self.y:
            screen.y_start_stop[0] += 1
            screen.y_start_stop[1] += 1


    def left(self, doc, screen):
        if self.x != 0:
            self.x -= 1

        elif self.y != 0:
            self.y -= 1
            self.x = self.paging.get_end_line(doc, self.y, screen)


    def right(self, doc, screen):
        if self.x != self.paging.get_end_line(doc, self.y, screen):
            self.x += 1

        elif self.y != len(doc)-1:
            self.y += 1
            self.x = 0
    

    def add_text(self, doc, text, screen):
        text_doc = doc[self.y][-1]
        gap_x = doc[self.y][0]
        doc[self.y][-1] = text_doc[:self.x-gap_x] + text + text_doc[self.x-gap_x:]
        for _ in range(len(text)):
            self.right(doc, screen)
        return doc
    

    def del_text(self, doc, screen):
        text_doc = doc[self.y][-1]
        if len(text_doc) != 0 and self.x != 0:
            doc[self.y][-1] = text_doc[:self.x-1] + text_doc[self.x:]
            self.left(doc, screen)
        elif self.x != 0 or self.y != 0: #if we can supr a line or a pagination
            if self.paging.len_pagination(doc, self.y) != 0: #if we can supr a pagination
                doc[self.y][2] = self.paging.move_left_pagination(self.paging.get_pagination(doc, self.y), self.y)
            else:
                doc = self.del_line(doc, screen)
                self.left(doc, screen)
        return doc


    def add_line(self, doc, screen):
        text_line_after_cursor = doc[self.y][-1][self.x:]
        doc[self.y][-1] = doc[self.y][-1][:self.x]
        self.x = 0
        pagination = self.paging.pagination(doc, self.y, screen) #new paging
        doc = doc[:self.y+1] + [[0, self.y+1, pagination, text_line_after_cursor]] + doc[self.y+1:] #add the line in the doc
        for l in doc[self.y+2:]: #changement des numéros de lignes
            l[1] += 1
            doc[l[1]] = l
        self.down(doc, screen)
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
        
        return doc
