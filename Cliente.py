from Livro import Livro
from Pessoa import Pessoa

class Cliente(Pessoa):
    def __init__(self, nome : str, cpf : str):
        super().__init__(nome=nome)
        self.cpf = cpf
        self.email = None

    def set_email(self, email : str):
        self.email = email

    def get_cpf(self) -> str:
        return self.cpf

    def get_email(self) -> str:
        return self.email
