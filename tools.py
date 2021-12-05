import curses
class Tools:
    def output(self, doc, _type, screen = None, file = None):
        t = []
        for line in doc:
            pagination = ""
            if len(line[2]) != 0:
                for i in line[2].items():
                    if i[1] == 0:
                        pagination = pagination + "      "
                    elif i[1] == 1:
                        pagination = pagination + "  |   "
                    elif i[1] == 2:
                        pagination = pagination + "  |-> "

            if _type == "screen" and screen is not None:
                if screen.mode == "view":
                    pass
                    """
                    text = line[-1].split("**")
                    if len(text) != 0 and len(text) % 2 != 0:
                        for i in range(0, len(text)-1):
                            if text[i] != "":
                                if i % 2 == 0:
                                    screen.screen.addstr(line[1], line[0], pagination + text[i])
                                else:
                                    screen.screen.addstr(line[1], line[0], pagination + text[i], curses.A_BOLD)
                    """
                else:
                    """
                    text = pagination + line[-1]
                    if len(text) > screen.cursor.xmax:
                        pos_x = screen.cursor.x + len(pagination)
                        if pos_x < screen.cursor.xmax:
                            text = text[:screen.cursor.xmax-1] + ">"
                        else:
                            text = text[pos_x-screen.cursor.xmax+1:pos_x]
                            if pos_x != len(pagination) + len(line[-1]):
                                text += ">"
                    
                    screen.screen.addstr(line[1], line[0], text)
                    """
                    text = line[-1]
                    if len(text) + len(pagination) >= screen.cursor.xmax:
                        pos_x = screen.cursor.x + len(pagination)
                        if pos_x < screen.cursor.xmax:
                            text = text[:screen.cursor.xmax - 1 - len(pagination)] + ">"
                        else:
                            text = text[pos_x-screen.cursor.xmax+1:pos_x - len(pagination)]
                            screen.paging.w(pos_x-screen.cursor.xmax+1, pos_x, text[pos_x-screen.cursor.xmax+1:pos_x])
                            if pos_x != len(pagination) + len(line[-1]):
                                text += ">"
                    screen.screen.addstr(line[1], line[0], pagination + text)
                    
            else:
                t.append(pagination + line[-1])

        
        if _type == "file" and file is not None:
            with open(file, "w") as f:
                f.write("\n".join(t))
    

    def remove_markdown(self, text):
        text = text.split("**")
        return text
    
    def save(self, doc, file):
        self.output(doc, "file", file = file)
    

    def move_cursor(self, screen, doc):
        pos_y = screen.cursor.y
        if pos_y > screen.cursor.ymax:
            pos_y = screen.cursor.ymax - 1

        pos_x = screen.cursor.x + screen.paging.len_pagination(doc, screen.cursor.y)
        if pos_x >= screen.cursor.xmax:
            pos_x = screen.cursor.xmax - 1
            
        screen.screen.move(pos_y, pos_x)