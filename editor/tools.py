import curses
import json
import mistune #mistune==2.0.0rc1

class Tools:
    def output(self, doc, _type, screen = None, file = None):
        t = []
        if _type == "screen" and screen is not None:
            doc = doc[screen.y_interval[0]:screen.y_interval[1]]

            if screen.line_reload is not None:
                _doc = []
                for line in screen.line_reload:
                    if len(doc) > line:
                        _doc.append(doc[line])
                    else: #si la ligne a edit est une ligne à supprimer
                        text = "".join([" " for _ in range(screen.cursor.box_xmax-1)])
                        screen.edit_box.addstr(line+1, 1, text)
                        screen.edit_box.addstr(line+1, 1, text)
                doc = _doc
            screen.line_reload = []

        for line in doc:
            pagination = ""
            if len(line[2]) != 0:
                for i in line[2].items():
                    if i[1] == 0:
                        pagination += "      "
                    elif i[1] == 1:
                        pagination += "  |   "
                    elif i[1] == 2:
                        pagination += "  |-> "

            if _type == "screen" and screen is not None:
                if screen.mode == "view":
                    pass
                    """
                    text = line[-1].split("**")
                    if len(text) != 0 and len(text) % 2 != 0:
                        for i in range(0, len(text)-1):
                            if text[i] != "":
                                if i % 2 == 0:
                                    screen.screen.addstr(line[1], 0, pagination + text[i])
                                else:
                                    screen.screen.addstr(line[1], 0, pagination + text[i], curses.A_BOLD)
                    """
                else:
                    text = (pagination + line[-1])[screen.x_interval[0]:screen.x_interval[1]]
                    text += "".join(" " for _ in range(screen.cursor.box_xmax-len(text)))
                    if screen.view_box is not None:
                        screen.view_box.addstr(line[1]-screen.y_interval[0]+1, 1, text)
                        #pass
                    screen.edit_box.addstr(line[1]-screen.y_interval[0]+1, 1, text)
                    
                    
            else:
                t.append(pagination + line[-1])

        
        if _type == "file" and file is not None:
            with open(file, "w") as f:
                f.write("\n".join(t))

    
    def save(self, doc, file):
        self.output(doc, "file", file = file+".txt")
        with open(file+".json", "w") as file:
            file.write(json.dumps(doc, indent=4))
    

    def open_file(self, screen):
        doc = [[0, 0, {}, ""]]
        screen.line_reload = None
        screen.cursor.x = screen.paging.len_text(doc, len(doc) - 1, screen)
        screen.cursor.y = len(doc) - 1
        screen.refresh_x_interval(doc, screen.cursor.x)
        screen.refresh_y_interval(doc)
        return doc


    def debug(self, *t):
        with open("debug.txt", "w") as f:
            f.write(str(t))