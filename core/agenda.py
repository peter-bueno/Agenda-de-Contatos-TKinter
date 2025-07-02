from .contato import Contato # import relativo (mesmo nivel)
from db.conexao import Conexao #import absoluto (de outro package)
from mysql.connector import Error # Importa objeto Error para deixar o codigo mais limpo

#Agenda crud
class Agenda:
    def __init__(self):
       self.lista_de_contatos = [] #Guarda contatos  do banco
       self.conexao = Conexao().get_connection() # Cria conexão pelo objeto
       self.cursor = self.conexao.cursor() if self.conexao else None #Cria cursor pelo objeto, se conexão for sucesso, senão cursor é nulo
    
    #Carrega dados do banco e adiciona na lista
    def carregar_contatos(self):
        #try/except p/ tratamento de erros
        try:
            #limpa lista antes de carregar, para evitar duplicatas
            self.lista_de_contatos.clear()
            #se o cursor não for nulo, executa consulta
            if self.cursor:
                #Busca os dados dos contatos no banco
                self.cursor.execute("SELECT nome_contato, telefone_contato, email_contato, id_contato FROM contatos")
                # aqui fetchall retorna tupla
                dados = self.cursor.fetchall()
                
                #converte dados do banco em novo objeto Contato
                for (nome, telefone, email, id) in dados:
                    #Cria um objeto pra cada conjunto 
                    contato = Contato(nome, telefone, email, id)
                    #verifica se o objeto é instancia de Contato(aumenta segurança)
                    if isinstance(contato, Contato):
                        #Adiciona um contato pra cada posição da lista
                        self.lista_de_contatos.append(contato)
        except Error as error:
            print(f"Erro ao carregar contatos: {error}") 
    #Adiciona novo contato à lista                        
    def adicionar_contato(self, novo_nome, novo_telefone, novo_email=None):
        #try/except p/ tratamento de erros
        try:
            if (novo_nome.strip() and novo_telefone.strip()): #Verifica se nome e fone são validos(deixei  email opcional no db)
                #Se o cursor existir, insere novo contato no db
                if self.cursor:
                        sql = "INSERT INTO contatos (nome_contato, telefone_contato, email_contato) VALUES (%s, %s, %s)"
                        self.cursor.execute(sql, (novo_nome, novo_telefone, novo_email))
                        self.commitar_conexao()
                        
                        #busca id gerado no db
                        novo_id = self.cursor.lastrowid
                        
                        #Criando o objeto novo_contato, passando id do banco para o objeto
                        novo_contato = Contato(nome=novo_nome, telefone=novo_telefone, email=novo_email, id=novo_id)

                        #Adicionando o contato na lista
                        self.lista_de_contatos.append(novo_contato)
                        
                        #para reaproveitamento
                        return novo_contato
            else:
                #levanta exceção se Nome ou Fone não forem validos
                raise ValueError("Nome e Telefone devem ser preenchidos.")
        #Se der erro no MYSQL  
        except Error as error:
                print(f"Erro no MYSQL ao adicionar contato: {error}")           
    #Edita contato pelo id
    def editar_contato(self, indice, novo_nome, novo_telefone, novo_email=None):
        try:
            #Verificar se o índice existe
            if 0 <= indice < len(self.lista_de_contatos):#se indice maior que 0 e no range da lista 
                #Verifica se nome e telefone são nulos e levanta exceção, caso sim
                if not novo_nome.strip() or not novo_telefone.strip():
                    raise ValueError("Nome e telefone devem ser preenchidos.")     
                
                #Pega os dados do objeto contato e atualiza com os novos dados
                contato = self.lista_de_contatos[indice]
                contato.nome = novo_nome
                contato.telefone =  novo_telefone
                contato.email = novo_email
                
                #Atualiza banco
                sql = "UPDATE contatos SET nome_contato = %s, telefone_contato = %s, email_contato = %s WHERE id_contato = %s"
                if self.cursor:
                    self.cursor.execute(sql,(contato.nome, contato.telefone, contato.email, contato.id))
                    self.commitar_conexao()
                    return True # Contato Atualizado.
            return False # id invalido ou cursor não existe
                    
        except Error as error:
            print(f"Erro no MYSQL ao editar contato: {error}")
            return False #Problema no mysql
    #remove contato pelo id
    def remover_contato(self, indice):
        try:
            #Verificar se o índice existe
            if 0 <= indice < len(self.lista_de_contatos):
                #localiza objeto pelo id
                contato = self.lista_de_contatos[indice]
                sql = "DELETE FROM contatos WHERE id_contato = %s"
                #Se o cursor existir, remove contato
                if self.cursor:
                    self.cursor.execute(sql,(contato.id,))
                    self.commitar_conexao()
                #deleta objeto da lista
                del self.lista_de_contatos[indice]
                return True
            return False # Caso cursor ou id não existam
        except Error as error:
            print(f"Erro no MYSQL ao deletar contato: {error}")
            return False #Problema no mysql
    #Para não repetir logica de commit
    def commitar_conexao(self):
        if self.conexao:
            self.conexao.commit()
    #Encerra conexão       
    def fechar_conexao(self):
        if self.cursor and self.conexao:
            print("Encerrando conexão...")
            self.cursor.close()
            self.conexao.commit()
            
