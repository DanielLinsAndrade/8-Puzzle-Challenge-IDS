from __future__ import annotations
from typing import Iterable, List, Tuple

OBJETIVO: Tuple[int, ...] = (1,2,3
                            ,4,5,6
                            ,7,8,0)

def indice_para_rc(i: int) -> Tuple[int, int]:
    return divmod(i, 3)

def rc_para_indice(r: int, c: int) -> int:
    return r*3 + c

def pretty_state(s: Iterable[int]) -> str:
    a: List[int] = list(s)
    rows = [a[0:3], a[3:6], a[6:9]]
    return "\n".join(" ".join("_" if x==0 else str(x) for x in r) for r in rows)

def inversions_parity(estado: Iterable[int]) -> int:
    arr = [x for x in estado if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2

def eh_soluvel(estado: Iterable[int]) -> bool:
    return inversions_parity(estado) == 0
