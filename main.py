import requests
import tkinter as tk
import psycopg2
from tkinter import ttk, Label

from private_data import API_KEY,con


print(API_KEY["type"])

class QuestionApp:
    def __init__(self, root):
        self.root =root
        self.root.title('question manager')
        self.question = tk.StringVar()
        self.alternative_a = tk.StringVar()
        self.alternative_b = tk.StringVar()
        self.alternative_c = tk.StringVar()
        self.alternative_d = tk.StringVar()
        self.alternative_e = tk.StringVar()
        self.correct = [
            "a","b","c","d","e"
        ]
        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set(self.correct[0])

        self.drop = tk.OptionMenu(root, self.selected_option, *self.correct)
        self.drop.pack()

        self.create_widgets()

    def create_widgets(self):
        self.drop.pack()

        question_label = Label(self.root, text='question', height=4)
        question_label.pack()
        self.question = tk.Text(self.root, width=30, height=5)
        self.question.pack()


        self.alternative_a = tk.Text(self.root, width=30, height=5)
        self.alternative_a.pack()

        self.alternative_b = tk.Text(self.root, width=30, height=5)
        self.alternative_b.pack()

        self.alternative_c = tk.Text(self.root, width=30, height=5)
        self.alternative_c.pack()

        self.alternative_d = tk.Text(self.root, width=30, height=5)
        self.alternative_d.pack()

        self.alternative_e = tk.Text(self.root, width=30, height=5)
        self.alternative_e.pack()

        save_button = tk.Button(self.root, text = 'save data', command= self.save_data)
        save_button.pack()
        
    def save_data(self):
        question = self.question.get("1.0", "end-1c")
        a = self.alternative_a.get("1.0", "end-1c")
        b = self.alternative_b.get("1.0", "end-1c")
        c = self.alternative_c.get("1.0", "end-1c")
        d = self.alternative_d.get("1.0", "end-1c")
        e = self.alternative_e.get("1.0", "end-1c")
        
        command = f'insert into questions (question, alternative_a,alternative_b,alternative_c,alternative_d,alternative_e)'
        

    
if __name__ == '__main__':
    root = tk.Tk()
    app = QuestionApp(root)
    root.mainloop()