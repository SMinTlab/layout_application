# -*- coding: utf8 -*-
import sys
from tkinter import *
import tkinter as Tk

class Application(Tk.Frame):
    def __init__(self, master = None):
        super().__init__(master, width = 500, height = 500)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        frame = []
        labels = []
        vars = []
        for i in range(5):
            if len(frame) > 0:
                f = frame[len(frame)-1]
            else:
                f = self
            f = Tk.Frame(f, relief = RIDGE, bd = 2)
            frame.append(f)
            for j in range(5-i):
                var = Tk.StringVar()
                var.set(str(j))
                vars.append(var)
                l = Tk.Label(f, textvariable = var, bg = 'yellow', relief = RIDGE, bd = 2)
                l.grid(row = 0, column = j+1, stick = N+W)
                labels.append(l)
            for j in range(5-i):
                var = Tk.StringVar()
                var.set(str(j))
                vars.append(var)
                l = Tk.Label(f, textvariable = var, bg = 'blue', relief = RIDGE, bd = 2)
                l.grid(row = j,column = 10-i, stick = N+E)
                labels.append(l)
            f.grid(row = 1, column = 0, columnspan = 10-i, rowspan = 5)
            #f.place(relx=1-i*0.1-0.4,rely=i*0.1)
        for i,v in enumerate(vars):
            v.set(str(i))

if __name__ == '__main__':
    root = Tk.Tk()
    root.title('Pack Three Labels')
    app = Application(master = root)
    root.mainloop()
