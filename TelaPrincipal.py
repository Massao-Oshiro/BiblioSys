import customtkinter as ctk
from PIL import Image
import random
import string
from datetime import date, timedelta
import sqlite3
from typing import List

# --- Definições de Cores ---
COR_FUNDO_ROXO = "#4A0C75"
COR_BARRA_MENU_SUPERIOR = "#D1D1D1"
COR_TEXTO_BEMVINDO = "#FFFFFF"
COR_TEXTO_FALLBACK_LOGO = "#FFFFFF"
COR_TEXTO_TITULO_TELAS = "#FFFFFF"
COR_FORMULARIO_FUNDO = "#D9D9D9"
COR_TEXTO_LABEL_FORM = "#000000"
COR_LARANJA_CAMPOS_BOTOES = "#FFB74D"
COR_TEXTO_BOTAO_LARANJA = "#000000"
COR_BOTAO_ACAO_SALVAR = "#28A745"
COR_TEXTO_BOTAO_SALVAR = "#FFFFFF"
COR_BOTAO_BUSCAR_CONSULTA = "#007BFF"
COR_TEXTO_BOTAO_BUSCAR = "#FFFFFF"
COR_BOTAO_VOLTAR = "#6C757D"
COR_MENU_LATERAL_CONSULTA = "#C8C8C8"
COR_BOTAO_MENU_LATERAL = "#333333"

