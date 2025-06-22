class Pedido:
    def __init__(self, nome, tipo, status="solicitado"):
        self.nome = nome
        self.tipo = tipo  # Comida, Bebida etc
        self.status = status

    def marcar_como_pronto(self):
        self.status = "pronto"
