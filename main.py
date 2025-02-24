import requests
import tkinter as tk
import psycopg2
from tkinter import ttk, Label, simpledialog, filedialog
from tkinter import TclError
from tkinter.simpledialog import Dialog
from datetime import datetime

from private_data import API_KEY, con



import customtkinter

class QuestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("question manager")
        self.question = tk.StringVar()
        self.alternative_a = tk.StringVar()
        self.alternative_b = tk.StringVar()
        self.alternative_c = tk.StringVar()
        self.alternative_d = tk.StringVar()
        self.alternative_e = tk.StringVar()

        self.used = ['yes' ,'no']
        self.selected_used = tk.StringVar(self.root)
        self.selected_used.set(self.used[0])

        self.correct = ["a", "b", "c", "d", "e"]

        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set(self.correct[0])

        self.type = ["microsoft", "word", "excel", "email", "internet"]
        self.selected_type = tk.StringVar(self.root)
        self.selected_type.set(self.type[0])

        self.drop_type = tk.OptionMenu(root, self.selected_type, *self.type)
        self.drop_type.pack()

        self.view_table()

    def create_widgets(self):
        for i in self.root.winfo_children():
            i.destroy()
        self.selected_type = tk.StringVar(self.root)
        self.selected_type.set(self.type[0])

        self.drop_type = tk.OptionMenu(root, self.selected_type, *self.type)
        self.drop_type.pack()

        self.drop = tk.OptionMenu(root, self.selected_option, *self.correct)
        self.drop.pack()

        self.was_used = tk.OptionMenu(root, self.selected_used, *self.used)
        self.was_used.pack()

        

        question_label = Label(self.root, text="question", height=4)
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

        save_button = tk.Button(self.root, text="save data", command=self.save_data)
        save_button.pack()

        view_table = tk.Button(self.root, text="table", command=self.view_table)
        view_table.pack()

    def save_data(self):
        question = self.question.get("1.0", "end-1c")
        a = self.alternative_a.get("1.0", "end-1c")
        b = self.alternative_b.get("1.0", "end-1c")
        c = self.alternative_c.get("1.0", "end-1c")
        d = self.alternative_d.get("1.0", "end-1c")
        e = self.alternative_e.get("1.0", "end-1c")
        correct_alternative = self.selected_option.get()
        type_question = self.selected_type.get()
        was_used = self.selected_used.get()

        command = "insert into questions (question, alternative_a,alternative_b,alternative_c,alternative_d,alternative_e, correct_option, type_question, date_created, question_was_used) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur = con.cursor()
        cur.execute(
            command,
            (
                question,
                a,
                b,
                c,
                d,
                e,
                correct_alternative,
                type_question,
                datetime.now(),
                was_used

            ),
        )
        con.commit()

    def view_table(self):
        for i in self.root.winfo_children():
            i.destroy()

        search = tk.Entry()
        search.pack()

        create_question = tk.Button(
            self.root, text="create question", command=self.create_widgets
        )
        create_question.pack()

        self.tree = ttk.Treeview(
            self.root,
            columns=[
                "question",
                "a",
                "b",
                "c",
                "d",
                "e",
                "correct_option",
                "type",
                "date",
                "update",
                "delete",
            ],
        )
        self.tree.heading("question", text="question")
        self.tree.heading("a", text="a")
        self.tree.heading("b", text="b")
        self.tree.heading("c", text="c")
        self.tree.heading("d", text="d")
        self.tree.heading("e", text="e")
        self.tree.heading("correct_option", text="correct_option")
        self.tree.heading("type", text="type")
        self.tree.heading("date", text="date")
        self.tree.heading("update", text="update")
        self.tree.heading("delete", text="delete")

        self.tree.pack(expand=True, fill="both")

        type_q = [
            "all",
            "microsoft",
            "word",
            "excel",
            "email",
            "internet",
        ]  # type_q for type of question
        s_type = tk.StringVar(self.root)
        s_type.set(type_q[0])
        theme = s_type.get()

        type_label = Label(self.root, text="type", height=4, width=5)
        type_label.pack()
        filter_by_type = tk.OptionMenu(root, s_type, *type_q, command=self.table_view)
        filter_by_type.pack()

       


    def update(self, id, question, alternative_a,alternative_b,alternative_c,alternative_d,alternative_e, correct, s_type,was_used):

        question =question.get("1.0", "end-1c")
        a = alternative_a.get("1.0", "end-1c")
        b = alternative_b.get("1.0", "end-1c")
        c = alternative_c.get("1.0", "end-1c")
        d = alternative_d.get("1.0", "end-1c")
        e = alternative_e.get("1.0", "end-1c")
        correct_alternative = correct.get()
        type_question = s_type.get()
        question_was_used = was_used.get()

        command = "update questions set question = %s, alternative_a = %s,alternative_b = %s,alternative_c = %s,alternative_d = %s,alternative_e = %s, correct_option = %s, type_question = %s, date_created = %s, question_was_used = %s where question_id = %s"
      
        cur = con.cursor()
        cur.execute(
            command,
            (
                question,
                a,
                b,
                c,
                d,
                e,
                correct_alternative,
                type_question,
                datetime.now(),
                question_was_used,
                id
            ),
        )
        con.commit()

    def table_view(self, theme):

        for i in self.tree.get_children():
            self.tree.delete(i)

        cur = con.cursor()
        if theme == "all":
            cur.execute("SELECT * FROM questions")
            for table in cur.fetchall():
              
                self.tree.insert(
                    "",
                    "end",
                    id=table[0],
                    values=(
                        table[1],
                        table[2],
                        table[3],
                        table[4],
                        table[5],
                        table[6],
                        table[7],
                        table[8],
                        table[9],
                    ),
                )

        else:
            cur.execute("SELECT * FROM questions where type_question = %s", (theme,))
            for table in cur.fetchall():
               
                self.tree.insert(
                    "",
                    "end",
                    id=table[0],
                    values=(
                        table[1],
                        table[2],
                        table[3],
                        table[4],
                        table[5],
                        table[6],
                        table[7],
                        table[8],
                        table[9],
                    ),
                )
        self.tree.bind("<ButtonRelease-1>", self.question_view)

    def question_view(self, id):
        cur = con.cursor()
        value = []
        try:
            item = self.tree.selection()
            
            if item:
                
                
            
                cur.execute('select question, alternative_a, alternative_b, alternative_c, alternative_d, alternative_e, correct_option, type_question, date_created, question_was_used  from questions where question_id = %s', (item[0],))

                value = cur.fetchall()[0]
        except TclError:   
            if id:
                cur.execute('select question, alternative_a, alternative_b, alternative_c, alternative_d, alternative_e, correct_option, type_question, date_created, question_was_used  from questions where question_id = %s', (id,))
                value = cur.fetchall()[0]
                item = [id]
                
        

        for i in self.root.winfo_children():
            i.destroy()
        count = 0
        labels = [
            "question",
            "alternative a",
            "alternative b",
            "alternative c",
            "alternative d",
            "alternative e",
            "correct alternative",
        ]
        if value[9]:
            question_used = 'yes'

        else:
            question_used = 'no'
        s_type = tk.StringVar(self.root)
        s_type.set(value[7])
        drop_type = tk.OptionMenu(root, s_type, *self.type)
        drop_type.pack()
        
        correct = tk.StringVar(self.root)
        correct.set(value[6])
        drop = tk.OptionMenu(root, correct, *self.correct)
        drop.pack()
        used = tk.StringVar(self.root)
        used.set(question_used)
        was_used = tk.OptionMenu(root, used , *self.used)
        was_used.pack()

        print(value)
        question_label = Label(self.root, text="question", height=4)
        question_label.pack()
        question = tk.Text(self.root, width=30, height=5)
        question.pack()
        question.insert("1.0", value[0])

        alternative_a = tk.Text(self.root, width=30, height=5)
        alternative_a.pack()
        alternative_a.insert("1.0", value[1])

        alternative_b = tk.Text(self.root, width=30, height=5)
        alternative_b.pack()
        alternative_b.insert("1.0", value[2])

        alternative_c = tk.Text(self.root, width=30, height=5)
        alternative_c.pack()
        alternative_c.insert("1.0", value[3])

        alternative_d = tk.Text(self.root, width=30, height=5)
        alternative_d.pack()
        alternative_d.insert("1.0", value[4])

        alternative_e = tk.Text(self.root, width=30, height=5)
        alternative_e.pack()
        alternative_e.insert("1.0", value[5])

        update_button = tk.Button(
            self.root, text="update question", command=lambda:self.update(item[0], question, alternative_a,alternative_b,alternative_c,alternative_d,alternative_e, correct, s_type, used)
        )
        update_button.pack()

        delete_button = tk.Button(
            self.root, text = 'delete question', command = lambda:self.delete_view(item[0], con)
        )
        delete_button.pack()

        view_table = tk.Button(self.root, text="table", command=self.view_table)
        view_table.pack()

    def delete_view(self,id, con):
        for i in self.root.winfo_children():
            i.destroy()
        button_yes = tk.Button(self.root, text="yes", command=lambda: self.delete_question(id, con))
        button_yes.pack()
        button_no = tk.Button(self.root, text = 'no', command=lambda: self.question_view(id))
        button_no.pack()
        
    def delete_question(self, id, con):
        cur = con.cursor()
        cur.execute('delete from questions where question_id = %s', (id,))
        con.commit()
        self.view_table()

class MyFrame(customtkinter.CTkScrollableFrame):
    def __ini__(self, master, **kwargs):
        super().__init__(master, kwargs)

class QuestionManager:
    def __init__(self, root):
        self.root = root
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)
        self.title = self.root.title('test')

        self.my_frame = MyFrame(master=self.root, width=600, height=500, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky = "nsew")
        
        self.create_question()

    def create_question(self):

        

        question = customtkinter.CTkTextbox(self.root, width=200, height=50)
        question.insert("0.0", "question")
        question.delete("0.0", "end")
        question.place(relx = 0.5, rely = 0.5,anchor = "center")
       
        submit = customtkinter.CTkButton(self.root, text="submit", command=lambda:self.test(question.get("0.0", "end")))
        submit.place(relx = 0.5, rely = 0.7,anchor = "center")
    
    def test(self, question_value):
        print(question_value.strip())




        

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionApp(root)
    root.mainloop()
