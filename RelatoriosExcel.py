from GerenciadorBancoDados import GerenciadorBancoDados
from Livro import Livro
import pandas as pd

class RelatoriosExcel:
    def __init__(self):
        self.gerenciador = GerenciadorBancoDados()
    
    def gerar_relatorio_acervo(self):
        acervo = self.gerenciador.listar_acervo()
        if not acervo:
            print("nao ha livros a relatar")
        titulos = []
        autores = []
        status = []
        ids = []

        for livro in acervo:
            titulos.append(livro.get_titulo())
            autores.append(livro.get_autor())
            status.append("alugado" if livro.get_status() else "não alugado")
            ids.append(str(livro.get_id_livro()))

        df = pd.DataFrame({
            'Título' : titulos,
            'Autor' : autores,
            'Status' : status,
            'Id' : ids
        })

        df.to_excel("acervo.xlsx", index=False)
    
    def gerar_relatorio_emprestimos(self):
        emprestimos = self.gerenciador.listar_emprestimos()
        if not emprestimos:
            print("nao ha emprestimos a relatar")
            return
        ids = []
        cpfs = []
        id_livros = []
        prazos = []
        multas = []

        for emprestimo in emprestimos:
            ids.append(emprestimo.get_id_emprestimo())
            cpfs.append(emprestimo.get_cpf_cliente())
            id_livros.append(emprestimo.get_id_livro())
            prazos.append(emprestimo.get_prazo())
            multas.append(f'{emprestimo.get_multa():.2f}')

        df = pd.DataFrame({
            'Id' : ids,
            'CPF' : cpfs,
            'Id livro' : id_livros,
            'Prazo' : prazos,
            'Multa' : multas
        })

        df.to_excel("emprestimos.xlsx", index=False)

    def gerar_relatorio_clientes(self):
        clientes = self.gerenciador.listar_clientes()
        if not clientes:
            print("nao ha clientes a relatar")
        nomes = []
        cpfs = []
        emails = []

        for cliente in clientes:
            nomes.append(cliente.get_nome())
            cpfs.append(cliente.get_cpf())
            emails.append(cliente.get_email())

        df = pd.DataFrame({
            'Nome' : nomes,
            'CPF' : cpfs,
            'Email' : emails
        })

        df.to_excel("clientes.xlsx", index=False)