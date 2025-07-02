import tkinter as tk
from gui.interface import AgendaApp #Chama objeto pra criar a interface

#Criar a janela e rodar o App
if __name__ == "__main__":
    #cria janela
    janela = tk.Tk()
    #cria objeto do app
    app = AgendaApp()
    #cria a interface na janela
    app.criar_interface(janela)
    #Inicia o programa
    janela.mainloop()