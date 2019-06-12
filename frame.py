# -*- coding: utf8 -*-
import sys
import math
from tkinter import *
import tkinter as Tk
import tkinter.font as font

class Application(Tk.Frame):
    ROW = 5
    COLUMN = 5
    max_lable_width = 0
    max_label_height = 0
    FONT_SIZE = 8

    def __init__(self, master = None):
        super().__init__(master, width = 500, height = 500)
        self.master = master
        self.pack()
        frames = []
        labels = []
        vars = []
        lim = 5
        self.create_widgets(frames, labels, vars, lim)
        self.numbering(vars)

    def create_widgets(self, frames, labels, vars, lim):
        if lim >= 0:
            f = Tk.Frame(self.prev_frame(frames),relief = RIDGE, bd = 2)
            frames.append(f)
            f.place(x = 0, rely = 0.2)
            f.propagate(False)
            self.create_widgets(frames, labels, vars, lim-1)
            self.row_into_frame(f, vars, labels)
            self.column_into_frame(f, vars, labels)
            #f.config(height = f['height'] + 1.5*self.COLUMN*self.max_label_height)
            f.config(height=90*self.COLUMN)

    def row_into_frame(self, frame, vars, labels):
        frame.config(height = 300)
        for i in range(self.ROW):
            var = Tk.StringVar()
            var.set(str(i))
            vars.append(var)
            l = Tk.Label(frame, textvariable = var, bg = 'yellow', relief = RIDGE, bd = 2)
            #l.pack(anchor = NE, side = LEFT)
            if l.winfo_reqwidth() > self.max_lable_width:
                self.max_lable_width = l.winfo_reqwidth()
            l.place(x = 1.5*i*l.winfo_reqwidth()+math.floor(len(labels)/self.ROW-1)*(self.max_lable_width),rely = 0)
            labels.append(l)

    def column_into_frame(self, frame, vars, labels):
        frame.config(width = 1.5*(self.ROW+1)*self.max_lable_width+math.floor(len(labels)/self.ROW-1)*(self.max_lable_width))
        for i in range(self.COLUMN):
            var = Tk.StringVar()
            var.set(str(i))
            vars.append(var)
            l = Tk.Label(frame, textvariable = var, bg = 'blue', relief = RIDGE, bd = 2)
            #l.pack(anchor = NW, side = TOP)
            if l.winfo_reqheight() > self.max_label_height:
                self.max_lable_height = l.winfo_reqheight()
            print(self.max_lable_height)
            #l.place(x=1.5*self.ROW*self.max_lable_width+math.floor(10*len(labels)/self.ROW),y=1.5*i*l.winfo_reqheight())
            l.place(relx=1-0.1,y=1.5*i*l.winfo_reqheight())
            labels.append(l)

    def justify_frames(self, frame1, frame2):
        if frame1.winfo_id() is not frame2.winfo_id():
            x_ = frame2.winfo_screenwidth() / self.COLUMN
            y_ = frame1.winfo_screenheight() / self.ROW
            frame1.place(x = x_, y = 0)
            frame2.place(x = 0, y = y_)
            print(str(x_) + "/" +str(y_))

    def numbering(self, vars):
        for i,v in enumerate(vars):
            v.set(str(i))

    def prev_frame(self, frames):
        if len(frames) > 0:
            return frames[len(frames)-1]
        else:
            return self

    def clear(self):
        for s in root.pack_slaves():
            s.destroy()

if __name__ == '__main__':
    root = Tk.Tk()
    root.title('Pack Three Labels')
    app = Application(master = root)
    root.mainloop()
