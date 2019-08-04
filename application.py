import time
import sys
import math
from concurrent.futures import ThreadPoolExecutor

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from layout_manager import LayoutManager
from layout import Layout
from parser import Parser

class Application:

    root = None
    main_frame = None
    tool_frame = None
    is_centering = None
    chr_num = 0
    parser = None
    manager = None
    token = None
    index = 0

    def __init__(self):
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
        self.root = tk.Tk()
        self.main_frame = ttk.Frame(self.root)
        self.manager = LayoutManager(self.root)
        self.manager.layout([x for x in range(self.manager.settings['structure']['nest']*self.manager.settings['structure']['row']*self.manager.settings['structure']['column'])], Layout.STRIPE)
        self.tool_frame = self.make_tool_frame()
        self.key_binding(self.root)

    def make_tool_frame(self):
        root = tk.Toplevel(self.root)
        frame = ttk.Frame(root)
        self.is_centering = tk.BooleanVar()
        self.is_centering.set(False)
        self.chr_num = tk.DoubleVar()
        def btn_ctr_com():
            if self.is_centering.get():
                self.manager.centering()
            else:
                self.manager.settings['align'] = 'left'
                self.manager.relayout()
            self.root.focus_force()
        def scl_chr_com(*args):
            now = math.floor(self.chr_num.get()) + 1
            #print(now)
            if self.manager.settings['structure']['column'] != now:
                self.manager.settings['structure']['column'] = now
                self.manager.relayout()

        chk_btn_ctr = ttk.Checkbutton(frame,text='centering',command=btn_ctr_com,variable=self.is_centering)
        scl_chr_num = ttk.Scale(frame,orient=HORIZONTAL,length=200,from_=0,to=4,variable=self.chr_num,command=scl_chr_com)
        frame.pack()
        chk_btn_ctr.pack()
        scl_chr_num.pack()
        return frame

    def key_binding(self, target):
        target.bind("<Return>",self.on_pressed_return)
        target.bind("<Control-v>",self.on_paste)
        target.bind("<Button-1>",self.on_left_clicked)

    def on_pressed_return(self, e):
        self.index += self.manager.layout([''.join(list(map(lambda i : self.token.words[i], clause))).strip() for clause in self.token.clause_index[self.index:]], Layout.STRIPE)

    def on_paste(self, e):
        self.index = 0
        self.token = self.parser.parse(self.main_frame.clipboard_get().strip(), sys.maxsize)
        self.index = self.manager.layout([''.join(list(map(lambda i : self.token.words[i], clause))) for clause in self.token.clause_index], Layout.STRIPE)

    def on_left_clicked(self, e):
        #self.manager.centering()
        pass

def main():
    app = Application()
    app.root.mainloop()

if __name__ == '__main__':
    main()
