import customtkinter as ctk
from pathlib import Path
from PIL import Image
import json
import random
from cozinha import Cozinha
from garcom import Garcom
from dono import Dono




class Inicio:
    def abrir_painel(self, papel):
        self.tela_inicial.destroy()
    
        if papel == "garcom":
            garcom= Garcom()
            garcom.abrir_painel_garcom()
        elif papel == "cozinheiro":
            cozinha = Cozinha()
            cozinha.abrir_painel_cozinheiro()
        else:
            dono = Dono()
            dono.abrir_painel_padrao(papel)
