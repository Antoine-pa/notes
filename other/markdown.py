import mistune #mistune==2.0.0rc1
import json
import curses


class Markdown:
    def __init__(self):
        self.md = mistune.create_markdown(renderer=mistune.AstRenderer(), plugins=['strikethrough']) #'url', 
        self.dict_markdown = {"strong" : curses.A_BOLD, "strikethrough" : "strike", "emphasis" : curses.A_ITALIC, "text" : curses.A_NORMAL}
    
    def strike(self, text):
        return "\u0336".join(text) + "\u0336"

    def markdown(self, doc, line):
        md = self.md(doc[line])[0]["children"] #la ligne
        def children(md, line):
            pass
        for m in md: #parcours de
            _type = self.dict_markdown.get(m["type"])
            if _type is None:
                _type = self.dict_markdown["text"]
            

        return []
text = " "#"yes *ok __yes__*"
print(json.dumps(mistune.create_markdown(renderer=mistune.AstRenderer(), plugins=['strikethrough'])(text), indent=4))