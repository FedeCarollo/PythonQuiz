import tkinter as tk
from tkinter import ttk
from tkModule import tkinterApp
import sys
import os
sys.path.append(os.getcwd())

if __name__ == "__main__":
    app = tkinterApp()
    app.geometry("450x300")
    app.title("Quiz time")
    app.grid_columnconfigure([0, 1, 2], weight=1)
    app.grid_rowconfigure([0, 1, 2], weight=1)
    app.mainloop()