class TelaPrincipal(ctk.CTk):
    def __init__(self, gerenciador_sistema_instancia, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gerenciador_sistema = gerenciador_sistema_instancia
        self.title("Sistema Bibliosys - Principal")
        self.geometry("1100x750")
        self.configure(fg_color=COR_FUNDO_ROXO)
        self.vars_optionmenu = {}
        self._setup_barra_menu()
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.pack(fill="both", expand=True, padx=20, pady=20)
        self.mostrar_conteudo_inicial()

    def _setup_barra_menu(self):
        self.frame_barra_menu = ctk.CTkFrame(self, height=50, fg_color=COR_BARRA_MENU_SUPERIOR, corner_radius=0)
        self.frame_barra_menu.pack(fill="x", side="top", pady=0, padx=0)
        
        # ALTERAÇÃO: Adicionado o menu "Relatórios"
        self.menus_info = {
            "Cadastro": ["--- CADASTRO ---", "Livro", "Cliente"],
            "Consulta": ["--- CONSULTA ---", "Acervo", "Clientes", "Multas"],
            "Registro": ["--- REGISTRO ---", "Pagamento", "Empréstimos", "Devolução"],
            "Relatórios": ["--- RELATÓRIOS ---", "Acervo", "Clientes", "Empréstimos"],
        }
        
        for nome_menu, subitens in self.menus_info.items():
            self.vars_optionmenu[nome_menu] = ctk.StringVar(value=nome_menu)
            dropdown = ctk.CTkOptionMenu(
                self.frame_barra_menu, values=subitens,
                command=lambda escolha, menu=nome_menu: self.acao_submenu(escolha, menu),
                variable=self.vars_optionmenu[nome_menu], width=150, height=30,
                text_color_disabled="#A0A0A0"
            )
            dropdown.pack(side="left", padx=5, pady=5)

    def mostrar_conteudo_inicial(self):
        for widget in self.frame_conteudo.winfo_children(): widget.destroy()
        try:
            imagem_pil = Image.open("logoBranca.png")
            imagem_ctk = ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=(600, 450))
            label_logo = ctk.CTkLabel(self.frame_conteudo, image=imagem_ctk, text="")
            label_logo.pack(expand=True)
        except FileNotFoundError:
            ctk.CTkLabel(self.frame_conteudo, text="ACERVO bibliosys", font=ctk.CTkFont(size=40, weight="bold"), text_color=COR_TEXTO_FALLBACK_LOGO).pack(expand=True)
        except Exception as e:
            print(f"ERRO ao carregar logoBranca.png: {e}")
            ctk.CTkLabel(self.frame_conteudo, text="Erro ao carregar logo", font=ctk.CTkFont(size=30), text_color="red").pack(expand=True)
        ctk.CTkLabel(self.frame_conteudo, text="Bem-vindo bibliotecário!", font=ctk.CTkFont(size=24, weight="bold"), text_color=COR_TEXTO_BEMVINDO).pack(pady=20)

    def acao_submenu(self, acao_selecionada, nome_menu_pai):
        if nome_menu_pai in self.vars_optionmenu:
             self.after(50, lambda: self.vars_optionmenu[nome_menu_pai].set(nome_menu_pai))
        if acao_selecionada.startswith("---") or acao_selecionada == nome_menu_pai:
            return

        # Limpa o conteúdo da tela antes de qualquer ação
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        # Mapeamento para as telas principais
        telas = {
            "Livro": self.tela_cadastro_livro, "Cliente": self.tela_cadastro_cliente,
            "Acervo": self.tela_consulta_acervo, "Clientes": self.tela_consulta_clientes,
            "Multas": self.tela_consulta_multas, "Pagamento": self.tela_registro_pagamento,
            "Empréstimos": self.tela_registro_emprestimos, "Devolução": self.tela_registro_devolucao
        }
        
        # Lógica para diferenciar relatórios de outras ações com nomes iguais
        if nome_menu_pai == "Relatórios":
            print(f"Ação de Relatório selecionada: {acao_selecionada}")
            try:
                if acao_selecionada == "Acervo":
                    self.gerenciador_sistema.gerar_relatorio_acervo()
                elif acao_selecionada == "Clientes":
                    self.gerenciador_sistema.gerar_relatorio_clientes()
                elif acao_selecionada == "Empréstimos":
                    self.gerenciador_sistema.gerar_relatorio_emprestimos()
                
                label_feedback = ctk.CTkLabel(self.frame_conteudo, text=f"Relatório '{acao_selecionada}' gerado com sucesso!", font=ctk.CTkFont(size=18, weight="bold"), text_color="green")
                label_feedback.pack(pady=50, expand=True)
            except Exception as e:
                print(f"Erro ao gerar relatório: {e}")
                label_feedback = ctk.CTkLabel(self.frame_conteudo, text=f"Erro ao gerar relatório '{acao_selecionada}'.\nVerifique o console.", font=ctk.CTkFont(size=18, weight="bold"), text_color="red")
                label_feedback.pack(pady=50, expand=True)
            self._adicionar_botao_voltar(self.frame_conteudo)

        elif acao_selecionada in telas:
            telas[acao_selecionada]()
        else:
            self._placeholder_tela(f"Tela para '{acao_selecionada}'")

    def _criar_painel_padrao_formulario(self, frame_pai, titulo_tela):
        painel = ctk.CTkFrame(frame_pai, fg_color=COR_FORMULARIO_FUNDO, corner_radius=15)
        painel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.7)
        ctk.CTkLabel(painel, text=titulo_tela, font=ctk.CTkFont(size=20, weight="bold"), text_color=COR_TEXTO_LABEL_FORM).pack(pady=(30, 20))
        return painel

    def _adicionar_botao_voltar(self, frame_pai):
        ctk.CTkButton(frame_pai, text="Voltar ao Início", command=self.mostrar_conteudo_inicial, fg_color=COR_BOTAO_VOLTAR, text_color="#FFFFFF").pack(pady=20, side="bottom", anchor="s")

    def _placeholder_tela(self, nome_tela):
        for widget in self.frame_conteudo.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.frame_conteudo, text=f"{nome_tela} (Em Construção)", font=ctk.CTkFont(size=18), text_color=COR_TEXTO_TITULO_TELAS).pack(pady=30, expand=True)
        self._adicionar_botao_voltar(self.frame_conteudo)

    # --- TELAS DE CADASTRO ---
    def tela_cadastro_cliente(self):
        frame_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_tela.pack(fill="both", expand=True)
        painel_formulario = self._criar_painel_padrao_formulario(frame_tela, "CADASTRO DE CLIENTE")
        ctk.CTkLabel(painel_formulario, text="Cliente", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=50, pady=(10,0))
        self.entry_nome_cliente = ctk.CTkEntry(painel_formulario, placeholder_text="Nome completo (até 60 caracteres)", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_nome_cliente.pack(pady=(0,10), padx=50)
        ctk.CTkLabel(painel_formulario, text="CPF", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=50, pady=(10,0))
        self.entry_cpf_cliente = ctk.CTkEntry(painel_formulario, placeholder_text="Somente números (11 caracteres)", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_cpf_cliente.pack(pady=(0,20), padx=50)
        self.label_feedback_cliente = ctk.CTkLabel(painel_formulario, text="", font=ctk.CTkFont(size=12))
        self.label_feedback_cliente.pack(pady=5)
        btn_avancar = ctk.CTkButton(painel_formulario, text="Avançar", command=self.acao_efetuar_cadastro_cliente, width=200, height=35, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color=COR_TEXTO_BOTAO_LARANJA, corner_radius=10)
        btn_avancar.pack(pady=20)
        self._adicionar_botao_voltar(frame_tela)

    def acao_efetuar_cadastro_cliente(self):
        nome = self.entry_nome_cliente.get().strip(); cpf = self.entry_cpf_cliente.get().strip()
        self.label_feedback_cliente.configure(text="")
        if not nome or not cpf: self.label_feedback_cliente.configure(text="Nome e CPF são obrigatórios.", text_color="red"); return
        if len(cpf) != 11 or not cpf.isdigit(): self.label_feedback_cliente.configure(text="CPF inválido (11 dígitos numéricos).", text_color="red"); return
        try:
            if self.gerenciador_sistema.gerenciador_banco_dados.recuperar_cliente(cpf=cpf):
                self.label_feedback_cliente.configure(text=f"Cliente com CPF {cpf} já cadastrado.", text_color="orange")
            else:
                self.gerenciador_sistema.cadastrar_cliente(nome=nome, cpf=cpf)
                self.label_feedback_cliente.configure(text="Cadastro efetuado!", text_color="green")
                self.entry_nome_cliente.delete(0, 'end'); self.entry_cpf_cliente.delete(0, 'end')
        except Exception as e: self.label_feedback_cliente.configure(text="Erro ao cadastrar. Verifique o console.", text_color="red"); print(f"ERRO GUI (Cadastrar Cliente): {e}")

    def tela_cadastro_livro(self):
        frame_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_tela.pack(fill="both", expand=True)
        painel_formulario = self._criar_painel_padrao_formulario(frame_tela, "CADASTRO DE LIVRO")
        ctk.CTkLabel(painel_formulario, text="Título do Livro:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=20, pady=(10,0))
        self.entry_titulo_livro = ctk.CTkEntry(painel_formulario, placeholder_text="Ex: O Pequeno Príncipe", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_titulo_livro.pack(pady=(0,10), padx=20)
        ctk.CTkLabel(painel_formulario, text="Autor:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=20, pady=(10,0))
        self.entry_autor_livro = ctk.CTkEntry(painel_formulario, placeholder_text="Ex: Antoine de Saint-Exupéry", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_autor_livro.pack(pady=(0,20), padx=20)
        self.label_feedback_livro = ctk.CTkLabel(painel_formulario, text="", font=ctk.CTkFont(size=12))
        self.label_feedback_livro.pack(pady=5)
        btn_salvar = ctk.CTkButton(painel_formulario, text="Avançar", command=self.acao_efetuar_cadastro_livro, width=200, height=35, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color=COR_TEXTO_BOTAO_LARANJA, corner_radius=10)
        btn_salvar.pack(pady=20)
        self._adicionar_botao_voltar(frame_tela)

    def acao_efetuar_cadastro_livro(self):
        titulo = self.entry_titulo_livro.get().strip(); autor = self.entry_autor_livro.get().strip()
        self.label_feedback_livro.configure(text="")
        if not titulo or not autor: self.label_feedback_livro.configure(text="Título e Autor são obrigatórios.", text_color="red"); return
        id_livro_gerado = f"LIV{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}"
        try:
            self.gerenciador_sistema.cadastrar_livro(titulo=titulo, autor=autor, id_livro=id_livro_gerado)
            self.label_feedback_livro.configure(text="Cadastro efetuado!", text_color="green")
            self.entry_titulo_livro.delete(0, 'end'); self.entry_autor_livro.delete(0, 'end')
        except Exception as e: self.label_feedback_livro.configure(text="Erro ao cadastrar. Verifique o console.", text_color="red"); print(f"ERRO GUI (Cadastrar Livro): {e}")

    # --- TELAS DE CONSULTA ---
    def tela_consulta_acervo(self):
        frame_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_tela.pack(fill="both", expand=True)
        ctk.CTkLabel(frame_tela, text="Consulta de Acervo", font=ctk.CTkFont(size=22, weight="bold"), text_color=COR_TEXTO_TITULO_TELAS).pack(pady=(0, 5))
        frame_principal = ctk.CTkFrame(frame_tela, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, pady=(0,10))
        frame_principal.grid_columnconfigure(0, weight=1, minsize=180); frame_principal.grid_columnconfigure(1, weight=5); frame_principal.grid_rowconfigure(0, weight=1)
        frame_menu_selecao = ctk.CTkFrame(frame_principal, width=180, fg_color=COR_MENU_LATERAL_CONSULTA, corner_radius=10)
        frame_menu_selecao.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nswe")
        ctk.CTkLabel(frame_menu_selecao, text="CONSULTAR POR:", font=ctk.CTkFont(size=13, weight="bold"), text_color=COR_TEXTO_LABEL_FORM).pack(pady=15, padx=10)
        for texto_btn, tipo_con in [("Autor", "autor"), ("ID do Livro", "id"), ("Título", "titulo")]: ctk.CTkButton(frame_menu_selecao, text=texto_btn, height=30, text_color=COR_BOTAO_MENU_LATERAL, command=lambda t=tipo_con: self.preparar_consulta_acervo(t)).pack(fill="x", padx=15, pady=7)
        self.frame_conteudo_consulta = ctk.CTkFrame(frame_principal, fg_color=COR_FORMULARIO_FUNDO, corner_radius=10)
        self.frame_conteudo_consulta.grid(row=0, column=1, padx=(0,0), pady=10, sticky="nswe")
        self.mostrar_area_busca_inicial_acervo()
        self._adicionar_botao_voltar(frame_tela)

    def mostrar_area_busca_inicial_acervo(self, tipo_consulta_ativo=None, placeholder_text="Selecione um tipo de consulta à esquerda."):
        for widget in self.frame_conteudo_consulta.winfo_children(): widget.destroy()
        if tipo_consulta_ativo:
            self.entry_busca_acervo = ctk.CTkEntry(self.frame_conteudo_consulta, placeholder_text=placeholder_text, width=300, height=35)
            self.entry_busca_acervo.pack(pady=20, padx=20)
            ctk.CTkButton(self.frame_conteudo_consulta, text="Buscar", height=35, fg_color=COR_BOTAO_BUSCAR_CONSULTA, text_color=COR_TEXTO_BOTAO_BUSCAR, command=lambda: self.executar_busca_acervo(tipo_consulta_ativo, self.entry_busca_acervo.get())).pack(pady=5)
        else:
            ctk.CTkLabel(self.frame_conteudo_consulta, text=placeholder_text, font=ctk.CTkFont(size=16), text_color=COR_TEXTO_LABEL_FORM).pack(pady=50, padx=20, expand=True)
        self.frame_resultados_acervo = ctk.CTkScrollableFrame(self.frame_conteudo_consulta, label_text="Resultados da Consulta", label_text_color=COR_TEXTO_LABEL_FORM)
        self.frame_resultados_acervo.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkLabel(self.frame_resultados_acervo, text="Nenhum resultado para exibir.", text_color=COR_TEXTO_LABEL_FORM).pack(pady=20)

    def preparar_consulta_acervo(self, tipo_consulta):
        placeholders = {"autor": "Digite o nome do Autor", "id": "Digite o ID do Livro", "titulo": "Digite o Título do Livro"}
        self.mostrar_area_busca_inicial_acervo(tipo_consulta_ativo=tipo_consulta, placeholder_text=placeholders.get(tipo_consulta, "Digite sua busca"))

    def executar_busca_acervo(self, tipo_busca, termo_busca):
        for widget in self.frame_resultados_acervo.winfo_children(): widget.destroy()
        if not termo_busca.strip(): ctk.CTkLabel(self.frame_resultados_acervo, text="Digite um termo para a busca.", text_color="orange").pack(pady=20); return
        resultados = []
        try:
            if tipo_busca == "titulo": resultados = self.gerenciador_sistema.consultar_livros_por_titulo(titulo=termo_busca)
            elif tipo_busca == "autor": resultados = self.gerenciador_sistema.consultar_livro_autor(autor=termo_busca)
            elif tipo_busca == "id":
                livro = self.gerenciador_sistema.gerenciador_banco_dados.recuperar_livro_por_id(id_livro=termo_busca)
                if livro: resultados = [livro]
        except Exception as e: ctk.CTkLabel(self.frame_resultados_acervo, text=f"Erro ao buscar: {e}", text_color="red").pack(pady=10); return
        if resultados:
            headers = ["ID Livro", "Título", "Autor", "Status"]
            for col, header_text in enumerate(headers): ctk.CTkLabel(self.frame_resultados_acervo, text=header_text, font=ctk.CTkFont(weight="bold"), text_color=COR_TEXTO_LABEL_FORM).grid(row=0, column=col, padx=10, pady=5, sticky="w")
            for row_idx, livro_obj in enumerate(resultados, start=1):
                dados_livro = [livro_obj.get_id_livro(), livro_obj.get_titulo(), livro_obj.get_autor(), "Emprestado" if livro_obj.get_status() else "Disponível"]
                for col_idx, dado in enumerate(dados_livro): ctk.CTkLabel(self.frame_resultados_acervo, text=str(dado), text_color=COR_TEXTO_LABEL_FORM).grid(row=row_idx, column=col_idx, padx=10, pady=3, sticky="w")
        else: ctk.CTkLabel(self.frame_resultados_acervo, text=f"Nenhum livro encontrado para '{termo_busca}'.", text_color=COR_TEXTO_LABEL_FORM).pack(pady=20)

    def tela_consulta_clientes(self):
        for widget in self.frame_conteudo.winfo_children(): widget.destroy()
        label_titulo_tela = ctk.CTkLabel(self.frame_conteudo, text="Consulta de Clientes", font=ctk.CTkFont(size=22, weight="bold"), text_color=COR_TEXTO_TITULO_TELAS)
        label_titulo_tela.pack(pady=(10, 5))
        
        frame_tela_clientes = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_tela_clientes.pack(fill="both", expand=True, pady=(0,10))
        frame_tela_clientes.grid_columnconfigure(0, weight=1, minsize=180); frame_tela_clientes.grid_columnconfigure(1, weight=5); frame_tela_clientes.grid_rowconfigure(0, weight=1)
        
        frame_menu_selecao = ctk.CTkFrame(frame_tela_clientes, width=180, fg_color=COR_MENU_LATERAL_CONSULTA, corner_radius=10)
        frame_menu_selecao.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nswe")
        
        ctk.CTkLabel(frame_menu_selecao, text="CONSULTAR POR:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_LABEL_FORM).pack(pady=15, padx=10)
        
        # ALTERAÇÃO: Dicionário de opções atualizado, removendo "Com Multa"
        opcoes = {"CPF": "cpf", "Nome": "nome", "ID Livro": "id_livro"}
        
        for texto_btn, tipo_con in opcoes.items():
            ctk.CTkButton(frame_menu_selecao, text=texto_btn, height=30, text_color=COR_BOTAO_MENU_LATERAL, command=lambda t=tipo_con: self.preparar_consulta_clientes(t)).pack(fill="x", padx=15, pady=7)
            
        self.frame_conteudo_consulta_clientes = ctk.CTkFrame(frame_tela_clientes, fg_color=COR_FORMULARIO_FUNDO, corner_radius=10)
        self.frame_conteudo_consulta_clientes.grid(row=0, column=1, padx=(0,0), pady=10, sticky="nswe")
        
        self.mostrar_area_busca_inicial_clientes() 
        self._adicionar_botao_voltar(self.frame_conteudo)

    def mostrar_area_busca_inicial_clientes(self, tipo_consulta_ativo=None, placeholder_text="Selecione um tipo de consulta à esquerda."):
        for widget in self.frame_conteudo_consulta_clientes.winfo_children(): widget.destroy()
        if tipo_consulta_ativo:
            if tipo_consulta_ativo != "multa":
                self.entry_busca_clientes = ctk.CTkEntry(self.frame_conteudo_consulta_clientes, placeholder_text=placeholder_text, width=300, height=35)
                self.entry_busca_clientes.pack(pady=20, padx=20)
            ctk.CTkButton(self.frame_conteudo_consulta_clientes, text="Buscar", height=35, fg_color=COR_BOTAO_BUSCAR_CONSULTA, text_color=COR_TEXTO_BOTAO_BUSCAR, command=lambda: self.executar_busca_clientes(tipo_consulta_ativo, self.entry_busca_clientes.get() if hasattr(self, 'entry_busca_clientes') and tipo_consulta_ativo != "multa" else "")).pack(pady=5)
        else:
            ctk.CTkLabel(self.frame_conteudo_consulta_clientes, text=placeholder_text, font=ctk.CTkFont(size=16), text_color=COR_TEXTO_LABEL_FORM).pack(pady=50, padx=20, expand=True)
        self.frame_resultados_clientes = ctk.CTkScrollableFrame(self.frame_conteudo_consulta_clientes, label_text="Resultados da Consulta de Clientes", label_text_color=COR_TEXTO_LABEL_FORM)
        self.frame_resultados_clientes.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkLabel(self.frame_resultados_clientes, text="Nenhum resultado para exibir.", text_color=COR_TEXTO_LABEL_FORM).pack(pady=20)

    def preparar_consulta_clientes(self, tipo_consulta):
        placeholders = {"cpf": "Digite o CPF", "nome": "Digite o Nome", "id_livro": "Digite o ID do Livro", "multa": "Listar clientes com multas"}
        self.mostrar_area_busca_inicial_clientes(tipo_consulta_ativo=tipo_consulta, placeholder_text=placeholders.get(tipo_consulta, "Digite sua busca"))
        
    def executar_busca_clientes(self, tipo_busca, termo_busca):
        for widget in self.frame_resultados_clientes.winfo_children(): widget.destroy()
        if tipo_busca != "multa" and not termo_busca.strip(): ctk.CTkLabel(self.frame_resultados_clientes, text="Digite um termo para a busca.", text_color="orange").pack(pady=20); return
        resultados = []
        try:
            if tipo_busca == "cpf":
                cliente = self.gerenciador_sistema.gerenciador_banco_dados.recuperar_cliente(cpf=termo_busca)
                resultados = [cliente] if cliente else []
            elif tipo_busca == "nome":
                resultados = self.gerenciador_sistema.consultar_clientes_por_nome(nome=termo_busca)
            elif tipo_busca == "id_livro":
                resultados = self.gerenciador_sistema.consultar_clientes_por_livro_emprestado(id_livro=termo_busca)
            elif tipo_busca == "multa":
                resultados = self.gerenciador_sistema.consultar_clientes_com_multas()
        except AttributeError as ae:
            print(f"ERRO de Atributo (Busca Clientes): Método não implementado no backend: {ae}")
            ctk.CTkLabel(self.frame_resultados_clientes, text="Funcionalidade de busca não implementada.", text_color="red").pack(pady=10)
            return
        except Exception as e:
            print(f"ERRO Busca Clientes: {e}")
            ctk.CTkLabel(self.frame_resultados_clientes, text=f"Erro ao buscar: {e}", text_color="red").pack(pady=10)
            return
        
        if resultados:
            headers = ["CPF", "Nome", "Email"]
            for col, header_text in enumerate(headers):
                ctk.CTkLabel(self.frame_resultados_clientes, text=header_text, font=ctk.CTkFont(weight="bold"), text_color=COR_TEXTO_LABEL_FORM).grid(row=0, column=col, padx=10, pady=5, sticky="w")
            for row_idx, cliente_obj in enumerate(resultados, start=1):
                email_cliente = cliente_obj.get_email() if hasattr(cliente_obj, 'get_email') and cliente_obj.get_email() else "N/A"
                dados_cliente = [cliente_obj.get_cpf(), cliente_obj.get_nome(), email_cliente]
                for col_idx, dado in enumerate(dados_cliente):
                    ctk.CTkLabel(self.frame_resultados_clientes, text=str(dado), text_color=COR_TEXTO_LABEL_FORM).grid(row=row_idx, column=col_idx, padx=10, pady=3, sticky="w")
        else:
            ctk.CTkLabel(self.frame_resultados_clientes, text="Nenhum cliente encontrado.", text_color=COR_TEXTO_LABEL_FORM).pack(pady=20)

    # --- TELAS DE CONSULTA E REGISTRO (IMPLEMENTAÇÃO COMPLETA) ---
    def tela_consulta_multas(self):
        frame_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_tela.pack(fill="both", expand=True)
        painel_formulario = self._criar_painel_padrao_formulario(frame_tela, "CONSULTA DE MULTA")
        ctk.CTkLabel(painel_formulario, text="CPF do Cliente:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=50, pady=(15,0))
        self.entry_cpf_consulta_multa = ctk.CTkEntry(painel_formulario, placeholder_text="Digite o CPF (somente números)", width=300, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_cpf_consulta_multa.pack(pady=(0, 20), padx=50)
        btn_avancar_multa = ctk.CTkButton(painel_formulario, text="Avançar", command=self.acao_consultar_multa, width=150, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color=COR_TEXTO_BOTAO_LARANJA, hover_color="#FF8C00", corner_radius=10)
        btn_avancar_multa.pack(pady=15)
        self.frame_resultado_multa = ctk.CTkFrame(painel_formulario, fg_color="transparent")
        self.frame_resultado_multa.pack(pady=10, padx=20, fill="both", expand=True)
        self.label_info_multa = ctk.CTkLabel(self.frame_resultado_multa, text="Digite um CPF para consultar a multa.", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM, wraplength=400)
        self.label_info_multa.pack(pady=10)
        self._adicionar_botao_voltar(frame_tela)

    def acao_consultar_multa(self):
        cpf = self.entry_cpf_consulta_multa.get().strip()
        for widget in self.frame_resultado_multa.winfo_children(): widget.destroy()
        self.label_info_multa = ctk.CTkLabel(self.frame_resultado_multa, text="", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM, wraplength=400); self.label_info_multa.pack(pady=10)
        if not cpf: self.label_info_multa.configure(text="Digite o CPF.", text_color="red"); return
        if len(cpf) != 11 or not cpf.isdigit(): self.label_info_multa.configure(text="CPF inválido.", text_color="red"); return
        try:
            self.gerenciador_sistema.calcular_multa(cpf=cpf) 
            emprestimo = self.gerenciador_sistema.gerenciador_banco_dados.recuperar_emprestimo(cpf=cpf)
            if emprestimo:
                multa_valor = emprestimo.get_multa()
                if multa_valor > 0:
                    livro_emprestado = self.gerenciador_sistema.gerenciador_banco_dados.recuperar_livro_por_id(emprestimo.get_id_livro())
                    titulo_livro = livro_emprestado.get_titulo() if livro_emprestado else "Desconhecido"
                    data_prazo_obj = emprestimo.get_prazo(); prazo_formatado = data_prazo_obj.strftime('%d/%m/%Y') if data_prazo_obj else "N/A"
                    texto_resultado = (f"Multa Pendente: R$ {multa_valor:.2f}\n\nLivro: '{titulo_livro}' (ID: {emprestimo.get_id_livro()})\n\nPrazo Devolução: {prazo_formatado}")
                    self.label_info_multa.configure(text=texto_resultado, text_color="orange", justify="left")
                else: self.label_info_multa.configure(text="Nenhuma multa pendente para este CPF.", text_color="green")
            else:
                cliente = self.gerenciador_sistema.gerenciador_banco_dados.recuperar_cliente(cpf=cpf)
                if cliente: self.label_info_multa.configure(text="Cliente sem empréstimos ativos ou multas.", text_color="blue", wraplength=380)
                else: self.label_info_multa.configure(text="Cliente não cadastrado com este CPF.", text_color="red")
        except Exception as e: print(f"ERRO GERAL (Consulta Multa): {type(e).__name__} - {e}"); self.label_info_multa.configure(text="Erro ao consultar. Tente novamente.", text_color="red")
        
    def tela_registro_pagamento(self):
        frame_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_tela.pack(fill="both", expand=True)
        painel_formulario = self._criar_painel_padrao_formulario(frame_tela, "REGISTRO DE PAGAMENTO DE MULTA")
        ctk.CTkLabel(painel_formulario, text="CPF do Cliente:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=50, pady=(10,0))
        self.entry_cpf_pag_multa = ctk.CTkEntry(painel_formulario, placeholder_text="CPF do cliente", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_cpf_pag_multa.pack(pady=(0,10), padx=50)
        ctk.CTkLabel(painel_formulario, text="Valor Pago: R$", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=50, pady=(10,0))
        self.entry_valor_pago_multa = ctk.CTkEntry(painel_formulario, placeholder_text="Valor recebido", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_valor_pago_multa.pack(pady=(0,20), padx=50)
        self.label_feedback_pag_multa = ctk.CTkLabel(painel_formulario, text="", font=ctk.CTkFont(size=12))
        self.label_feedback_pag_multa.pack(pady=5)
        btn_avancar = ctk.CTkButton(painel_formulario, text="Avançar", command=self.acao_registrar_pagamento_multa, width=200, height=35, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color=COR_TEXTO_BOTAO_LARANJA, corner_radius=10)
        btn_avancar.pack(pady=20)
        self._adicionar_botao_voltar(frame_tela)

    def acao_registrar_pagamento_multa(self):
        cpf = self.entry_cpf_pag_multa.get().strip()
        self.label_feedback_pag_multa.configure(text="")
        if not cpf: self.label_feedback_pag_multa.configure(text="CPF é obrigatório.", text_color="red"); return
        try:
            self.gerenciador_sistema.calcular_multa(cpf=cpf)
            emprestimo = self.gerenciador_sistema.gerenciador_banco_dados.recuperar_emprestimo(cpf=cpf)
            if not emprestimo or emprestimo.get_multa() == 0:
                self.label_feedback_pag_multa.configure(text="Pagamento negado! Cliente não possui multas pendentes.", text_color="orange")
                return
            sucesso = self.gerenciador_sistema.registrar_pagamento_multa_usuario(cpf=cpf)
            if sucesso:
                self.label_feedback_pag_multa.configure(text="Pagamento efetuado!", text_color="green")
                self.entry_cpf_pag_multa.delete(0, 'end'); self.entry_valor_pago_multa.delete(0, 'end')
            else:
                self.label_feedback_pag_multa.configure(text="Erro ao registrar pagamento. Verifique o console.", text_color="red")
        except Exception as e: self.label_feedback_pag_multa.configure(text="Erro ao registrar pagamento. Verifique console.", text_color="red"); print(f"ERRO GUI (Reg Pag Multa): {e}")

    def tela_registro_emprestimos(self):
        frame_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_tela.pack(fill="both", expand=True)
        painel_formulario = self._criar_painel_padrao_formulario(frame_tela, "REGISTRO DE EMPRÉSTIMO")
        ctk.CTkLabel(painel_formulario, text="CPF do Cliente:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=50, pady=(10,0))
        self.entry_cpf_emprestimo = ctk.CTkEntry(painel_formulario, placeholder_text="CPF do cliente", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_cpf_emprestimo.pack(pady=(0,10), padx=50)
        ctk.CTkLabel(painel_formulario, text="ID do Livro:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=50, pady=(10,0))
        self.entry_idlivro_emprestimo = ctk.CTkEntry(painel_formulario, placeholder_text="ID do livro a ser emprestado", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_idlivro_emprestimo.pack(pady=(0,20), padx=50)
        self.label_feedback_emprestimo = ctk.CTkLabel(painel_formulario, text="", font=ctk.CTkFont(size=12))
        self.label_feedback_emprestimo.pack(pady=5)
        btn_avancar = ctk.CTkButton(painel_formulario, text="Avançar", command=self.acao_registrar_emprestimo, width=200, height=35, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color=COR_TEXTO_BOTAO_LARANJA, corner_radius=10)
        btn_avancar.pack(pady=20)
        self._adicionar_botao_voltar(frame_tela)

    def acao_registrar_emprestimo(self):
        cpf = self.entry_cpf_emprestimo.get().strip(); id_livro = self.entry_idlivro_emprestimo.get().strip()
        self.label_feedback_emprestimo.configure(text="")
        if not cpf or not id_livro: self.label_feedback_emprestimo.configure(text="CPF e ID do Livro são obrigatórios.", text_color="red"); return
        try:
            sucesso = self.gerenciador_sistema.registrar_emprestimo_usuario(cpf=cpf, id_livro=id_livro)
            if sucesso:
                self.label_feedback_emprestimo.configure(text="Empréstimo efetuado!", text_color="green")
                self.entry_cpf_emprestimo.delete(0, 'end'); self.entry_idlivro_emprestimo.delete(0, 'end')
            else:
                self.label_feedback_emprestimo.configure(text="Empréstimo negado. Verifique o console.", text_color="red")
        except Exception as e: self.label_feedback_emprestimo.configure(text="Erro ao registrar empréstimo. Verifique o console.", text_color="red"); print(f"ERRO GUI (Reg Empréstimo): {e}")

    def tela_registro_devolucao(self):
        frame_tela = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_tela.pack(fill="both", expand=True)
        painel_formulario = self._criar_painel_padrao_formulario(frame_tela, "REGISTRO DE DEVOLUÇÃO")
        ctk.CTkLabel(painel_formulario, text="CPF do Cliente:", font=ctk.CTkFont(size=14), text_color=COR_TEXTO_LABEL_FORM).pack(anchor="w", padx=50, pady=(10,0))
        self.entry_cpf_devolucao = ctk.CTkEntry(painel_formulario, placeholder_text="CPF do cliente que está devolvendo", width=350, height=40, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color="#000000", placeholder_text_color="#333333", border_width=0, corner_radius=10)
        self.entry_cpf_devolucao.pack(pady=(0,10), padx=50)
        self.label_feedback_devolucao = ctk.CTkLabel(painel_formulario, text="", font=ctk.CTkFont(size=12))
        self.label_feedback_devolucao.pack(pady=5)
        btn_avancar = ctk.CTkButton(painel_formulario, text="Avançar", command=self.acao_registrar_devolucao, width=200, height=35, fg_color=COR_LARANJA_CAMPOS_BOTOES, text_color=COR_TEXTO_BOTAO_LARANJA, corner_radius=10)
        btn_avancar.pack(pady=20)
        self._adicionar_botao_voltar(frame_tela)

    def acao_registrar_devolucao(self):
        cpf = self.entry_cpf_devolucao.get().strip()
        self.label_feedback_devolucao.configure(text="")
        if not cpf:
            self.label_feedback_devolucao.configure(text="CPF é obrigatório.", text_color="red")
            return
        
        try:
            # O backend agora retorna True se a devolução for bem-sucedida
            sucesso = self.gerenciador_sistema.registrar_devolucao_emprestimo_usuario(cpf=cpf)
            
            if sucesso:
                self.label_feedback_devolucao.configure(text="Devolução efetuada!", text_color="green")
                self.entry_cpf_devolucao.delete(0, 'end')
                self.entry_idlivro_devolucao.delete(0, 'end')
            else:
                # O backend já imprime a razão do erro no console (ex: multa pendente).
                self.label_feedback_devolucao.configure(text="Devolução negada. Verifique o console.", text_color="red")

        except Exception as e:
            self.label_feedback_devolucao.configure(text="Erro ao processar devolução.", text_color="red")
            print(f"ERRO GUI (Reg Devolução): {e}")

if __name__ == '__main__':
    # --- Mocks Atualizados ---
    class MockLivro:
        def __init__(self, id_livro, titulo, autor, status): self._id_livro, self._titulo, self._autor, self._status = id_livro, titulo, autor, status
        def get_id_livro(self): return self._id_livro
        def get_titulo(self): return self._titulo
        def get_autor(self): return self._autor
        def get_status(self): return self._status
    class MockCliente:
        def __init__(self, cpf, nome, email="mock@example.com"): self._cpf, self._nome, self._email = cpf, nome, email
        def get_cpf(self): return self._cpf; 
        def get_nome(self): return self._nome; 
        def get_email(self): return self._email
    class MockEmprestimo:
        def __init__(self, cpf, id_livro, prazo, multa): # 'prazo' é um parâmetro aqui
            self._cpf = cpf
            self._id_livro = id_livro
            self._multa = multa
            
            # CORREÇÃO: Lógica de conversão do 'prazo' DENTRO do __init__
            if isinstance(prazo, str): 
                self._prazo = date.fromisoformat(prazo)
            else:
                self._prazo = prazo # Assume que já é um objeto date se não for string
        
        def get_multa(self): return self._multa
        def get_id_livro(self): return self._id_livro
        def get_prazo(self): return self._prazo
    class MockGerenciadorBancoDados:
        def __init__(self):
            self.emprestimos_mock = {"11122233344": MockEmprestimo("11122233344", "LIV001", date.today() - timedelta(days=5), 2.50), "55566677788": MockEmprestimo("55566677788", "LIV002", date.today() + timedelta(days=5), 0.00)}
            self.clientes_mock = {"11122233344": MockCliente("11122233344", "Fulano Mock CPF"), "55566677788": MockCliente("55566677788", "Ciclana Mock Nome"), "00011122233": MockCliente("00011122233", "Cliente Sem Emprestimo")}
            self.livros_mock = {"LIV001": MockLivro("LIV001", "O Apanhador no Campo de Centeio", "J.D. Salinger", True), "LIV002": MockLivro("LIV002", "A Metamorfose", "Franz Kafka", True)}
        def recuperar_cliente(self, cpf): print(f"MOCK GBD: recuperando cliente CPF {cpf}"); return self.clientes_mock.get(cpf)
        def recuperar_livro_por_id(self, id_livro): print(f"MOCK GBD: recuperando livro ID {id_livro}"); return self.livros_mock.get(id_livro)
        def recuperar_emprestimo(self, cpf): print(f"MOCK GBD: recuperando emprestimo CPF {cpf}"); return self.emprestimos_mock.get(cpf)
        def cadastrar_pessoa(self, pessoa): print(f"MOCK GBD: Cadastrando pessoa {pessoa.get_nome() if hasattr(pessoa, 'get_nome') else 'N/A'}")
        def cadastrar_livro(self, livro): print(f"MOCK GBD: Cadastrando livro {livro.get_titulo() if hasattr(livro, 'get_titulo') else 'N/A'}")
        # Adicione mocks para os métodos de registro se quiser testar o fluxo completo nos mocks
        def registrar_devolucao_emprestimo_usuario(self, cpf): print(f"MOCK GBD: Devolução para CPF {cpf}")
        def cadastrar_emprestimo(self, cpf_cliente, id_livro): print(f"MOCK GBD: Empréstimo CPF {cpf_cliente}, Livro {id_livro}")
        def registrar_pagamento_multa_usuario(self, cpf): print(f"MOCK GBD: Pagamento multa CPF {cpf}")


    class MockGerenciadorSistema:
        def __init__(self): 
            self.gerenciador_banco_dados = MockGerenciadorBancoDados()
            self.livros_mock_sistema = [MockLivro("LIV002", "A Revolução dos Bichos", "George Orwell", False), MockLivro("LIV003", "O Senhor dos Anéis", "J.R.R. Tolkien", True)]
            print("MockGerenciadorSistema inicializado.")
        def cadastrar_cliente(self, nome, cpf): print(f"MOCK GS: Cadastrando cliente {nome}, {cpf}"); self.gerenciador_banco_dados.cadastrar_pessoa(MockCliente(cpf, nome))
        def cadastrar_livro(self, titulo, autor, id_livro): print(f"MOCK GS: Cadastrando livro {titulo}, {autor}, {id_livro}"); self.gerenciador_banco_dados.cadastrar_livro(MockLivro(id_livro, titulo, autor, False))
        def consultar_livros_por_titulo(self, titulo): return [l for l in self.livros_mock_sistema if titulo.lower() in l.get_titulo().lower()]
        def consultar_livro_autor(self, autor): return [l for l in self.livros_mock_sistema if autor.lower() in l.get_autor().lower()]
        def calcular_multa(self, cpf): print(f"MOCK GS: calcular_multa chamado para CPF {cpf}.")
        def consultar_clientes_por_nome(self, nome): return [c for c in self.gerenciador_banco_dados.clientes_mock.values() if nome.lower() in c.get_nome().lower()]
        def consultar_clientes_por_livro_emprestado(self, id_livro): return [self.gerenciador_banco_dados.clientes_mock["11122233344"]] if id_livro == "LIV001" else []
        def consultar_clientes_com_multas(self): return [self.gerenciador_banco_dados.clientes_mock["11122233344"]] # Fulano tem multa no mock
        # --- Mocks para as novas telas de Registro ---
        def registrar_emprestimo_usuario(self, cpf, id_livro):
            livro = self.gerenciador_banco_dados.recuperar_livro_por_id(id_livro)
            if livro:
                livro._status = True  # Marcar como emprestado
                print(f"Livro '{livro.get_titulo()}' marcado como emprestado.")

        def registrar_devolucao_emprestimo_usuario(self, cpf): print(f"MOCK GS: Registrando devolução para CPF:{cpf}") # Simula sucesso
        def registrar_pagamento_multa_usuario(self, cpf): print(f"MOCK GS: Registrando pagamento de multa para CPF:{cpf}") # Simula sucesso


    mock_gs = MockGerenciadorSistema()
    app = TelaPrincipal(gerenciador_sistema_instancia=mock_gs)
    app.mainloop()