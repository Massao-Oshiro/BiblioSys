from Bibliotecario import Bibliotecario
from Pessoa import Pessoa
from Livro import Livro
from Cliente import Cliente
from Emprestimo import Emprestimo
from datetime import datetime
from typing import List
import sqlite3

class GerenciadorBancoDados:
    def __init__(self):
        #inicia o banco de dados do sistema
        self.conn = sqlite3.connect("BiblioSys.db") #se conecta com o banco de dados
        self.cursor = self.conn.cursor()
        self.cadastrar_tabelas() #cadastra todas as tabelas do banco de dados
    
    def __del__(self):
        self.fechar_conexao()

    def cadastrar_tabelas(self):
        #funcao para cadastrar todas as tabelas no banco de dados
        try:
            #cadastra a tabela de livros
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS livro(
                    titulo VARCHAR(100),
                    autor VARCHAR(60),
                    status INTEGER,
                    id_livro VARCHAR(10) PRIMARY KEY,
                    FOREIGN KEY (autor) REFERENCES autor(nome)
                )
            ''')

            #cadastra a tabela de clientes
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS cliente(
                    nome VARCHAR(60) NOT NULL,
                    cpf VARCHAR(11) PRIMARY KEY,
                    email VARCHAR(50)
                )
            ''')

            #cadastra a tabela de bibliotecarios
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS bibliotecario(
                    nome VARCHAR(60) NOT NULL,
                    id_bibliotecario VARCHAR(5) PRIMARY KEY
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS emprestimo(
                    id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpf_cliente VARCHAR(11) NOT NULL,
                    id_livro VARCHAR(10) NOT NULL,
                    prazo TEXT NOT NULL,
                    multa FLOAT NOT NULL,
                    FOREIGN KEY (cpf_cliente) REFERENCES cliente(cpf),
                    FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS autor(
                    id_autor INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(60) NOT NULL UNIQUE
                )
            ''')

            self.conn.commit()

        except sqlite3.Error as e:
            print(f'Erro ao criar tabelas no banco de dados: {e}')
    
    def recuperar_livro_por_id(self, id_livro : str) -> Livro:
        #busca e retorna o livro do banco de dados a partir do id fornecido
        try:
            if id_livro is None:
                print("id livro é nulo")
                return None
            
            self.cursor.execute('''
                SELECT titulo, autor, status, id_livro FROM livro WHERE id_livro = ?
            ''', (id_livro,))

            livro_recuperado_tupla = self.cursor.fetchone()

            if not livro_recuperado_tupla:
                print("livro nao cadastrado")
                return None
            
            livro_recuperado = Livro(titulo=livro_recuperado_tupla[0], autor=livro_recuperado_tupla[1], id_livro=livro_recuperado_tupla[3])
            livro_recuperado.set_status(status=True if livro_recuperado_tupla[2] == 1 else False)
            return livro_recuperado
        
        except sqlite3.Error as e:
            print(f'erro ao recuperar livro {e}')
            return None
        
        
    def recuperar_cliente(self, cpf : str) -> Cliente:
        #busca e retorna o cliente do banco de dados a partir do cpf fornecido
        try:
            self.cursor.execute('''
                SELECT nome, cpf, email FROM cliente WHERE cpf = ?
            ''', (cpf,))

            cliente_recuperado_tupla = self.cursor.fetchone()

            if not cliente_recuperado_tupla:
                print("cliente nao cadastrado")
                return None
            
            cliente_recuperado = Cliente(nome=cliente_recuperado_tupla[0], cpf=cliente_recuperado_tupla[1])
            cliente_recuperado.set_email(email=cliente_recuperado_tupla[2])
            return cliente_recuperado
            
        except sqlite3.Error as e:
            print(f'erro ao recuperar cliente {e}')
            return None
        
    def recuperar_emprestimo(self, cpf : str) -> Emprestimo:
        try:
            self.cursor.execute('''
                SELECT id_emprestimo, cpf_cliente, id_livro, prazo, multa FROM emprestimo WHERE cpf_cliente = ?
            ''', (cpf,))

            emprestimo_recuperado_tupla = self.cursor.fetchone()

            if not emprestimo_recuperado_tupla:
                print("Emprestimo nao cadastrado")
                return None
            
            emprestimo_recuperado = Emprestimo(cpf_cliente=emprestimo_recuperado_tupla[1], id_livro=emprestimo_recuperado_tupla[2])
            emprestimo_recuperado.set_id_emprestimo(id_emprestimo=emprestimo_recuperado_tupla[0])
            data_recuperada = datetime.strptime(emprestimo_recuperado_tupla[3], '%Y-%m-%d')
            emprestimo_recuperado.set_prazo(prazo=data_recuperada)
            emprestimo_recuperado.set_multa(multa=emprestimo_recuperado_tupla[4])
            return emprestimo_recuperado
            
        except sqlite3.Error as e:
            print(f'erro ao recuperar cliente {e}')
            return None
        
    def recuperar_bibliotecario_por_id(self, id_bibliotecario : str) -> Bibliotecario:
        #busca e retorna o bibliotecario do banco de dados a partir do id fornecido
        try:
            self.cursor.execute('''
                SELECT nome, id_bibliotecario FROM bibliotecario WHERE id_bibliotecario = ?
            ''', (id_bibliotecario,))

            bibliotecario_recuperado_tupla = self.cursor.fetchone()

            if not bibliotecario_recuperado_tupla:
                print("bibliotecario nao cadastrado")
                return None
            
            bibliotecario_recuperado = Bibliotecario(nome=bibliotecario_recuperado_tupla[0], id_bibliotecario=bibliotecario_recuperado_tupla[1])
            return bibliotecario_recuperado
            
        except sqlite3.Error as e:
            print(f'erro ao recuperar pessoa {e}')
            return None
    
    def recuperar_autor(self, nome : str):
        try:
            self.cursor.execute('''
                SELECT id_autor, nome FROM autor WHERE nome = ? 
            ''', (nome,))

            autor_recuperado_tupla = self.cursor.fetchone()

            if not autor_recuperado_tupla:
                print("autor nao cadastrado")
                return None
            
            return autor_recuperado_tupla
        except sqlite3.Error as e:
            print(f'erro ao recuperar autor {e}')
            return None

    def cadastrar_livro(self, livro : Livro):
        #cadastra o livro no banco de dados caso ele já não estiver cadastrado a partir do objeto fornecido
        try:
            livro_existente = self.recuperar_livro_por_id(id_livro=livro.get_id_livro())
            if livro_existente:
                print(f'livro {livro.get_titulo()} já está cadastrado')
                return
            
            self.cursor.execute('''
                INSERT INTO livro (titulo, autor, status, id_livro) VALUES (?, ?, ?, ?)
            ''', (livro.get_titulo(), livro.get_autor(),1 if livro.get_status() else 0, livro.get_id_livro()))
            self.cadastrar_autor(nome=livro.get_autor())
            self.conn.commit()
            print("livro cadastrado com sucesso")

        except sqlite3.Error as e:
            print(f'erro ao cadastrar livro no banco de dados {e}')
    
    def cadastrar_emprestimo(self, cpf_cliente : str, id_livro : str):
        try:
            emprestimo_recuperado = self.recuperar_emprestimo(cpf=cpf_cliente)
            if emprestimo_recuperado:
                print(f'emprestimo {emprestimo_recuperado.get_id_emprestimo()}')
                return

            emprestimo = Emprestimo(cpf_cliente=cpf_cliente, id_livro=id_livro)
            data_emprestimo = emprestimo.get_prazo().strftime('%Y-%m-%d')
            livro_recuperado = self.recuperar_livro_por_id(id_livro=id_livro)
            livro_recuperado.set_status(status=True)

            self.cursor.execute('''
                INSERT INTO emprestimo (cpf_cliente, id_livro, prazo, multa)
                VALUES (?, ?, ?, ?)
            ''', (cpf_cliente, id_livro, data_emprestimo, emprestimo.get_multa()))
            
            self.cursor.execute('''
                UPDATE livro SET status = ? WHERE id_livro = ?
            ''', (1 if livro_recuperado.get_status() else 0, id_livro))
            self.conn.commit()
            print("emprestimo cadastrado com sucesso")
        except sqlite3.Error as e:
            print(f'erro ao cadastrar emprestimo {e}')
    
    def cadastrar_autor(self, nome : str):
        try:
            if self.recuperar_autor(nome=nome):
                print("autor ja cadastrado")
                return
            
            self.cursor.execute('''
                INSERT INTO autor (nome)
                VALUES (?)
            ''', (nome,))

            self.conn.commit()
            print("autor cadastrado")
        except sqlite3.Error as e:
            print(f'erro ao cadastrar autor {e}')

    def cadastrar_pessoa(self, pessoa : Pessoa):
        #cadastra uma pessoa no banco de dados polimorficamente (cliente ou bibliotecario) caso não estiver cadastrado a partir do objeto fornecido
        try:
            if isinstance(pessoa, Cliente):
                if self.recuperar_cliente(cpf=pessoa.get_cpf()):
                    print("cliente ja cadastrado")
                    return
                
                self.cursor.execute('''
                    INSERT INTO cliente (nome, cpf, email)
                    VALUES (?, ?, ?)
                ''', (pessoa.get_nome(), pessoa.get_cpf(), pessoa.get_email()))
                self.conn.commit()
                print("cliente cadastrado com sucesso")
                return
            
            elif isinstance(pessoa, Bibliotecario):
                bibliotecario_existente = self.recuperar_bibliotecario_por_id(id_bibliotecario=pessoa.get_id_bibliotecario())
                if bibliotecario_existente:
                    print("bibliotecario ja cadastrado")
                    return
                
                self.cursor.execute('''
                    INSERT INTO bibliotecario (nome, id_bibliotecario)
                    VALUES (?, ?)
                ''', (pessoa.get_nome(), pessoa.get_id_bibliotecario()))
                self.conn.commit()
                print("bibliotecario cadastrado com sucesso")
                return
        
        except sqlite3.Error as e:
            print(f'erro ao cadastrar pessoa no banco de dados {e}')

    def registrar_devolucao_emprestimo_usuario(self, cpf : str):
        #registra a devolução do empréstimo de um livro a partir do cpf
        try:            
            emprestimo_recuperado = self.recuperar_emprestimo(cpf=cpf)

            if not emprestimo_recuperado:
                print("cliente nao possui nenhum livro alugado")
                return
        
            if emprestimo_recuperado.get_prazo():
                self.calcular_multa(cpf=cpf)
                if emprestimo_recuperado.get_multa() > 0:
                    print("usuario deve pagar multa antes de fazer a devolucao")
                    return
            
            livro_recuperado = self.recuperar_livro_por_id(id_livro=emprestimo_recuperado.get_id_livro())
            livro_recuperado.set_status(status=False)

            self.cursor.execute('''
                DELETE FROM emprestimo WHERE cpf_cliente = ?
            ''', (cpf,))

            self.cursor.execute('''
                UPDATE livro SET status = ? WHERE id_livro = ?
            ''', (1 if livro_recuperado.get_status() else 0, livro_recuperado.get_id_livro()))
            self.conn.commit()
            print("devolucao feita com sucesso")

        except sqlite3.Error as e:
            print("erro ao registrar devolucao de emprestimo {e}")
        

    def calcular_multa(self, cpf : str):
        #calcula o valor da multa de um usuário a partir do cpf de um usuário
        try:
            emprestimo_recuperado = self.recuperar_emprestimo(cpf=cpf)
            if not emprestimo_recuperado:
                return
            
            data_atual = datetime.now().date()
            prazo = emprestimo_recuperado.get_prazo()
            if data_atual > prazo:
                dias_atraso = (data_atual - prazo).days
                if dias_atraso > 0:
                    multa = dias_atraso * 0.5
                    emprestimo_recuperado.set_multa(multa=multa)
                    self.cursor.execute('''
                        UPDATE emprestimo SET multa = ? WHERE id_emprestimo = ?
                    ''', (emprestimo_recuperado.get_multa(), emprestimo_recuperado.get_id_emprestimo()))
                    self.conn.commit()
            
            else:
                print("dentro do prazo")
        except sqlite3.Error as e:
            print(f'erro ao calcular multa do cliente {e}')
    
    def registrar_pagamento_multa_usuario(self, cpf : str):
        #registra o pagamento da multa de um usuário a partir do cpf de um usuário
        try:
            emprestimo_recuperado = self.recuperar_emprestimo(cpf=cpf)
            if not emprestimo_recuperado:
                return
            
            if emprestimo_recuperado.get_multa() == 0:
                print("cliente nao tem multa a pagar")
                return
            
            emprestimo_recuperado.set_multa(multa=0.0)
            emprestimo_recuperado.set_prazo_entrega(None)
            self.cursor.execute('''
                UPDATE emprestimo SET multa = ?, prazo = ? WHERE id_emprestimo = ?
            ''', (emprestimo_recuperado.get_multa(), emprestimo_recuperado.get_prazo(), emprestimo_recuperado.get_id_emprestimo()))
            self.conn.commit()

        except sqlite3.Error as e:
            print("erro ao registrar pagamento de multa {e}")

    def consultar_livros_por_titulo(self, titulo :str) -> List[Livro]:
        #consulta e retorna uma lista de objetos Livro a partir do título do livro 
        try:
            self.cursor.execute('''
                SELECT id_livro FROM livro WHERE titulo LIKE ?
            ''', ('%' + titulo + '%',))

            lista_ids_tupla = self.cursor.fetchall()

            if not lista_ids_tupla:
                print("nenhum livro com esse titulo")
                return []
            
            lista_livros = []

            for (id,) in lista_ids_tupla:
                livro_recuperado = self.recuperar_livro_por_id(id_livro=id)
                if livro_recuperado:
                    lista_livros.append(livro_recuperado)
            
            return lista_livros

        except sqlite3.Error as e:
            print(f'erro ao consultar livros por titulo {e}')
            return []

    def listar_todos_clientes(self) -> List[Cliente]:
        #retorna uma lista de objetos Cliente de todos os clientes registrados no banco de dados em ordem alfabética
        try:
            self.cursor.execute('''
                SELECT cpf FROM cliente
            ''')

            lista_cpfs_tupla = self.cursor.fetchall()

            if not lista_cpfs_tupla:
                return []
            
            lista_clientes = []

            for (cpf,) in lista_cpfs_tupla:
                cliente_recuperado = self.recuperar_cliente(cpf=cpf)
                if cliente_recuperado:
                    lista_clientes.append(cliente_recuperado)
            
            lista_clientes_ordem_alfabetica = sorted(lista_clientes, key=lambda c : c.get_nome())
            
            return lista_clientes_ordem_alfabetica

        except sqlite3.Error as e:
            print(f'erro ao listar todos os clientes {e}')
            return []
    
    def listar_acervo(self) -> List[Livro]:
        try:
            self.cursor.execute('''
                SELECT id_livro FROM livro
            ''')

            lista_acervo_tupla = self.cursor.fetchall()

            if not lista_acervo_tupla:
                return []

            lista_acervo = []

            for (id_livro,) in lista_acervo_tupla:
                livro_recuperado = self.recuperar_livro_por_id(id_livro=id_livro)
                if livro_recuperado:
                    lista_acervo.append(livro_recuperado)
            
            lista_acervo_ordem_alfabetica = sorted(lista_acervo, key=lambda l : l.get_id_livro())

            return lista_acervo_ordem_alfabetica

        except sqlite3.Error as e:
            print(f'erro ao listar acervo {e}')
    
    def listar_emprestimos(self) -> List[Emprestimo]:
        try:
            self.cursor.execute('''
                SELECT cpf_cliente FROM emprestimo
            ''')

            lista_emprestimos_tupla = self.cursor.fetchall()

            if not lista_emprestimos_tupla:
                return []

            lista_emprestimos = []

            for (cpf,) in lista_emprestimos_tupla:
                emprestimo_recuperado = self.recuperar_emprestimo(cpf=cpf)
                if emprestimo_recuperado:
                    lista_emprestimos.append(emprestimo_recuperado)

            return lista_emprestimos

        except sqlite3.Error as e:
            print(f'erro ao listar acervo {e}')
            return []
    
    def listar_clientes(self) -> List[Cliente]:
        try:
            self.cursor.execute('''
                SELECT cpf FROM cliente
            ''')

            lista_clientes_tupla = self.cursor.fetchall()

            if not lista_clientes_tupla:
                return []

            lista_clientes = []

            for (cpf,) in lista_clientes_tupla:
                cliente_recuperado = self.recuperar_cliente(cpf=cpf)
                if cliente_recuperado:
                    lista_clientes.append(cliente_recuperado)

            lista_clientes_ordem_alfabetica = sorted(lista_clientes, key=lambda c : c.get_nome())

            return lista_clientes_ordem_alfabetica

        except sqlite3.Error as e:
            print(f'erro ao listar acervo {e}')
            return []
        
    def consultar_livros_por_autor(self, autor : str) -> List[Livro]:
        try:
            self.cursor.execute('''
                SELECT id_livro FROM livro WHERE autor = ?
            ''', (autor,))

            lista_livros_tupla = self.cursor.fetchall()

            if not lista_livros_tupla:
                return []
            
            lista_livros = []

            for (id_livro,) in lista_livros_tupla:
                livro_recuperado = self.recuperar_livro_por_id(id_livro=id_livro)
                if livro_recuperado:
                    lista_livros.append(livro_recuperado)
            
            lista_livros_ordem_alfabetica = sorted(lista_livros, key=lambda l : l.get_titulo())

            return lista_livros_ordem_alfabetica
        
        except sqlite3.Error as e:
            print(f'erro ao listar livros escritos por {autor} {e}')
            return []

    def fechar_conexao(self):
        self.conn.close()
        print("conexao fechada")
