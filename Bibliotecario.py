from Pessoa import Pessoa

class Bibliotecario(Pessoa):
    def __init__(self, nome : str, id_bibliotecario : str):
        super().__init__(nome=nome)
        self.id_bibliotecario = id_bibliotecario
    
    def get_id_bibliotecario(self) -> str:
        return self.id_bibliotecario
