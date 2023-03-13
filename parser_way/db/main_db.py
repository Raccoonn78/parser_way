import psycopg2
from config import host, user, password, db_name
#from way_to_a import  number_list,name_list,type_list,hard_list,answer_list



# # подключение к БД
     

class Db_connect:  # класс для подключения к БД 
    def __init__(self) : # подключение 
        self.connection= psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
        self.connection.autocommit=True # автоматическое сохранение БД
        self.cursor =self.connection.cursor()
        print('[INFO] PostgreSQL connection open')
    pass  
    def __del__(self): # сохранение и закрытие соединения 
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print('[INFO] PostgreSQL connection closed')

    def create_table(self): # создание таблиц
        with self.connection.cursor() as self.cursor:
            self.cursor.execute(
          """  CREATE TABLE tasks(
                id_task serial PRIMARY KEY,

                name_id_task varchar(50) NOT NULL,
                name_id_task_href varchar(50) NOT NULL,

                name_task varchar(50) NOT NULL,
                name_task_href varchar(50) NOT NULL,

                hard_task varchar(50) NOT NULL,
                type_name text[],
                answer_task varchar(50) NOT NULL,
                answer_task_href varchar(50) NOT NULL ); """
        )

        print('[INFO] Table create successfully')

class Db_insert(Db_connect):
    
    def __init__(self, element,id_pod=0) : # создание элементов которые мы помещаем в БД
        super().__init__()
        
        self.number= element[0]
        self.number_href= element[1]
        self.name= element[2]
        self.name_href= element[3]
        self.hard= element[4]
        self.answer= element[5]
        self.answer_href= element[6]

        self.type_name=element[7]
        self.tuple_name= id_pod
           

    def add_element(self): # добавление в БД
        try :
            self.cursor.execute(
                    """INSERT INTO tasks (
                        name_id_task,
                        name_id_task_href,
                        name_task,
                        name_task_href,
                        hard_task,
                        answer_task,
                        answer_task_href,
                        type_name
                    ) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)""" , (self.number,self.number_href,
                                                             self.name,self.name_href,
                                                             self.hard,
                                                             self.answer,self.answer_href,self.type_name)        
                )
        except Exception as ex_:
            print('[INFO] Error ', ex_)
        pass
        

    def element_exists(self,name_name): # проверяет есть ли такой элемент в базе данных
        text_sql="SELECT * FROM tasks WHERE name_id_task ='%s'" %name_name[0]
        self.cursor.execute(text_sql)
        result = self.cursor.fetchall()
        
        return bool(len(result))
    

   
