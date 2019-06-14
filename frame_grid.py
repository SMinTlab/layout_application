# -*- coding: utf8 -*-
import sys
import math
from tkinter import *
import tkinter as tk
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
    NUM_CHAR = 1
    ROW = 15
    COLUMN = int(25/NUM_CHAR)
    NEST = 3
    MY_LABEL_STYLE_NAME = "my.TLabel"
    font_size = 50
    MY_FONT = ("Helvetica",font_size)
    ROTATE_SYMBOLS = ['（','）','(',')']
    TRANS_SYMBOLS = ['、','。']
    style = None
    ids = []
    canvases = []
    words = None
    idx = [0,0]

    _num_max = 1000

    def __init__(self, master = None):
        super().__init__(master=None)
        self.master = master
        self.style = ttk.Style()
        self.style.configure(self.MY_LABEL_STYLE_NAME,font=self.MY_FONT)
        self.create_widgets()
        self.words = [list(takewhile(lambda n : n < self._num_max,N(0)))]
        self.arranging(self.words)
        self.key_binding()
        self.pack()

    def key_binding(self):
        self.master.bind("<Return>",self.on_pressed_return)
        self.master.bind("<Control-v>",self.on_paste)
        self.master.bind("<Control-Key-plus>",self.on_pressed_ctrl_plus)
        self.master.bind("<Control-Key-minus>",self.on_pressed_ctrl_minus)
        self.master.bind("<Button-1>",self.on_left_clicked)

    def create_widgets(self):
        for i in range(self.NEST):
            for j in range(self.COLUMN-2*i):
                label = tk.Canvas(self,width=self.NUM_CHAR*self.font_size,height=self.font_size)
                label.grid(column=j,row=2*i,sticky=NSEW)
                id = label.create_text(self.font_size/2*self.NUM_CHAR,self.font_size/2,text="M",font=self.MY_FONT)
                self.ids.append(id)
                self.canvases.append(label)
                self.columnconfigure(j,weight=1)
            for k in range(1,self.ROW-2*i):
                label = tk.Canvas(self,width=self.NUM_CHAR*self.font_size,height=self.font_size)
                label.grid(column=j,row=2*i+k,sticky=NSEW)
                id = label.create_text(self.font_size/2*self.NUM_CHAR,self.font_size/2,text="M",font=self.MY_FONT)
                self.ids.append(id)
                self.canvases.append(label)
                self.rowconfigure(2*i+k,weight=1)
        self.grid(column=0,row=0,sticky=NSEW)
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=1)

    def on_left_clicked(self,event):
        for i,l in enumerate(self.canvases):
            print("{}: x={}, y={}".format(i,l.winfo_x(),l.winfo_y()))

    def on_pressed_return(self,event):
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

    def on_pressed_ctrl_plus(self,event):
        print(str(self.font_size) + " => ")
        self.font_size += 5
        print(self.font_size)
        self.style.configure(self.MY_LABEL_STYLE_NAME,font=("Helvetica",self.font_size))

    def on_pressed_ctrl_minus(self,event):
        print(str(self.font_size) + " => ")
        self.font_size -= 5
        if self.font_size < 0:
            self.font_size = 0
        print(self.font_size)
        self.style.configure(self.MY_LABEL_STYLE_NAME,font=("Helvetica",self.font_size))

    def arranging(self, words):
        finalize=False
        for i, v in enumerate(self.ids):
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
            """
            if self.contains_symbol(s):
                angle = 90
            else:
                angle = 0
            """
            self.canvases[i].itemconfigure(v,text=s,angle=0)

    def is_symbol(self, ch, symbols):
        for s in symbols:
            if s == ch:
                return True
        return False

    def contains_symbol(self, str, symbols):
        for s in str:
            if self.is_symbol(s,symbols):
                return True
        return False

    def clear(self):
        for s in root.pack_slaves():
            s.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('L ettering')
    app = Application(master = root)
    root.mainloop()
