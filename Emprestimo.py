from datetime import datetime, timedelta

class Emprestimo:
    def __init__(self, cpf_cliente : str, id_livro : str):
        self.id_emprestimo = None
        self.cpf_cliente = cpf_cliente
        self.id_livro = id_livro
        data_atual = datetime.now().date()
        self.prazo = data_atual + timedelta(days=15)
        self.multa = 0.0
    
    def get_prazo(self) -> datetime:
        return self.prazo
    
    def get_cpf_cliente(self) -> str:
        return self.cpf_cliente
    
    def get_id_livro(self) -> str:
        return self.id_livro

    def get_id_emprestimo(self) -> int:
        return self.id_emprestimo
    
    def set_id_emprestimo(self, id_emprestimo : int):
        self.id_emprestimo = id_emprestimo

    def set_prazo(self, prazo : datetime):
        self.prazo = prazo.date()
    
    def set_multa(self, multa : float):
        self.multa = multa
    
    def get_multa(self) -> float:
        return self.multa