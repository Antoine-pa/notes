class Paging:
    def __init__(self):
        pass


    def pagination(self, doc, line) -> dict:
        #self.w(doc)
        if len(doc)-1 == line: #last line
            pagination = self.get_pagination(doc, line)
            pagination = self.move_right_pagination(pagination, line)
        elif line == 0: #first line
            pagination = []
        else:
            paging_before = self.get_pagination(doc, line-1)
            paging_after = self.get_pagination(doc, line+1)

            pagination = paging_before
            if len(paging_after) > len(paging_before):
                pagination = paging_after
            else:
                pagination = self.move_right_pagination(pagination, line)
                
        return pagination
    

    def get_pagination(self, doc, line) -> dict:
        return doc[line][2]
    

    def move_left_pagination(self, pagination, line) -> dict:
        pagination = list(pagination.items())[1:]
        pagination = {str(i+1): pagination[i][1] for i in range(len(pagination))}
        return pagination
    

    def move_right_pagination(self, pagination, line) -> dict:
        pagination = list(pagination.items())
        new_pagination = {"1" : 0}
        for i in range(2, len(pagination) + 2):
            new_pagination[str(i)] = pagination[i-2][1]
        return new_pagination
    

    def len_line(self, doc, line) -> int:
        return len(doc[line][-1]) - len(doc[line][2]) + len(doc[line][2])
    

    def len_pagination(self, doc, line) -> int:
        return 6*len(doc[line][2])
    

    def get_end_line(self, doc, line) -> int:
        return self.len_line(doc, line) + doc[line][0]




    def w(self, *t):
        with open("write.txt", "w") as f:
            f.write(str(t))