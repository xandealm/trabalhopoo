from pessoa import Pessoa

class Garcom(Pessoa):
    def __init__(self, id, nome, senha, valor_vendido=0):
        super().__init__(id, nome, senha, "garcom")
        self.valor_vendido = valor_vendido

    def calcular_comissao(self):
        return self.valor_vendido * 0.10
