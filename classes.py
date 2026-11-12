from dados import Dados
from arma import Arma

# Classe base para as profissoes (Guerreiro, Mago, Ladrao, Arqueiro)
class Classe:
    def __init__(self, nome: str, dano_base: int):
        self.nome = nome
        self.dano_base = dano_base
        self.dados = Dados() # Usando a classe Dados

    def calcular_dano(self, arma: Arma) -> int:
        # Soma dano da classe + dano da arma + dado aleatorio
        return self.dano_base + arma.dano + self.dados.jogar()

# Classes filhas minimalistas
class Guerreiro(Classe):
    def __init__(self):
        super().__init__("Guerreiro", 15)

class Mago(Classe):
    def __init__(self):
        super().__init__("Mago", 20)

class Ladrao(Classe):
    def __init__(self):
        super().__init__("Ladrao", 12)

class Arqueiro(Classe):
    def __init__(self):
        super().__init__("Arqueiro", 14)