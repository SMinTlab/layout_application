import time
import sys
from concurrent.futures import ThreadPoolExecutor

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from layout_manager import LayoutManager
from layout import Layout
from parser import Parser

class Application:

    main_root = None
    tool_root = None
    main_frame = None
    tool_frame = None
    is_centering = None
    chr_num = 0
    parser = None
    manager = None
    token = None
    index = 0

    def __init__(self):
        self.index = 0
        self.chr_num = 0
        ruby = ["《", "》"]
        for_printer1 = ["[", "]"]
        for_printer2 = ["［","］"]
        self.parser = Parser()
        try:
            self.parser.add_ignore(ruby)
            self.parser.add_ignore(for_printer1)
            self.parser.add_ignore(for_printer2)
        except Exception as e:
            print(e)
            sys.exit(1)
        self.main_root = tk.Tk()
        self.tool_root = tk.Toplevel()
        self.main_frame = ttk.Frame(self.main_root)
        self.tool_frame = ttk.Frame(self.tool_root)
        self.manager = LayoutManager(self.main_frame,self.tool_frame)
        self.manager.layout([x for x in range(self.manager.settings['structure']['nest']*self.manager.settings['structure']['row']*self.manager.settings['structure']['column'])], Layout.STRIPE)
        self.key_binding(self.main_root)
        self.main_frame.pack()
        self.tool_frame.pack()

    def key_binding(self, target):
        target.bind("<Return>",self.on_pressed_return)
        target.bind("<Control-v>",self.on_paste)
        target.bind("<Button-1>",self.on_left_clicked)
        target.bind('<Configure>',self.on_configured)

    def on_pressed_return(self, e):
        self.index += self.manager.layout([''.join(list(map(lambda i : self.token.words[i], clause))).strip() for clause in self.token.clause_index[self.index:]], Layout.STRIPE)

    def on_paste(self, e):
        self.index = 0
        cb = self.main_root.clipboard_get().strip()
        self.token = self.parser.parse(cb, sys.maxsize)
        self.index = self.manager.layout([''.join(list(map(lambda i : self.token.words[i], clause))) for clause in self.token.clause_index], Layout.STRIPE)

    def on_left_clicked(self, e):
        #self.manager.centering()
        pass

    def on_configured(self,e):
        print('{}'.format(e))

def main():
    app = Application()
    app.main_root.mainloop()

if __name__ == '__main__':
    main()
