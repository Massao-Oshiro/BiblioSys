import customtkinter as ctk
from PIL import Image # Se estiver usando para a logo
# Importe GerenciadorSistema (ajuste o caminho se ele estiver em outra pasta)
# Exemplo: from seu_modulo_gerenciador import GerenciadorSistema
# Se GerenciadorSistema.py está na mesma pasta:
from GerenciadorSistema import GerenciadorSistema # << IMPORTANTE
from TelaPrincipal import TelaPrincipal
# --- Suas definições de cores ---
COR_FUNDO_ROXO = "#4B0082"
COR_PAINEL_CENTRAL = "#F0F0F0"
COR_LARANJA_CAMPOS = "#FFB74D"
COR_TEXTO_BOTAO_AVANCAR = "#FFFFFF"
COR_TEXTO_ROTULOS = "#333333"
COR_TEXTO_ACERVO = "#4B0082"
COR_TEXTO_BIBLIOSYS = COR_LARANJA_CAMPOS

class TelaLogin(ctk.CTk):
    # Adicione 'gerenciador_sistema_instancia' ao construtor
    def __init__(self, gerenciador_sistema_instancia, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Armazene a instância do gerenciador
        self.gerenciador_sistema = gerenciador_sistema_instancia

        self.title("Login - Acervo Bibliosys")
        self.geometry("800x600")
        self.configure(fg_color=COR_FUNDO_ROXO)
        self.resizable(True, True)
        # self.centralizar_janela() # Se você tiver esta função

        self.frame_central = ctk.CTkFrame(self, fg_color=COR_PAINEL_CENTRAL, corner_radius=15)
        self.frame_central.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.7)

        # Label para mensagens de erro/sucesso (inicialmente vazio)
        self.label_mensagem_login = ctk.CTkLabel(self.frame_central, text="", font=ctk.CTkFont(size=14))
        self.label_mensagem_login.pack(pady=(10,0)) # Posicione conforme seu layout

        # --- Conteúdo do Painel Central (logo, campos, etc.) ---
        # (Seu código para logo aqui)
        try:
            # Se você tem a logo como imagem
            # imagem_logo_pil = Image.open("logo.png")
            # imagem_logo_ctk = ctk.CTkImage(light_image=imagem_logo_pil, dark_image=imagem_logo_pil, size=(250, 80))
            # label_logo = ctk.CTkLabel(self.frame_central, image=imagem_logo_ctk, text="")
            # label_logo.pack(pady=(40, 20))
            pass # Remova o 'pass' se tiver código de logo
        except FileNotFoundError:
            label_logo_texto_acervo = ctk.CTkLabel(self.frame_central, text="ACERVO", font=ctk.CTkFont(size=30, weight="bold"), text_color=COR_TEXTO_ACERVO)
            label_logo_texto_acervo.pack(pady=(30,0))
            label_logo_texto_bibliosys = ctk.CTkLabel(self.frame_central, text="bibliosys", font=ctk.CTkFont(size=24, weight="bold"), text_color=COR_TEXTO_BIBLIOSYS)
            label_logo_texto_bibliosys.pack(pady=(0,20))
        except Exception as e:
            print(f"Erro ao carregar a logo: {e}")
            label_logo_fallback = ctk.CTkLabel(self.frame_central, text="ACERVO bibliosys", font=ctk.CTkFont(size=20, weight="bold"))
            label_logo_fallback.pack(pady=(40, 20))

        label_usuario = ctk.CTkLabel(self.frame_central, text="ID Bibliotecário:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_ROTULOS)
        label_usuario.pack(pady=(10,0), padx=50, anchor="w")

        self.entry_usuario = ctk.CTkEntry(self.frame_central,
                                          width=300, height=40, font=ctk.CTkFont(size=14),
                                          fg_color=COR_LARANJA_CAMPOS, border_width=0, corner_radius=10,
                                          placeholder_text="Digite seu ID", text_color="#000000")
        self.entry_usuario.pack(pady=(0, 20), padx=50)

        label_senha = ctk.CTkLabel(self.frame_central, text="Senha do Sistema:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_ROTULOS)
        label_senha.pack(pady=(10,0), padx=50, anchor="w")

        self.entry_senha = ctk.CTkEntry(self.frame_central,
                                        width=300, height=40, font=ctk.CTkFont(size=14),
                                        fg_color=COR_LARANJA_CAMPOS, border_width=0, corner_radius=10,
                                        show="*", placeholder_text="Digite a senha do sistema", text_color="#000000")
        self.entry_senha.pack(pady=(0, 30), padx=50)

        botao_avancar = ctk.CTkButton(self.frame_central,
                                      text="Avançar", command=self.funcao_avancar,
                                      width=150, height=40, font=ctk.CTkFont(size=16, weight="bold"),
                                      fg_color=COR_LARANJA_CAMPOS, text_color=COR_TEXTO_BOTAO_AVANCAR,
                                      hover_color="#FF8C00", corner_radius=10)
        botao_avancar.pack(pady=(10, 20)) # Ajustado pady

    def funcao_avancar(self):
        id_bibliotecario = self.entry_usuario.get()
        senha_sistema_digitada = self.entry_senha.get()

        # Limpa mensagem anterior
        self.label_mensagem_login.configure(text="")

        if not id_bibliotecario or not senha_sistema_digitada:
            self.label_mensagem_login.configure(text="Por favor, preencha todos os campos.", text_color="red")
            return

        # Chama o método de autenticação do GerenciadorSistema
        if self.gerenciador_sistema.autenticar(login=id_bibliotecario, senha=senha_sistema_digitada):
            self.label_mensagem_login.configure(text="Login bem-sucedido!", text_color="green")
            print("Login bem-sucedido!")

            # Fechar a janela de login
            self.destroy()

            # Abrir a tela principal (vamos criar esta classe em breve)
            # Precisamos passar a instância do gerenciador_sistema para a próxima tela também
            app_principal = TelaPrincipal(self.gerenciador_sistema) # Supondo que TelaPrincipal está definida
            app_principal.mainloop() # Inicia o loop da nova janela
        else:
            # A função autenticar já imprime "senha incorreta" no console se for o caso.
            # Ou "Bibliotecário não encontrado" implicitamente.
            self.label_mensagem_login.configure(text="ID do Bibliotecário ou Senha do Sistema inválidos.", text_color="red")
            print("Falha no login.") # Para log no console
            self.entry_senha.delete(0, 'end') # Limpa o campo de senha

    # def centralizar_janela(self): # Se você tiver esta função
    #     # ... seu código para centralizar ...
    #     pass

# Para testar esta tela isoladamente (opcional, mas útil)
# Lembre-se que GerenciadorSistema pode precisar de arquivos como 'bibliotecarios.txt'
if __name__ == "__main__":
    # Você precisaria de uma instância de GerenciadorSistema para testar
    # Supondo que GerenciadorSistema.py está na mesma pasta
    # e que o arquivo bibliotecarios.txt existe e é acessível.
    try:
        gerenciador_para_teste = GerenciadorSistema()
        app = TelaLogin(gerenciador_sistema_instancia=gerenciador_para_teste)
        app.mainloop()
        # É uma boa prática fechar a conexão do banco ao final, se o app for encerrado aqui
        gerenciador_para_teste.fechar_conexao_banco_dados()
    except Exception as e_teste:
        print(f"Erro ao iniciar para teste: {e_teste}")