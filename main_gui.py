import os
import tkinter as tk
from tkinter import ttk
from contextlib import redirect_stdout

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None

from jogador import Jogador
from arma import Arma
from classes import Guerreiro, Mago, Ladrao, Arqueiro
from evento import sortear_evento


# Paleta visual
BG = "#10131d"
PANEL = "#191f2e"
PANEL_ALT = "#20283a"
GOLD = "#e6b85c"
GOLD_DARK = "#9d7736"
TEXT = "#f1f3f8"
MUTED = "#9ba6ba"
GREEN = "#43c982"
RED = "#ef626c"
PURPLE = "#a78bfa"
BLUE = "#66b8e8"

OPCOES = [
    ("Guerreiro", Guerreiro, "Espada", 10, "⚔", "#d97757", "Resistente e poderoso"),
    ("Mago", Mago, "Cajado", 12, "✦", "#9b82ed", "Domina a magia arcana"),
    ("Ladrao", Ladrao, "Daga", 8, "🗡", "#55bd9a", "Ágil e imprevisível"),
    ("Arqueiro", Arqueiro, "Arco", 9, "➶", "#65a9df", "Ataca com precisão"),
]

PASTA_SPRITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
TAMANHO_SPRITE = 92
_cache_sprites = {}


def carregar_sprite(nome_classe):
    if nome_classe in _cache_sprites:
        return _cache_sprites[nome_classe]
    caminho = os.path.join(PASTA_SPRITES, nome_classe.lower() + ".png")
    imagem = None
    if os.path.exists(caminho):
        try:
            if Image:
                img = Image.open(caminho).convert("RGBA")
                img = img.resize((TAMANHO_SPRITE, TAMANHO_SPRITE), Image.NEAREST)
                imagem = ImageTk.PhotoImage(img)
            else:
                imagem = tk.PhotoImage(file=caminho)
        except Exception:
            imagem = None
    _cache_sprites[nome_classe] = imagem
    return imagem


def montar_classe_e_arma(indice):
    _, classe, nome_arma, dano_arma, *_ = OPCOES[indice]
    return classe(), Arma(nome_arma, dano_arma)


class SaidaParaTela:
    def __init__(self, widget):
        self.widget = widget

    def write(self, texto):
        tag = ()
        if "[EVENTO]" in texto:
            tag = "evento"
        elif "[VENENO]" in texto or "causando" in texto:
            tag = "dano"
        self.widget.config(state="normal")
        self.widget.insert("end", texto, tag)
        self.widget.see("end")
        self.widget.config(state="disabled")

    def flush(self):
        pass


