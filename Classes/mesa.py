from pedido import Pedido

class Mesa:
    def __init__(self, numero):
        self.numero = numero
        self.pedidos = []
        self.valor_conta = 0.0

    def adicionar_pedido(self, pedido: Pedido):
        self.pedidos.append(pedido)
        # Pode-se somar valor ao total se necessário

    def pedidos_por_status(self, status):
        return [p for p in self.pedidos if p.status == status]
