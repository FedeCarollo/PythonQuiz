import tkinter as tk
from tkinter import ttk, messagebox
from functions.fileutil import upload_file, delete_files
import os
from random import randint, shuffle
import pages.StartPage


class QuizPage(tk.Frame):
    def __init__(self, parent, controller, fileList: list[str]):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        self.nQuestions = 0
        self.right = []
        self.wrong = []
        self.questions = []
        self.fileList = [f"{os.getcwd()}\\files\\{file}" for file in fileList]



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

        style = ttk.Style(self)
        style.configure("BTN_NS.TButton", background=None)
        style.configure("BTN_S.TButton", background="blue")


    def start_quiz(self, nQuestions):
        if(nQuestions <= 0):
            messagebox.showerror("Valore inserito non valido")
            return None
        self.nQuestions = nQuestions
        self.gen_questions()
        self.destroy_start()
        self.i = 0
        self.create_question()
        
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

            shuffle(q["answers"])

        
        shuffle(self.questions)
        self.questions =self.questions[:self.nQuestions]
        [print(q) for q in self.questions]
        
    def read_question_file(self, path:str, delim=",") -> list:
        lstQuestions = []
        with open(path, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                obj={}
                obj["question"]=line.split(delim)[0]
                obj["true_ans"]=line.split(delim)[1].rstrip('\n')
                obj["answers"]=[obj["true_ans"]]
                obj["your_ans"]=""
                lstQuestions.append(obj)
        return lstQuestions
    
    def destroy_start(self) -> None:
        self.btnStart.destroy()
        self.lbl.destroy()
        self.lblEntry.destroy()
        self.entry.destroy()

    def create_question(self):
        q = self.questions[self.i]
        self.btns: list[ttk.Button] = []
        self.lblQuestion = ttk.Label(self, text=q["question"].capitalize(), font=("Arial", 12, "bold"))
        self.lblQuestion.grid(row=0, column=3)
        for n in range(len(q["answers"])):
            i = n//2
            j = 2*(n%2) + 2
            btn = ttk.Button(self, text=str(q["answers"][n]).capitalize(), command=lambda n=n: self.select_choice(self.i, n), style="BTN_NS.TButton")
            btn.grid(row=i+1, column=j, sticky="ew", padx=20, pady=20)
            self.btns.append(btn)
        self.btnContinue = ttk.Button(self, text="Continua", command=self.next_question)
        self.btnContinue.grid(row=4, column=3)
        

    def select_choice(self, i, n):


        if self.questions[i]["your_ans"] == self.questions[i]["answers"][n]:
            self.questions[i]["your_ans"] = ""
            self.btns[n].configure(style="BTN_NS.TButton")
        else:
            self.questions[i]["your_ans"] = self.questions[i]["answers"][n]

            for btn in self.btns:
                btn.configure(style="BTN_NS.TButton")
            self.btns[n].configure(style="BTN_S.TButton")

        print(self.questions[i])

    def destroy_btns(self):
        for btn in self.btns:
            btn.destroy()
        self.btnContinue.destroy()
        self.lblQuestion.destroy()
        

    def next_question(self):
        self.destroy_btns()
        self.i+=1
        if(self.i == self.nQuestions):
            self.create_summary()
        else:
            self.create_question()

    def create_summary(self):
        right=wrong=ng=0
        i=1
        summary_elems=[]
        for q in self.questions:
            lblQ = ttk.Label(self, text=f"Domanda {i}: {q['question']}", font=("Arial", 10, "bold"))
            lblQ.grid(row=2*(i-1), column=0, sticky="ew", padx=5, pady=3)
            summary_elems.append(lblQ)
            if q["your_ans"] == "":
                ng+=1
                lblYA = ttk.Label(self, text="Hai risposto: Non Data")
                lblYA.grid(row=2*i-1, column=0, sticky="ew", padx=5, pady=3)
                summary_elems.append(lblYA)
                
            elif q["your_ans"] == q["true_ans"]:
                right+=1
                lblYA = ttk.Label(self, text=f"Hai risposto: {q['your_ans']}. Corretto", foreground="green")
                lblYA.grid(row=2*i-1, column=0, sticky="ew", padx=5, pady=3)
                summary_elems.append(lblYA)
            else:
               wrong+=1
               lblYA = ttk.Label(self, text=f"Hai risposto: {q['your_ans']}. Sbagliato. Era {q['true_ans']}", foreground="red")
               lblYA.grid(row=2*i-1, column=0, sticky="ew", padx=5, pady=3)
               summary_elems.append(lblYA)
            i+=1
        lblTotal=ttk.Label(self, text=f"Giuste: {right}, Sbagliate: {wrong}, Non date: {ng}. Totale {right}/{self.nQuestions}", font=("Arial", 10))
        lblTotal.grid(row=2*(i-1), column=0, padx=10, pady=10)
        summary_elems.append(lblTotal)
        i+=1

        btnHome=ttk.Button(self, text="Ritorna alla home", command=self.back_home)
        btnHome.grid(row=2*(i-1), column=0)
        summary_elems.append(btnHome)
        self.summary = summary_elems

    def back_home(self):
        for elem in self.summary:
            elem.destroy()
        self.controller.show_frame(pages.StartPage.StartPage)
        
