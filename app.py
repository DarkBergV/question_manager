import customtkinter
import psycopg2
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from private_data import con
import CTkTable
from tksheet import Sheet


class MyFrame(customtkinter.CTkScrollableFrame):
    def __ini__(self, master, **kwargs):
        super().__init__(master, kwargs)


class TopLevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, fg_color=None, **kwargs):

        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.geometry("400x300")
        self.label = customtkinter.CTkLabel(self, text="question")

        self.question_frame = customtkinter.CTkScrollableFrame(
            self, width=400, height=300
        )
        self.question_frame.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=5)
        self.text_boxes = []
        self.options = {
            "theme": ["microsoft", "word", "excel", "email", "internet"],
            "correct option": ["a", "b", "c", "d", "e"],
            "question was used": ["yes", "no"],
        }

        self.option_boxes = []

    def question_page(self, id):
        cur = con.cursor()
        cur.execute("select * from questions where question_id = %s", (id,))
        values = cur.fetchall()
       
        values = values[0]

        question_label = customtkinter.CTkLabel(self.question_frame, text="question")
        question_label.grid()
        question = customtkinter.CTkTextbox(self.question_frame)
        question.grid()
        question.insert(0.0,text=values[1])

        alternative_a_label = customtkinter.CTkLabel(self.question_frame, text = 'alternative a')
        alternative_a_label.grid()
        alternative_a = customtkinter.CTkTextbox(self.question_frame)
        alternative_a.grid()
        alternative_a.insert(0.0, text=values[2])


        alternative_b_label = customtkinter.CTkLabel(self.question_frame, text = 'alternative b')
        alternative_b_label.grid()
        alternative_b = customtkinter.CTkTextbox(self.question_frame)
        alternative_b.grid()
        alternative_b.insert(0.0, text=values[3])

        alternative_c_label = customtkinter.CTkLabel(self.question_frame, text = 'alternative c')
        alternative_c_label.grid()
        alternative_c = customtkinter.CTkTextbox(self.question_frame)
        alternative_c.grid()
        alternative_c.insert(0.0, text=values[4])

        alternative_d_label = customtkinter.CTkLabel(self.question_frame, text = 'alternative d')
        alternative_d_label.grid()
        alternative_d = customtkinter.CTkTextbox(self.question_frame)
        alternative_d.grid()
        alternative_d.insert(0.0, text=values[5])


        alternative_e_label = customtkinter.CTkLabel(self.question_frame, text = 'alternative e')
        alternative_e_label.grid()
        alternative_e = customtkinter.CTkTextbox(self.question_frame)
        alternative_e.grid()
        alternative_e.insert(0.0, text=values[6])

        question_text = {"question":question, "alternative_a":alternative_a, "alternative_b":alternative_b, "alternative_c": alternative_c, "alternative_d":alternative_d, "alternative_e":alternative_e}

        option_box_value = [values[8], values[7], values[10]]
        print(option_box_value)
        count = 0
        for combo in self.options:
            label = customtkinter.CTkLabel(
                self.question_frame,
                text=combo,
                anchor="w",
                text_color="white",
                font=("Arial", 20),
            )
            
            label.grid(padx=10, pady=20)
            question_theme = customtkinter.CTkComboBox(
                self.question_frame, values=self.options[combo], state="readonly"
            )
            
            question_theme.set(option_box_value[count])
            question_theme.grid(pady=20, sticky="ew")
            self.option_boxes.append(question_theme)
            count+=1
        update = customtkinter.CTkButton(self.question_frame, text="Update", command= lambda:self.update_question(id, question_text))
        update.grid(pady = 20, sticky="ew")

    def update_question(self, id, question_text):
        cur = con.cursor()
        command = "UPDATE questions SET"
        values = []
        for i in question_text:
            print(i)

            command+= f" {i}"
            command += " = %s,"
            values.append(question_text[i].get("0.0", "end"))
        
        command = command[0:(len(command)-1)]
        print(command)
        command += " WHERE question_id = %s"
        values.append(id)

        cur.execute(command, values)
        con.commit()

            

        




       
            
           


