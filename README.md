# 8-Puzzle Challenge — IDS (Tkinter)

Repositório do 8-Puzzle com solução automática via **Busca em Aprofundamento Iterativo (IDS)**.  
Interface gráfica em **Tkinter**, suporte a **embaralhar**, **digitar estado**, **resolver** e **reproduzir animação** do caminho.
 
> **Algoritmo**: IDS (Iterative Deepening Search)  
> **Linguagem**: Python 3.8+ (Tkinter nativo)

## Features

- GUI 3×3: clique nas peças para mover (como no puzzle físico).
- Embaralhar por N movimentos (sempre solúvel).
- Digitar qualquer configuração 0..8 (valida e recusa insolúveis).
- Resolver com **IDS**, exibindo: **Passos, Nós visitados, L**.
- Reproduzir a solução com animação (velocidade ajustável).
- Projeto modular (pacote `eight_puzzle/`).

## Instalação e execução

```bash
# entre na pasta do repositório clonado
cd 8-Puzzle-Challenge-IDS

# (opcional) criar venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# instalar em modo dev
pip install -e .

# rodar
python main.py
# ou via entrypoint (pyproject.toml):
eight-puzzle
```

## Modelagem do problema

### Representação do estado: tupla de 9 posições (linha a linha), com 0 como espaço vazio.

**Estado Inicial**
```bash
1 2 3
4 _ 6
7 5 8
```

**Estado Objetivo**
```bash
1 2 3
4 5 6
7 8 _
```

**Teste de objetivo:** estado == OBJETIVO
**Solubilidade (3×3):** número de inversões (ignorando o 0) par.

## Função Sucessora

Mover o 0 em {CIMA, BAIXO, ESQ, DIR} quando possível (troca com o vizinho e gera novo estado).
Pré-condições: r>0 (cima), r<2 (baixo), c>0 (esq), c<2 (dir).

## Função de Custo

Custo uniforme = 1 por movimento.
Custo do caminho = nº de passos até o objetivo.

## Árvore de busca simplificada (IDS)

O IDS executa DLS com **limites crescentes** `L=0,1,2,…`.

Para o inicial `(1,2,3,4,0,6,7,5,8)`, o **caminho ótimo** é:
- **Movimentos**: **BAIXO → DIREITA**  
- **Passos (custo)**: **2**  
- **Limite onde encontrou**: **L = 2**  
- **Nós visitados (somando L=0,1,2)**: **15**  
  - L=0 → 1 nó  
  - L=1 → 5 nós  
  - L=2 → 9 nós  
  - **Total:** 15

> A GUI mostra esses números ao final da resolução.

## Análise do algoritmo (IDS)

- **Completo**: sim (espaço finito, solução de profundidade finita).  
- **Ótimo**: sim com custo uniforme (=1 movimento).  
- **Memória**: baixa (semelhante a DFS).  
- **Tempo**: maior que BFS em geral, porque **re-expande** nós a cada novo limite.  
- **Trade-off**: economiza memória e ainda acha solução ótima; paga em tempo quando a profundidade cresce.

## Estrutura do Projeto

```bash
.
├─ pyproject.toml
├─ README.md
├─ main.py
└─ src/
   └─ eight_puzzle/
      ├─ __init__.py
      ├─ core/
      │  ├─ state.py
      │  └─ puzzle.py
      ├─ search/
      │  ├─ __init__.py
      │  └─ ids.py
      └─ gui/
         ├─ __init__.py
         └─ app.py
```

## Como reproduzir os números do relatório

1. Abra o app → **Digitar Tabuleiro** → cole `(1,2,3,4,0,6,7,5,8)`.  
2. Clique **Resolver (IDS)**.  
3. Anote: **L**, **Passos**, **Nós visitados**.  
4. Passo Opcional: **Reproduzir** para animar o caminho.

## Créditos
 
Autores: Bruno Paiva, Daniel Lins, Gerson Douglas, Pollyana Dias.
