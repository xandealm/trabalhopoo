# dono.py
import customtkinter as ctk
from dados import Dados

class Dono(Dados):
    def __init__(self):
        super().__init__()

    def abrir_painel_padrao(self, papel):
        painel = ctk.CTk()
        painel.title(f"Painel do {papel.capitalize()}")
        painel.geometry("800x600")

        titulo = ctk.CTkLabel(painel, text=f"Painel do {papel.capitalize()}", font=("Arial", 26, "bold"))
        titulo.pack(pady=20)

        texto_inicial = self.gerar_dados_painel(papel)
        conteudo = ctk.CTkLabel(painel, text=texto_inicial, font=("Arial", 16), justify="left", wraplength=700)
        conteudo.pack(pady=10)

        if papel == "dono":
            admin_frame = ctk.CTkFrame(painel, fg_color="transparent")
            admin_frame.pack(pady=20, padx=20, fill="x")

            status_label = ctk.CTkLabel(admin_frame, text="", font=("Arial", 14))
            status_label.pack(pady=5)

            def executar_zeramento():
                dados = self.carregar_dados_restaurante()
                for mesa in dados["mesas"]:
                    mesa["pedidos"] = []
                    mesa["valor_conta"] = 0.0
                for garcom in dados["garcons"]:
                    garcom["valor_vendido"] = 0.0
                    garcom["valor_10"] = 0.0
                self.salvar_dados_restaurante(dados)

                conteudo.configure(text=self.gerar_dados_painel("dono"))
                status_label.configure(text="Expediente zerado", text_color="green")

                botao_confirmar.pack_forget()
                botao_zerar.pack(pady=10)

            def iniciar_processo_de_zerar():
                status_label.configure(text="")
                botao_zerar.pack_forget()
                botao_confirmar.pack(pady=10)

            botao_zerar = ctk.CTkButton(
                admin_frame, 
                text="Zerar Expediente", 
                command=iniciar_processo_de_zerar,
                font=("Arial", 16, "bold")
            )
            botao_zerar.pack(pady=10)
            botao_confirmar = ctk.CTkButton(
                admin_frame,
                text="Tem certeza que deseja reiniciar os pedidos realizados?",
                command=executar_zeramento,
                font=("Arial", 16)
            )

        # --- BOTÃO VOLTAR COM LAMBDA ---
        botao_voltar = ctk.CTkButton(
            painel, 
            text="Sair (Voltar para Tela de Login)",
            command=lambda: (painel.destroy(), self.criar_tela_login()), 
            font=("Arial", 16),
            fg_color="#DB3E39",
            hover_color="#B7302B"
        )
        botao_voltar.pack(side="bottom", pady=20)
        
        painel.mainloop()

    def gerar_dados_painel(self, papel=None):
        self.dados_restaurante = self.carregar_dados_restaurante()
        faturamento_total = sum(mesa["valor_conta"] for mesa in self.dados_restaurante.get("mesas", []))
        texto = f"Faturamento do Dia: R$ {faturamento_total:.2f}\n\n"

        texto += "Comissões dos Garçons:\n"
        if "garcons" in self.dados_restaurante and self.dados_restaurante["garcons"]:
            for g in self.dados_restaurante["garcons"]:
                texto += f"    • {g['nome']}: R$ {g.get('valor_10', 0.0):.2f} (Total Vendido: R$ {g.get('valor_vendido', 0.0):.2f})\n"
        return texto