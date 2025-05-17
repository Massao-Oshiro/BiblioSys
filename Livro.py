class Livro:
    def __init__(self, titulo : str, autor : str, id_livro : str):
        self.titulo = titulo
        self.autor = autor
        self.status = False
        self.id_livro = id_livro
        
    def set_status(self, status: bool):
        if status < 0:
            raise ValueError("Quantidade nao pode ser negativa")
        self.status = status

    def get_status(self) -> bool:
        return self.status
    
    def get_autor(self) -> str:
        return self.autor
    
    def get_id_livro(self) -> str:
        return self.id_livro

    def get_titulo(self) -> str:
        return self.titulo