import customtkinter as ctk
from pathlib import Path
from PIL import Image
import json

def carregar_funcionarios():
    with open("json/funcionarios.json", "r", encoding="utf-8") as f:
        lista = json.load(f)
        return {f["id"]: f for f in lista} 

def carregar_dados_restaurante():
    with open("json/dados.json", "r", encoding="utf-8") as f:
        return json.load(f)

funcionarios = carregar_funcionarios()
dados_restaurante = carregar_dados_restaurante()

def gerar_dados_painel(papel):
    #Visão do cozinheiro
    if papel == "cozinheiro":
        texto = "Solicitações de Pedidos:\n\n"
        pedidos_encontrados = False
        for mesa in dados_restaurante["mesas"]:
            pedidos_da_mesa = []
            for pedido in mesa["pedidos"]:
                if pedido.get("status") == "solicitado":
                    pedidos_da_mesa.append(f"  • {pedido['nome']}")
                    pedidos_encontrados = True
            
            if pedidos_da_mesa:
                texto += f"Mesa {mesa['numero']}:\n"
                texto += "\n".join(pedidos_da_mesa) + "\n\n"

        return texto if pedidos_encontrados else "Nenhum pedido novo no momento."

    #Visão do Garçom
    elif papel == "garcom":
        texto = "Pedidos Prontos para Entrega:\n\n"
        pedidos_encontrados = False
        for mesa in dados_restaurante["mesas"]:
            pedidos_prontos = []
            for pedido in mesa["pedidos"]:
                if pedido.get("status") == "pronto":
                    pedidos_prontos.append(f"  • {pedido['nome']}")
                    pedidos_encontrados = True

            if pedidos_prontos:
                texto += f"Mesa {mesa['numero']}:\n"
                texto += "\n".join(pedidos_prontos) + "\n\n"
        
        return texto if pedidos_encontrados else "Nenhum pedido pronto no momento."

    #Visão do Dono
    elif papel == "dono":

        faturamento_total = sum(mesa["valor_conta"] for mesa in dados_restaurante["mesas"])
        texto = f"Faturamento do Dia: R$ {faturamento_total:.2f}\n"
        
        texto += "Comissões dos Garçons:\n"
        for g in dados_restaurante["garcons"]:
            texto += f"  • {g['nome']}: R$ {g['valor_10']:.2f} (Total Vendido: R$ {g['valor_vendido']:.2f})\n"
        return texto

    return "Função desconhecida."

def abrir_painel(papel):
    tela_inicial.destroy()
    painel = ctk.CTk()
    painel.title(f"Painel do {papel}")
    painel.geometry("800x600")

    titulo = ctk.CTkLabel(painel, text=f"Painel do {papel}", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    texto = gerar_dados_painel(papel)
    conteudo = ctk.CTkLabel(painel, text=texto, font=("Arial", 16), justify="left", wraplength=580)
    conteudo.pack(pady=10)

    painel.mainloop()

def entrar():
    user = IDtxt.get()
    senha = senhatxt.get()

    if user in funcionarios and funcionarios[user]["senha"] == senha:
        papel = funcionarios[user]["papel"]
        abrir_painel(papel)
    else:
        erro = ctk.CTkLabel(tela_inicial, text="ID ou senha incorretos!", text_color="red", font=("Arial", 16))
        erro.pack(pady=10)


#Criando a tela inicial
tela_inicial = ctk.CTk()
tela_inicial.title("Trabalho POO")
tela_inicial.geometry("800x600") 

#Colocando os intens da tela inicial
titulo_tela_inicial = ctk.CTkLabel(tela_inicial, text = "Restaurante Bom de Garfo",font = ("Arial",32,"bold"))
titulo_tela_inicial.pack(pady=50)

ID_tela_inicial = ctk.CTkLabel(tela_inicial, text = "Digite seu ID:", font = ("Arial",22))
ID_tela_inicial.pack()
IDtxt = ctk.CTkEntry(tela_inicial)
IDtxt.pack(pady=30)

senha_tela_inicial = ctk.CTkLabel(tela_inicial, text = "Digite sua senha:", font = ("Arial",22))
senha_tela_inicial.pack()
senhatxt = ctk.CTkEntry(tela_inicial)
senhatxt.pack(pady=30)

#Botão para entrar como usuário
botao_entrar = ctk.CTkButton(tela_inicial, text = "Entrar", command = entrar)
botao_entrar.pack(pady=20)

#Colocando a imagem para qualquer um acessar
try:
    script_dir = Path(__file__).parent 

    caminho_da_imagem = script_dir / "imagens" / "restaurante_bomdegarfoimg.png"
    
    imagem_restaurante = Image.open(caminho_da_imagem)
    imagem_ctk = ctk.CTkImage(light_image=imagem_restaurante, dark_image= imagem_restaurante, size=(150, 150))
    label_imagem = ctk.CTkLabel(tela_inicial, image = imagem_ctk, text='') 
    label_imagem.pack(pady=20)
except FileNotFoundError:
    print("Imagem não encontrada.")

tela_inicial.mainloop()