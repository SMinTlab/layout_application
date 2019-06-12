# -*- coding: utf8 -*-
import sys
import math
from tkinter import *
import tkinter as Tk
import tkinter.font as font
from tkinter import ttk
import nagisa
from itertools import takewhile

def N(s):
    n = s
    while True:
        n += 1
        yield n

class Application(ttk.Frame):
    ROW = 10
    COLUMN = 1
    NEST = 10
    NUM_CHAR = 3
    MY_LABEL_STYLE_NAME = "my.TLabel"
    style = None
    font_size = 15
    vars = []
    words = None
    idx = [0,0]

    _num_max = 1000

    def __init__(self, master = None):
        super().__init__(master=None)
        self.master = master
        self.style = ttk.Style()
        self.style.configure(self.MY_LABEL_STYLE_NAME,font=("Helvetica",self.font_size))
        self.create_widgets()
        self.words = [list(takewhile(lambda n : n < self._num_max,N(0)))]
        self.arranging(self.words)
        self.key_binding()

    def key_binding(self):
        self.master.bind("<Button-1>",self.on_button_pressed)
        self.master.bind("<Control-v>",self.on_paste)
        self.master.bind("<Control-Key-plus>",self.on_press_ctrl_plus)
        self.master.bind("<Control-Key-minus>",self.on_press_ctrl_minus)
        self.master.bind("<Configure>",self.on_configured)

    def create_widgets(self):
        for i in range(self.NEST):
            for j in range(self.COLUMN-2*i):
                var = Tk.StringVar()
                self.vars.append(var)
                ttk.Label(self,textvariable=var,style=self.MY_LABEL_STYLE_NAME).grid(column=j,row=2*i,sticky=NSEW)
                self.columnconfigure(j,weight=1)
            for k in range(1,self.ROW-2*i):
                var = Tk.StringVar()
                self.vars.append(var)
                ttk.Label(self,textvariable=var,style=self.MY_LABEL_STYLE_NAME).grid(column=j,row=2*i+k,sticky=NSEW)
                self.rowconfigure(2*i+k,weight=1)
        self.grid(column=0,row=0,sticky=NSEW)
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=1)

    def on_button_pressed(self,event):
        if isinstance(self.words,list):
            if self.idx[1] > self._num_max / 2:
                self._num_max += self._num_max / 2
                self.words = [list(takewhile(lambda n : n < self._num_max,N(self.idx[1])))]
            self.arranging(self.words)
        else:
            self.arranging(self.words.words)

    def on_paste(self,event):
        self.words = nagisa.tagging(self.master.clipboard_get())
        print(self.words.words)
        self.idx = [0,0]
        self.arranging(self.words.words)

    def on_press_ctrl_plus(self,event):
        print(str(self.font_size) + " => ")
        self.font_size += 5
        print(self.font_size)
        self.style.configure(self.MY_LABEL_STYLE_NAME,font=("Helvetica",self.font_size))

    def on_press_ctrl_minus(self,event):
        print(str(self.font_size) + " => ")
        self.font_size -= 5
        if self.font_size < 0:
            self.font_size = 0
        print(self.font_size)
        self.style.configure(self.MY_LABEL_STYLE_NAME,font=("Helvetica",self.font_size))

    def on_configured(self,event):
        print(event)
        print(self.master.geometry())

    def arranging(self, words):
        finalize=False
        for v in self.vars:
            s=""
            for n in range(self.NUM_CHAR):
                if finalize:
                    s += ""
                else:
                    if self.idx[1] >= len(words[self.idx[0]]):
                        self.idx[0] += 1
                        self.idx[1] = 0
                    if self.idx[0] < len(words):
                        s += str(words[self.idx[0]][self.idx[1]])
                        self.idx[1] += 1
                    else:
                        finalize = True
                        s += ""
            v.set(s)

    def numbering(self):
        for i,v in enumerate(self.vars):
            v.set(str(i))

    def clear(self):
        for s in root.pack_slaves():
            s.destroy()

if __name__ == '__main__':
    root = Tk.Tk()
    root.title('Pack Three Labels')
    app = Application(master = root)
    root.mainloop()
