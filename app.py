import customtkinter
import psycopg2
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from private_data import con
import CTkTable



class MyFrame(customtkinter.CTkScrollableFrame):
    def __ini__(self, master, **kwargs):
        super().__init__(master, kwargs)

class QuestionManager(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('900x675')
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 5)
        self.grid_rowconfigure(0, weight = 5)
        self.title = self.title('test')
        

        self.my_frame = customtkinter.CTkScrollableFrame(self, width=250, height=300)
        self.my_frame.grid( row = 0 , column = 1 , padx = 10, pady = 20,sticky = 'ew')


        self.test_frame = customtkinter.CTkScrollableFrame(self, width=250, height=300)
        self.test_frame.grid( row= 1 ,column = 1,  padx = 10, pady = 20, sticky = 'ew')

        self.table_frame = customtkinter.CTkScrollableFrame(self, width=700, height=300)
        self.table_frame.grid(row = 0, column = 2, padx = 10, pady = 20, sticky = 'ew')
        
        
        
        self.values = ["question", "alternative a", "alternative b", "alternative c", "alternative d", "alternative e"]

        self.values_table = ["question", "alternative_a", "alternative_b", "alternative_c", "alternative_d", "alternative_e"]
        self.text_boxes = []

        self.options = {"theme": ['microsoft', 'word', 'excel', 'email', 'internet'], "correct option":["a","b","c","d","e"], "question was used": ["yes", "no"]}
        self.option_table = ["type_question", "correct_option", "question_was_used"]
        self.option_boxes = []
        self.table_view()

    def create_question(self):

        
        #question
        """label = customtkinter.CTkLabel(self.my_frame, text="question", anchor="w", text_color="white", font=("Arial",20))
        label.pack(padx = 10, pady = 20)
        question = customtkinter.CTkTextbox(self.my_frame, width=200, height=50)
        question.pack(pady = 20)
        
        label = customtkinter.CTkLabel(self.my_frame, text="alternative a", anchor="w", text_color="white", font=("Arial",20))
        label.pack(padx = 10, pady = 20)
        alternative_a = customtkinter.CTkTextbox(self.my_frame, width=200, height=50)
        alternative_a.pack(pady = 20)
        
        label = customtkinter.CTkLabel(self.my_frame, text="alternative b", anchor="w", text_color="white", font=("Arial",20))
        label.pack(padx = 10, pady = 20)
        alternative_b = customtkinter.CTkTextbox(self.my_frame, width=200, height=50)
        alternative_b.pack(pady = 20)

        label = customtkinter.CTkLabel(self.my_frame, text="alternative c", anchor="w", text_color="white", font=("Arial",20))
        label.pack(padx = 10, pady = 20)
        alternative_c = customtkinter.CTkTextbox(self.my_frame, width=200, height=50)
        alternative_c.pack(pady = 20)

        label = customtkinter.CTkLabel(self.my_frame, text="alternative d", anchor="w", text_color="white", font=("Arial",20))
        label.pack(padx = 10, pady = 20)
        alternative_d = customtkinter.CTkTextbox(self.my_frame, width=200, height=50)
        alternative_d.pack(pady = 20)

        label = customtkinter.CTkLabel(self.my_frame, text="alternative e", anchor="w", text_color="white", font=("Arial",20))
        label.pack(padx = 10, pady = 20)
        alternative_e = customtkinter.CTkTextbox(self.my_frame, width=200, height=50)
        alternative_e.pack(pady = 20)
"""
        for i, value in enumerate(self.values):
            label = customtkinter.CTkLabel(self.my_frame, text=value, anchor="w", text_color="white", font=("Arial",20))
            label.grid(padx = 10, pady = 20)
            alternative = customtkinter.CTkTextbox(self.my_frame, width=200, height=50)
            alternative.grid( pady = 20)
            self.text_boxes.append(alternative)
        


        
        

        #another grid
        

        

        for combo in self.options:
            label = customtkinter.CTkLabel(self.test_frame, text=combo, anchor="w", text_color="white", font=("Arial",20))
            label.grid(padx = 10, pady = 20)
            question_theme = customtkinter.CTkComboBox(self.test_frame, values=self.options[combo], state="readonly")
            question_theme.set(self.options[combo][0])
            question_theme.grid(pady = 20, sticky = "ew")
            self.option_boxes.append(question_theme)


        submit = customtkinter.CTkButton(self.my_frame, text='submit', command=lambda:self.test(self.text_boxes, self.option_boxes))
        submit.grid(pady = 20)
        

       
       
       
    
    def test(self, question_value, option_value):
        cur = con.cursor()
        command = "INSERT INTO questions ("
        count = 0
        values = []
        for box in question_value:
            command += f" {self.values_table[count]},"
            values.append(box.get("1.0", "end").replace('\n', ''))
            count+=1

       
        for n, option in enumerate(option_value):
            command += f" {self.option_table[n]},"
            values.append(option.get().replace('\n', ''))
       
        command += "date_created)"
    
        command += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values.append(datetime.now())
        values = tuple(values)
    
        cur.execute(command, values)
        con.commit()

    def table_view(self):
        cur = con.cursor()
        get_number_of_rows = "select count(*) from questions"
        cur.execute(get_number_of_rows)

        rows = cur.fetchall()

        cur.execute("select question, correct_option, type_question, date_created, question_was_used from questions")
        data = cur.fetchall()

        headers = ["question", "correct alternative", "type of question", "date", "question was used"]
        table = CTkTable.CTkTable(self.table_frame, row = rows[0][0], column=5, values=data)
        table.add_row(["question", "correct alternative", "type of question", "date", "question was used"], 0)
        table.grid(padx=20, pady=20)

        filter_by_type = customtkinter.CTkButton(self)
        



        

        



        


if __name__ == "__main__":
    
    app = QuestionManager()
    app.mainloop()
