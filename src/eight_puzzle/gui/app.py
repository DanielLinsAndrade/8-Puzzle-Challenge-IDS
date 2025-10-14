from __future__ import annotations
import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List, Tuple

from ..core.state import OBJETIVO, pretty_state, eh_soluvel
from ..core.puzzle import scramble_from_goal
from ..search.ids import ids

Estado = Tuple[int, ...]


class PuzzleGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("8-Puzzle — IDS")

        self.state: List[int] = list(scramble_from_goal(steps=8, seed=42))
        self.buttons: list[tk.Button] = []
        self.animating = False
        self.anim_speed = 300
        self.solution_path: list[Estado] | None = None
        self.step_index = 0
        self.original_state = self.state[:]

        self.status = tk.StringVar(value="Pronto.")
        tk.Label(root, textvariable=self.status, font=("Segoe UI", 11)).pack(pady=6)

        self.board = tk.Frame(root, bd=6, relief="ridge", bg="#111")
        self.board.pack(padx=10, pady=10)
        for r in range(3):
            for c in range(3):
                idx = r*3 + c
                b = tk.Button(
                    self.board,
                    command=lambda i=idx: self.on_click(i),
                    font=("Segoe UI", 20, "bold"),
                    width=3, height=1, relief="raised", bd=3, cursor="hand2",
                    activebackground="#ddd", activeforeground="#000"
                )
                b.grid(row=r, column=c, padx=6, pady=6, ipadx=15, ipady=15)
                self.buttons.append(b)

        ctrls = tk.Frame(root); ctrls.pack(pady=6)
        tk.Button(ctrls, text="Embaralhar", command=self.cmd_shuffle).grid(row=0, column=0, padx=4, pady=4)
        tk.Button(ctrls, text="Digitar Tabuleiro", command=self.cmd_input).grid(row=0, column=1, padx=4, pady=4)
        tk.Button(ctrls, text="Resolver (IDS)", command=self.cmd_solve).grid(row=0, column=2, padx=4, pady=4)
        tk.Button(ctrls, text="▶️ Reproduzir", command=self.cmd_play).grid(row=0, column=3, padx=4, pady=4)
        tk.Button(ctrls, text="⏸️ Pausar", command=self.cmd_pause).grid(row=0, column=4, padx=4, pady=4)
        tk.Button(ctrls, text="↺ Reset", command=self.cmd_reset).grid(row=0, column=5, padx=4, pady=4)

        sp = tk.Frame(root); sp.pack(pady=2)
        tk.Label(sp, text="Velocidade (ms por passo):").pack(side="left")
        self.speed_scale = tk.Scale(sp, from_=50, to=1000, orient="horizontal",
                                    command=self.on_speed_change, length=200)
        self.speed_scale.set(self.anim_speed)
        self.speed_scale.pack(side="left", padx=6)

        self.render()

    # ---------- GUI helpers ----------
    def render(self) -> None:
        for i, b in enumerate(self.buttons):
            val = self.state[i]
            if val == 0:
                b.config(text="", state="disabled", bg="#e6e6e6")
            else:
                b.config(text=str(val), state="normal", bg="#ffffff")

        if tuple(self.state) == OBJETIVO:
            self.status.set("✅ Objetivo alcançado!")
        else:
            self.status.set("Movimente clicando nas peças adjacentes ao vazio.")

    def on_click(self, idx: int) -> None:
        if self.animating: return
        i0 = self.state.index(0)
        r0, c0 = divmod(i0, 3)
        r, c = divmod(idx, 3)
        if abs(r-r0) + abs(c-c0) == 1:
            self.state[i0], self.state[idx] = self.state[idx], self.state[i0]
            self.render()

    def cmd_shuffle(self) -> None:
        if self.animating: return
        n = simpledialog.askinteger("Embaralhar", "Quantos movimentos (ex.: 12)?",
                                    initialvalue=12, minvalue=1, maxvalue=200)
        if n is None: return
        self.state = list(scramble_from_goal(steps=n))
        self.original_state = self.state[:]
        self.solution_path = None
        self.step_index = 0
        self.render()

    def _parse_nums(self, s: str) -> list[int] | None:
        s = s.replace(",", " ")
        toks = [t for t in s.split() if t]
        try:
            return [int(t) for t in toks]
        except ValueError:
            return None

    def cmd_input(self) -> None:
        if self.animating: return
        s = simpledialog.askstring(
            "Digitar Tabuleiro",
            "Digite 9 números (0 a 8), separados por espaço/ vírgula. 0 é o vazio.\nEx.: 1 2 3 4 0 6 7 5 8"
        )
        if not s: return
        nums = self._parse_nums(s)
        if nums is None or len(nums) != 9 or set(nums) != set(range(9)):
            messagebox.showerror("Erro", "Entrada inválida. Use todos os números 0..8 sem repetir.")
            return
        if not eh_soluvel(tuple(nums)):
            messagebox.showwarning("Atenção", "Este estado NÃO é solúvel. Tente outro.")
            return
        self.state = nums
        self.original_state = self.state[:]
        self.solution_path = None
        self.step_index = 0
        self.render()

    def cmd_solve(self) -> None:
        if self.animating: return
        est = tuple(self.state)
        if not eh_soluvel(est):
            messagebox.showwarning("Atenção", "Este estado não é solúvel.")
            return
        self.status.set("Resolvendo com IDS…")
        self.root.update_idletasks()
        caminho, visitados, L = ids(est, limite_max=60)
        if not caminho:
            messagebox.showinfo("Resultado", "Não encontrou solução no limite.")
            self.status.set("Sem solução no limite.")
            return
        self.solution_path = caminho
        self.step_index = 0
        msg = f"Solução encontrada! L={L} | Passos={len(caminho)-1} | Nós visitados={visitados}"
        messagebox.showinfo("Resultado", msg)
        self.status.set(msg)

    def cmd_play(self) -> None:
        if not self.solution_path:
            messagebox.showinfo("Info", "Primeiro clique em 'Resolver (IDS)'.")
            return
        if self.animating: return
        self.animating = True
        self._animate_step()

    def _animate_step(self) -> None:
        if not self.animating: return
        if not self.solution_path: return
        if self.step_index >= len(self.solution_path):
            self.animating = False
            return
        self.state = list(self.solution_path[self.step_index])
        self.render()
        self.step_index += 1
        self.root.after(self.anim_speed, self._animate_step)

    def cmd_pause(self) -> None:
        self.animating = False

    def cmd_reset(self) -> None:
        self.animating = False
        self.state = self.original_state[:]
        self.step_index = 0
        self.render()

    def on_speed_change(self, _val: str) -> None:
        try:
            self.anim_speed = int(self.speed_scale.get())
        except Exception:
            pass


def run() -> None:
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.resizable(False, False)
    root.mainloop()
