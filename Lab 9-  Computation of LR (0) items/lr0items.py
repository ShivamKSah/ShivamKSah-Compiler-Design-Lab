"""
Lab 9 - Computation of LR(0) Items
"""

from typing import Dict, FrozenSet, Iterable, List, Optional, Sequence, Set, Tuple

Symbol = str
RHS = Tuple[Symbol, ...]
Production = Tuple[Symbol, RHS, int]
State = FrozenSet[Production]
Grammar = Dict[Symbol, List[List[Symbol]]]

def closure(items: Iterable[Production], grammar: Grammar) -> State:
    result: List[Production] = list(items)
    seen: Set[Production] = set(items)
    i = 0
    while i < len(result):
        lhs, rhs, dot = result[i]
        if dot < len(rhs) and rhs[dot] in grammar:
            B = rhs[dot]
            for prod in grammar[B]:
                item = (B, tuple(prod), 0)
                if item not in seen:
                    seen.add(item)
                    result.append(item)
        i += 1
    return frozenset(result)

def goto(state: State, symbol: Symbol, grammar: Grammar) -> Optional[State]:
    moved = [(l, r, d + 1) for l, r, d in state if d < len(r) and r[d] == symbol]
    return closure(moved, grammar) if moved else None

def lr0_items(grammar: Grammar, start: Symbol) -> Tuple[List[State], Dict[State, Dict[Symbol, int]], Symbol]:
    # Work on a copy so callers keep their original grammar unchanged.
    grammar = {lhs: [prod[:] for prod in rhs_list] for lhs, rhs_list in grammar.items()}
    aug = start + "'"
    grammar[aug] = [[start]]
    init = closure([(aug, (start,), 0)], grammar)
    states: List[State] = [init]
    trans: Dict[State, Dict[Symbol, int]] = {init: {}}
    queue: List[State] = [init]
    syms: Set[Symbol] = {s for p in grammar.values() for prod in p for s in prod}
    while queue:
        cur = queue.pop(0)
        for sym in syms:
            nxt = goto(cur, sym, grammar)
            if nxt and nxt not in states:
                states.append(nxt)
                trans[nxt] = {}
                queue.append(nxt)
            if nxt:
                trans[cur][sym] = states.index(nxt)
    return states, trans, aug

def fmt(item: Production) -> str:
    l, r, d = item
    r2 = list(r); r2.insert(d, '•')
    return f"{l} -> {' '.join(r2)}"

def display(states: Sequence[State], trans: Dict[State, Dict[Symbol, int]]) -> None:
    for i, state in enumerate(states):
        print(f"\n  I{i}:")
        for item in sorted(state, key=str): print(f"    {fmt(item)}")
        for sym, j in trans.get(state, {}).items():
            print(f"    GOTO({sym}) = I{j}")

if __name__ == "__main__":
    grammar = {
        'E': [['E','+','T'], ['T']],
        'T': [['T','*','F'], ['F']],
        'F': [['(','E',')'], ['id']],
    }
    states, trans, aug = lr0_items(grammar, 'E')
    print(f"Augmented start: {aug} -> E")
    print(f"Total states: {len(states)}")
    display(states, trans)
