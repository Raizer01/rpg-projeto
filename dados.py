import random

# Classe responsavel pelo dano aleatorio
class Dados:
    def jogar(self) -> int:
        return random.randint(1, 20)