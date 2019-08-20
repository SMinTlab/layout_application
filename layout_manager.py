from threading import Thread
import math

import tkinter as tk
from tkinter import *
from tkinter.colorchooser import *
from tkinter.font import Font

from layout import Layout

class LayoutManager:
    main_frame = None
    tool_frame = None
    widgets = []
    now_layout = None
    now_clause_list = None
    update_after = 50
    settings = {'spaces' : {'char' : 1, 'sentence' : 10, 'paragraph' : 20}, 'font' : {'name' : "Helvetica",'size' : 24, 'weight' : 'normal', 'slant': 'roman', 'underline': 'normal', 'overstrike' : 'normal'}, 'canvas' : {'width' : 40, 'height' : 40}, 'label' : {'width' : 40, 'height' : 40}, 'screen' : {'width' : 1440, 'height' : 870}, 'window' : {'width' : 1440, 'height' : 870}, 'structure' : {'nest' : 3, 'row' : 10, 'column' : 20, 'char_lim' : 5}, 'align' : 'left', 'variables' : {'centering' : None, 'char_num' : None}, 'color' : {'foreground' : '#f0f', 'background' : '#fff'}}

    def __init__(self, main_frame: ttk.Frame, tool_frame: ttk.Frame):
        self.main_frame = main_frame
        self.tool_frame = tool_frame
        self.make_tool_frame()
        self.init_styles()
        self.main_frame.after(self.update_after, self.update)

    def make_tool_frame(self):
        def btn_ctr_com():
            if self.settings['variables']['centering'].get():
                self.centering()
            else:
                self.settings['align'] = 'left'
                self.relayout()
            self.main_frame.focus_force()
        def scl_chr_com(*args):
            now = math.floor(self.settings['variables']['char_num'].get()) + 1
            if self.settings['structure']['char_lim'] != now:
                self.settings['structure']['char_lim'] = now
                self.relayout()
        def fg_color_com():
            color = askcolor()
            self.settings['color']['foreground'] = color[1]
            self.relayout()
        self.settings['variables']['centering'] = tk.BooleanVar()
        self.settings['variables']['centering'].set(False)
        self.settings['variables']['char_num'] = tk.DoubleVar()
        self.settings['variables']['char_num'].set(0.0)
        chk_btn_ctr = ttk.Checkbutton(self.tool_frame,text='centering',command=btn_ctr_com,variable=self.settings['variables']['centering'])
        lbl_frm_for_scl_chr_num = ttk.Labelframe(self.tool_frame,text='character limit',labelanchor='n')
        scl_chr_num = ttk.Scale(lbl_frm_for_scl_chr_num,orient=HORIZONTAL,length=200,from_=0,to=19,variable=self.settings['variables']['char_num'],command=scl_chr_com)
        fg_col_but = ttk.Button(self.tool_frame,text='color',command=fg_color_com)
        fg_col_but.pack()
        chk_btn_ctr.pack()
        lbl_frm_for_scl_chr_num.pack()
        lbl_frm_for_scl_chr_num.propagate(True)
        scl_chr_num.pack()
 

    def init_styles(self):
        style = ttk.Style()
        if 'alt' in style.theme_names():
            style.theme_use('alt')
        else:
            style.theme_use(style.theme_names[0])
        #print(style.theme_names())
        style.configure('TLabel',background='#fff')

    def layout(self, clause_list, layout: Layout):
        print(clause_list)
        if layout == Layout.STRIPE:
            self.now_layout = layout
            self.now_clause_list = clause_list
            return self.layout_stripe(clause_list)
        else:
            print("Not implemented layout {}".format(layout))
            return 0

    def relayout(self):
        return self.layout(self.now_clause_list,self.now_layout)

    def clear(self, main_frame):
        for s in main_frame.place_slaves():
            s.destroy()

    def layout_stripe(self, clause_list):
        self.clear(self.main_frame)
        self.widgets = []
        index = 0
        max_width = 0
        max_height = 0
        for n in range(self.settings['structure']['nest']):
            _max_width=max_width
            _max_height=max_height
            row_widgets =[]
            for r in range(self.settings['structure']['row']):
                tail = 0
                ground = 0
                chr_num = 0
                column_widgets = []
                for c in range(self.settings['structure']['column']):
                    if index >= len(clause_list):
                        txt = ''
                    else:
                        txt = clause_list[index]
                    if chr_num > 0 and chr_num + len(str(txt)) > self.settings['structure']['char_lim']:
                        break
                    chr_num += len(str(txt))
                    _font = Font(self.main_frame,family=self.settings['font']['name'],size=self.settings['font']['size'],weight=self.settings['font']['weight'])
                    label = ttk.Label(self.main_frame,text=txt,anchor=W,font=_font,foreground=self.settings['color']['foreground'],justify=CENTER,borderwidth=1,relief=GROOVE)
                    column_widgets.append(label)
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
                        self.main_frame.configure(width=_max_width)
                    if h > _max_height:
                        _max_height = h
                        self.main_frame.configure(height=_max_height)
                row_widgets.append(column_widgets)
            max_width=_max_width + self.settings['spaces']['paragraph']
            max_height=_max_height
            self.widgets.append(row_widgets)
        self.main_frame.after(self.update_after, self.update)
        #self.main_frame.configure(width = max_width, height = max_height)
        return index

    def centering(self):
        if self.now_layout == Layout.STRIPE:
            self.settings['align'] = 'center'
            all_rows_widths = []
            max_widths = []
            for n_w in self.widgets:
                _max_width = 0
                row_widths = []
                for r_w in n_w:
                    row_width = 0
                    for c_w in r_w:
                        row_width += c_w.winfo_width()
                    row_widths.append(row_width)
                    if _max_width < row_width:
                        _max_width = row_width
                max_widths.append(_max_width)
                all_rows_widths.append(row_widths)
            #print(all_rows_widths)
            for n,n_w in enumerate(self.widgets):
                for r,r_w in enumerate(n_w):
                    move = (max_widths[n] - all_rows_widths[n][r]) / 2
                    for c,c_w in enumerate(r_w):
                        label = c_w
                        label.place_configure(x = label.winfo_x() + move)

        else:
            print("Not implemented centering on layout {}".format(self.layout))

    def update(self):
        if self.settings['align'] == 'center':
            self.centering()
        self.main_frame.pack()


def main():
    root = tk.Tk()
    root.title('Frame')
    manager = LayoutManager(root)
    manager.layout([x for x in range(manager.settings['structure']['nest']*manager.settings['structure']['row']*manager.settings['structure']['column'])], Layout.STRIPE)
    root.mainloop()

if __name__ == '__main__':
    main()
