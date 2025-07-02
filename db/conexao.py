#importa conector
import mysql.connector
from utils.db_config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD #Importa dados das variaveis de ambiente


class Conexao:
    def __init__(self):
        pass  # Por enquanto não tem nada, mas pode futuramente ter configs

    def get_connection(self):
        try:
            # Cria e retorna uma conexão com o banco de dados
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,         
                password=DB_PASSWORD,
                database=DB_NAME
            )
            print("\nConexão realizada com sucesso!")
            return connection# É oque permite a logica no atributo 'Agenda/self.cursor' funcionar 
        #Se a conexão falhar
        except mysql.connector.Error as error:
            print(f"Erro no MYSQL: {error}")
            return None#Se erro, conexão é nula
