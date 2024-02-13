import tkinter as tk
from tkinter import ttk
import pages.StartPage as sp


LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self, width=800, height=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (sp.StartPage, ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(sp.StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()