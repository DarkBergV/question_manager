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

       
        self.text_boxes = []
        self.options = {
            "theme": ["microsoft", "word", "excel", "email", "internet"],
            "correct option": ["a", "b", "c", "d", "e"],
            "question was used": ["yes", "no"],
        }

        self.option_boxes = []
        

    def question_page(self, id):
        self.create_frames()
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

        delete = customtkinter.CTkButton(self.question_frame, text="delete", command = lambda:self.delete(id))
        delete.grid(padx = 20, sticky="ew")


    def create_frames(self):
        self.question_frame = customtkinter.CTkScrollableFrame(
            self, width=350, height=300
        )
        self.question_frame.grid(row=2, column=2, padx=10, pady=20)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

    def delete(self, id):
        
        for i in self.winfo_children():
            i.destroy()
        self.create_frames()
        yes = customtkinter.CTkButton(self.question_frame, text="yes", command=lambda:self.delete_question(id))
        yes.grid(pady=20, sticky="ew")
        no = customtkinter.CTkButton(self.question_frame, text="no", command=lambda:self.question_page(id))
        no.grid(pady=20, sticky="ew")
    def delete_question(self,id):
        command = "delete from questions where question_id = %s"
        
        cur = con.cursor()
        cur.execute(command, (id,))
        con.commit()
        self.destroy()
        
    
        
        
    def update_question(self, id, question_text):
        cur = con.cursor()
        command = "UPDATE questions SET"
        values = []
        
            

       
        for i in question_text:
        

            command+= f" {i}"
            command += " = %s,"
            values.append(question_text[i].get("0.0", "end"))

        for t in self.option_boxes:
            values.append(t.get())

        command += " type_question = %s, correct_option = %s, question_was_used = %s, date_created = %s"

        values.append(datetime.now())
        
        
       
        command += " WHERE question_id = %s"
        values.append(id)

        cur.execute(command, values)
        con.commit()

            

        




       
            
           


