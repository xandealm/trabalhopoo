class Cozinha:
    def listar_pedidos_para_preparo(mesas):
        resultado = []
        for mesa in mesas:
            pedidos = mesa.pedidos_por_status("solicitado")
            if pedidos:
                resultado.append((mesa.numero, pedidos))
        return resultado
