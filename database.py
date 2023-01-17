import sqlite3
import os

class Database():
    def __init__(self) -> None:
        self.create_db()

    def create_db(self, name="database"):
        conn = sqlite3.connect(name+".db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE if not exists `jobs` (
                `id` BIGINT NOT NULL,
                `title` VARCHAR(100) NOT NULL,
                `desc` TEXT NOT NULL,
                PRIMARY KEY (`id`))
        """)
        conn.close()
    
    def query_params_db(self, query_sql: str, params: tuple = ()) -> list:
        '''Função para manejo do banco de dados com uso de parametros'''
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "database.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query_sql, params)
            conn.commit()
            res = cursor.fetchall()
            conn.close()
            print(f'Executando comando no banco de dados', 'query_params_db')
            return res
        except Exception as erro:
            print('Erro ao executar comando','query_params_db', erro)
    
    def set_job(self, id, title, desc):
        try:
            set_query = 'INSERT INTO `jobs` (`id`, `title`, `desc`) VALUES (?, ?, ?)'
            set_params = (id, title, desc,)
            set_result = self.query_params_db(set_query, set_params)
            return True
        except Exception as erro:
            print(erro)
            return False

    def get_all_id_jobs(self) -> list:
        try:
            query = 'SELECT id FROM `jobs`'
            response = self.query_params_db(query)
            # Convert result in array
            array = []
            for i in range(len(response)):
                array.append(response[i][0])
            return array
        except Exception as erro:
            print('ERRO -',erro)

    def get_job(self, id) -> list:
        try:
            query = 'SELECT * FROM `jobs` WHERE jobs.title=(?)'
            # query = 'SELECT * FROM `jobs`'
            params = (id,)
            response = self.query_params_db(query, params)
            return response
        except Exception as erro:
            print('ERRO -',erro)

    def delete_job(self, id):
        try:
            query = 'DELETE FROM jobs WHERE jobs.id = (?)'
            params = (id,)
            response = self.query_params_db(query, params)
            return True
        except Exception as erro:
            print('ERRO -', erro)
        pass
