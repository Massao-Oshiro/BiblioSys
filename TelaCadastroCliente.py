import customtkinter as ctk
from PIL import Image

# --- Definições de Cores ---
COR_FUNDO_ROXO = "#4A0C75"
COR_BARRA_MENU = "#D1D1D1"
COR_FORMULARIO = "#D9D9D9"
COR_TEXTO_LABEL = "#000000"

class TelaCadastroCliente(ctk.CTkToplevel):  # Alterado para abrir como janela secundária
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Cadastro de Cliente")
        self.geometry("800x500")
        self.configure(fg_color=COR_FUNDO_ROXO)

        # Barra de Menu Superior (Mantida da Tela Principal)
        self.frame_barra_menu = ctk.CTkFrame(self, height=50, fg_color=COR_BARRA_MENU, corner_radius=0)
        self.frame_barra_menu.pack(fill="x", side="top", padx=0, pady=0)

        self.menus_info = {
            "Cadastro": ["Livro", "Cliente"],
            "Consulta": ["Acervo", "Clientes", "Multas"],
            "Registro": ["Pagamento", "Empréstimos", "Devolução"]
        }

        for nome_menu, subitens in self.menus_info.items():
            dropdown = ctk.CTkOptionMenu(self.frame_barra_menu, values=subitens)
            dropdown.set(nome_menu)
            dropdown.pack(side="left", padx=5, pady=5)

        # Frame de Conteúdo
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.pack(fill="both", expand=True, padx=20, pady=20)

        # Logo Centralizada
        try:
            imagem_pil = Image.open("logoBranca.png")
            imagem_ctk = ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=(250, 150))
            label_logo = ctk.CTkLabel(self.frame_conteudo, image=imagem_ctk, text="")
            label_logo.pack(pady=10)
        except:
            label_logo_fallback = ctk.CTkLabel(self.frame_conteudo, text="ACERVO bibliosys",
                                               font=ctk.CTkFont(size=30, weight="bold"), text_color="white")
            label_logo_fallback.pack(pady=10)

        # Retângulo do Formulário
        frame_formulario = ctk.CTkFrame(self.frame_conteudo, fg_color=COR_FORMULARIO, corner_radius=10)
        frame_formulario.pack(pady=20, padx=20, fill="x", expand=False)

        label_titulo = ctk.CTkLabel(frame_formulario, text="Cadastro de Cliente",
                                    font=ctk.CTkFont(size=22, weight="bold"), text_color=COR_TEXTO_LABEL)
        label_titulo.pack(pady=10)

        # Campos de Entrada
        self.entry_nome = ctk.CTkEntry(frame_formulario, placeholder_text="Nome (máx. 60 caracteres)", width=400)
        self.entry_nome.pack(pady=5)

        self.entry_cpf = ctk.CTkEntry(frame_formulario, placeholder_text="CPF (máx. 11 caracteres)", width=400)
        self.entry_cpf.pack(pady=5)

        # Botão "Avançar"
        btn_avancar = ctk.CTkButton(frame_formulario, text="Avançar", command=self.avancar_cadastro, width=200)
        btn_avancar.pack(pady=10)

    def avancar_cadastro(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        print(f"Avançando cadastro com: Nome={nome}, CPF={cpf}")

if __name__ == "__main__":
    app = TelaCadastroCliente()
    app.mainloop()
