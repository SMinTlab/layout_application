from threading import Thread

import tkinter as tk
from tkinter import *

from layout import Layout

class LayoutManager:
    target = None
    widgets = []
    now_layout = None
    now_clause_list = None
    update_after = 100
    settings = {'spaces' : {'char' : 1, 'sentence' : 10, 'paragraph' : 20}, 'font' : {'name' : "Helvetica",'size' : 24}, 'canvas' : {'width' : 40, 'height' : 40}, 'label' : {'width' : 40, 'height' : 40}, 'screen' : {'width' : 1440, 'height' : 870}, 'window' : {'width' : 1440, 'height' : 870}, 'structure' : {'nest' : 3, 'row' : 10, 'column' : 10}, 'align' : 'left'}

    def __init__(self, frame: ttk.Frame):
        self.target = frame
        self.init_styles()
        self.target.after(self.update_after, self.update)

    def init_styles(self):
        style = ttk.Style()
        style.theme_use('aqua')
        #print(style.theme_names())
        #style.configure('TLabel',background='#fff')

    def layout(self, clause_list, layout: Layout):
        if layout == Layout.STRIPE:
            self.now_layout = layout
            self.now_clause_list = clause_list
            return self.layout_stripe(clause_list)
        else:
            print("Not implemented layout {}".format(layout))
            return 0

    def relayout(self):
        return self.layout(self.now_clause_list,self.now_layout)

    def clear(self, target):
        for s in target.place_slaves():
            s.destroy()

    def layout_stripe(self, clause_list):
        self.clear(self.target)
        self.widgets.clear()
        index = 0
        max_width = 0
        max_height = 0
        for n in range(self.settings['structure']['nest']):
            _max_width=max_width
            _max_height=max_height
            for r in range(self.settings['structure']['row']):
                tail = 0
                ground = 0
                for c in range(self.settings['structure']['column']):
                    if index >= len(clause_list):
                        txt = ''
                    else:
                        txt = clause_list[index]
                    label = ttk.Label(self.target,text=txt,anchor=W,font=(self.settings['font']['name'], self.settings['font']['size']),justify=CENTER,borderwidth=1,relief=GROOVE)
                    self.widgets.append(label)
                    index += 1
                    x = max_width + tail
                    w = x+label.winfo_reqwidth()
                    y = r * (label.winfo_reqheight() + self.settings['spaces']['sentence'])
                    h = y+label.winfo_reqheight()
                    label.place(x=x,y=y,width=label.winfo_reqwidth(),height=label.winfo_reqheight())
                    tail += label.winfo_reqwidth()+self.settings['spaces']['char'] + 1
                    ground += label.winfo_reqheight() + self.settings['spaces']['sentence'] + 1
                    if w > _max_width:
                        _max_width = w
                        self.target.configure(width=_max_width)
                    if h > _max_height:
                        _max_height = h
                        self.target.configure(height=_max_height)
            max_width=_max_width + self.settings['spaces']['paragraph']
            max_height=_max_height
        self.target.after(self.update_after, self.update)
        #self.target.configure(width = max_width, height = max_height)
        return index

    def centering(self):
        if self.now_layout == Layout.STRIPE:
            self.settings['align'] = 'center'
            index = 0
            all_rows_widths = []
            max_widths = []
            for n in range(self.settings['structure']['nest']):
                _max_width = 0
                row_widths = []
                for r in range(self.settings['structure']['row']):
                    row_width = 0
                    for c in range(self.settings['structure']['column']):
                        row_width += self.widgets[index].winfo_width()
                        index += 1
                    row_widths.append(row_width)
                    if _max_width < row_width:
                        _max_width = row_width
                max_widths.append(_max_width)
                all_rows_widths.append(row_widths)
            index = 0
            for n in range(self.settings['structure']['nest']):
                for r in range(self.settings['structure']['row']):
                    move = (max_widths[n] - all_rows_widths[n][r]) / 2
                    for c in range(self.settings['structure']['column']):
                        label = self.widgets[index]
                        label.place_configure(x = label.winfo_x() + move)
                        index += 1

        else:
            print("Not implemented centering on layout {}".format(self.layout))

    def update(self):
        if self.settings['align'] == 'center':
            self.centering()


def main():
    root = tk.Tk()
    root.title('Frame')
    manager = LayoutManager(root)
    manager.layout([x for x in range(manager.settings['structure']['nest']*manager.settings['structure']['row']*manager.settings['structure']['column'])], Layout.STRIPE)
    root.mainloop()

if __name__ == '__main__':
    main()