class QuestionManager(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x675")

        # row configuration
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=0)

        # column configuration
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(2, weight=5)
       
        
        self.create_question()
    def create_variables(self):
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

    def create_frames(self):
        self.resizable(4,4)
        self.my_frame = customtkinter.CTkScrollableFrame(self, width=250, height=900)
        self.my_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew", columnspan = 1)
        self.my_frame.grid_forget()

        self.table_frame = customtkinter.CTkScrollableFrame(self, width=700, height=450)
        self.table_frame.grid(row=0, column=2, padx=20, pady=10, sticky="new", columnspan = 3)


        self.filters_frames = customtkinter.CTkFrame(self, width=700, height=200)
        self.filters_frames.grid(row = 1, column=2,padx = 20, pady = 10, sticky = 'nsew', columnspan = 2, rowspan = 2)


        self.menu_frames = customtkinter.CTkFrame(self, width = 200, height=200)
        self.menu_frames.grid(row = 0, column = 0)
    
    def filters(self):
        self.filter_by_theme = customtkinter.CTkComboBox(self.filters_frames, values = ["all", "microsoft", "word", "excel", "email", "internet"])
        
        self.filter_by_theme.grid(padx = 10, pady = 10)

        self.search = customtkinter.CTkEntry(self.filters_frames)
        self.search.grid(padx = 10)


        self.was_used = customtkinter.CTkComboBox(self.filters_frames, values=["all", "yes", "no"])
        self.was_used.grid(row = 0, column = 2, padx =20)


        self.order_by = customtkinter.CTkComboBox(self.filters_frames, values=["id",
            "question",
            "correct alternative",
            "type of question",
            "date",
            "question was used", "NONE"])
        self.order_by.grid(row = 0, column = 3, padx = 10)

        sumbit = customtkinter.CTkButton(self.filters_frames, width=20,height=20, text="submit", command=lambda:self.filtered_table(self.filter_by_theme.get(),self.search.get(), self.was_used.get(), self.order_by.get()))

        
        sumbit.grid(row = 1, column = 2, padx = 10)

        clear = customtkinter.CTkButton(self.filters_frames, width=20,height=20, text="clear filters", command = lambda:(self.filter_by_theme.set("all"), self.search.delete("0","end"), self.was_used.set("all") ))
        clear.grid(row = 1, column = 3)


    def filtered_table(self,choice, search, was_used, order):
        order_by = {"id":"question_id",
            "question":"question",
            "correct alternative":"correct_option",
            "type of question":"type_question",
            "date":"date_created",
            "question was used":"question_was_used", "NONE":"NONE"}
        
        for i in self.table_frame.winfo_children():
            i.destroy()
        cur = con.cursor()
        get_number_of_rows = "select count(*) from questions"
        cur.execute(get_number_of_rows)

        rows = cur.fetchall()
        

        command = "select question_id, question, correct_option, type_question, date_created, question_was_used from questions where"
        values = []

        if not choice == "all":
            command += " type_question = %s AND"
            values.append(choice)

        if not search == "":
            
            command += " question like %s AND"
            search = '%%%s%%' % search
            values.append(search)

        if not was_used == "all":
            command += " question_was_used = %s"
            values.append(was_used)

        if was_used == "all" and search == "" and choice == "all":
            command = "select question_id, question, correct_option, type_question, date_created, question_was_used from questions"

        
            
        if command[len(command)-3:len(command)] == "AND":
            command = command[0:len(command) - 4]

        if order != "NONE":
            print(order)
            

            order = str(order_by[order])
            command += f" ORDER BY {order}"
            values.append(order)

        print(command)
        values = tuple(values)
        cur.execute(command, values)
        data = cur.fetchall()
        print(data)
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


        

        

        
        print(choice)
        
        print(type(search))
        print(was_used)
    def try_thing(self):
        for i in self.winfo_children():
            i.destroy()
        self.create_question

    def minimize_create_question(self):
        self.my_frame.grid_forget()
        self.menu_frames.grid(row = 0, column = 0)

    def maximize_create_question(self):
        self.my_frame.grid(row=0, column=0, padx=10, pady=20, sticky="ew")
        
        self.menu_frames.grid_forget()
        

    def create_question(self):
        for i in self.winfo_children():
            i.destroy()
        self.create_frames()
        self.create_variables()
        self.filters()
        # question
        self.maximaze = customtkinter.CTkButton(self.menu_frames, width=10, height=20, text="create question",fg_color="#3a3a3a", hover_color="#454545", command = self.maximize_create_question)
        self.maximaze.grid(row = 2, column=1)

        minimize = customtkinter.CTkButton(self.my_frame, width=10, height=20, text="-", command = self.minimize_create_question )
        minimize.grid(row = 0, column = 1)

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
            values.append(box.get(0.0, "end").replace("\n", ""))
            count += 1
            print(values)

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

    def table_view(self, theme = "all"):
        for i in self.table_frame.winfo_children():
            i.destroy()
        cur = con.cursor()
        

        if theme == "all":
            cur.execute(
            "select question_id, question, correct_option, type_question, date_created, question_was_used from questions"
            )
            data = cur.fetchall()

            get_number_of_rows = "select count(*) from questions"
            cur.execute(get_number_of_rows)

            rows = cur.fetchall()
        
        else:
            cur.execute("select question_id, question, correct_option, type_question, date_created, question_was_used from questions where type_question = %s", (theme,))
            data = cur.fetchall()

            get_number_of_rows = "select count(*) from questions where type_question = %s"
            cur.execute(get_number_of_rows, (theme,))

            rows = cur.fetchall()
            

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
        if not id == "id":
            print(id)

        
            if self.question_window is None or not self.question_window.winfo_exists():
            
                
                self.question_window = TopLevelWindow(self)
                self.question_window.question_page(id)
                

            else:
                
                self.question_window.focus()
               
        else :
            pass

       
        
    def format_text(self, data):
        for d in data:
            new_d = list(d)
            formating = d[1].split(" ")
            count = 0
            count_after = 15
            
            if len(formating)>=15:
                for _ in formating:
                    count+=1
                    if count==count_after:
                        formating.insert(count, "\n")
                        count_after+=15
                        
                question = " ".join(formating)
                new_d[1] = question
                index = data.index(d)
                data[index] = tuple(new_d)

        return data
           



if __name__ == "__main__":

    app = QuestionManager()
    app.mainloop()
