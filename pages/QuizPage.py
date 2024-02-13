import tkinter as tk
from tkinter import ttk, messagebox
from functions.fileutil import upload_file, delete_files
import tkModule
import os
from random import randint

class QuizPage(tk.Frame):
    def __init__(self, parent, controller, fileList: list[str]):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        self.nQuestions = 0
        self.questions = []
        self.fileList = [f"{os.getcwd()}\\files\\{file}" for file in fileList]

        self.gen_questions()

        lbl = ttk.Label(self, text="Quiz", font=("Arial", 12, "bold"))
        lbl.grid(row=0, column=0, padx=10, pady=10)

        lblEntry = ttk.Label(self, text="Inserisci il numero di domande")
        lblEntry.grid(row=2, column=0, padx=10, pady=10)

        entry = ttk.Entry(self)
        entry.insert(0, "5")
        entry.grid(row=2, column=1, padx=10, pady=10)

        btnStart = ttk.Button(self, text="Inizia", command=lambda: self.start_quiz(int(entry.get()) if entry.get().isdigit() else -1))
        btnStart.grid(row=2, column=2, padx=10, pady=10)

        self.lbl=lbl
        self.lblEntry=lblEntry
        self.entry=entry
        self.btnStart=btnStart


    def start_quiz(self, nQuestions):
        if(nQuestions <= 0):
            messagebox.showerror("Valore inserito non valido")
            return None
        
    def gen_questions(self):
        for path in self.fileList:
            self.questions.extend(self.read_question_file(path))
        #TODO check cases in which it iterates forever
        all_ans = [q["true_ans"] for q in self.questions]
        for q in self.questions:
            for _ in range(3):
                j = randint(0, len(all_ans)-1)
                while(all_ans[j] in q["answers"]):
                    j = randint(0, len(all_ans)-1)
                q["answers"].append(all_ans[j])

        [print(q) for q in self.questions]
        
    def read_question_file(self, path:str, delim=","):
        lstQuestions = []
        with open(path, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                obj={}
                obj["question"]=line.split(delim)[0]
                obj["true_ans"]=line.split(delim)[1].rstrip('\n')
                obj["answers"]=[obj["true_ans"]]
                lstQuestions.append(obj)
        return lstQuestions

