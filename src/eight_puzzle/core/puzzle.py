from __future__ import annotations
import random
from typing import Generator, Iterable, List, Tuple
from .state import indice_para_rc, rc_para_indice, OBJETIVO

Estado = Tuple[int, ...]
Movimentos = List[Estado]

def sucessores(estado: Estado) -> Generator[Estado, None, None]:
    i0 = estado.index(0)
    r, c = indice_para_rc(i0)
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:  # cima, baixo, esq, dir
        nr, nc = r+dr, c+dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = rc_para_indice(nr, nc)
            lst = list(estado)
            lst[i0], lst[j] = lst[j], lst[i0]
            yield tuple(lst)

def scramble_from_goal(steps: int = 20, seed: int | None = None) -> Estado:
    s: Estado = OBJETIVO
    if seed is not None:
        random.seed(seed)
    last: Tuple[int, int] | None = None
    for _ in range(steps):
        cand: list[tuple[Estado, tuple[int,int]]] = []
        i0 = s.index(0)
        r, c = indice_para_rc(i0)
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                if last is None or (dr,dc) != (-last[0], -last[1]):
                    j = rc_para_indice(nr, nc)
                    lst = list(s); lst[i0], lst[j] = lst[j], lst[i0]
                    cand.append((tuple(lst),(dr,dc)))
        s, last = random.choice(cand)
    return s
