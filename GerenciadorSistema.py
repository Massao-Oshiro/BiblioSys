from GerenciadorBancoDados import GerenciadorBancoDados
from Bibliotecario import Bibliotecario
from RelatoriosExcel import RelatoriosExcel
from Cliente import Cliente
from Pessoa import Pessoa
from Livro import Livro
from typing import List
from datetime import datetime, timedelta

class GerenciadorSistema:
    senha_sistema = "BiblioSys123"
    def __init__(self):
        self.gerenciador_banco_dados = GerenciadorBancoDados()
        self.relatorios = RelatoriosExcel()
        self.cadastrar_todos_os_bibliotecarios()

    def cadastrar_todos_os_bibliotecarios(self):
        try:
            with open('bibliotecarios.txt', 'r', encoding='utf-8') as bibliotecarios:
                for linha in bibliotecarios:
                    linha_limpa = linha.strip()
                    if not linha_limpa: continue # Pula linhas em branco

                    informacoes_bibliotecario = linha_limpa.split(',')
                    if len(informacoes_bibliotecario) == 2:
                        nome = informacoes_bibliotecario[0].strip()
                        id_bibliotecario = informacoes_bibliotecario[1].strip() # <-- O .strip() aqui é a correção chave

                        bibliotecario_recuperado = Bibliotecario(nome=nome, id_bibliotecario=id_bibliotecario)
                        self.gerenciador_banco_dados.cadastrar_pessoa(pessoa=bibliotecario_recuperado)
        except FileNotFoundError:
            print("arquivo 'bibliotecarios.txt' não encontrado.")
        except Exception as e:
            print(f"erro ao cadastrar os funcionarios: {e}")

    def cadastrar_livro(self, titulo : str, autor : str, id_livro : str):
        livro = Livro(titulo=titulo, autor=autor, id_livro=id_livro)
        self.gerenciador_banco_dados.cadastrar_livro(livro=livro)
    
    def cadastrar_cliente(self, nome : str, cpf : str):
        cliente = Cliente(nome=nome, cpf=cpf)
        self.gerenciador_banco_dados.cadastrar_pessoa(pessoa=cliente)

    def registrar_emprestimo_usuario(self, cpf: str, id_livro: str):
        """CORRIGIDO: Passa os dados corretos, incluindo a data do empréstimo."""
        # A lógica de validação robusta agora está no GerenciadorBancoDados
        # Esta função apenas chama a função correspondente no GBD
        return self.gerenciador_banco_dados.cadastrar_emprestimo(cpf_cliente=cpf, id_livro=id_livro)


    def registrar_devolucao_emprestimo_usuario(self, cpf : str):
        """CORRIGIDO: Repassa o status de sucesso/falha da operação."""
        return self.gerenciador_banco_dados.registrar_devolucao_emprestimo_usuario(cpf=cpf)

    def calcular_multa(self, cpf : str):
        #calcula o valor da multa de um usuário a partir do cpf de um usuário
        self.gerenciador_banco_dados.calcular_multa(cpf=cpf)

    def registrar_pagamento_multa_usuario(self, cpf : int):
        self.gerenciador_banco_dados.registrar_pagamento_multa_usuario(cpf=cpf)

    def consultar_livros_por_titulo(self, titulo :str) -> List[Livro]:
        return self.gerenciador_banco_dados.consultar_livros_por_titulo(titulo=titulo)

    def listar_todos_clientes(self) -> List[Cliente]:
        return self.gerenciador_banco_dados.listar_todos_clientes()
    
    def listar_acervo(self) -> List[Livro]:
        return self.gerenciador_banco_dados.listar_acervo()
    
    def consultar_livro_autor(self, autor : str) -> List[Livro]:
        return self.gerenciador_banco_dados.consultar_livros_por_autor(autor=autor)
    
    def gerar_relatorio_acervo(self):
        self.relatorios.gerar_relatorio_acervo()
    
    def gerar_relatorio_emprestimos(self):
        self.relatorios.gerar_relatorio_emprestimos()
    
    def gerar_relatorio_clientes(self):
        self.relatorios.gerar_relatorio_clientes()
    
    def fechar_conexao_banco_dados(self):
        self.gerenciador_banco_dados.fechar_conexao()
    
    def autenticar(self, login : str, senha : str) -> bool:
        if not self.gerenciador_banco_dados.recuperar_bibliotecario_por_id(id_bibliotecario=login):
            return False
        
        if senha != GerenciadorSistema.senha_sistema:
            print("senha incorreta")
            return False
        
        return True
    
    def consultar_clientes_por_nome(self, nome: str) -> List[Cliente]:
        """ADICIONADO: Repassa a chamada para o GerenciadorBancoDados."""
        return self.gerenciador_banco_dados.consultar_clientes_por_nome(nome=nome)
        
    def consultar_clientes_por_livro_emprestado(self, id_livro: str) -> List[Cliente]:
        """ADICIONADO: Repassa a chamada para o GerenciadorBancoDados."""
        return self.gerenciador_banco_dados.consultar_clientes_por_livro_emprestado(id_livro=id_livro)

gerenciador = GerenciadorSistema()