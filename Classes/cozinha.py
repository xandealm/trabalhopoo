import customtkinter as ctk
from pathlib import Path
from PIL import Image
import json
from dados import Dados
class Cozinha(Dados):
    def abrir_painel_cozinheiro(self):
        d = Dados()
        painel = ctk.CTk()
        painel.title("Painel do Cozinheiro")
        painel.geometry("800x600")

        titulo = ctk.CTkLabel(painel, text="Painel do Cozinheiro", font=("Arial", 26, "bold"))
        titulo.pack(pady=20)
        
        caixa_texto_pedidos = ctk.CTkTextbox(painel, font=("Arial", 16), width=700, height=350)
        caixa_texto_pedidos.pack(pady=10)
        
        def atualizar_pedidos():
            texto_pedidos = d.gerar_dados_painel("cozinheiro")
            caixa_texto_pedidos.delete("1.0", "end")
            caixa_texto_pedidos.insert("1.0", texto_pedidos)
        
        botao_atualizar = ctk.CTkButton(painel, text="Atualizar Pedidos", command=atualizar_pedidos, font=("Arial", 16))
        botao_atualizar.pack(pady=10)
        
        def voltar_para_login():
            painel.destroy()
            d.criar_tela_login()

        botao_voltar = ctk.CTkButton(painel, text="Voltar para Tela Inicial", command=voltar_para_login, font=("Arial", 16))
        botao_voltar.pack(side="bottom", pady=20)
        
        atualizar_pedidos()
        painel.mainloop()


    def gerar_dados_painel(self):
        texto = "Solicitações de Pedidos:\n\n"
        pedidos_encontrados = False
        for mesa in self.dados_restaurante["mesas"]:
            pedidos_da_mesa = []
            for pedido in mesa["pedidos"]:
                if pedido.get("status") == "solicitado":
                    pedidos_da_mesa.append(f"   • {pedido['nome']}")
                    pedidos_encontrados = True

            if pedidos_da_mesa:
                texto += f"Mesa {mesa['numero']}:\n"
                texto += "\n".join(pedidos_da_mesa) + "\n\n"
        return texto if pedidos_encontrados else "Nenhum pedido novo no momento."