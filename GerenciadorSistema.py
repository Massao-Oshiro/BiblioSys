from GerenciadorBancoDados import GerenciadorBancoDados
from Bibliotecario import Bibliotecario
from RelatoriosExcel import RelatoriosExcel
from Cliente import Cliente
from Pessoa import Pessoa
from Livro import Livro
from typing import List

class GerenciadorSistema:
    senha_sistema = "BiblioSys123"
    def __init__(self):
        self.gerenciador_banco_dados = GerenciadorBancoDados()
        self.relatorios = RelatoriosExcel()
        self.cadastrar_todos_os_bibliotecarios()

    def cadastrar_todos_os_bibliotecarios(self):
        #cadastra todos os bibliotecarios recuperados do arquivo bibliotecarios.txt no sistema
        try:
            #abre o arquivo txt
            with open('bibliotecarios.txt') as bibliotecarios:
                #pega as informações dos bibliotecários a partir de linhas
                for bibliotecario in bibliotecarios:
                    informacoes_bibliotecario = bibliotecario.split(',') #separada as informações recuperadas a partir de virgula e guarda em um array
                    bibliotecario_recuperado = Bibliotecario(nome=informacoes_bibliotecario[0], id_bibliotecario=informacoes_bibliotecario[1]) #recupera um objeto bibliotecario a partir das informações recuperadas
                    self.gerenciador_banco_dados.cadastrar_pessoa(pessoa=bibliotecario_recuperado) #cadastra o bibliotecario no banco de dados
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
        data_hoje = datetime.now().date()
        prazo = data_hoje + timedelta(days=15)
        return self.gerenciador_banco_dados.registrar_emprestimo_simples(
            cpf_cliente=cpf,
            id_livro=id_livro,
            data_emprestimo=data_hoje.isoformat(),
            prazo=prazo.isoformat()
        )



    def registrar_devolucao_emprestimo_usuario(self, cpf : int):
        #registra a devolução do empréstimo de um livro a partir do cpf
        self.gerenciador_banco_dados.registrar_devolucao_emprestimo_usuario(cpf=cpf)
    
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
    
    def consultar_clientes_por_nome(self, nome: str) -> List[Cliente]:
        return self.gerenciador_banco_dados.recuperar_cliente_por_nome(nome=nome)
    
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

    def consultar_clientes_com_multas(self) -> List[Cliente]:
        """ADICIONADO: Repassa a chamada para o GerenciadorBancoDados."""
        return self.gerenciador_banco_dados.consultar_clientes_com_multas()

gerenciador = GerenciadorSistema()