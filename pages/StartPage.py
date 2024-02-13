import tkinter as tk
from tkinter import ttk, messagebox
from functions.fileutil import upload_file, delete_files
import tkModule
import os
from pages.QuizPage import QuizPage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller

        lbl = ttk.Label(self, text="Carica nuovo", font=("Arial", 12, "bold"))
        lbl.grid(row=0, column=0, padx=10, pady=10)
        button = ttk.Button(self, text="Upload new file", command=self.upload_and_add)
        button.grid(row=0, column=2, padx=10, pady=10)

        lbl = ttk.Label(self, text="File caricati", font=("Arial", 12, "bold"))
        lbl.grid(row=1, column=0, padx=1, pady=10)

        self.n=0
        self.btn_grid:list[ttk.Button] = []
        self.selected_grid: dict[str, tk.BooleanVar] = dict()
        self.show_files()

        btn_delete = ttk.Button(self, text="Cancella file", command=self.delete_files)
        btn_delete.grid(row=3, column=3, sticky="ew")

        btn_start = ttk.Button(self, text="Inizia quiz", command=self.start_quiz)
        btn_start.grid(row=4, column=3, sticky="ew")

    def show_files(self):
        for file in os.listdir(os.getcwd() + "\\files"):
            self.show_file_in_list(file)



    def show_file_in_list(self, path):
        #TODO: only if file is valid
        i = self.n//4
        j = self.n%4
        self.selected_grid[path] = tk.BooleanVar(value=False)
        btn = ttk.Checkbutton(self, text=os.path.basename(path), variable=self.selected_grid[path], command=lambda: self.show_selected(path))
        self.btn_grid.append(btn)
        btn.grid(row=3+self.n, column=0, padx=1, pady=10, sticky="w")
        self.n+=1

    def upload_and_add(self) -> None:
        path=upload_file()
        if(path is None):
            return
        self.show_file_in_list(path)

    def show_selected(self, path):
        print(path)
        print(self.selected_grid[path].get())

    def delete_files(self):
        found=False
        to_del=[]
        for path,sel in self.selected_grid.items():
            if(sel.get()):
                found=True
                to_del.append(f"{os.getcwd()}\\files\\{path}")
        if not found:
            messagebox.showerror("Errore", "Seleziona almeno un file")
        else:
            delete_files(to_del)
            self.delete_show_files()
            self.show_files()

    def delete_show_files(self) -> None:
        for btn in self.btn_grid:
            btn.destroy()
        self.btn_grid = []
        self.selected_grid = dict()
        self.n = 0;

    def start_quiz(self)->None:
        files = [path for path, sel in self.selected_grid.items() if sel.get()]
        if not any(files):
            messagebox.showerror("Errore", "Seleziona almeno un insieme per iniziare")
        else:
            self.controller.init_frame(QuizPage, QuizPage(self.controller.container, self.controller, files))
            self.controller.show_frame(QuizPage)
            