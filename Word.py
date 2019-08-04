class Word:
    length = 0
    pos = "None"
    font_size = 0
    font_name = ""
    body = ""

    def __init__(self, text, font_size = 8, font_name = "Helvetica", pos = ""):
        self.body = text
        self.length = len(text)
        self.font_size = font_size
        self.font_name = font_name
        self.pos = pos