def botao_estilizado(parent, texto, comando, destaque=False, width=None):
    cor = GOLD if destaque else PANEL_ALT
    fg = "#171923" if destaque else TEXT
    hover = "#f3cc7b" if destaque else "#303b52"
    b = tk.Button(parent, text=texto, command=comando, width=width,
                  bg=cor, fg=fg, activebackground=hover, activeforeground=fg,
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"), padx=16, pady=10)
    b.bind("<Enter>", lambda _e: b.config(bg=hover))
    b.bind("<Leave>", lambda _e: b.config(bg=cor))
    return b


class PainelJogador(tk.Frame):
    def __init__(self, master, numero):
        super().__init__(master, bg=PANEL, highlightthickness=1,
                         highlightbackground="#30394d")
        self.numero = numero
        topo = tk.Frame(self, bg=PANEL)
        topo.pack(fill="x", padx=14, pady=(12, 4))
        self.lbl_numero = tk.Label(topo, text=f"JOGADOR {numero}",
                                   bg=PANEL, fg=GOLD,
                                   font=("Segoe UI", 8, "bold"))
        self.lbl_numero.pack(side="left")
        self.lbl_status = tk.Label(topo, text="● PRONTO", bg=PANEL,
                                   fg=GREEN, font=("Segoe UI", 8, "bold"))
        self.lbl_status.pack(side="right")

        centro = tk.Frame(self, bg=PANEL)
        centro.pack(fill="x", padx=14, pady=6)
        self.lbl_sprite = tk.Label(centro, bg=PANEL, width=5, height=2)
        self.lbl_sprite.pack(side="left", padx=(0, 12))
        info = tk.Frame(centro, bg=PANEL)
        info.pack(side="left", fill="x", expand=True)
        self.lbl_nome = tk.Label(info, text="Aguardando...", bg=PANEL,
                                 fg=TEXT, font=("Segoe UI", 12, "bold"),
                                 anchor="w")
        self.lbl_nome.pack(fill="x")
        self.lbl_arma = tk.Label(info, text="Arma: —", bg=PANEL,
                                 fg=MUTED, font=("Segoe UI", 9), anchor="w")
        self.lbl_arma.pack(fill="x", pady=(3, 0))

        self.barra = ttk.Progressbar(self, length=200, mode="determinate",
                                     style="HP.Horizontal.TProgressbar")
        self.barra.pack(fill="x", padx=14, pady=(8, 3))
        rodape = tk.Frame(self, bg=PANEL)
        rodape.pack(fill="x", padx=14, pady=(0, 12))
        self.lbl_hp = tk.Label(rodape, text="HP: —", bg=PANEL, fg=TEXT,
                               font=("Segoe UI", 9, "bold"))
        self.lbl_hp.pack(side="left")
        self.lbl_extra = tk.Label(rodape, text="", bg=PANEL, fg=RED,
                                  font=("Segoe UI", 8, "bold"))
        self.lbl_extra.pack(side="right")

    def atualizar(self, j):
        sprite = carregar_sprite(j.classe.nome)
        if sprite:
            # Com imagem, width/height do Label são em pixels
            self.lbl_sprite.config(image=sprite, text="",
                                   width=TAMANHO_SPRITE, height=TAMANHO_SPRITE)
        else:
            # Sem imagem, width/height do Label são em caracteres
            icone = next((o[4] for o in OPCOES if o[0] == j.classe.nome), "✦")
            self.lbl_sprite.config(image="", text=icone, fg=GOLD,
                                   font=("Segoe UI Symbol", 30),
                                   width=5, height=2)
        self.lbl_nome.config(text=f"{j.nome}  ·  {j.classe.nome}")
        self.lbl_arma.config(text=f"Equipamento: {j.arma.nome}")
        self.barra.configure(maximum=j.vida_maxima, value=j.vida)
        self.lbl_hp.config(text=f"HP  {j.vida}/{j.vida_maxima}")
        self.lbl_status.config(text="● VIVO" if j.esta_vivo() else "● DERROTADO",
                               fg=GREEN if j.esta_vivo() else RED)
        extras = []
        if j.imune:
            extras.append("ESCUDO")
        if j.veneno_turnos > 0:
            extras.append(f"VENENO {j.veneno_turnos}")
        self.lbl_extra.config(text="  |  ".join(extras))


class ArenaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Arena — Batalha PvP")
        self.root.geometry("1040x720")
        self.root.minsize(850, 650)
        self.root.configure(bg=BG)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("HP.Horizontal.TProgressbar",
                         troughcolor="#30394d", background=GREEN,
                         bordercolor=PANEL, lightcolor=GREEN,
                         darkcolor=GREEN, thickness=12)
        estilo.configure("TCombobox", fieldbackground=PANEL_ALT,
                         background=PANEL_ALT, foreground=TEXT,
                         arrowcolor=GOLD, bordercolor="#3b465e",
                         lightcolor=PANEL_ALT, darkcolor=PANEL_ALT,
                         padding=7)
        estilo.map("TCombobox",
                   fieldbackground=[("readonly", PANEL_ALT)],
                   foreground=[("readonly", TEXT)],
                   selectbackground=[("readonly", PANEL_ALT)],
                   selectforeground=[("readonly", TEXT)])

        self.jogadores = []
        self.turno = 1
        self.tela_config = tk.Frame(root, bg=BG)
        self.tela_jogo = tk.Frame(root, bg=BG)
        self.montar_tela_config()
        self.montar_tela_jogo()
        self.tela_config.pack(fill="both", expand=True)

    def montar_tela_config(self):
        tela = self.tela_config
        header = tk.Frame(tela, bg=BG)
        header.pack(fill="x", pady=(34, 20))
        tk.Label(header, text="⚔", bg=BG, fg=GOLD,
                 font=("Segoe UI Symbol", 30)).pack()
        tk.Label(header, text="RPG ARENA", bg=BG, fg=TEXT,
                 font=("Segoe UI", 28, "bold")).pack()
        tk.Label(header, text="DUELO DE CAMPEÕES  •  BATALHA POR TURNOS",
                 bg=BG, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(pady=(5, 0))

        area = tk.Frame(tela, bg=BG)
        area.pack(fill="x", padx=40, pady=8)
        area.columnconfigure(0, weight=1)
        area.columnconfigure(1, weight=1)
        self.entradas_nome = []
        self.combos_classe = []
        self.cards_classe = []

        for i in (1, 2):
            card = tk.Frame(area, bg=PANEL, highlightthickness=1,
                            highlightbackground="#30394d")
            card.grid(row=0, column=i-1, sticky="nsew",
                      padx=(0, 10) if i == 1 else (10, 0))
            tk.Label(card, text=f"JOGADOR {i}", bg=PANEL, fg=GOLD,
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=18, pady=(16, 10))
            tk.Label(card, text="Nome do personagem", bg=PANEL, fg=MUTED,
                     font=("Segoe UI", 9)).pack(anchor="w", padx=18)
            entrada = tk.Entry(card, bg=PANEL_ALT, fg=TEXT, insertbackground=TEXT,
                               relief="flat", font=("Segoe UI", 11),
                               highlightthickness=1, highlightbackground="#3b465e",
                               highlightcolor=GOLD)
            entrada.pack(fill="x", padx=18, pady=(5, 14), ipady=8)
            entrada.insert(0, f"Herói {i}")

            tk.Label(card, text="Escolha sua classe", bg=PANEL, fg=MUTED,
                     font=("Segoe UI", 9)).pack(anchor="w", padx=18)
            combo = ttk.Combobox(card, values=[o[0] for o in OPCOES],
                                 state="readonly", font=("Segoe UI", 10))
            combo.current(i-1)
            combo.pack(fill="x", padx=18, pady=(5, 18), ipady=4)
            self.entradas_nome.append(entrada)
            self.combos_classe.append(combo)

            preview = tk.Label(card, text="", bg=PANEL, fg=TEXT,
                               font=("Segoe UI", 9), justify="left")
            preview.pack(anchor="w", padx=18, pady=(0, 14))
            self.cards_classe.append(preview)
            combo.bind("<<ComboboxSelected>>",
                       lambda _e, idx=i-1: self.atualizar_preview(idx))
            self.atualizar_preview(i-1)

        self.aviso = tk.Label(tela, text="", bg=BG, fg=RED,
                              font=("Segoe UI", 9, "bold"))
        self.aviso.pack(pady=(10, 0))
        botao_estilizado(tela, "INICIAR BATALHA  →", self.iniciar_jogo,
                         destaque=True, width=23).pack(pady=16)
        tk.Label(tela, text="Prepare sua estratégia. Apenas um sairá vitorioso.",
                 bg=BG, fg="#69758b", font=("Segoe UI", 9, "italic")).pack()

    def atualizar_preview(self, idx):
        nome = self.combos_classe[idx].get()
        op = next((o for o in OPCOES if o[0] == nome), OPCOES[0])
        self.cards_classe[idx].config(
            text=f"{op[4]}   {op[6]}\n       Arma inicial: {op[2]}  •  Dano: {op[3]}")

    def montar_tela_jogo(self):
        tela = self.tela_jogo
        topo = tk.Frame(tela, bg=BG)
        topo.pack(fill="x", padx=22, pady=(18, 10))
        tk.Label(topo, text="⚔  RPG ARENA", bg=BG, fg=GOLD,
                 font=("Segoe UI", 17, "bold")).pack(side="left")
        self.vez = tk.StringVar(value="A batalha está prestes a começar")
        self.lbl_vez = tk.Label(topo, textvariable=self.vez, bg=PANEL_ALT,
                                fg=TEXT, font=("Segoe UI", 10, "bold"),
                                padx=14, pady=8)
        self.lbl_vez.pack(side="right")

        jogadores_area = tk.Frame(tela, bg=BG)
        jogadores_area.pack(fill="x", padx=22, pady=8)
        jogadores_area.columnconfigure(0, weight=1)
        jogadores_area.columnconfigure(1, weight=1)
        self.painel_j1 = PainelJogador(jogadores_area, 1)
        self.painel_j1.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.painel_j2 = PainelJogador(jogadores_area, 2)
        self.painel_j2.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        log_area = tk.Frame(tela, bg=PANEL, highlightthickness=1,
                            highlightbackground="#30394d")
        log_area.pack(fill="both", expand=True, padx=22, pady=(10, 8))
        cabecalho = tk.Frame(log_area, bg=PANEL)
        cabecalho.pack(fill="x", padx=14, pady=(12, 6))
        tk.Label(cabecalho, text="📜  DIÁRIO DE BATALHA", bg=PANEL,
                 fg=GOLD, font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(cabecalho, text="EVENTOS E AÇÕES", bg=PANEL,
                 fg=MUTED, font=("Segoe UI", 8)).pack(side="right")
        separador = tk.Frame(log_area, bg="#30394d", height=1)
        separador.pack(fill="x", padx=14, pady=(0, 4))
        corpo = tk.Frame(log_area, bg=PANEL)
        corpo.pack(fill="both", expand=True, padx=14, pady=(4, 12))
        rolagem = tk.Scrollbar(corpo)
        rolagem.pack(side="right", fill="y")
        self.log = tk.Text(corpo, state="disabled", wrap="word",
                           font=("Consolas", 10), bg="#121722", fg="#d8deeb",
                           insertbackground=TEXT, relief="flat", bd=0,
                           padx=12, pady=10, yscrollcommand=rolagem.set,
                           selectbackground="#46536e")
        self.log.pack(side="left", fill="both", expand=True)
        rolagem.config(command=self.log.yview)
        self.log.tag_configure("turno", foreground=GOLD, font=("Consolas", 10, "bold"))
        self.log.tag_configure("evento", foreground=PURPLE)
        self.log.tag_configure("dano", foreground=RED)

        barra = tk.Frame(tela, bg=BG)
        barra.pack(fill="x", padx=22, pady=(4, 18))
        self.botao_atacar = botao_estilizado(barra, "⚔  ATACAR",
                                             self.atacar, destaque=True, width=16)
        self.botao_atacar.pack(side="left")
        botao_estilizado(barra, "↻  NOVO JOGO", self.novo_jogo,
                         width=15).pack(side="right")

    def atualizar_paineis(self):
        self.painel_j1.atualizar(self.jogadores[0])
        self.painel_j2.atualizar(self.jogadores[1])

    def alguem_morreu(self):
        return not all(j.esta_vivo() for j in self.jogadores)

    def escrever_log(self, texto, tag=None):
        self.log.config(state="normal")
        self.log.insert("end", texto, tag or ())
        self.log.see("end")
        self.log.config(state="disabled")

    def iniciar_jogo(self):
        nomes = [e.get().strip() for e in self.entradas_nome]
        if not all(nomes):
            self.aviso.config(text="Preencha o nome dos dois jogadores para continuar.")
            return
        if nomes[0].casefold() == nomes[1].casefold():
            self.aviso.config(text="Escolha nomes diferentes para cada jogador.")
            return

        self.jogadores = []
        for nome, combo in zip(nomes, self.combos_classe):
            j = Jogador(nome)
            classe, arma = montar_classe_e_arma(combo.current())
            j.escolher_classe(classe, arma)
            self.jogadores.append(j)

        self.turno = 1
        self.aviso.config(text="")
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")
        self.tela_config.pack_forget()
        self.tela_jogo.pack(fill="both", expand=True)
        self.atualizar_paineis()
        self.escrever_log("  A arena está aberta. Que comece o duelo!\n\n", "turno")
        self.iniciar_turno()

    def iniciar_turno(self):
        atq = self.jogadores[(self.turno - 1) % 2]
        self.escrever_log(f"\n── TURNO {self.turno} ──\n", "turno")

        with redirect_stdout(SaidaParaTela(self.log)):
            for j in self.jogadores:
                j.aplicar_veneno()
            evento = sortear_evento()
            if evento:
                evento.aplicar(self.jogadores)
                print(evento.mensagem())

        self.atualizar_paineis()
        if self.alguem_morreu():
            self.fim_de_jogo()
            return
        self.vez.set(f"VEZ DE  {atq.nome.upper()}")
        self.botao_atacar.config(state="normal", bg=GOLD)

    def atacar(self):
        atq = self.jogadores[(self.turno - 1) % 2]
        defens = self.jogadores[self.turno % 2]
        with redirect_stdout(SaidaParaTela(self.log)):
            atq.atacar(defens)
        self.atualizar_paineis()
        self.turno += 1
        if self.alguem_morreu():
            self.fim_de_jogo()
        else:
            self.iniciar_turno()

    def fim_de_jogo(self):
        j1, j2 = self.jogadores
        vencedor = j1 if j1.esta_vivo() else j2
        self.escrever_log(f"\n★  FIM DE JOGO! VITÓRIA DE {vencedor.nome.upper()}!  ★\n",
                          "turno")
        self.vez.set(f"🏆  VITÓRIA: {vencedor.nome.upper()}")
        self.botao_atacar.config(state="disabled", bg="#555b68")

    def novo_jogo(self):
        self.tela_jogo.pack_forget()
        self.tela_config.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    ArenaApp(root)
    root.mainloop()
