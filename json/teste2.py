import json

def carregar_dados():
    with open("dados.json", "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open("dados.json", "w") as f:
        json.dump(dados, f, indent=4)

def adicionar_pedido(dados, numero_mesa, novo_pedido, nome_garcom):
    for mesa in dados["mesas"]:
        if mesa["numero"] == numero_mesa:
            mesa["pedidos"].append(novo_pedido)
            mesa["valor_conta"] += novo_pedido["valor"]
            break

    for garcom in dados["garcons"]:
        if garcom["nome"] == nome_garcom:
            garcom["valor_vendido"] += novo_pedido["valor"]
            garcom["valor_10"] = round(garcom["valor_vendido"] * 0.10, 2)
            break

def listar_mesas(dados):
    print("\nMesas:")
    for mesa in dados["mesas"]:
        print(f"Mesa {mesa['numero']} - Conta: R${mesa['valor_conta']:.2f}")
        for pedido in mesa["pedidos"]:
            print(f"  Pedido: {pedido['nome']} - R${pedido['valor']:.2f}")

def listar_garcons(dados):
    print("\nGarçons:")
    for garcom in dados["garcons"]:
        print(f"{garcom['nome']} - Vendas: R${garcom['valor_vendido']:.2f} | 10%: R${garcom['valor_10']:.2f}")

def calcular_total_aberto(dados):
    return sum(mesa["valor_conta"] for mesa in dados["mesas"])

# ----------- TESTE COM MESA 2 --------------

dados = carregar_dados()

# Novo pedido para mesa 2 feito pelo garçom Carlos
pedido_mesa2 = {
    "id": 4,
    "nome": "Porção de fritas",
    "valor": 15.0,
    "tipo": "Comida"
}
adicionar_pedido(dados, numero_mesa=2, novo_pedido=pedido_mesa2, nome_garcom="Carlos")

salvar_dados(dados)

# Mostrar resultados
listar_mesas(dados)
listar_garcons(dados)
print(f"\n Total aberto no restaurante: R${calcular_total_aberto(dados):.2f}")
