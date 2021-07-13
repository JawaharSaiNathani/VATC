import tkinter as Tkinter
from Editor_Tools import linenumber

class featured_text:
    def __init__(self, root=None, textbox=None, main=None):
        self.main=main
        self.root=root
        self.textbox=textbox
        # Nw Editing Scroll Bar
        self.scrollstart()
        self.line_count()

        # [ This Function is For Editing Scrolling Bar with Text Widget ]
    def scrollstart(self):
        # scroll Bar x For width
        self.scroll_x=Tkinter.Scrollbar(self.main, orient='horizontal')
        self.scroll_x.config(command=self.textbox.xview)
        self.textbox.configure(xscrollcommand=self.scroll_x.set)
        self.scroll_x.pack(side='bottom', fill='x', anchor='w')

        
        # Scroll Bar y For Height
        self.scroll_y=Tkinter.Scrollbar(self.textbox)
        self.scroll_y.config(command=self.textbox.yview)
        self.textbox.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_y.pack(side='right', fill='y')
    def line_count(self):
        self.linenumbers = linenumber.LineNumberCanvas(self.root, width=40)
        self.linenumbers.connect(self.textbox)
        self.linenumbers.pack(side="left", fill="y")
        self.linenumbers.bind('<Button-1>',self.linenumbers.get_breakpoint_number)
        self.textbox.pack(expand='yes', fill='both',side='right')

    def changed(self, event=None):
        self.linenumbers.re_render()