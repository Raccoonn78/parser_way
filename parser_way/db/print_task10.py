import psycopg2
from config import host, user, password, db_name
from main_db import Db_connect
import random

class Db_insert(Db_connect):

    def __init__(self):
        super().__init__()
        

    def insert_type(self,type_name):
        postgreSQL_select_Query="""SELECT type_name FROM tasks WHERE 'greedy' = ANY(type_name); 
        """
        self.cursor.execute(postgreSQL_select_Query)
        mobile_records = self.cursor.fetchall()
        print(mobile_records)
    
    def element_exists(self,name_name=0): # проверяет есть ли такой элемент в базе данных
        
        text_sql="SELECT * FROM tasks WHERE name_id_task ='%s'" %name_name[0]
        self.cursor.execute(text_sql)
        result = self.cursor.fetchall()
        print(result)
        return bool(len(result))
    def get_element_bot(self):
        number_random=random.randint(1,99)
        text_sql="SELECT * FROM tasks WHERE id_task=%s"%number_random 
        self.cursor.execute(text_sql)
        result = self.cursor.fetchall()
        return result

new_insert=Db_insert()
#new_insert.insert_type('geedy')
# new_insert.element_exists()
nn=new_insert.get_element_bot()
print(type(nn), type(nn[0]), type(nn[0][0]), nn[0][0],nn[0][2])