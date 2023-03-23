import mysql.connector
from mysql.connector import Error

import env as v

def query(query):
    results = []
    try:
        con = mysql.connector.connect(host=v.DB_HOST, database=v.DB_DATABASE, user=v.DB_USER, password=v.DB_PASS, port=v.DB_PORT)
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    except Error as e:
        print("Erro ao acessar tabela MySQL", e)

    if con.is_connected():
        con.close()
        cursor.close()
    return results

def execute_query(execute):
    con = mysql.connector.connect(host=v.DB_HOST, database=v.DB_DATABASE, user=v.DB_USER, password=v.DB_PASS, port=v.DB_PORT)
    cursor = con.cursor()
    try:
        cursor.execute(execute)
        con.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def get_repo_db(NOME_REPO):
    return query(f'''SELECT * FROM ti_git_repositorios 
        WHERE nome_repositorio = '{NOME_REPO}'
    ''')

def insert_repo_db(NOME_REPO, URL_REPO):
    query = f'''INSERT INTO ti_git_repositorios 
        (nome_repositorio, url_repositorio) VALUES 
        ('{NOME_REPO}', '{URL_REPO}')
    '''
    print("Executando => ")
    print(query)
    return execute_query(query)