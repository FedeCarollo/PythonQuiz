import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.getcwd())
from functions.fileutil import upload_file
import os

class StartPage(tk.Frame):
    def __init__(self, parent, controller : tk.Tk):
        tk.Frame.__init__(self, parent)
        button = ttk.Button(self, text="Upload new file", command=self.upload_and_add)
        button.grid(row=0, column=0, padx=10, pady=10)
        self.n=0
        self.btn_grid = []
        for file in os.listdir(os.getcwd() + "\\files"):
            self.show_file_in_list(file)
            
    def show_file_in_list(self, path):
        #TODO: only if file is valid
        i = self.n//4
        j = self.n%4
        btn = ttk.Button(self, text=os.path.basename(path))
        self.btn_grid.append(btn)
        btn.grid(row=10+i, column=j, padx=1, pady=10, sticky="w")
        self.n+=1

    def upload_and_add(self) -> None:
        path=upload_file()
        if(path is None):
            return None
        self.show_file_in_list(path)
        


        



    