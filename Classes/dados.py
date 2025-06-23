# dados.py
import customtkinter as ctk
from pathlib import Path
from PIL import Image, ImageTk
import json
from abc import ABC, abstractmethod

class Dados(ABC):
    def __init__(self):
        self.dados_restaurante = self.carregar_dados_restaurante()
        self.tela_inicial = None

    @abstractmethod
    def gerar_dados_painel(self, papel=None):
        pass

    def criar_tela_login(self):
        funcionarios = self.carregar_funcionarios()

        tela_inicial = ctk.CTk()
        self.tela_inicial = tela_inicial 
        tela_inicial.title("Trabalho POO - Login")
        tela_inicial.geometry("800x600")

        self.label_erro = None

        def entrar():
            user = IDtxt.get()
            senha = senhatxt.get()

            if user in funcionarios and funcionarios[user]["senha"] == senha:
                papel = funcionarios[user]["papel"]
                abrir_painel(papel, self) 
            else:
                if not self.label_erro:
                    self.label_erro = ctk.CTkLabel(tela_inicial, text="ID ou senha incorretos", text_color="red", font=("Arial", 16))
                    self.label_erro.pack(pady=10)
                else:
                    self.label_erro.configure(text="ID ou senha incorretos!")
        
        titulo_tela_inicial = ctk.CTkLabel(tela_inicial, text="Restaurante Bom de Garfo", font=("Arial", 32, "bold"))
        titulo_tela_inicial.pack(pady=50)

        ctk.CTkLabel(tela_inicial, text="Digite seu ID:", font=("Arial", 22)).pack()
        IDtxt = ctk.CTkEntry(tela_inicial)
        IDtxt.pack(pady=30)

        ctk.CTkLabel(tela_inicial, text="Digite sua senha:", font=("Arial", 22)).pack()
        senhatxt = ctk.CTkEntry(tela_inicial, show="*")
        senhatxt.pack(pady=30)

        botao_entrar = ctk.CTkButton(tela_inicial, text="Entrar", command=entrar)
        botao_entrar.pack(pady=20)

        try:
            script_dir = Path(__file__).parent
            caminho_da_imagem = script_dir / "restaurante_bomdegarfoimg.png"
            imagem_restaurante = Image.open(caminho_da_imagem)
            imagem_ctk = ctk.CTkImage(light_image=imagem_restaurante, dark_image=imagem_restaurante, size=(150, 150))
            label_imagem = ctk.CTkLabel(tela_inicial, image=imagem_ctk, text='')
            label_imagem.pack(pady=20)
        except FileNotFoundError:
            print("Imagem 'imagens/restaurante_bomdegarfoimg.png' não encontrada")

        tela_inicial.mainloop()

    def salvar_dados_restaurante(self, novos_dados):
        with open("json/dados.json", "w", encoding="utf-8") as f:
            json.dump(novos_dados, f, indent=4, ensure_ascii=False)

    def carregar_dados_restaurante(self):
        try:
            with open("json/dados.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Arquivo 'json/dados.json' não encontrado. Criando um novo.")
            return {"mesas": [{"numero": 1, "pedidos": [], "valor_conta": 0.0}], "garcons": []}

    def carregar_funcionarios(self):
        try:
            with open("json/funcionarios.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Arquivo 'json/funcionarios.json' não encontrado.")
            return {}

def abrir_painel(papel, app_instance):
    if app_instance.tela_inicial:
        app_instance.tela_inicial.destroy()

    if papel == "garcom":
        from garcom import Garcom
        g = Garcom()
        g.abrir_painel_garcom()
    elif papel == "dono":
        from dono import Dono
        d = Dono()
        d.abrir_painel_padrao("dono")
    elif papel == "cozinheiro":
        from cozinha import Cozinha
        c = Cozinha()
        c.abrir_painel_cozinheiro()
    else:
        print(f"Papel '{papel}' desconhecido. Não é possível abrir painel.")