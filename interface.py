import customtkinter as ctk
from TelaLogin import TelaLogin
from GerenciadorSistema import GerenciadorSistema # << IMPORTANTE

if __name__ == "__main__":
    try:
        # 1. Cria a instância principal do seu gerenciador de sistema
        # Esta instância será usada por toda a aplicação.
        # O __init__ de GerenciadorSistema tentará ler 'bibliotecarios.txt'
        gerenciador_app = GerenciadorSistema()
        print("GerenciadorSistema inicializado.") # Para depuração

        # 2. Cria e exibe a TelaLogin, passando a instância do gerenciador
        app_login = TelaLogin(gerenciador_sistema_instancia=gerenciador_app)
        print("TelaLogin inicializada.") # Para depuração
        app_login.mainloop() # Inicia o loop da interface gráfica (TelaLogin)

        # Este código só será executado após a janela principal (app_login ou app_principal) ser fechada.
        print("Aplicação encerrada. Fechando conexão com o banco de dados...")
        gerenciador_app.fechar_conexao_banco_dados()

    except FileNotFoundError as fnf_error:
        print(f"ERRO CRÍTICO: Arquivo não encontrado durante a inicialização: {fnf_error}.")
        print("Verifique se 'bibliotecarios.txt' e outros arquivos de dados necessários existem no local correto.")
    except Exception as e:
        print(f"Ocorreu um erro geral não tratado na aplicação: {e}")
        # Em um app real, você poderia logar este erro de forma mais robusta.