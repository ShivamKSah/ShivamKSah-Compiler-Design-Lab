# Lab 11 - Intermediate Code: Quadruple, Triple, Indirect Triple

## Aim
Generate three forms of intermediate code — Quadruples, Triples, and Indirect Triples — from an expression.

## Theory

### Quadruples `(op, arg1, arg2, result)`
Each instruction has 4 fields. Result stored in a temp variable.
```
(*, b, c, t1)   →   t1 = b * c
(+, a, t1, t2)  →   t2 = a + t1
```

### Triples `(op, arg1, arg2)`
No result field — referenced by position number `(i)`.
```
(0): (*, b, c)
(1): (+, a, (0))
```

### Indirect Triples
A pointer table that lists triple indices — allows reordering without renaming.
```
Ptr 0 → (0): (*, b, c)
Ptr 1 → (1): (+, a, (0))
```

## How to Run
```bash
python quad_triple.py
```

## Sample Output
```
Expression : a + b * c

QUADRUPLES
#    Op    Arg1      Arg2      Result
──────────────────────────────────────
0    *     b         c         t1
1    +     a         t1        t2

TRIPLES
#    Op    Arg1        Arg2
──────────────────────────────
0    *     b           c
1    +     a           (0)
```
