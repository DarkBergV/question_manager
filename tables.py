import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from private_data import con


def create_tables():
    commands = (
        
        "select * from questions where question like '%sd%'"
    )

    
    
    cur = con.cursor()
    
    cur.execute(commands)

    print(cur.fetchall())

def main():
    create_tables()
if __name__ == '__main__':
   
    main()