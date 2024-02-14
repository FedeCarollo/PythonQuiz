import tkinter as tk
from tkinter import ttk, messagebox
from functions.fileutil import write_log
import os
from random import randint, shuffle
import pages.StartPage
import datetime


class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        self.objects=[]
        self.cnt=0

        history=self.read_log_file()
        self.write_summary(history)

        self.btnQuit = ttk.Button(self, text="Ritorna al menù principale", command=self.back_home)
        self.btnQuit.grid(row=self.cnt, column=0, padx=10, pady=10)



        
    def read_log_file(self):
        logfile = os.getcwd() + "\\log\\logfile.log"
        out=[]
        with open(logfile, "r", encoding="UTF-8") as f:
            headers=f.readline().rstrip("\n").split(",")
            for line in f.readlines():
                format_line=[]
                splitted=line.rstrip("\n").split(",")
                for i in range(len(headers)):
                    format_line.append([headers[i],splitted[i]])
                format_line = dict(format_line)
                out.append(format_line)
            return out
        
    def write_summary(self, history:list[dict]):
        i=1
        lbl = ttk.Label(self, text="Storico prove", font=("Arial", 12, "bold"))
        lbl.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.objects.append(lbl)
        for obj in history:
            date = datetime.datetime.fromtimestamp(float(obj['data'])).strftime("%Y-%m-%d %H:%M:%S")
            lbl = ttk.Label(self, text=f"Data: {date}")
            lbl.grid(row=i, column=0, sticky="ew", padx=10, pady=10)
            self.objects.append(lbl)
            lbl = ttk.Label(self, text=f"Giuste: {obj['giuste']}")
            lbl.grid(row=i, column=1, sticky="ew", padx=10, pady=10)
            self.objects.append(lbl)
            lbl = ttk.Label(self, text=f"Sbagliate: {obj['sbagliate']}")
            lbl.grid(row=i, column=2, sticky="ew", padx=10, pady=10)
            self.objects.append(lbl)
            lbl = ttk.Label(self, text=f"Non date: {obj['ng']}")
            lbl.grid(row=i, column=3, sticky="ew", padx=10, pady=10)
            self.objects.append(lbl)
            i+=1
        self.cnt=i
        


    def back_home(self):
        for elem in self.objects:
            elem.destroy()
        self.btnQuit.destroy()
        self.controller.show_frame(pages.StartPage.StartPage)
        
