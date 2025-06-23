
class Painel:
    def abrir_painel(papel):
        if papel == "garcom":
            from garcom import Garcom
            g = Garcom()
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