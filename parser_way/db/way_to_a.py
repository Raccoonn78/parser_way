import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from main_db import Db_insert
import asyncio
from datetime import datetime
ua = UserAgent()
headers = {'accept': '*/*', 'user-agent': ua.chrome} # создание сессии
URL_TEMPLATE = "https://codeforces.com/problemset/page/1?order=BY_SOLVED_DESC" # ссылка на сайт
#r = requests.get(URL_TEMPLATE) # делаем запрос на сервер 
# print(r.status_code) # 200 означает положительный ответ


global new_list,list_type_fuck,id_p

name_list={}
type_list={}
new_list=[]
list_type_fuck=[]


class Print_elemt:

    def __init__(self,element ,help_number) -> None:
        self.element=element
        self.help_number=help_number

        pass
    
    def sort_elemt(self):

        if self.help_number==0:
            self.number_task()
        if self.help_number=='название задания':
            self.name_task()
        if self.help_number==4:
            self.answer_task()
        if self.help_number=='тип задания':
            self.type_task()
        if self.help_number==3:
            self.hard_task()
            # Обычные они потому что не лежат в сраных div-ах еще внутри 
     
    def number_task(self,element=0,id_p=0):
    
        if len(new_list)==7:
            new_list.append(list_type_fuck)
            class_my_fan=Db_insert(new_list) 
            if (not class_my_fan.element_exists(new_list)): # проверка есть ли такой пример в бд
                
                class_my_fan.add_element()
            else:print('[INFO] ТАКАЯ ЗАДАЧА ЕСТЬ')
            new_list.clear()
            list_type_fuck.clear()

        new_list.append(self.element.text.strip())
        new_list.append(self.element.a['href'])
   

    def name_task(self,element=0,help_number=0):
        name_list[self.element.text.strip()]=self.element.a['href']
        new_list.append(self.element.text.strip())
        new_list.append(self.element.a['href'])
        

    def type_task(self,element=0,help_number=0):
    
        if name_list: len_list=len(list(name_list.keys()))-1 # длина для вывода ключа названия задания, чтобы поместить типы этого задания в словарь 
        else: len_list=len(list(name_list.keys())) # длина для вывода ключа названия задания, чтобы поместить типы этого задания в словарь 

        keys_name_task=list(name_list.keys())[len_list] # создание ключа , т.е. название задания 
        
        if (keys_name_task in type_list )==False and self.element.text.strip()!='' and self.element.text.strip()!=',': # создание нового списка в ключе(названия) для того чтобы помесить типы задания
            
            type_list[keys_name_task]=[]
            type_list[keys_name_task].append(self.element.text.strip())
            
            list_type_fuck.append(self.element.text.strip())
        elif self.element.text.strip()!='' and self.element.text.strip()!=',':
            type_list[keys_name_task].append(self.element.text.strip())
            list_type_fuck.append(self.element.text.strip())


    def hard_task(self,element=0,help_number=0):
    
        new_list.append(self.element.text.strip())
    
    def answer_task(self,element=0,help_number=0):
        new_list.append(self.element.text.strip())
        new_list.append(self.element.a['href'])


def pars_task_scool():
    session =requests.Session()
    number_href=1
    URL_TEMPLATE = "https://codeforces.com/problemset/page/%s?order=BY_SOLVED_DESC"%number_href
    request=session.get(URL_TEMPLATE,headers=headers) # имитация пользователя

    if request.status_code==200:
        soup = bs(request.content, "lxml") #сохранается страница
        all_table = soup.find( "table", attrs={"class": "problems"} ) #переходим в талицу
        all_task_tr=all_table.find_all('tr') #  переходим на блок таблицы 
        for item in all_task_tr:
            td_items=item.find_all('td')  # проходимся по каждой строке или по каждому столбцу тут уже как посмотреть 
            s=0
            for element in td_items:
                if s==1:
                    new_s=0
                    for i in element.find_all('div'): # сраный div
                        if new_s==0:
                            #print_elemt(i,'название задания')
                            random_number=Print_elemt(i,'название задания')  
                            random_number.sort_elemt()
                        if new_s==1:
                            for new_i in i:
                                #print_elemt(new_i, 'тип задания') 
                                random_number=Print_elemt(new_i, 'тип задания')  
                                random_number.sort_elemt()  
                        new_s+=1
                elif s!=1 and s!=2: # нужно как раз для того чтобы выести все блоки div в названии (Жесткий костыль да и вообще это все костыль и сыйт г....)
                    #print_elemt(element, s)
                    random_number=Print_elemt(element, s)  
                    random_number.sort_elemt() 
                    
                s+=1


async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)


if __name__=='__main__':
    
    asyncio.run(scheduled(10))
    pars_task_scool()
#     #pars_task_scool()
#     for i in range(10):
#         print(list(number_list.keys())[i], list(name_list.keys())[i],  type_list[list(name_list.keys())[i]],  hard_list[list(name_list.keys())[i]],  list(answer_list.keys())[i])

