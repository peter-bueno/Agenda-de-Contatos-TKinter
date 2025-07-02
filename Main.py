import tkinter as tk
from core.agenda import Agenda
from gui.interface import AgendaApp #Chama objeto pra criar a interface

#Criar a janela e rodar o App
if __name__ == "__main__":
    #cria janela
    janela = tk.Tk()
    
    #cria a interface na janela
    app = AgendaApp()
    app.criar_interface(janela)
    
    #Inicia o programa
    janela.mainloop()
    
    #encerra conexão com db, dps do programa encerrado
    fechar = Agenda()
    fechar.fechar_conexao()