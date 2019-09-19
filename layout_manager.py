from threading import Thread
import math

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.colorchooser import *
from tkinter.font import Font

from layout import Layout

class LayoutManager:
    main_frame = None
    tool_frame = None
    progress = None
    widgets = []
    now_layout = None
    now_clause_list = None
    index = None
    update_after = 50
    settings = {'spaces' : {'char' : 1, 'sentence' : 10, 'paragraph' : 20}, 'font' : {'name' : "Helvetica",'size' : 24, 'weight' : 'normal', 'slant': 'roman', 'underline': 'normal', 'overstrike' : 'normal'}, 'canvas' : {'width' : 40, 'height' : 40}, 'label' : {'width' : 40, 'height' : 40}, 'screen' : {'width' : 1440, 'height' : 870}, 'window' : {'width' : 1440, 'height' : 870}, 'structure' : {'nest' : 3, 'row' : 10, 'column' : 20, 'char_lim' : 5, 'strict_char_lim' : 5}, 'align' : 'left', 'variables' : {'centering' : None, 'char_num' : None, 'size' : None, 'nest_num' : None, 'time' : None}, 'color' : {'foreground' : '#f0f', 'background' : '#fff'}}

    def __init__(self, main_frame: ttk.Frame, tool_frame: ttk.Frame, settings=None):
        if not settings is None:
            self.settings = settings
        self.main_frame = main_frame
        self.tool_frame = tool_frame
        self.init_styles()
        self.make_tool_frame()
        self.index = [0,0]

    def make_tool_frame(self):
        """Widget's command functions"""
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
        def scl_siz_com(*args):
            now = math.floor(self.settings['variables']['size'].get()) + 1
            now *= 10
            self.settings['font']['size'] = now
            self.relayout()
        def scl_nst_com(*args):
            now = math.floor(self.settings['variables']['nest_num'].get()) + 1
            self.settings['structure']['nest'] = now
            self.relayout()

        def fg_color_com():
            color = askcolor()
            self.settings['color']['foreground'] = color[1]
            style=ttk.Style()
            style.configure('MainFrame.TLabel',foreground=color[1])
            self.main_frame.focus_set()
            #self.relayout()
        def bg_color_com():
            color = askcolor()
            self.settings['color']['background'] = color[1]
            style=ttk.Style()
            style.configure('MainFrame.TFrame',background=color[1])
            style.configure('MainFrame.TLabel',background=color[1])
            self.main_frame.focus_set()
            #self.relayout()

        """Registering tk variables to setting dict"""
        self.settings['variables']['centering'] = tk.BooleanVar()
        self.settings['variables']['centering'].set(False)
        self.settings['variables']['char_num'] = tk.DoubleVar()
        self.settings['variables']['char_num'].set(0.0)
        self.settings['variables']['nest_num'] = tk.DoubleVar()
        self.settings['variables']['nest_num'].set(False)
        self.settings['variables']['size'] = tk.DoubleVar()
        self.settings['variables']['size'].set(0.0)

        """Create tk(ttk) objects"""
        self.progress = ttk.Progressbar(self.tool_frame)
        chk_btn_ctr = ttk.Checkbutton(self.tool_frame,text='centering',command=btn_ctr_com,variable=self.settings['variables']['centering'])
        lbl_frm_for_scl_chr_num = ttk.Labelframe(self.tool_frame,text='character limit',labelanchor='n')
        lbl_frm_for_scl_siz = ttk.Labelframe(self.tool_frame,text='size',labelanchor='n')
        lbl_frm_for_col = ttk.Labelframe(self.tool_frame,text='colors',labelanchor='n')
        lbl_frm_for_scl_nst = ttk.Labelframe(self.tool_frame,text='nest number',labelanchor='n')
        scl_chr_num = ttk.Scale(lbl_frm_for_scl_chr_num,orient=HORIZONTAL,length=200,from_=0,to=19,variable=self.settings['variables']['char_num'],command=scl_chr_com)
        scl_siz = ttk.Scale(lbl_frm_for_scl_siz,orient=HORIZONTAL,length=200,from_=0,to=10,variable=self.settings['variables']['size'],command=scl_siz_com)
        fg_col_but = ttk.Button(lbl_frm_for_col,text='foreground color',command=fg_color_com)
        bg_col_but = ttk.Button(lbl_frm_for_col,text='background color',command=bg_color_com)
        scl_nst = ttk.Scale(lbl_frm_for_scl_nst,orient=HORIZONTAL,length=200,from_=0,to=10,variable=self.settings['variables']['nest_num'],command=scl_nst_com)

        """Packing"""
        lbl_frm_for_col.pack()
        fg_col_but.pack()
        bg_col_but.pack()
        chk_btn_ctr.pack()
        lbl_frm_for_scl_chr_num.pack()
        scl_chr_num.pack()
        lbl_frm_for_scl_nst.pack()
        scl_nst.pack()
        lbl_frm_for_scl_siz.pack()
        scl_siz.pack()
        self.progress.pack()
        self.tool_frame.pack() 
    
    def init_styles(self):
        style = ttk.Style()
        if 'default' in style.theme_names():
            style.theme_use('default')
        else:
            style.theme_use(list(style.theme_names())[0])
        #print(style.theme_names())
        style.configure('MainFrame.TFrame',foreground=self.settings['color']['foreground'],background=self.settings['color']['background'])
        self.main_frame.configure(style='MainFrame.TFrame')

    def next(self):
        self.layout

    def layout(self, clause_list, layout: Layout):
        #print(clause_list)
        if layout == Layout.STRIPE:
            self.now_layout = layout
            self.now_clause_list = clause_list
            return self.layout_stripe(clause_list)
        else:
            print("Not implemented layout {}".format(layout))
            return 0

    def relayout(self):
        #self.main_frame.pack_forget()
        return self.layout(self.now_clause_list,self.now_layout)

    def clear(self, main_frame):
        for s in main_frame.place_slaves():
            s.destroy()

    def make_fixed_clause_list(self, clause_list):
        #print(clause_list)
        fixed = []
        carry = ''
        lim = self.settings['structure']['char_lim']
        for c in clause_list:
            con = carry + str(c)
            if len(con) > lim:
                carry = con[lim:]
                con = con[:lim]
            else:
                carry = ''
            fixed.append(con)
        return fixed

    def layout_stripe(self, clause_list, clause_num=None):
        self.clear(self.main_frame)
        self.widgets = []
        self.index = [0,0] # [clause index of the clause list, character index of the clause]
        max_width = 0
        max_height = 0
        target_clause = ''
        lim = self.settings['structure']['char_lim']
        for n in range(self.settings['structure']['nest']):
            _max_width=max_width
            _max_height=max_height
            foot = 0
            row_widgets =[]
            for r in range(self.settings['structure']['row']):
                tail = 0
                chr_num = 0
                column_widgets = []
                y = foot
                for c in range(self.settings['structure']['column']):
                    if c > 0 and len(clause_list) > c and chr_num + len(str(clause_list[self.index[0]])) > lim:
                        break
                    if len(target_clause) == 0:
                        if self.index[0] < len(clause_list):
                            target_clause = str(clause_list[self.index[0]])
                    txt = target_clause[:lim]
                    if chr_num > lim:
                        break
                    chr_num += len(txt)
                    target_clause = target_clause[lim:]
                    if len(target_clause) == 0:
                        self.index[0] += 1
                        self.index[1] = 0
                    else:
                        self.index[1] += lim
                    _font = Font(self.main_frame,family=self.settings['font']['name'],size=self.settings['font']['size'],weight=self.settings['font']['weight'])
                    label = ttk.Label(self.main_frame,text=txt,anchor=W,font=_font,style='MainFrame.TLabel',justify=CENTER)
                    column_widgets.append(label)
                    x = max_width + tail
                    w = x+label.winfo_reqwidth() + self.settings['spaces']['char']
                    h = y+label.winfo_reqheight() + self.settings['spaces']['sentence']
                    label.place(x=x,y=y,width=label.winfo_reqwidth(),height=label.winfo_reqheight())
                    tail += label.winfo_reqwidth() + self.settings['spaces']['char']
                    if w > _max_width:
                        _max_width = w
                        self.main_frame.configure(width=_max_width)
                    if h > _max_height:
                        _max_height = h
                        self.main_frame.configure(height=_max_height)
                    if h > foot:
                        foot = h
                row_widgets.append(column_widgets)
            max_width=_max_width + self.settings['spaces']['paragraph']
            max_height=_max_height
            self.widgets.append(row_widgets)
        self.main_frame.after(self.update_after, self.update)
        max_width -= self.settings['spaces']['char'] + self.settings['spaces']['paragraph']
        max_height -= self.settings['spaces']['sentence']
        self.main_frame.configure(width = max_width, height = max_height)
        return self.index

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
    manager = LayoutManager(root,tk.Toplevel())
    manager.layout([x for x in range(manager.settings['structure']['nest']*manager.settings['structure']['row']*manager.settings['structure']['column'])], Layout.STRIPE)
    root.mainloop()

if __name__ == '__main__':
    main()
