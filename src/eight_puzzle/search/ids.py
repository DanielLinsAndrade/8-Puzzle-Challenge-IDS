from __future__ import annotations
from typing import List, Tuple
from ..core.state import OBJETIVO
from ..core.puzzle import sucessores

Estado = Tuple[int, ...]
Caminho = List[Estado]

def dls(estado_inicial: Estado, limite: int) -> tuple[bool, Caminho | None, int]:
    visitados = 0
    stack: list[tuple[Estado, int, Caminho]] = [(estado_inicial, 0, [estado_inicial])]
    while stack:
        estado, prof, caminho = stack.pop()
        visitados += 1
        if estado == OBJETIVO:
            return True, caminho, visitados
        if prof < limite:
            for s in sucessores(estado):
                if s not in caminho:  # evita ciclos no caminho
                    stack.append((s, prof+1, caminho+[s]))
    return False, None, visitados

def ids(estado_inicial: Estado, limite_max: int = 50) -> tuple[Caminho | None, int, int]:
    total_visitados = 0
    for L in range(limite_max + 1):
        achou, caminho, vis = dls(estado_inicial, L)
        total_visitados += vis
        if achou:
            return caminho, total_visitados, L
    return None, total_visitados, limite_max
