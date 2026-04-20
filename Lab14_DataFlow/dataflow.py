"""
Lab 14 - Global Data Flow Analysis
Computes: GEN, KILL, IN, OUT sets for Reaching Definitions
"""

def build_definition_tables(blocks):
    """Assign unique global definition ids and map vars to all their def ids."""
    block_defs = {}
    defs_by_var = {}
    did = 1

    for name, stmts in blocks:
        ids = []
        for var, _ in stmts:
            def_id = f"d{did}"
            did += 1
            ids.append((var, def_id))
            defs_by_var.setdefault(var, set()).add(def_id)
        block_defs[name] = ids

    return block_defs, defs_by_var, did - 1


def parse_block(block_def_entries, defs_by_var):
    """
    block_def_entries: list of (var, def_id) in statement order for one block.
    Returns GEN and KILL sets for the block.
    """
    gen = set()
    seen = set()

    # GEN: only the last definition of each variable in the block reaches OUT directly.
    for var, def_id in reversed(block_def_entries):
        if var not in seen:
            gen.add(def_id)
            seen.add(var)

    # KILL: all other definitions of variables that are defined in this block.
    kill_set = set()
    for var in seen:
        kill_set |= defs_by_var[var]
    kill_set -= gen

    return gen, kill_set

def reaching_definitions(blocks, edges, all_defs_count=None):
    """
    blocks : list of (name, stmts)
    edges  : list of (from_name, to_name)
    Iterative data-flow: IN[B] = ∪ OUT[pred(B)], OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])
    """
    block_names = [b[0] for b in blocks]
    block_defs, defs_by_var, total_defs = build_definition_tables(blocks)

    GEN, KILL, IN, OUT = {}, {}, {}, {}
    for name, stmts in blocks:
        GEN[name], KILL[name] = parse_block(block_defs[name], defs_by_var)
        IN[name]  = set()
        OUT[name] = set(GEN[name])

    # Build predecessor map
    preds = {n: [] for n in block_names}
    for src, dst in edges:
        preds[dst].append(src)

    changed = True
    while changed:
        changed = False
        for name, _ in blocks:
            new_in = set()
            for p in preds[name]:
                new_in |= OUT[p]
            new_out = set(GEN[name]) | (new_in - set(KILL[name]))
            if new_in != IN[name] or new_out != OUT[name]:
                IN[name], OUT[name] = new_in, new_out
                changed = True

    return GEN, KILL, IN, OUT, total_defs

def display(blocks, GEN, KILL, IN, OUT):
    print(f"\n  {'Block':<8}{'GEN':<20}{'KILL':<20}{'IN':<25}{'OUT'}")
    print("  " + "-" * 85)
    for name, _ in blocks:
        g  = "{" + ",".join(sorted(GEN[name]))  + "}"
        k  = "{" + ",".join(sorted(KILL[name])) + "}"
        i  = "{" + ",".join(sorted(IN[name]))   + "}"
        o  = "{" + ",".join(sorted(OUT[name]))  + "}"
        print(f"  {name:<8}{g:<20}{k:<20}{i:<25}{o}")

if __name__ == "__main__":
    # Classic textbook example:
    # B1: d1: a=3, d2: b=5, d3: c=1
    # B2: d4: c=c+1, d5: b=b+c   (loop body)
    # B3: d6: a=b+c               (exit)
    # Edges: B1->B2, B2->B2 (loop), B2->B3

    blocks = [
        ('B1', [('a', []), ('b', []), ('c', [])]),
        ('B2', [('c', ['c']), ('b', ['b','c'])]),
        ('B3', [('a', ['b','c'])]),
    ]
    edges = [('B1','B2'), ('B2','B2'), ('B2','B3')]

    print("=" * 55)
    print("  Reaching Definitions Analysis")
    print("  Blocks: B1 -> B2 (loop) -> B3")
    print("  d1:a=3  d2:b=5  d3:c=1  d4:c=?  d5:b=?  d6:a=?")
    print("=" * 55)

    G, K, I, O, total_defs = reaching_definitions(blocks, edges)
    display(blocks, G, K, I, O)

    print(f"\n  Total definitions discovered: {total_defs}")

    print("\n  Interpretation:")
    print("  IN[B]  = definitions that REACH the start of block B")
    print("  OUT[B] = definitions that REACH the end of block B")
