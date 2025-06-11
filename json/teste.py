import json

def carregar_dados():
    with open('dados.json', 'r') as arquivo:
        return json.load(arquivo)

def salvar_dados(dados):
    with open('dados.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

def listar_mesas(dados):
    print("\nMesas:")
    for mesa in dados['mesas']:
        print(f"Mesa {mesa['numero']} - Conta: R${mesa['valor_conta']}")
        for pedido in mesa['pedidos']:
            print(f"  Pedido: {pedido['nome']} - R${pedido['valor']}")

def listar_garcons(dados):
    print("\nGarçons:")
    for garcom in dados['garcons']:
        print(f"{garcom['nome']} - Vendas: R${garcom['valor_vendido']} | 10%: R${garcom['valor_10']}")

def adicionar_pedido(dados, numero_mesa, novo_pedido, nome_garcom):
    # Atualiza mesa
    mesa_encontrada = False
    for mesa in dados['mesas']:
        if mesa['numero'] == numero_mesa:
            mesa['pedidos'].append(novo_pedido)
            mesa['valor_conta'] += novo_pedido['valor']
            mesa_encontrada = True
            break
    if not mesa_encontrada:
        print(f"Mesa {numero_mesa} não encontrada.")
        return

    # Atualiza garçom
    garcom_encontrado = False
    for garcom in dados['garcons']:
        if garcom['nome'].lower() == nome_garcom.lower():
            garcom['valor_vendido'] += novo_pedido['valor']
            garcom['valor_10'] = round(garcom['valor_vendido'] * 0.10, 2)
            garcom_encontrado = True
            break
    if not garcom_encontrado:
        print(f"Garçom '{nome_garcom}' não encontrado.")

def calcular_total_aberto(dados):
    return sum(mesa['valor_conta'] for mesa in dados['mesas'])

# ----------- Execução -----------
dados = carregar_dados()

# Exibir dados antes
listar_mesas(dados)
listar_garcons(dados)

# Adicionar pedidos
pedido1 = {
    "id": 1,
    "nome": "Hamburguer",
    "valor": 25.0,
    "tipo": "Comida"
}
pedido2 = {
    "id": 2,
    "nome": "Suco",
    "valor": 10.0,
    "tipo": "Bebida"
}

adicionar_pedido(dados, numero_mesa=1, novo_pedido=pedido1, nome_garcom="Carlos")
adicionar_pedido(dados, numero_mesa=1, novo_pedido=pedido2, nome_garcom="João")

salvar_dados(dados)

# Exibir dados depois
listar_mesas(dados)
listar_garcons(dados)

print(f"\n💰 Total aberto no restaurante: R${calcular_total_aberto(dados):.2f}")
