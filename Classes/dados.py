# dados.py
import customtkinter as ctk
from pathlib import Path
from PIL import Image
import json
from abc import ABC, abstractmethod

class Funcionario:
    def __init__(self, id_func, nome, senha, papel):
        self.id = id_func
        self.nome = nome
        self._senha = senha  # Apenas a senha está encapsulada
        self.papel = papel

    def verificar_senha(self, senha_digitada):
        return self._senha == senha_digitada

class Dados(ABC):
    def __init__(self):
        self.dados_restaurante = self.carregar_dados_restaurante()
        self.funcionarios = self.carregar_funcionarios()
        self.tela_inicial = None

    @abstractmethod
    def gerar_dados_painel(self, papel=None):
        pass

    def criar_tela_login(self):
        tela_inicial = ctk.CTk()
        self.tela_inicial = tela_inicial
        tela_inicial.title("Trabalho POO - Login")
        tela_inicial.geometry("800x600")

        self.label_erro = None

        def entrar():
            user = IDtxt.get()
            senha = senhatxt.get()

            funcionario = self.funcionarios.get(user)
            if funcionario and funcionario.verificar_senha(senha):
                abrir_painel(funcionario.papel, self, user)
            else:
                if not self.label_erro:
                    self.label_erro = ctk.CTkLabel(
                        tela_inicial, text="ID ou senha incorretos",
                        text_color="red", font=("Arial", 16)
                    )
                    self.label_erro.pack(pady=10)
                else:
                    self.label_erro.configure(text="ID ou senha incorretos!")

        ctk.CTkLabel(
            tela_inicial, text="Restaurante Bom de Garfo", font=("Arial", 32, "bold")
        ).pack(pady=50)

        ctk.CTkLabel(tela_inicial, text="Digite seu ID:", font=("Arial", 22)).pack()
        IDtxt = ctk.CTkEntry(tela_inicial)
        IDtxt.pack(pady=30)

        ctk.CTkLabel(tela_inicial, text="Digite sua senha:", font=("Arial", 22)).pack()
        senhatxt = ctk.CTkEntry(tela_inicial, show="*")
        senhatxt.pack(pady=30)

        ctk.CTkButton(tela_inicial, text="Entrar", command=entrar).pack(pady=20)

        try:
            script_dir = Path(__file__).parent
            caminho_da_imagem = script_dir / "restaurante_bomdegarfoimg.png"
            imagem_restaurante = Image.open(caminho_da_imagem)
            imagem_ctk = ctk.CTkImage(
                light_image=imagem_restaurante, dark_image=imagem_restaurante, size=(150, 150)
            )
            ctk.CTkLabel(tela_inicial, image=imagem_ctk, text='').pack(pady=20)
        except FileNotFoundError:
            print("Imagem 'restaurante_bomdegarfoimg.png' não encontrada")

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
        funcionarios = {}
        try:
            with open("json/funcionarios.json", "r", encoding="utf-8") as f:
                dados_json = json.load(f)
                for id_func, dados in dados_json.items():
                    funcionario = Funcionario(
                        id_func=id_func,
                        nome=dados["nome"],
                        senha=dados["senha"],
                        papel=dados["papel"]
                    )
                    funcionarios[id_func] = funcionario
        except FileNotFoundError:
            print("Arquivo 'json/funcionarios.json' não encontrado.")
        return funcionarios

# ---- Função para abrir o painel do funcionário logado ----
def abrir_painel(papel, app_instance, id_usuario):
    if app_instance.tela_inicial:
        app_instance.tela_inicial.destroy()

    if papel == "garcom":
        from garcom import Garcom
        g = Garcom(id_garcom=id_usuario)
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
