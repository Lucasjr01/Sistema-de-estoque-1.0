# Importa os módulos necessários do Tkinter e o módulo sqlite3 para banco de dados
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Cria a janela principal
root = Tk()

# Classe com funções auxiliares
class Funcoes():
    def cadastrar(self):
        valor = self.entry.get()
        print("Cadastrar:", valor)

    def atualizar(self):
        valor = self.entry.get()
        print("Atualizar:", valor)

    def pesquisar(self):
        valor = self.entry.get()
        print("Pesquisar:", valor)

    def limpar(self):
        self.entry.delete(0, END)
        for item in self.lista_tab.get_children():
            self.lista_tab.delete(item)

# Classe principal da aplicação, herdando de Funcoes
class Application(Funcoes):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.criando_botoes()
        self.lista_tabelas()
        self.Menus()
        self.banco_de_dados()
        self.listar_dados()

    # Cria a barra de menu
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        sobre_menu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Sobre", menu=sobre_menu)

        filemenu.add_command(label="Sair", command=self.root.destroy)
        sobre_menu.add_command(label="Sobre o Projeto", command=self.abrir_janela)

    # Abre a janela "Sobre o Projeto"
    def abrir_janela(self):
        nova_janela = Toplevel(self.root)
        nova_janela.title("Sobre o Projeto")
        nova_janela.geometry("400x200")
        nova_janela.configure(background="#FFFFFF")

        texto = """Projeto: MotoXpress
Dev: Lucas Junio V. 
Sistema de cadastro e controle de estoque."""

        rotulo = Label(nova_janela, text=texto, bg="#FFFFFF", fg="#000000", font=(12))
        rotulo.pack(padx=20, pady=40)

    # Configura a janela principal
    def tela(self):
        self.root.title("MotosXpress")
        self.root.configure(background="#012030")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)

    # Cria os frames da tela
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#FFFFFF")
        self.frame_1.place(relx=0, rely=0, relwidth=1, relheight=0.13)
        self.titulo = Label(self.frame_1, text="MotoXpress", bg="#FFFFFF", fg="#012030", font=("NCAA Army Black Knight", 30))
        self.titulo.place(relx=0.35, rely=0.25)

    # Cria os botões e campos principais
    def criando_botoes(self):
        self.bt_cadastrar = Button(self.root, text="CADASTRAR", command=self.abrir_janela_cadastro)
        self.bt_cadastrar.place(relx=0.83, rely=0.45, relwidth=0.1, relheight=0.05)
        self.bt_atualizar = Button(self.root, text="ATUALIZAR", command=self.atualizar)
        self.bt_atualizar.place(relx=0.83, rely=0.65, relwidth=0.1, relheight=0.05)
        self.bt_limpar = Button(self.root, text="LIMPAR", command=self.limpar)
        self.bt_limpar.place(relx=0.83, rely=0.55, relwidth=0.1, relheight=0.05)

        self.lb_codigo = Label(self.root, text="CÓDIGO/ NOME DO PRODUTO", fg="#FFFFFF", background="#012030")
        self.lb_codigo.place(relx=0.01, rely=0.18, relwidth=0.20, relheight=0.04)

        self.bt_pesquisar = Button(self.root, text="PESQUISAR", command=self.pesquisar)
        self.bt_pesquisar.place(relx=0.83, rely=0.22, relwidth=0.1, relheight=0.05)
        self.entry = Entry(self.root)
        self.entry.place(relx=0.03, rely=0.22, relwidth=0.75, relheight=0.05)

    # Cria o banco de dados e a tabela, se não existir
    def banco_de_dados(self):
        conn = sqlite3.connect('loja.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT (50) NOT NULL,
                marca TEXT (10) NOT NULL,
                modelo TEXT (15) NOT NULL,
                categoria TEXT (10) NOT NULL,
                preco FLOAT (5) NOT NULL,
                estoque INT (5) NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    # Insere dados no banco de dados
    def inserir_dados(self, produto, marca, modelo, categoria, preco, estoque):
        conn = sqlite3.connect('loja.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO estoque (produto, marca, modelo, categoria, preco, estoque)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (produto, marca, modelo, categoria, preco, estoque))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
        self.listar_dados()

    # Lista todos os dados da tabela
    def listar_dados(self):
        conn = sqlite3.connect('loja.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estoque")
        registros = cursor.fetchall()
        self.limpar()
        for row in registros:
            self.lista_tab.insert("", END, values=row)
        conn.close()

    # Cria a tabela visual (Treeview)
    def lista_tabelas(self):
        self.lista_tab = ttk.Treeview(self.root, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.lista_tab.heading("col1", text="Código", anchor="center")
        self.lista_tab.heading("col2", text="Produto", anchor="center")
        self.lista_tab.heading("col3", text="Marca", anchor="center")
        self.lista_tab.heading("col4", text="Modelo", anchor="center")
        self.lista_tab.heading("col5", text="Categoria", anchor="center")
        self.lista_tab.heading("col6", text="Preço", anchor="center")
        self.lista_tab.heading("col7", text="Estoque", anchor="center")

        self.lista_tab.column("#0", width=0, stretch=NO)
        self.lista_tab.column("col1", width=20, anchor="center")
        self.lista_tab.column("col2", width=100, anchor="center")
        self.lista_tab.column("col3", width=50, anchor="center")
        self.lista_tab.column("col4", width=60, anchor="center")
        self.lista_tab.column("col5", width=50, anchor="center")
        self.lista_tab.column("col6", width=20, anchor="center")
        self.lista_tab.column("col7", width=20, anchor="center")

        self.lista_tab.place(relx=0.03, rely=0.30, relwidth=0.75, relheight=0.69)

        self.scroolLista = Scrollbar(self.root, orient="vertical")
        self.lista_tab.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.configure(command=self.lista_tab.yview)
        self.scroolLista.place(relx=0.76, rely=0.30, relwidth=0.02, relheight=0.69)

    # Realiza pesquisa por código ou nome do produto
    def pesquisar(self):
        termo = self.entry.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um código ou produto para pesquisar.")
            return

        try:
            conn = sqlite3.connect('loja.db')
            cursor = conn.cursor()

            try:
                codigo = int(termo)
                cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (codigo,))
            except ValueError:
                cursor.execute("SELECT * FROM estoque WHERE produto LIKE ?", (f"%{termo}%",))

            resultados = cursor.fetchall()
            conn.close()

            self.limpar()

            if resultados:
                for item in resultados:
                    self.lista_tab.insert("", END, values=item)
            else:
                messagebox.showinfo("Resultado", "Nenhum produto encontrado.")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    # Abre janela para cadastrar novo produto
    def abrir_janela_cadastro(self):
        janela_cadastro = Toplevel(self.root)
        janela_cadastro.title("Cadastrar Produto")
        janela_cadastro.geometry("600x500")
        janela_cadastro.configure(background="#012030")

        # Criação dos campos do formulário
        # (repetido para cada atributo)
        Label(janela_cadastro, text="Produto:").place(x=20, y=30)
        entry_produto = Entry(janela_cadastro)
        entry_produto.place(x=125, y=30, relwidth=0.75, relheight=0.05)

        Label(janela_cadastro, text="Marca:").place(x=20, y=90)
        entry_marca = Entry(janela_cadastro)
        entry_marca.place(x=125, y=90, relwidth=0.75, relheight=0.05)

        Label(janela_cadastro, text="Modelo:").place(x=20, y=150)
        entry_modelo = Entry(janela_cadastro)
        entry_modelo.place(x=125, y=150, relwidth=0.75, relheight=0.05)

        Label(janela_cadastro, text="Categoria:").place(x=20, y=210)
        entry_categoria = Entry(janela_cadastro)
        entry_categoria.place(x=125, y=210, relwidth=0.75, relheight=0.05)

        Label(janela_cadastro, text="Preço:").place(x=20, y=270)
        entry_preco = Entry(janela_cadastro)
        entry_preco.place(x=125, y=270, relwidth=0.75, relheight=0.05)

        Label(janela_cadastro, text="Estoque:").place(x=20, y=330)
        entry_estoque = Entry(janela_cadastro)
        entry_estoque.place(x=125, y=330, relwidth=0.75, relheight=0.05)

        # Salva os dados no banco
        def salvar_produto():
            produto = entry_produto.get()
            marca = entry_marca.get()
            modelo = entry_modelo.get()
            categoria = entry_categoria.get()
            preco = entry_preco.get()
            estoque = entry_estoque.get()
            self.inserir_dados(produto, marca, modelo, categoria, preco, estoque)
            janela_cadastro.destroy()

        Button(janela_cadastro, text="Salvar", command=salvar_produto).place(x=275, y=400, relwidth=0.10, relheight=0.05)

    # Abre janela de atualização de produto
    def atualizar(self):
        janela_atualizar = Toplevel(self.root)
        janela_atualizar.title("Atualizar Produto")
        janela_atualizar.geometry("700x500")
        janela_atualizar.configure(background="#012030")

        # Campos de entrada
        Label(janela_atualizar, text="Código:").place(x=20, y=30)
        entry_codigo = Entry(janela_atualizar)
        entry_codigo.place(x=135, y=30, relwidth=0.50, relheight=0.05)

        Label(janela_atualizar, text="Produto:").place(x=20, y=80)
        entry_produto = Entry(janela_atualizar)
        entry_produto.place(x=135, y=80, relwidth=0.75, relheight=0.05)

        Label(janela_atualizar, text="Marca:").place(x=20, y=130)
        entry_marca = Entry(janela_atualizar)
        entry_marca.place(x=135, y=130, relwidth=0.75, relheight=0.05)

        Label(janela_atualizar, text="Modelo:").place(x=20, y=180)
        entry_modelo = Entry(janela_atualizar)
        entry_modelo.place(x=135, y=180, relwidth=0.75, relheight=0.05)

        Label(janela_atualizar, text="Categoria:").place(x=20, y=230)
        entry_categoria = Entry(janela_atualizar)
        entry_categoria.place(x=135, y=230, relwidth=0.75, relheight=0.05)

        Label(janela_atualizar, text="Preço:").place(x=20, y=280)
        entry_preco = Entry(janela_atualizar)
        entry_preco.place(x=135, y=280, relwidth=0.75, relheight=0.05)

        Label(janela_atualizar, text="Estoque:").place(x=20, y=330)
        entry_estoque = Entry(janela_atualizar)
        entry_estoque.place(x=135, y=330, relwidth=0.75, relheight=0.05)

        # Busca produto pelo código e preenche os campos
        def buscar_produto():
            codigo = entry_codigo.get().strip()
            if not codigo.isdigit():
                messagebox.showwarning("Aviso", "Digite um código válido.")
                return

            try:
                conn = sqlite3.connect('loja.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (codigo,))
                resultado = cursor.fetchone()
                conn.close()

                if resultado:
                    _, produto, marca, modelo, categoria, preco, estoque = resultado
                    entry_produto.insert(0, produto)
                    entry_marca.insert(0, marca)
                    entry_modelo.insert(0, modelo)
                    entry_categoria.insert(0, categoria)
                    entry_preco.insert(0, preco)
                    entry_estoque.insert(0, estoque)
                else:
                    messagebox.showinfo("Resultado", "Produto não encontrado.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar: {e}")

        # Salva os novos dados no banco
        def salvar_atualizacao():
            codigo = entry_codigo.get().strip()
            if not codigo.isdigit():
                messagebox.showwarning("Aviso", "Código inválido.")
                return

            try:
                conn = sqlite3.connect('loja.db')
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE estoque SET
                        produto = ?, marca = ?, modelo = ?, categoria = ?, preco = ?, estoque = ?
                    WHERE codigo = ?
                """, (
                    entry_produto.get(),
                    entry_marca.get(),
                    entry_modelo.get(),
                    entry_categoria.get(),
                    entry_preco.get(),
                    entry_estoque.get(),
                    codigo
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                self.listar_dados()
                janela_atualizar.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

        Button(janela_atualizar, text="Buscar", command=buscar_produto).place(x=550, y=30, relwidth=0.12, relheight=0.05)
        Button(janela_atualizar, text="Salvar", command=salvar_atualizacao).place(x=300, y=400, relwidth=0.15, relheight=0.07)


# Inicia a aplicação
Application()
root.mainloop()