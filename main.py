from jogador import Jogador
from arma import Arma
from classes import Guerreiro, Mago, Ladrao, Arqueiro
from evento import sortear_evento


CLASSES = {
    "1": (Guerreiro(), Arma("Espada", 10)),
    "2": (Mago(), Arma("Cajado", 12)),
    "3": (Ladrao(), Arma("Daga", 8)),
    "4": (Arqueiro(), Arma("Arco", 9))
}


def criar_jogador(p_num: str) -> Jogador:
    nome = input(f"Nome do {p_num}: ").strip()
    j = Jogador(nome)

    print("1. Guerreiro | 2. Mago | 3. Ladrao | 4. Arqueiro")
    opcao = input("Escolha a classe (1-4): ").strip()
    while opcao not in CLASSES:
        print("Opcao invalida! Digite um numero de 1 a 4.")
        opcao = input("Escolha a classe (1-4): ").strip()

    classe, arma = CLASSES[opcao]
    j.escolher_classe(classe, arma)
    return j


def main():
    print("=== ARENA PVP ===")
    j1 = criar_jogador("Jogador 1")
    j2 = criar_jogador("Jogador 2")

    turno = 1
    jogadores = [j1, j2]

    while j1.esta_vivo() and j2.esta_vivo():
        atq = jogadores[(turno - 1) % 2]
        defens = jogadores[turno % 2]

        print(f"\n--- TURNO {turno} ---")

        for j in jogadores:
            j.aplicar_veneno()

        evento = sortear_evento()
        if evento:
            evento.aplicar(jogadores)
            print(evento.mensagem())

        print(j1)
        print(j2)

        if not (j1.esta_vivo() and j2.esta_vivo()):
            break

        input(f"Pressione ENTER para {atq.nome} atacar...")

        atq.atacar(defens)
        turno += 1

    vencedor = j1 if j1.esta_vivo() else j2
    print(f"\nFIM DE JOGO! Vitoria de {vencedor.nome}!")


if __name__ == "__main__":
    main()