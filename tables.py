import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from private_data import con


def create_tables():
    commands = (
        
        "create type correct_option as ENUM('a','b','c','d','e')",
        "create type type_question as ENUM('word','microsoft','excel','email','internet')",

        "CREATE TABLE questions ( question_id SERIAL PRIMARY KEY, question varchar(500), alternative_a varchar(500),alternative_b varchar(500),alternative_c varchar(500),alternative_d varchar(500), alternative_e varchar(500), correct_option correct_option, type_question type_question)"
    )

    
    
    cur = con.cursor()
    for command in commands:
        print(command)
        cur.execute(command,)
    con.commit()

def main():
    create_tables()
if __name__ == '__main__':
   
    main()