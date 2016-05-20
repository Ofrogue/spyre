# -*- coding: utf-8 -*-

from spyre import server
import pandas as pd
import os
# from Lab1 import get_df,districts    #импорт модулей
districts=["Вінницька",
    "Волинська",
    "Дніпропетровська",
    "Донецька",
    "Житомирська",
    "Закарпатська",
    "Запорізька",
    "Івано-Франківська",
    "Київська",
    "Кіровоградська",
    "Луганська",
    "Львівська",
    "Миколаївська",
    "Одеська",
    "Полтавська",
    "Рівенська",
    "Сумська",
    "Тернопільська",
    "Харківська",
    "Херсонська",
    "Хмельницька",
    "Черкаська",
    "Чернівецька",
    "Чернігівська",
    "Республіка Крим"]

class VHI_Visual(server.App):   # создаём класс(наше приложение)

    title = 'Visual VHI'   # название страницы

    districts=["Вінницька",
    "Волинська",
    "Дніпропетровська",
    "Донецька",
    "Житомирська",
    "Закарпатська",
    "Запорізька",
    "Івано-Франківська",
    "Київська",
    "Кіровоградська",
    "Луганська",
    "Львівська",
    "Миколаївська",
    "Одеська",
    "Полтавська",
    "Рівенська",
    "Сумська",
    "Тернопільська",
    "Харківська",
    "Херсонська",
    "Хмельницька",
    "Черкаська",
    "Чернівецька",
    "Чернігівська",
    "Республіка Крим"]


    inputs = [{                          # список словарей, который описывает типы входных данных
                                         # их id и вид на странице
            'type': 'dropdown', # выпадающий список (для районов)
            'label': 'District', # название
            'options': [{'label': d, 'value': districts.index(d)+1}for d in districts],  # варианты заполнения
            'key': 'distr',
            'action_id': 'update_data'  # при нажатии Enter данные будут обновляться

                }, {
            'type': 'dropdown',  # выпадающий список для индексов
            'label': 'Index\n',
            'options': [{'label': 'VCI', 'value': 'VCI'},
                        {'label': 'TCI', 'value': 'TCI'},
                        {'label': 'VHI', 'value': 'VHI'}],
            'key': 'index',
            'action_id': 'update_data'
            },{

            'type': 'text',    # текстовое поле для начальной недели
            'label': 'Week limits.\nFrom',  # текст над полем
            'key': 'from_week',
            'value': '1', # начальное значение
            'action_id': 'update_data'
            },
            {
                'type': 'text',  # текстовое поле для конечной недели
                'label': 'To',
                'key': 'to_week',
                'value': '52',
                'action_id': 'update_data'
            },
            {"type": "text",
             "label": 'Year',
             "key": "year",
             "value": '2007'}]

    controls = [{'type': 'hidden', 'id': 'update_data'}]  # контроллер для обновления данных

    tabs = ['Plot', 'Table']  # вкладки на странице

    outputs = [{          # список словарей, отображает все выходные данные
        'type': 'table',     # тип - таблица
        'id': 'table_id',
        'control_id': 'update_data',
        'tab': 'Table',   # находится во вкладке Table
        'on_page_load': True  # отображение на странице
    },
        {
            'type': 'plot',  # тип - график
            'id': 'plot_id',
            'control_id': 'update_data',
            'tab': 'Plot'  # этот графки находится во вкладке Plot
        }]

    def getData(self, params):  # функция вывода  таблицы на страницу
        total = merge()  # получить датафрейм
        total['district_id'] = total['district_id'].astype('int64')
        total['year'] = total['year'].astype('int64')
        total = total[total['district_id'] == int(params['distr'])]   # выбрать из фрейма только те строки, которые соответствуют выбраному на странице району
        total = total[total['year'] == int(params['year'])] #выбрать только определенный год
        return total[(total['week'] >= int(params['from_week'])) & (total['week'] <= int(params['to_week']))][['year', 'week',  params['index']]]
        # вернуть строки из диапозона from_week и to_week и выбрать из них колонки year, week и выбраный индекс

    def getPlot(self, params):  # функция вывода графика на страницу
       # df = self.getData(params).set_index('year').drop(['week'], axis=1)  # получаем фрейм
        df = self.getData(params)
        plt = df.plot(x='week', y=params['index'])
        plt.set_ylabel(params['index'])  # установить значения для оси y
        plt.set_title(params['index'])  # название графика
        return plt.get_figure()  # вернуть график

def frame(path):
    if os.path.isfile(path):
        df = pd.read_csv(path, header=1, index_col=False)
        t = df[df['VHI'] != -1]
        t.reset_index()
        return (t)

def merge(path=r"data"):
    filelist = os.listdir(path=path)
    distr = ['''Cherkasy''', '''Chernihiv''', '''Chernivtsi''', '''Crimea''', '''Dnipropetrovs'k''', '''Donetsk''',
             '''Ivano-Frankivs'k''', '''Kharkiv''', '''Kherson''', '''Khmel'nyts'kyy''', '''Kiev''', '''Kiev City''', '''Kirovohrad''',
             '''Luhans'k''', '''Lviv''', '''Mykolayiv''', '''Odessa''', '''Poltava''', '''Rivne''', '''Sevastopol''',
             '''Sumy''', '''Ternopil''', '''Transcarpathia''', '''Vinnytsya''', '''Volyn''', '''Zaporizhzhya''',
             '''Zhytomyr''']
    d_id = [x for x in range(27) if ((x != 0))]
    # some of the districts are not needed
    new_id = [22, 24, 23, 25, 3, 4, 8, 19, 20, 21, 9, -1, 10, 11, 12, 13, 14, 15, 16, -1, 17, 18, 6, 1, 2, 7, 5]
    id_change = dict(zip(d_id, new_id))

    # d_id = [x for x in range(27) if ((x != 0)&(x != 12)&(x != 20))]
    # df_list a list frames of csv file
    df_list = [frame(os.path.join(path, file)) for file in filelist]
    # id_list a list of district ids of files
    id_list = [int(file.split(sep='_')[2]) for file in filelist]

    df_name = zip(df_list, distr)
    for df_name in df_name:
        df_name[0].insert(loc=0, column='district', value=df_name[1])

    df_id = zip(df_list, id_list)
    for df_id in df_id:
        df_id[0].insert(loc=0, column='district_id', value=id_change.get(df_id[1]))

    global_df = pd.concat(df_list, axis=0, ignore_index=True)
    global_df.to_csv('concat_'+path+'.csv')
    return global_df

app = VHI_Visual()  # запуск приложения
app.launch(port=8080)
