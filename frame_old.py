# -*- coding: utf8 -*-
import sys
import math
from tkinter import *
import tkinter as tk
import tkinter.font as font
from tkinter import ttk
import itertools
import nagisa

import Word

def sequence_gen(start):
    i = start
    while True:
        yield i
        i += 1

def multiples_gen(m):
    i = 0
    while True:
        yield i
        i += m

class Application(tk.Frame):
    ROW = 10
    COLUMN = 1
    NEST = 3
    FONT_SIZE = 24
    MY_FONT = ("Helvetica",FONT_SIZE)
    CANVAS_WIDTH = 40
    CANVAS_HEIGHT = 40
    NARROW_SPACE = 1
    WIDE_SPACE = 20
    SCREEN_WIDTH = 1440
    SCREEN_HEIGHT = 870
    WINDOW_WIDTH = COLUMN * CANVAS_WIDTH + (COLUMN - 1) * NARROW_SPACE + (NEST - 1) * (WIDE_SPACE + CANVAS_WIDTH)
    WINDOW_HEIGHT = ROW * CANVAS_HEIGHT + (ROW - 1) * NARROW_SPACE + (NEST - 1) * (WIDE_SPACE + CANVAS_HEIGHT)
    layout = None
    canvases = []
    ids = []
    txt_vars = []
    labels = []
    words = None
    edited_words = None
    arranging = None
    idx = sequence_gen(1)
    display_per_screen = 0
    Dependents = frozenset(["動詞", "形状詞", "形容動詞", "名詞", "副詞", "連体詞", "接続詞", "感動詞"])

    InDependents = frozenset(["助詞", "助動詞", "補助記号", "接尾辞"])

    def __init__(self, master = None):
        super().__init__(master, width = self.WINDOW_WIDTH, height = self.WINDOW_HEIGHT)
        self.master = master
        self.pack()
        self.create_widgets()
        self.on_pressed_return(None)
        self.key_binding()

    def key_binding(self):
        self.master.bind("<Return>",self.on_pressed_return)
        self.master.bind("<Control-v>",self.on_paste)
        self.master.bind("<Button-1>",self.on_left_clicked)

    def create_widgets(self):
        #self.layout = self.fixed_reverse_L
        #self.layout = self.flexible_reverse_L
        #self.layout = self.by_clause;
        #self.layout = self.stripe_by_clause
        self.layout = self.stripe_by_chars
        self.layout();

    def by_clause(self):
        self.arranging = self.arrange_labels
        y = 0
        for i in range(self.ROW):
            var = tk.StringVar()
            self.txt_vars.append(var)
            var.set("文節")
            label = Label(self,textvariable=var,anchor=W,font=self.MY_FONT,justify=CENTER,borderwidth=1,relief=GROOVE)
            self.labels.append(label)
            label.place(x=0,y=y)
            y+=label.winfo_reqheight()+self.NARROW_SPACE

    def stripe_by_chars(self):
        self.arranging = self.arrange_labels
        max_width = 0
        max_height = 0
        for n in range(self.NEST):
            _max_width=max_width
            _max_height=max_height
            for r in range(self.ROW):
                tail = 0
                ground = 0
                for c in range(self.COLUMN):
                    var = tk.StringVar()
                    self.txt_vars.append(var)
                    var.set("字")
                    label = Label(self,textvariable=var,anchor=W,font=self.MY_FONT,justify=CENTER,borderwidth=1,relief=GROOVE)
                    self.labels.append(label)
                    x = max_width + tail
                    w = x+label.winfo_reqwidth()
                    y = r * (label.winfo_reqheight() + self.WIDE_SPACE)
                    h = y+label.winfo_reqheight()
                    label.place(x=x,y=y,width=label.winfo_reqwidth(),height=label.winfo_reqheight())
                    tail += label.winfo_reqwidth()+self.NARROW_SPACE
                    ground += label.winfo_reqheight() + self.WIDE_SPACE
                    if w > _max_width:
                        _max_width = w
                        self.configure(width=_max_width)
                    if h > _max_height:
                        _max_height = h
                        self.configure(height=_max_height)
            max_width=_max_width + self.FONT_SIZE/2*self.WIDE_SPACE
            max_height=_max_height

    def stripe_by_clause(self):
        self.arranging=self.arrange_labels
        max_width = 0
        max_height = 0
        for n in range(self.NEST):
            _max_width=max_width
            _max_height=max_height
            for r in range(self.ROW):
                tail = 0
                ground = 0
                for c in range(self.COLUMN):
                    var = tk.StringVar()
                    self.txt_vars.append(var)
                    var.set("文節")
                    label = Label(self,textvariable=var,anchor=W,font=self.MY_FONT,justify=CENTER,borderwidth=1,relief=GROOVE)
                    self.labels.append(label)
                    x = max_width + tail
                    w = x+label.winfo_reqwidth()
                    y = r * (label.winfo_reqheight() + self.WIDE_SPACE)
                    h = y+label.winfo_reqheight()
                    label.place(x=x,y=y,width=label.winfo_reqwidth(),height=label.winfo_reqheight())
                    tail += label.winfo_reqwidth()+self.NARROW_SPACE
                    ground += label.winfo_reqheight() + self.WIDE_SPACE
                    if w > _max_width:
                        _max_width = w
                        self.configure(width=_max_width)
                    if h > _max_height:
                        _max_height = h
                        self.configure(height=_max_height)
            max_width=_max_width + self.FONT_SIZE/2*self.WIDE_SPACE
            max_height=_max_height

    def flexible_reverse_L(self):
        self.arranging=self.arrange_canvases
        for n in range(self.NEST):
            c = 0
            r = 0
            x=self.WINDOW_WIDTH - (self.COLUMN - c - 1) * (self.CANVAS_WIDTH + self.NARROW_SPACE) - n * (self.CANVAS_WIDTH + self.WIDE_SPACE) - self.CANVAS_WIDTH
            while x > 0:
                c -= 1
                x=self.WINDOW_WIDTH - (self.COLUMN - c - 1) * (self.CANVAS_WIDTH + self.NARROW_SPACE) - n * (self.CANVAS_WIDTH + self.WIDE_SPACE) - self.CANVAS_WIDTH
            while True:
                c += 1
                x=self.WINDOW_WIDTH - (self.COLUMN - c - 1) * (self.CANVAS_WIDTH + self.NARROW_SPACE) - n * (self.CANVAS_WIDTH + self.WIDE_SPACE) - self.CANVAS_WIDTH
                y=n * (self.CANVAS_HEIGHT + self.WIDE_SPACE)
                if x > self.WINDOW_WIDTH-self.CANVAS_WIDTH-self.NARROW_SPACE-n*(self.CANVAS_WIDTH+self.WIDE_SPACE):
                    break
                canvas = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
                canvas.place(x=x, y=y)
                id = canvas.create_text(self.FONT_SIZE, self.FONT_SIZE, font = self.MY_FONT, text = "M")
                self.canvases.append(canvas)
                self.ids.append(id)
            while True:
                x=self.WINDOW_WIDTH - n * (self.CANVAS_WIDTH + self.WIDE_SPACE) - self.CANVAS_WIDTH
                y=n * (self.CANVAS_HEIGHT + self.WIDE_SPACE) + r * (self.CANVAS_HEIGHT + self.NARROW_SPACE)
                if y > self.WINDOW_HEIGHT - self.CANVAS_HEIGHT:
                    break
                canvas = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
                canvas.place(x=x, y=y)
                id = canvas.create_text(self.FONT_SIZE, self.FONT_SIZE,font=self.MY_FONT, text = "M")
                self.canvases.append(canvas)
                self.ids.append(id)
                r += 1

    def fixed_reverse_L(self):
        self.arranging=self.arrange_canvases
        for n in range(self.NEST):
            for c in range(self.COLUMN - 1):
                canvas = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
                canvas.place(x=self.WINDOW_WIDTH - (self.COLUMN - c - 1) * (self.CANVAS_WIDTH + self.NARROW_SPACE) - n * (self.CANVAS_WIDTH + self.WIDE_SPACE) - self.CANVAS_WIDTH, y=n * (self.CANVAS_HEIGHT + self.WIDE_SPACE))
                id = canvas.create_text(self.FONT_SIZE, self.FONT_SIZE, text = "M")
                self.canvases.append(canvas)
                self.ids.append(id)
            for r in range(self.ROW):
                canvas = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
                canvas.place(x=self.WINDOW_WIDTH - n * (self.CANVAS_WIDTH + self.WIDE_SPACE) - self.CANVAS_WIDTH, y=n * (self.CANVAS_HEIGHT + self.WIDE_SPACE) + r * (self.CANVAS_HEIGHT + self.NARROW_SPACE))
                id = canvas.create_text(self.FONT_SIZE, self.FONT_SIZE, text = "M")
                self.canvases.append(canvas)
                self.ids.append(id)

    def arrange_canvases(self, l, pos):
        for i,id in enumerate(self.ids):
            self.canvases[i].itemconfigure(id, text=str(l[i]))

    def arrange_labels(self, words, pos=[]):
        if len(words)==0:
            return
        if pos is not None and len(pos)>0 and self.edited_words is None:
            if self.layout == self.stripe_by_clause:
                phrase_sizes_list = self.make_phrase_sizes_list_by_columns(pos)
                self.insert_spaces(words, pos, phrase_sizes_list)
            if self.layout == self.by_clause:
                phrase_sizes_list = self.make_phrase_sizes_list(pos)
                words=self.make_clauses(words,pos,phrase_sizes_list)
            if self.layout == self.stripe_by_chars:
                phrase_sizes_list = self.make_phrase_sizes_list(pos)
                words = self.make_char_num_limit_clauses(words, phrase_sizes_list, 8)
        for i,var in enumerate(self.txt_vars):
            if len(words) > i:
                    if not self.edited_words is None:
                        next(self.idx)
                    var.set(words[i])
            else:
                var.set("")
    
    def make_char_num_limit_clauses(self, words, phrase_sizes_list, limit = 5):
        print("make_char_num_limit_clauses")
        print("words = {}".format(words))
        print("PSL = {}".format(phrase_sizes_list))
        char_num_list = self.make_char_num_list(words, phrase_sizes_list)
        print("given char_num_list = {}".format(char_num_list))
        new_words = []
        count = 0
        aword = ""
        next_clause_len = 0
        add_idx = 0
        for i in range(len(char_num_list)):
            for j in range(char_num_list[i]):
                if i+add_idx+j < len(words):
                    next_clause_len += len(words[i+add_idx+j])
            if (count != 0) and (count+next_clause_len >= limit):
                new_words.append(aword)
                count = 0
                aword = ""
            for j in range(char_num_list[i]):
                if i+add_idx+j < len(words):
                    aword += words[i+add_idx+j]
            count += next_clause_len
            next_clause_len = 0
            add_idx += char_num_list[i]-1
            print("count = {}, aword = {}".format(count, aword))
        print(new_words)
        self.edited_words = new_words
        return new_words

    def make_clauses(self,words,pos,phrase_sizes_list):
        print("phrase_sizes_list={}".format(phrase_sizes_list))
        flatten = sum(phrase_sizes_list,[])
        print("flatten={}".format(flatten))
        new_words = []
        for i,n in enumerate(flatten):
            tmp =[]
            for j in range(n):
                if len(words) <= i+j:
                    break
                tmp.append(words[i+j])
            if len(tmp) > 0:
                new_words.append(tmp)
        print("new_words={}".format(new_words))
        return new_words

    def insert_spaces(self,words,pos,phrase_sizes_list):
        index = 0
        for i,l in enumerate(phrase_sizes_list):
            count = 0
            over_index = len(l)
            for j,e in enumerate(l):
                count += e
                if over_index == len(l) and count > self.COLUMN:
                    over_index = j
            if over_index != len(l) and i < len(phrase_sizes_list) - 1:
                phrase_sizes_list[i+1][0:0]=l[over_index:]
                del l[over_index:]
                add_num = self.COLUMN - len(l)
                lst = [""] * add_num
                ins = index + over_index
                words[ins:ins] = lst
                pos = lst

            index += self.COLUMN
        print(phrase_sizes_list)
        print(words)

    def make_phrase_sizes_list(self,pos):
        phrase_sizes_list = []
        i = 0
        while True:
            if len(pos) <= i:
                break
            j = 1
            if not pos[i] in self.InDependents:
                while True:
                    if len(pos) <= i+j:
                        break
                    if not pos[i+j] in self.InDependents:
                        if "名詞" == pos[i+j-1] and "動詞" == pos[i+j]:
                            print("Except pattern => {}: {} and {}: {}".format(self.words.words[i+j-1],pos[i+j-1],self.words.words[i+j],pos[i+j]))
                            pass
                        else:
                            break
                    j += 1
                l = [j]
                for k in range(1,j):
                    l.append(0)
                phrase_sizes_list.append(l)
            i += j
        return phrase_sizes_list

    def make_phrase_sizes_list_by_columns(self,pos):
        phrase_sizes_list = []
        for i in multiples_gen(self.COLUMN):
            if i >= len(self.labels):
                break
            phrase_sizes = []
            for j in range(self.COLUMN):
                if i+j < len(self.labels) and i+j<len(pos):
                    pos_ij = pos[i+j]
                    if not "助" in pos_ij:
                        k=1
                        while i+j+k<len(pos):
                            if not "助" in pos[i+j+k]:
                                break
                            k += 1
                    else:
                        k=0
                    phrase_sizes.append(k)
            phrase_sizes_list.append(phrase_sizes)
        return phrase_sizes_list

    def make_char_num_list(self, words, phrase_sizes_list):
        print("make_char_num_list")
        print(phrase_sizes_list)
        sizes = [sum(x) for x in phrase_sizes_list]
        return sizes

    def on_left_clicked(self,event):
        for i,l in enumerate(self.canvases):
            x =int(self.FONT_SIZE/2+l.winfo_x())
            y =int(self.FONT_SIZE/2+l.winfo_y())
            print("t.add_track(({},{}))".format(x,y))

    def on_pressed_return(self,event):
        if self.arranging == self.arrange_labels:
            max = len(self.labels)
        else:
            max = len(self.canvases)
        if self.words is None:
            self.arranging([next(self.idx) for n in range(max)],None)
        elif self.edited_words is None:
            self.arranging(self.words.words,self.words.postags)
            self.format()
        else:
            next_idx = next(self.idx)
            self.arranging(self.edited_words[next_idx:])
            self.format()

    def on_paste(self,event):
        self.words = nagisa.tagging(self.master.clipboard_get())
        self.idx = sequence_gen(0)
        for i in range(len(self.words.words)):
            print("{}: {}".format(self.words.words[i],self.words.postags[i]))
        self.on_pressed_return(None)

    def format(self):
        if self.layout == self.stripe_by_clause or self.layout == self.stripe_by_chars:
            max_height = 0
            max_width = 0
            for i in range(len(self.labels)):
                label_i = self.labels[i]
                if i % (self.COLUMN * self.ROW) == 0:
                    if i == 0:
                        nest_align = 0
                    else:
                        nest_align = max_width + self.FONT_SIZE/2*self.WIDE_SPACE
                if i % self.ROW == 0:
                    diff_y_acc = 0
                if i % self.COLUMN == 0:
                    diff_x = label_i.winfo_reqwidth()-label_i.winfo_width() - self.NARROW_SPACE -  label_i.winfo_x() + nest_align
                    diff_y = label_i.winfo_reqheight()-label_i.winfo_height()
                    label_i.place_configure(x=nest_align, width=label_i.winfo_reqwidth())
                    for j in range(1,self.COLUMN):
                        if i+j == len(self.labels):
                            break
                        label_j = self.labels[i+j]
                        label_j.place_configure(x=label_j.winfo_x()+diff_x)
                        diff_x += label_j.winfo_reqwidth()-label_j.winfo_width() - self.NARROW_SPACE
                        tmp = label_j.winfo_reqheight()-label_j.winfo_height()
                        if diff_y < tmp:
                            diff_y = tmp
                        label_j.place_configure(width=label_j.winfo_reqwidth())
                    for j in range(0,self.COLUMN):
                        if i+j == len(self.labels):
                            break
                        label_j = self.labels[i+j]
                        label_j.place_configure(height=label_j.winfo_reqheight(),y=label_j.winfo_y()+diff_y_acc)
                    diff_y_acc += diff_y
                    w = label_i.winfo_x() + label_i.winfo_reqwidth() 
                    h = label_i.winfo_y() + label_i.winfo_reqheight()
                    if max_width < w:
                        max_width = w
                    if max_height < h:
                        max_height = h
            self.configure(width=max_width + self.NEST * self.COLUMN * self.NARROW_SPACE + self.FONT_SIZE/2*(self.NEST - 1) * self.WIDE_SPACE, height = max_height)
        if self.layout == self.by_clause:
            diff_y = 0
            max_height = 0
            for i in range(len(self.labels)):
                label_i = self.labels[i]
                diff_y += label_i.winfo_reqheight() - label_i.winfo_height()
                label_i.place_configure(y=label_i.winfo_y()+diff_y)
                max_height += label_i.winfo_reqheight() + self.WIDE_SPACE
            print("height={}, reqheight={}".format(self.master.winfo_height(),self.master.winfo_reqheight()))
            self.configure(height=max_height)


    def clear(self):
        for s in root.pack_slaves():
            s.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Pack Three Labels')
    app = Application(master = root)
    root.mainloop()
