from classes import Classe
from arma import Arma

# Classe Jogador com vida e classe equipada
class Jogador:
    def __init__(self, nome: str):
        self.nome = nome
        self.vida_maxima = 200
        self.vida = self.vida_maxima # Vida inicial
        self.veneno_turnos = 0
        self.imune = False
        self.classe: Classe = None
        self.arma: Arma = None

    def escolher_classe(self, classe: Classe, arma: Arma):
        self.classe = classe
        self.arma = arma

    def atacar(self, alvo: 'Jogador'):
        if alvo.imune:
            alvo.imune = False
            print(f"{self.nome} atacou {alvo.nome}, mas {alvo.nome} estava imune!")
            return
        dano_total = self.classe.calcular_dano(self.arma)
        alvo.vida -= dano_total
        if alvo.vida < 0:
            alvo.vida = 0
        print(f"{self.nome} atacou {alvo.nome} causando {dano_total} de dano!")

    def curar(self, valor: int):
        self.vida = min(self.vida + valor, self.vida_maxima)

    def sofrer_dano(self, valor: int):
        self.vida = max(self.vida - valor, 0)

    def aplicar_veneno(self):
        if self.veneno_turnos > 0:
            dano = 8
            self.sofrer_dano(dano)
            self.veneno_turnos -= 1
            print(f"[VENENO] {self.nome} sofreu {dano} de dano! (restam {self.veneno_turnos} turnos)")

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def __str__(self):
        marca = " [IMUNE]" if self.imune else ""
        return f"{self.nome} ({self.classe.nome}) - HP: {self.vida}/{self.vida_maxima}{marca}"