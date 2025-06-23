# cozinha.py
import customtkinter as ctk
from dados import Dados

class Cozinha(Dados):
    def abrir_painel_cozinheiro(self):
        painel = ctk.CTk()
        painel.title("Painel do Cozinheiro")
        painel.geometry("800x600")

        titulo = ctk.CTkLabel(painel, text="Painel do Cozinheiro", font=("Arial", 26, "bold"))
        titulo.pack(pady=20)
        
        caixa_texto_pedidos = ctk.CTkTextbox(painel, font=("Arial", 16), width=700, height=350)
        caixa_texto_pedidos.pack(pady=10)
        
        def atualizar_pedidos():
            texto_pedidos = self.gerar_dados_painel() 
            caixa_texto_pedidos.delete("1.0", "end")
            caixa_texto_pedidos.insert("1.0", texto_pedidos)
        
        botao_atualizar = ctk.CTkButton(painel, text="Atualizar Pedidos", command=atualizar_pedidos, font=("Arial", 16))
        botao_atualizar.pack(pady=10)
        
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
        
        atualizar_pedidos()
        painel.mainloop()

    def gerar_dados_painel(self, papel=None): 
        texto = "Solicitações de Pedidos:\n\n"
        pedidos_encontrados = False
        self.dados_restaurante = self.carregar_dados_restaurante()
        for mesa in self.dados_restaurante["mesas"]:
            pedidos_da_mesa = []
            for pedido in mesa["pedidos"]:
                if pedido.get("status") == "solicitado":
                    pedidos_da_mesa.append(f"    • {pedido['nome']}")
                    pedidos_encontrados = True

            if pedidos_da_mesa:
                texto += f"Mesa {mesa['numero']}:\n"
                texto += "\n".join(pedidos_da_mesa) + "\n\n"
        return texto if pedidos_encontrados else "Nenhum pedido novo no momento."