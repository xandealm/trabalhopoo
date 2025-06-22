import customtkinter as ctk
from pathlib import Path
from PIL import Image
import json
import random

def carregar_funcionarios():
    with open("json/funcionarios.json", "r", encoding="utf-8") as f:
        lista = json.load(f)
        return {f["id"]: f for f in lista} 

def carregar_dados_restaurante():
    with open("json/dados.json", "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados_restaurante(novos_dados):
    with open("json/dados.json", "w", encoding="utf-8") as f:
        json.dump(novos_dados, f, indent=4, ensure_ascii=False)

funcionarios = carregar_funcionarios()
dados_restaurante = carregar_dados_restaurante()

def gerar_dados_painel(papel):
    # Recarrega os dados toda vez que for gerar o painel para garantir que estão atualizados
    dados_restaurante = carregar_dados_restaurante()
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
    #Função principal que decide qual painel abrir com base no papel
    tela_inicial.destroy()

    if papel == "garcom":
        abrir_painel_garcom()
    elif papel == "cozinheiro":
        abrir_painel_cozinheiro()
    else:
        abrir_painel_padrao(papel)

def abrir_painel_padrao(papel):
    #Abre um painel genérico de visualização (para Dono)
    painel = ctk.CTk()
    painel.title(f"Painel do {papel.capitalize()}")
    painel.geometry("800x600")

    titulo = ctk.CTkLabel(painel, text=f"Painel do {papel.capitalize()}", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    texto = gerar_dados_painel(papel)
    conteudo = ctk.CTkLabel(painel, text=texto, font=("Arial", 16), justify="left", wraplength=700)
    conteudo.pack(pady=10)

    painel.mainloop()

def abrir_painel_cozinheiro():
    #Abre o painel do Cozinheiro
    painel = ctk.CTk()
    painel.title("Painel do Cozinheiro")
    painel.geometry("800x600")

    titulo = ctk.CTkLabel(painel, text="Painel do Cozinheiro", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)
    
    caixa_texto_pedidos = ctk.CTkTextbox(painel, font=("Arial", 16), width=700, height=400)
    caixa_texto_pedidos.pack(pady=10)
    
    def atualizar_pedidos():
        #Recarrega os pedidos do json e atualiza a caixa de texto
        texto_pedidos = gerar_dados_painel("cozinheiro")
        caixa_texto_pedidos.delete("1.0", "end")
        caixa_texto_pedidos.insert("1.0", texto_pedidos)
    
    botao_atualizar = ctk.CTkButton(painel, text="Atualizar Pedidos", command=atualizar_pedidos, font=("Arial", 16))
    botao_atualizar.pack(pady=10)
    
    atualizar_pedidos()
    painel.mainloop()

def abrir_painel_garcom():
    #Abre o painel do Garçom
    painel = ctk.CTk()
    painel.title("Painel do Garçom")
    painel.geometry("800x600")
    
    frame_adicionar = ctk.CTkFrame(painel)
    frame_adicionar.pack(pady=20, padx=20, fill="x")

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

        dados_atuais = carregar_dados_restaurante()
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
        
        if not mesa_encontrada:
            label_status.configure(text=f"Erro: Mesa {num_mesa} não encontrada!", text_color="red")
            return

        salvar_dados_restaurante(dados_atuais)
        label_status.configure(text=f"Pedido '{nome_pedido}' enviado para a cozinha!", text_color="green")
        entry_mesa.delete(0, 'end')
        entry_pedido.delete(0, 'end')
        entry_valor.delete(0, 'end')

    botao_adicionar = ctk.CTkButton(frame_adicionar, text="Adicionar para a Cozinha", command=adicionar_para_cozinha, font=("Arial", 16))
    botao_adicionar.pack(pady=10)

    frame_visualizar = ctk.CTkFrame(painel)
    frame_visualizar.pack(pady=10, padx=20, fill="both", expand=True)
    
    titulo_visualizar = ctk.CTkLabel(frame_visualizar, text="Pedidos Prontos para Entrega", font=("Arial", 18, "bold"))
    titulo_visualizar.pack(pady=10)
    
    texto_prontos = gerar_dados_painel("garcom")
    label_prontos = ctk.CTkLabel(frame_visualizar, text=texto_prontos, font=("Arial", 16), justify="left")
    label_prontos.pack(pady=10)
    
    painel.mainloop()

#Login Tela Inicial

label_erro = None

def entrar():
    #Valida o login e abre o painel correspondente
    global label_erro

    user = IDtxt.get()
    senha = senhatxt.get()

    if user in funcionarios and funcionarios[user]["senha"] == senha:
        papel = funcionarios[user]["papel"]
        if label_erro:
            label_erro.pack_forget()
        abrir_painel(papel)
    else:
        if not label_erro:
            label_erro = ctk.CTkLabel(tela_inicial, text="ID ou senha incorretos", text_color="red", font=("Arial", 16))
            label_erro.pack(pady=10)
        else:
            label_erro.configure(text="ID ou senha incorretos!")
            label_erro.pack(pady=10)


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
    print("Imagem não encontrada")

tela_inicial.mainloop()