from dados import Dados

class App(Dados):
    def gerar_dados_painel(self):
        # Implementação mínima apenas para satisfazer a classe abstrata
        return ""

if __name__ == "__main__":
    app = App()
    app.criar_tela_login()
