import requests
from bs4 import BeautifulSoup as bs

from fake_useragent import UserAgent
import pprint
import re
ua = UserAgent()
headers = {'accept': '*/*', 'user-agent': ua.chrome} # создание сессии


URL_TEMPLATE = "https://codeforces.com/problemset?order=BY_SOLVED_DESC&tags=greedy" # ссылка на сайт
#r = requests.get(URL_TEMPLATE) # делаем запрос на сервер 
# print(r.status_code) # 200 означает положительный ответ


result_list = {'number_task': [], 'name_task': [],'type_task':[], 'hard_task': [],'answer_task':[]}
href_list={ 'number_task_href': [], 'name_task_href': [],'type_task_href':[], 'hard_task_href': [],'answer_task_href':[]  }




def print_elemt(element,help_number):

    name_task_helper={0:'номер задания', 3:'сложность' , 4:'кол-во решений', 'название задания': 'название задания','тип задания':'тип задания'}
    try:

        print(name_task_helper[help_number],' => ',element.text.strip(), '+ ссылка => ',element.a['href']) # вывод обычных элементов 
        # Обычные они потому что не лежат в сраных div-ах еще внутри 
    except:

        try:
            if element.text.strip().isnumeric():
                print(name_task_helper[help_number],' => ',element.text.strip(), '+ ссылка => ',element.get('href')) # а вот это сраные элементы
            else:
                print(name_task_helper[help_number],' => ',element.text.strip(), '+ ссылка => ',element.get('href')) # а вот это сраные элементы

            # они лежат в div-ах
        except: 
            pass

    



def pars_task_scool():
    session =requests.Session()
    request=session.get(URL_TEMPLATE,headers=headers) # имитация пользователя

    if request.status_code==200:
        soup = bs(request.content, "lxml") #сохранается страница
        all_table = soup.find( "table", attrs={"class": "problems"} ) #переходим в талицу
        all_task_tr=all_table.find_all('tr') #  переходим на блок таблицы 
        

        for item in all_task_tr:
            td_items=item.find_all('td')  # проходимся по каждой строке или по каждому столбцу тут уже как посмотреть 
            print('----------------')
            s=0
            for element in td_items:
            
                if s==1:

                    new_s=0
                    for i in element.find_all('div'): # сраный div
                        if new_s==0:
                            print_elemt(i,'название задания')  
                        if new_s==1:
                            for new_i in i:
                                print_elemt(new_i, 'тип задания')   
                        new_s+=1


                elif s!=1 and s!=2: # нужно как раз для того чтобы выести все блоки div в названии (Жесткий костыль да и вообще это все костыль и сыйт г....)
                    print_elemt(element, s)
            
                s+=1


pars_task_scool()
