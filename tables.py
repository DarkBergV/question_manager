import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from private_data import con


def create_tables():
    commands = (
        
        "alter table questions add date_created date"
    )

    
    
    cur = con.cursor()
    
    cur.execute(commands)
    con.commit()

def main():
    create_tables()
if __name__ == '__main__':
   
    main()