class QuestionManager(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x675")

        # row configuration
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # column configuration
        self.grid_columnconfigure(2, weight=5)

        self.values = [
            "question",
            "alternative a",
            "alternative b",
            "alternative c",
            "alternative d",
            "alternative e",
        ]

        self.values_table = [
            "question",
            "alternative_a",
            "alternative_b",
            "alternative_c",
            "alternative_d",
            "alternative_e",
        ]
        self.text_boxes = []

        self.options = {
            "theme": ["microsoft", "word", "excel", "email", "internet"],
            "correct option": ["a", "b", "c", "d", "e"],
            "question was used": ["yes", "no"],
        }
        self.option_table = ["type_question", "correct_option", "question_was_used"]
        self.option_boxes = []
        self.create_question()

    def create_frames(self):
        self.my_frame = customtkinter.CTkScrollableFrame(self, width=250, height=900)
        self.my_frame.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

        self.table_frame = customtkinter.CTkScrollableFrame(self, width=700, height=900)
        self.table_frame.grid(row=0, column=2, padx=10, pady=20, sticky="ew")

    def create_question(self):
        for i in self.winfo_children():
            i.destroy()
        self.create_frames()

        # question

        for i, value in enumerate(self.values):
            label = customtkinter.CTkLabel(
                self.my_frame,
                text=value,
                anchor="w",
                text_color="white",
                font=("Arial", 20),
            )
            label.grid(padx=10, pady=20)
            alternative = customtkinter.CTkTextbox(self.my_frame, width=200, height=50)
            alternative.grid(pady=20)
            self.text_boxes.append(alternative)

        # another grid

        for combo in self.options:
            label = customtkinter.CTkLabel(
                self.my_frame,
                text=combo,
                anchor="w",
                text_color="white",
                font=("Arial", 20),
            )
            label.grid(padx=10, pady=20)
            question_theme = customtkinter.CTkComboBox(
                self.my_frame, values=self.options[combo], state="readonly"
            )
            question_theme.set(self.options[combo][0])
            question_theme.grid(pady=20, sticky="ew")
            self.option_boxes.append(question_theme)

        submit = customtkinter.CTkButton(
            self.my_frame,
            text="submit",
            command=lambda: self.test(self.text_boxes, self.option_boxes),
        )
        submit.grid(pady=20)

        self.table_view()

    def test(self, question_value, option_value):
        cur = con.cursor()
        command = "INSERT INTO questions ("
        count = 0
        values = []
        for box in question_value:
            command += f" {self.values_table[count]},"
            values.append(box.get("1.0", "end").replace("\n", ""))
            count += 1

        for n, option in enumerate(option_value):
            command += f" {self.option_table[n]},"
            values.append(option.get().replace("\n", ""))

        command += "date_created)"

        command += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values.append(datetime.now())
        values = tuple(values)

        cur.execute(command, values)
        con.commit()
        self.create_question()

    def table_view(self):
        cur = con.cursor()
        get_number_of_rows = "select count(*) from questions"
        cur.execute(get_number_of_rows)

        rows = cur.fetchall()

        cur.execute(
            "select question_id, question, correct_option, type_question, date_created, question_was_used from questions"
        )
        data = cur.fetchall()
        

        data = self.format_text(data)

        headers = [
            "id",
            "question",
            "correct alternative",
            "type of question",
            "date",
            "question was used",
        ]
        self.table = CTkTable.CTkTable(
            self.table_frame,
            row=rows[0][0],
            column=6,
            values=data,
            command=self.test_thing,
        )
        self.table.add_row(
            headers,
            0,
        )
        self.table.grid(padx=20, pady=20)
        self.question_window = None

    """    self.table = Sheet(self.table_frame, data = data, height=900, width=1000)
        
        
        
        self.table.grid(padx=20, pady=20, sticky="nsew")
        self.table.set_all_cell_sizes_to_text()"""

    def test_thing(self, i):

        self.table.get_row(i["row"])
        id = self.table.get_row(i["row"])
        id = id[0]

      
        if self.question_window is None or not self.question_window.winfo_exists():
            print("something")

            self.question_window = TopLevelWindow(self)
            self.question_window.question_page(id)

        else:
            print("something else")
            self.question_window.focus()

    def format_text(self, data):
        for d in data:
            new_d = list(d)
            formating = d[1].split(" ")
            count = 0
            count_after = 8
            
            if len(formating)>=8:
                for _ in formating:
                    count+=1
                    if count==count_after:
                        formating.insert(count, "\n")
                        count_after+=8
                        
                question = " ".join(formating)
                new_d[1] = question
                index = data.index(d)
                data[index] = tuple(new_d)

        return data
           



if __name__ == "__main__":

    app = QuestionManager()
    app.mainloop()
