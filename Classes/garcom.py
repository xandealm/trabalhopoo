import customtkinter as ctk
from pathlib import Path
from PIL import Image
import json
import random
from dados import Dados

class Garcom(Dados):
    def abrir_painel_garcom(self):
        d = Dados()
        painel = ctk.CTk()
        painel.title("Painel do Garçom")
        painel.geometry("800x600")
        
        frame_adicionar = ctk.CTkFrame(painel)
        frame_adicionar.pack(pady=10, padx=20, fill="x")

        #Código para adicionar pedidos
        titulo_adicionar = ctk.CTkLabel(frame_adicionar, text="Adicionar Novo Pedido", font=("Arial", 20, "bold"))
        titulo_adicionar.pack(pady=(10, 15))
        ctk.CTkLabel(frame_adicionar, text="Número da Mesa:", font=("Arial", 16)).pack()
        entry_mesa = ctk.CTkEntry(frame_adicionar, placeholder_text="Ex: 1")
        entry_mesa.pack(pady=(0, 10))
        ctk.CTkLabel(frame_adicionar, text="Nome do Pedido:", font=("Arial", 16)).pack()
        entry_pedido = ctk.CTkEntry(frame_adicionar, placeholder_text="Ex: Hamburguer", width=250)
        entry_pedido.pack(pady=(0, 10))
        ctk.CTkLabel(frame_adicionar, text="Valor do Pedido (R$):", font=("Arial", 16)).pack()
        entry_valor = ctk.CTkEntry(frame_adicionar, placeholder_text="Ex: 25.50")
        entry_valor.pack(pady=(0, 15))
        label_status = ctk.CTkLabel(frame_adicionar, text="", font=("Arial", 14))
        label_status.pack(pady=(0, 10))
        def adicionar_para_cozinha():
            num_mesa = entry_mesa.get()
            nome_pedido = entry_pedido.get()
            valor_pedido = entry_valor.get()
            if not num_mesa or not nome_pedido or not valor_pedido:
                label_status.configure(text="Erro: Preencha todos os campos!", text_color="red")
                return
            try:
                num_mesa = int(num_mesa)
                valor_pedido = float(valor_pedido)
            except ValueError:
                label_status.configure(text="Erro: Mesa e Valor devem ser números!", text_color="red")
                return
            dados_atuais = d.carregar_dados_restaurante()
            mesa_encontrada = False
            for mesa in dados_atuais["mesas"]:
                if mesa["numero"] == num_mesa:
                    novo_pedido = {"id": random.randint(100, 9999),"nome": nome_pedido,"valor": valor_pedido,"tipo": "Comida","status": "solicitado"}
                    mesa["pedidos"].append(novo_pedido)
                    mesa["valor_conta"] += valor_pedido
                    mesa_encontrada = True
                    break
            if not mesa_encontrada:
                label_status.configure(text=f"Erro: Mesa {num_mesa} não encontrada!", text_color="red")
                return
            d.salvar_dados_restaurante(dados_atuais)
            label_status.configure(text=f"Pedido '{nome_pedido}' enviado para a cozinha!", text_color="green")
            entry_mesa.delete(0, 'end')
            entry_pedido.delete(0, 'end')
            entry_valor.delete(0, 'end')
            # Atualiza o painel de pedidos prontos
            texto_prontos = self.gerar_dados_painel("garcom")
            label_prontos.configure(text=texto_prontos)
        botao_adicionar = ctk.CTkButton(frame_adicionar, text="Adicionar para a Cozinha", command=adicionar_para_cozinha, font=("Arial", 16))
        botao_adicionar.pack(pady=10)
        
        frame_visualizar = ctk.CTkFrame(painel)
        frame_visualizar.pack(pady=10, padx=20, fill="both", expand=True)
        titulo_visualizar = ctk.CTkLabel(frame_visualizar, text="Pedidos Prontos para Entrega", font=("Arial", 18, "bold"))
        titulo_visualizar.pack(pady=10)
        texto_prontos = self.gerar_dados_painel("garcom")
        label_prontos = ctk.CTkLabel(frame_visualizar, text=texto_prontos, font=("Arial", 16), justify="left")
        label_prontos.pack(pady=10)
        
        def voltar_para_login():
            painel.destroy()
            d.criar_tela_login()
            
        botao_voltar = ctk.CTkButton(painel, text="Voltar para Tela Inicial", command=voltar_para_login, font=("Arial", 16))
        botao_voltar.pack(side="bottom", pady=20)

        painel.mainloop()

    def gerar_dados_painel(self):
        texto = "Pedidos Solicitados:\n\n"
        pedidos_encontrados = False
        for mesa in self.dados_restaurante.get("mesas", []):
            pedidos_da_mesa = []
            for pedido in mesa.get("pedidos", []):
                if pedido.get("status") == "solicitado":
                    pedidos_da_mesa.append(f"   • {pedido['nome']}")
                    pedidos_encontrados = True

            if pedidos_da_mesa:
                texto += f"Mesa {mesa['numero']}:\n"
                texto += "\n".join(pedidos_da_mesa) + "\n\n"

        return texto if pedidos_encontrados else "Nenhum pedido novo no momento."
