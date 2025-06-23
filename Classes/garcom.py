# garcom.py (versão compacta)
import customtkinter as ctk
import random
from dados import Dados

class Garcom(Dados):
    def __init__(self, id_garcom=None):
        super().__init__()
        self.id = id_garcom

    def abrir_painel_garcom(self):
        painel = ctk.CTk()
        painel.title("Painel do Garçom")
        painel.geometry("700x600")  # Dimensão um pouco menor

        # Frame para adicionar pedido
        frame_adicionar = ctk.CTkFrame(painel)
        frame_adicionar.pack(pady=8, padx=15, fill="x")

        titulo_adicionar = ctk.CTkLabel(frame_adicionar, text="Adicionar Novo Pedido", font=("Arial", 18, "bold"))
        titulo_adicionar.pack(pady=(8, 12))

        ctk.CTkLabel(frame_adicionar, text="Número da Mesa:", font=("Arial", 14)).pack()
        entry_mesa = ctk.CTkEntry(frame_adicionar, placeholder_text="Ex: 1", width=120)
        entry_mesa.pack(pady=(0, 8))

        ctk.CTkLabel(frame_adicionar, text="Nome do Pedido:", font=("Arial", 14)).pack()
        entry_pedido = ctk.CTkEntry(frame_adicionar, placeholder_text="Ex: Hamburguer", width=200)
        entry_pedido.pack(pady=(0, 8))

        ctk.CTkLabel(frame_adicionar, text="Valor do Pedido (R$):", font=("Arial", 14)).pack()
        entry_valor = ctk.CTkEntry(frame_adicionar, placeholder_text="Ex: 25.50", width=120)
        entry_valor.pack(pady=(0, 12))

        label_status = ctk.CTkLabel(frame_adicionar, text="", font=("Arial", 12))
        label_status.pack(pady=(0, 8))

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

            dados_atuais = self.carregar_dados_restaurante()

            mesa_encontrada = False
            for mesa in dados_atuais["mesas"]:
                if mesa["numero"] == num_mesa:
                    novo_pedido = {
                        "id": random.randint(100, 9999),
                        "nome": nome_pedido,
                        "valor": valor_pedido,
                        "tipo": "Comida",
                        "status": "solicitado"
                    }
                    mesa["pedidos"].append(novo_pedido)
                    mesa["valor_conta"] += valor_pedido
                    mesa_encontrada = True
                    break

            for garcom in dados_atuais["garcons"]:
                if garcom["id"] == self.id:
                    garcom["valor_vendido"] += valor_pedido
                    garcom["valor_10"] += valor_pedido * 0.1

            if not mesa_encontrada:
                label_status.configure(text=f"Erro: Mesa {num_mesa} não encontrada!", text_color="red")
                return

            self.salvar_dados_restaurante(dados_atuais)
            label_status.configure(text=f"Pedido '{nome_pedido}' enviado para a cozinha!", text_color="green")
            entry_mesa.delete(0, 'end')
            entry_pedido.delete(0, 'end')
            entry_valor.delete(0, 'end')

            texto_prontos = self.gerar_dados_painel()
            label_prontos.configure(text=texto_prontos)

        botao_adicionar = ctk.CTkButton(frame_adicionar, text="Adicionar para a Cozinha", command=adicionar_para_cozinha, font=("Arial", 14))
        botao_adicionar.pack(pady=8)

        # Frame para visualizar pedidos solicitados
        frame_visualizar = ctk.CTkFrame(painel)
        frame_visualizar.pack(pady=8, padx=15, fill="both", expand=True)

        titulo_visualizar = ctk.CTkLabel(frame_visualizar, text="Pedidos Solicitados na Cozinha", font=("Arial", 16, "bold"))
        titulo_visualizar.pack(pady=8)

        texto_prontos = self.gerar_dados_painel()
        label_prontos = ctk.CTkLabel(frame_visualizar, text=texto_prontos, font=("Arial", 12), justify="left", wraplength=650)
        label_prontos.pack(pady=8)

        # Frame para fechar conta
        frame_fechar = ctk.CTkFrame(painel)
        frame_fechar.pack(pady=8, padx=15, fill="x")

        titulo_fechar = ctk.CTkLabel(frame_fechar, text="Fechar Conta", font=("Arial", 18, "bold"))
        titulo_fechar.pack(pady=(8, 12))

        ctk.CTkLabel(frame_fechar, text="Número da Mesa para Fechar:", font=("Arial", 14)).pack()
        entry_numero_mesa = ctk.CTkEntry(frame_fechar, placeholder_text="Ex: 1", width=120)
        entry_numero_mesa.pack(pady=(0, 8))

        label_status_fechar = ctk.CTkLabel(frame_fechar, text="", font=("Arial", 12))
        label_status_fechar.pack(pady=(0, 8))

        def fechar_conta():
            try:
                num_mesa = int(entry_numero_mesa.get())
            except ValueError:
                label_status_fechar.configure(text="Erro: Número da mesa inválido!", text_color="red")
                return

            dados = self.carregar_dados_restaurante()

            mesa_encontrada = False
            for mesa in dados["mesas"]:
                if mesa["numero"] == num_mesa:
                    mesa["pedidos"] = []
                    mesa["valor_conta"] = 0.0
                    mesa_encontrada = True
                    break

            if not mesa_encontrada:
                label_status_fechar.configure(text=f"Mesa {num_mesa} não encontrada!", text_color="red")
                return

            # NÃO ALTERAR valor_vendido nem valor_10 para manter histórico

            self.salvar_dados_restaurante(dados)
            label_status_fechar.configure(text=f"Conta da mesa {num_mesa} fechada com sucesso!", text_color="green")
            entry_numero_mesa.delete(0, 'end')

            texto_prontos = self.gerar_dados_painel()
            label_prontos.configure(text=texto_prontos)

        botao_fechar = ctk.CTkButton(frame_fechar, text="Fechar Conta", command=fechar_conta, font=("Arial", 14))
        botao_fechar.pack(pady=8)

        # --- BOTÃO VOLTAR COM LAMBDA ---
        botao_voltar = ctk.CTkButton(
            painel,
            text="Sair (Voltar para Tela de Login)",
            command=lambda: (painel.destroy(), self.criar_tela_login()),
            font=("Arial", 14),
            fg_color="#DB3E39",
            hover_color="#B7302B"
        )
        botao_voltar.pack(side="bottom", pady=15)

        painel.mainloop()

    def gerar_dados_painel(self, papel=None):
        texto = "Pedidos Solicitados:\n\n"
        pedidos_encontrados = False
        self.dados_restaurante = self.carregar_dados_restaurante()
        for mesa in self.dados_restaurante.get("mesas", []):
            pedidos_da_mesa = []
            for pedido in mesa.get("pedidos", []):
                if pedido.get("status") == "solicitado":
                    pedidos_da_mesa.append(f"    • {pedido['nome']}")
                    pedidos_encontrados = True

            if pedidos_da_mesa:
                texto += f"Mesa {mesa['numero']}:\n"
                texto += "\n".join(pedidos_da_mesa) + "\n\n"

        return texto if pedidos_encontrados else "Nenhum pedido novo no momento."
