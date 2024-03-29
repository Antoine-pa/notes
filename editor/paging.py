import itertools
from time import sleep

class Paging:
    def __init__(self):
        pass


    def pagination(self, doc, line, screen) -> dict:
        pagination = self.get_pagination(doc, line)
        if 6*len(pagination) < screen.cursor.box_xmax and doc[line][-1] != "":
            pagination = self.move_right_pagination(pagination, line+1, screen)
                
        return pagination
    

    def get_pagination(self, doc, line) -> dict:
        return doc[line][2]
    

    def move_left_pagination(self, pagination, line, screen) -> dict:
        pagination = list(pagination.items())[1:]
        pagination = {str(i+1): pagination[i][1] for i in range(len(pagination))}
        screen.line_reload = None
        return pagination
    

    def move_right_pagination(self, pagination, line, screen) -> dict:
        pagination = list(pagination.items())
        if pagination != []:
            new_pagination = {"1" : 0}
            for i in range(2, len(pagination) + 2):
                new_pagination[str(i)] = pagination[i-2][1]
            screen.line_reload = None
            return new_pagination
        new_pagination = {"1" : 2}
        screen.line_reload = None
        return new_pagination
    

    def len_text(self, doc, line, screen, mode = None) -> int:
        if mode is None:
            mode = screen.mode
        if mode == "view":
            return len("".join(screen.tools.remove_markdown(doc[line][-1])))
        return len(doc[line][-1])
    

    def len_pagination(self, doc, line) -> int:
        return 6*len(doc[line][2])
    

    def get_end_line(self, doc, line, screen, mode = None) -> int:
        if mode is None:
            mode = screen.mode
        return self.len_text(doc, line, screen, mode) + doc[line][0]


    def refresh_pagination(self, doc, screen):
        add_paging = {}
        for line in doc[::-1]: #parcours du doc en sens inverse
            paging = line[2] #pagination de la ligne
            if line != doc[-1] and add_paging != {}: #si ce n'est pas la derniere ligne et qu'il y a de la pagination à ajouter
                for i in range(len(paging)-1):
                    if add_paging.get(str(i+1), None) is None: #si il n'y a pas la pagination est plus longue que celle a ajouter
                        add_paging[str(i+1)] = 0 #on ajouter un cran à vide
                    if paging[str(i+1)] != add_paging[str(i+1)]:
                        paging[str(i+1)] = add_paging[str(i+1)] #on ajouter la pagination
                        if screen.line_reload is not None:
                            screen.line_reload.append(line[1] - screen.y_start_stop[0])
            else: #si c la derniere ligne ou qu'il n'y a rien a ajouter
                for p in paging.items():
                    if p[1] == 1:
                        paging[p[0]] = 0
                        if screen.line_reload is not None:
                            screen.line_reload.append(line[1] - screen.y_start_stop[0])
                
                        
            if paging != {}: #si la ligne a une pagination
                for p in paging.items():
                    if p[1] == 2: #si c'est une fleche
                        add_paging[p[0]] = 1 #on ajoute un niveau de pagination
                        add_paging = dict(itertools.islice(add_paging.items(), int(p[0])))
                    else:
                        if add_paging.get(p[0], None) is None:
                            add_paging[p[0]] = 0
                        else:
                            add_paging[p[0]] = p[1]

            else:
                add_paging = {}

        return doc