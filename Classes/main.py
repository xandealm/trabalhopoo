# main.py
from dados import Dados
from dono import Dono 

# Como a classe Dados é abstrata, não podemos criar uma instância dela.
# Em vez disso, criamos uma instância de uma de suas classes filhas, como Dono,
# para iniciar o processo. A tela de login é a mesma para todos.

if __name__ == "__main__":
    app = Dono() # Pode ser Dono(), Garcom() ou Cozinha(). A tela de login é chamada de Dados.
    app.criar_tela_login()