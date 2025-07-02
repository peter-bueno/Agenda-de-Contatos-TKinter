from dotenv import load_dotenv # metodo da python-dotenv que carrega as variaveis
import os #importa os para buscar variaveis

#Carrega as variaveis do .env
load_dotenv()

#Usa as variaveis
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME= os.getenv("DB_NAME")