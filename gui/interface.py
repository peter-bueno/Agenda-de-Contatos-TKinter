import tkinter as tk
from tkinter import ttk, messagebox
from core.agenda import Agenda

class AgendaApp:

    #centraliza janela
    def centralizar_janela(self,janela, largura, altura):
        # Calcula posição para centralizar a janela na tela
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    #Cria interface
    def criar_interface(self, janela):
        self.janela = janela
        self.janela.title(" Agenda de Contatos")
        self.centralizar_janela(janela, 700, 500)

        # Criando modo escuro simples com fundo escuro e texto claro
        bg_color = "#2b2b2b"
        fg_color = "#FFFFFF"
        entry_bg = "#3c3f41"

        #configura cor de fundo da janela
        self.janela.configure(bg=bg_color)
        
        #cria gerenciador do app
        self.gerenciador = AgendaManager()

        # Cria tema do ttk para o dark mode
        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("TLabel", background=bg_color, foreground=fg_color)
        estilo.configure("TFrame", background=bg_color)
        estilo.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color)
        estilo.configure("TButton", background=entry_bg, foreground=fg_color)
        estilo.map("TButton", background=[("active", "#3c3f41")])

        # Configura o estilo da Treeview para dark
        estilo.configure("Treeview",
            background=entry_bg,
            foreground=fg_color,
            rowheight=25,
            fieldbackground=entry_bg)
        estilo.map("Treeview", background=[("selected", "#5c5c5c")])
        estilo.configure("Treeview.Heading", background="#1e1e1e", foreground=fg_color)

        # Cria frame principal com padding na janela
        self.frame_principal = ttk.Frame(janela, padding=20)
        self.frame_principal.pack(pady=10)

        # Cria campo de Nome no frame principal
        ttk.Label(self.frame_principal, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.nome_entrada = ttk.Entry(self.frame_principal, width=35)
        self.nome_entrada.grid(row=0, column=1, padx=5, pady=5)

        # Cria campo de Telefone no frame principal
        ttk.Label(self.frame_principal, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.telefone_entrada = ttk.Entry(self.frame_principal, width=35)
        self.telefone_entrada.grid(row=1, column=1, padx=5, pady=5)

        # Cria campo de Email no frame principal
        ttk.Label(self.frame_principal, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.email_entrada = ttk.Entry(self.frame_principal, width=35)
        self.email_entrada.grid(row=2, column=1, padx=5, pady=5)

        # Cria frame dos botões na janela
        button_frame = ttk.Frame(janela, padding=10)
        button_frame.pack()

        # Botão Adicionar
        ttk.Button(button_frame, text="Adicionar", command=self.adicionar_ui).pack(side=tk.LEFT, padx=5)
        # Botão Editar
        ttk.Button(button_frame, text="Editar", command=self.editar_ui).pack(side=tk.LEFT, padx=5)
        # Botão Remover
        ttk.Button(button_frame, text="Remover", command=self.remover_ui).pack(side=tk.LEFT, padx=5)

        # Cria frame da lista
        self.lista_frame = ttk.Frame(janela, padding=10)
        self.lista_frame.pack(pady=10, fill="both", expand=True)

        # Treeview (tabela de contatos)
        self.tree = ttk.Treeview(
            self.lista_frame,
            columns=("Nome", "Telefone", "Email"),
            show="headings",
            height=10
        )
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Email", text="Email")
        self.tree.column("Nome", width=200)
        self.tree.column("Telefone", width=120)
        self.tree.column("Email", width=250)
        self.tree.pack(fill="both", expand=True)

        # 🦓 Tags para zebra striping (linhas alternadas)
        self.tree.tag_configure("odd", background="#323232")
        self.tree.tag_configure("even", background="#3a3a3a")

        # Preencher a tabela com os contatos
        self.atualizar_lista()

    #Atualizar a lista
    def atualizar_lista(self):
        #carrega dados do banco e add pra lista
        self.gerenciador.carregar()
        #Deletar tudo caso já teha cadastro
        self.tree.delete(*self.tree.get_children())

        for contato in self.gerenciador.agenda.lista_de_contatos:
            #Inserir os dados na tabela
            self.tree.insert("", tk.END, values=(contato.nome, contato.telefone, contato.email))

    #Função para adicionar contatos
    def adicionar_ui(self):
        #Pega os dados do contato
        nome = self.nome_entrada.get()
        telefone = self.telefone_entrada.get()
        email = self.email_entrada.get()

        #Se todos os campos forem preenchidos
        if nome.strip() and telefone and email.strip():
            #Adiciona os dados na agenda
            self.gerenciador.adicionar(nome=nome, telefone=telefone, email=email)
            #Atualiza a lista
            self.atualizar_lista()
            #Apaga os campos
            self.limpar_campos()
            #Mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Contato: {nome} adicionado.")
        else:
            #Mensagem de erro
            messagebox.showerror("Erro", "Nome e Telefone devem ser preenchidos!")

    #Função para editar contatos
    def editar_ui(self):
        #Selecionar da lista/tabela
        selecionado = self.tree.selection()
        #Se nenhum item for selecionado
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um contato para editar.")
            return

        #Pega os novos dados
        nome = self.nome_entrada.get()
        telefone = self.telefone_entrada.get()
        email = self.email_entrada.get()

        if nome.strip() and telefone and email.strip():
            #Selecionar o índice
            index = self.tree.index(selecionado)
            #Edita os dados salvo na agenda
            self.gerenciador.editar(index, nome, telefone, email)
            #Atualiza a lista
            self.atualizar_lista()
            #Apaga os campos
            self.limpar_campos()
            #Mensagem de sucesso
            messagebox.showinfo("Sucesso", "Contato atualizado.")
        else:
            #Mensagem de erro
            messagebox.showerror("Erro", "Nome e Telefone devem ser preenchidos.")

    #Função remover contatos
    def remover_ui(self):
        #Selecionar da lista/tabela
        selecionado = self.tree.selection()
        #Se nenhum item for selecionado
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um contato para remover.")
            return

        #Selecionar o índice
        index = self.tree.index(selecionado)
        #Remove os dados na agenda
        nome = self.gerenciador.remover(user_indice=index)
        #Atualiza a lista
        self.atualizar_lista()
        #Mensagem de sucesso
        messagebox.showinfo("Sucesso", f"Contato {nome} removido.")

    #Função para limpar os campos
    def limpar_campos(self):
        self.nome_entrada.delete(0, tk.END)
        self.telefone_entrada.delete(0, tk.END)
        self.email_entrada.delete(0, tk.END)

#Classe para gerenciar a agenda
class AgendaManager:
    def __init__(self):
        #objeto do crud
        self.agenda = Agenda()    
    
    def carregar(self):  
        #carrega dados do backend (que carrega do db)
        self.agenda.carregar_contatos()
    
    #chama adicionar do backend 
    def adicionar(self, nome, telefone, email):
        self.agenda.adicionar_contato(novo_nome=nome, novo_telefone=telefone, novo_email=email)
        
    #chama editar do backend
    def editar(self, indice, nome, telefone, email):
        #atualiza com os novos dados
        self.agenda.editar_contato(indice=indice, novo_nome=nome, novo_telefone=telefone, novo_email=email)
    
    #chama remover do backend
    def remover(self, user_indice):
        nome_removido = self.agenda.lista_de_contatos[user_indice].nome
        self.agenda.remover_contato(indice=user_indice)
        return nome_removido

