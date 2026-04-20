"""
Lab 11 - Intermediate Code: Quadruple, Triple, Indirect Triple
"""

# ── Temp variable generator ───────────────────────────────────────────────────
class TempGen:
    def __init__(self): self.n = 0
    def new(self): self.n += 1; return f"t{self.n}"

# ── Parse postfix and generate all three representations ─────────────────────
def generate(postfix_expr):
    tokens = postfix_expr.split()
    ops = set('+-*/^')
    stack = []
    quads, triples = [], []
    temp = TempGen()

    for tok in tokens:
        if tok not in ops:
            stack.append(tok)
        else:
            b, a = stack.pop(), stack.pop()
            t = temp.new()
            idx = len(triples)     # 0-based index

            quads.append((tok, a, b, t))
            triples.append((tok, a, b))
            stack.append(t)

    # Indirect triples = pointer list into triples table
    indirect = list(range(len(triples)))
    return quads, triples, indirect

def display_all(quads, triples, indirect):
    # Quadruples
    print("\n  QUADRUPLES")
    print(f"  {'#':<5}{'Op':<6}{'Arg1':<10}{'Arg2':<10}{'Result'}")
    print("  " + "-" * 38)
    for i, (op, a, b, r) in enumerate(quads):
        print(f"  {i:<5}{op:<6}{a:<10}{b:<10}{r}")

    # Triples
    print("\n  TRIPLES")
    print(f"  {'#':<5}{'Op':<6}{'Arg1':<12}{'Arg2'}")
    print("  " + "-" * 30)
    for i, (op, a, b) in enumerate(triples):
        arg1 = f"({a})" if a.startswith('t') and a[1:].isdigit() else a
        arg2 = f"({b})" if b.startswith('t') and b[1:].isdigit() else b
        # Replace temp refs with triple index refs
        ta = int(a[1:])-1 if a.startswith('t') and a[1:].isdigit() else None
        tb = int(b[1:])-1 if b.startswith('t') and b[1:].isdigit() else None
        arg1 = f"({ta})" if ta is not None else a
        arg2 = f"({tb})" if tb is not None else b
        print(f"  {i:<5}{op:<6}{arg1:<12}{arg2}")

    # Indirect Triples
    print("\n  INDIRECT TRIPLES")
    print(f"  {'Ptr':<6}{'→ Triple #':<12}{'Op':<6}{'Arg1':<12}{'Arg2'}")
    print("  " + "-" * 42)
    for ptr, idx in enumerate(indirect):
        op, a, b = triples[idx]
        ta = int(a[1:])-1 if a.startswith('t') and a[1:].isdigit() else None
        tb = int(b[1:])-1 if b.startswith('t') and b[1:].isdigit() else None
        arg1 = f"({ta})" if ta is not None else a
        arg2 = f"({tb})" if tb is not None else b
        print(f"  {ptr:<6}{idx:<12}{op:<6}{arg1:<12}{arg2}")

if __name__ == "__main__":
    exprs = [
        ("a + b * c",       "a b c * +"),
        ("(a+b)*(c-d)",     "a b + c d - *"),
        ("a*b + c*d - e",   "a b * c d * + e -"),
    ]
    for infix, postfix in exprs:
        print("\n" + "=" * 50)
        print(f"  Expression : {infix}")
        print(f"  Postfix    : {postfix}")
        q, t, ind = generate(postfix)
        display_all(q, t, ind)
