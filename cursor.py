import paging

class Cursor(paging.Paging):
    def __init__(self, screen, x, y, xmax, ymax):
        self.screen = screen
        self.x = x
        self.y = y
        self.xmax = xmax
        self.ymax = ymax
    

    def up(self, doc):
        if self.y != 0:
            self.y -= 1
            x_end_line = self.get_end_line(doc, self.y)
            if x_end_line < self.x:
                self.x = x_end_line
        elif self.x != 0:
            self.x = 0


    def down(self, doc):
        if self.y != len(doc)-1:
            self.y += 1
            x_end_line = self.get_end_line(doc, self.y)
            if x_end_line < self.x:
                self.x = x_end_line
        elif self.x != self.get_end_line(doc, self.y):
            self.x = self.get_end_line(doc, self.y)


    def left(self, doc):
        if self.x != 0:
            self.x -= 1

        elif self.y != 0:
            self.y -= 1
            self.x = self.get_end_line(doc, self.y)


    def right(self, doc):
        if self.x != self.get_end_line(doc, self.y):
            self.x += 1

        elif self.y != len(doc)-1:
            self.y += 1
            self.x = 0
    

    def add_text(self, doc, text):
        text_doc = doc[self.y][-1]
        gap_x = doc[self.y][0]
        doc[self.y][-1] = text_doc[:self.x-gap_x] + text + text_doc[self.x-gap_x:]
        for _ in range(len(text)):
            self.right(doc)
        return doc
    

    def del_text(self, doc):
        line = self.y
        text_doc = doc[line][-1]
        if len(text_doc) != 0 and self.x != 0:
            doc[line][-1] = text_doc[:self.x-1] + text_doc[self.x:]
            self.left(doc)
        elif self.x != 0 or line != 0: #if we can supr a line or a pagination
            if self.len_pagination(doc, line) != 0: #if we can supr a pagination
                doc[line][2] = self.move_left_pagination(self.get_pagination(doc, line), line)
            else:
                doc = self.del_line(doc)
                self.left(doc)
        return doc


    def add_line(self, doc):
        line = self.y
        text_line_after_cursor = doc[line][-1][self.x:]
        doc[line][-1] = doc[line][-1][:self.x]
        self.x = 0
        pagination = self.pagination(doc, line)
        doc = doc[:line+1] + [[0, line+1, pagination, text_line_after_cursor]] + doc[line+1:]
        for l in doc[line+2:]:
            l[1] += 1
            doc[l[1]] = l
        self.down(doc)
        return doc
    

    def del_line(self, doc):
        line = self.y
        text_line_after_cursor = doc[line][-1] #get rest
        doc[line-1][-1] += text_line_after_cursor #add rest
        doc = doc[:line] + doc[line+1:] #supr line

        for l in doc[line:]:
            l[1] -= 1
            doc[l[1]] = l

        self.y -= 1
        line -= 1
        self.x = self.get_end_line(doc, line) - len(text_line_after_cursor) + 1


        return doc
