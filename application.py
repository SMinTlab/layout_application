import json
import os
import time
import sys
from concurrent.futures import ThreadPoolExecutor
import copy

import tkinter as tk
from tkinter import ttk

from layout_manager import LayoutManager
from layout import Layout
from parser_ import Parser

class Application:

    setting_file_path = './settings'
    main_root = None
    tool_root = None
    main_frame = None
    tool_frame = None
    is_centering = None
    chr_num = 0
    parser = None
    manager = None
    token = None
    indexes = None
    lap_time = None

    def __init__(self):
        def empty2None(d:dict):
            for k in d:
                if isinstance(d[k],dict):
                    empty2None(d[k])
                elif d[k] == '':
                    d[k] = None
        self.lap_time = []
        self.indexes = [[0,0]]
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
        if os.path.isfile(self.setting_file_path):
            with open(self.setting_file_path) as f:
                s = f.read()
                d = json.loads(s)
                empty2None(d)
                self.manager = LayoutManager(self.main_frame,self.tool_frame,d)
        else:
            self.manager = LayoutManager(self.main_frame,self.tool_frame)
        self.manager.layout([x for x in range(self.manager.settings['structure']['nest']*self.manager.settings['structure']['row']*self.manager.settings['structure']['column'])], Layout.STRIPE)
        self.key_binding(self.main_root)
        self.main_frame.focus_set()

    def key_binding(self, target):
        target.bind("<Return>",self.on_pressed_return)
        target.bind("<Control-v>",self.on_paste)
        target.bind("<space>",self.on_pressed_space)
        target.bind("<Key-t>",self.on_pressed_t)

    def on_pressed_return(self, e):
        #print('{} {}'.format(self.indexes[-1],len(self.token.clause_index)))
        if self.indexes[-1][0] < len(self.token.clause_index):
            index = copy.copy(self.indexes[-1])
            new_index = self.manager.layout([''.join(list(map(lambda i : self.token.words[i], clause))).strip() for clause in self.token.clause_index[index[0]:]], Layout.STRIPE)
            index[0] += new_index[0]
            index[1] += new_index[1]
            if len(self.lap_time) > 0:
                s = ''.join(self.manager.now_clause_list)
                self.lap_time.append((s,time.time()))
            self.indexes.append(index)
            print(self.indexes)
            self.manager.progress.configure(value=index[0])

    def on_paste(self, e):
        self.indexes = [[0,0]]
        cb = self.main_root.clipboard_get().strip()
        self.token = self.parser.parse(cb, sys.maxsize)
        self.indexes.append(self.manager.layout([''.join(list(map(lambda i : self.token.words[i], clause))).strip() for clause in self.token.clause_index], Layout.STRIPE))
        self.manager.progress.configure(value=self.indexes[-1][0],maximum=len(self.token.clause_index),mode='determinate')

    def on_pressed_space(self,e):
        if len(self.indexes) > 2:
            self.indexes.pop(-1)
            self.indexes.pop(-1)
            index = copy.copy(self.indexes[-1])
            print(self.indexes)
            new_index = self.manager.layout([''.join(list(map(lambda i : self.token.words[i], clause))).strip() for clause in self.token.clause_index[index[0]:]], Layout.STRIPE)
            index[0] += new_index[0]
            index[1] += new_index[1]
            self.indexes.append(index)
            self.manager.progress.configure(value=index[0])

    def on_pressed_t(self,e):
        if len(self.lap_time) == 0:
            self.lap_time.append(('',time.time()))
        else:
            for i in range(len(self.lap_time)):
                if i != 0:
                    print('Read {} chars in {} sec.'.format(len(self.lap_time[i][0]),self.lap_time[i][1]-self.lap_time[i-1][1]))
            self.lap_time.clear()
  
def main():
    app = Application()
    app.main_root.resizable(0,0)
    app.tool_root.resizable(0,0)
    app.main_root.mainloop()

if __name__ == '__main__':
    main()
