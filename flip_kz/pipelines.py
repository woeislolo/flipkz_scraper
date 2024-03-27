# from itemadapter import ItemAdapter

import mysql.connector

import re


class MySqlPipeline:

    def __init__(self):
        ''' Создает в MySQL соединение и таблицу '''

        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '1234',
            database = 'test',
            )

        self.cur = self.conn.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS books(
                id int NOT NULL auto_increment, 
                title VARCHAR(255),
                author VARCHAR(100),
                url VARCHAR(255),
                PRIMARY KEY (id)
            )
            """)

    def process_item(self, item, spider):
        ''' Валидирует поля author и сохраняет Item'ы в таблицу БД '''

        regex = re.compile(r'[А-Я].\s{0,1}[А-Я].') # есть ли в author инициалы
        if not re.search(regex, item['author']):
            item['author'] = 'Неизвестный'

        self.cur.execute("""INSERT INTO books (title, author, url) VALUES (%s, %s, %s)""", (
            item["title"],
            item["author"],
            item["url"]
        ))

        self.conn.commit()

    def close_spider(self, spider):
        ''' Закрывает курсор и соединение '''

        self.cur.close()
        self.conn.close()
