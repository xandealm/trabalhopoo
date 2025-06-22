from mesa import Mesa
from garcom import Garcom

class Restaurante:
    def __init__(self):
        self.mesas = []
        self.garcons = []

    def carregar_dados(self, dados_json):
        for m in dados_json["mesas"]:
            mesa = Mesa(m["numero"])
            mesa.valor_conta = m["valor_conta"]
            for p in m["pedidos"]:
                from pedido import Pedido
                pedido = Pedido(p["nome"], p["tipo"], p.get("status", "solicitado"))
                mesa.adicionar_pedido(pedido)
            self.mesas.append(mesa)

        for g in dados_json["garcons"]:
            garcom = Garcom(g["id"], g["nome"], "", g["valor_vendido"])
            self.garcons.append(garcom)

    def faturamento_total(self):
        return sum(m.valor_conta for m in self.mesas)
