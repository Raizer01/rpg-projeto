import random
from abc import ABC, abstractmethod
from arma import Arma

class Evento(ABC):
    def __init__(self, nome: str):
        self.nome = nome
        self.alvo = None

    @abstractmethod
    def aplicar(self, jogadores: list):
        pass

    def mensagem(self) -> str:
        match self.nome:
            case "Cura":
                return "[EVENTO] Cura! Os dois jogadores recuperaram 20 de vida!"
            case "Escudo":
                return f"[EVENTO] Escudo! {self.alvo.nome} ficou imune ao proximo ataque!"
            case "Fadiga":
                return f"[EVENTO] Fadiga! {self.alvo.nome} perdeu 10 de vida!"
            case "Veneno":
                return f"[EVENTO] Veneno! {self.alvo.nome} foi envenenado por 3 turnos!"
            case "Roubo de Armas":
                return "[EVENTO] Roubo de armas! Os dois jogadores perderam as armas e vao no soco!"
            case _:
                return f"[EVENTO] {self.nome}!"


class Cura(Evento):
    def __init__(self):
        super().__init__("Cura")

    def aplicar(self, jogadores):
        for j in jogadores:
            j.curar(20)


class Escudo(Evento):
    def __init__(self):
        super().__init__("Escudo")

    def aplicar(self, jogadores):
        self.alvo = random.choice(jogadores)
        self.alvo.imune = True


class Fadiga(Evento):
    def __init__(self):
        super().__init__("Fadiga")

    def aplicar(self, jogadores):
        self.alvo = random.choice(jogadores)
        self.alvo.sofrer_dano(10)


class Veneno(Evento):
    def __init__(self):
        super().__init__("Veneno")

    def aplicar(self, jogadores):
        self.alvo = random.choice(jogadores)
        self.alvo.veneno_turnos = 3


class RouboDeArmas(Evento):
    def __init__(self):
        super().__init__("Roubo de Armas")

    def aplicar(self, jogadores):
        for j in jogadores:
            j.arma = Arma("Soco", 0)


EVENTOS = [Cura, Escudo, Fadiga, Veneno, RouboDeArmas]


def sortear_evento(chance: float = 0.3):
    """Retorna um evento novo com a probabilidade 'chance', ou None."""
    if random.random() < chance:
        return random.choice(EVENTOS)()
    return None