# Compiler Design Lab

<div align="center">

**A complete implementation of core Compiler Design concepts in Python.**

*Covering all phases from Lexical Analysis to Advanced Parsing techniques.*

[![Python Version](https://img.shields.io/badge/Language-Python_3-blue.svg?logo=python&logoColor=white)](https://github.com/ShivamKSah/ShivamKSah-Compiler-Design-Lab)
[![Maintained](https://img.shields.io/badge/Maintained%3F-Yes-green.svg)](https://github.com/ShivamKSah/ShivamKSah-Compiler-Design-Lab/commits/master)
![Course](https://img.shields.io/badge/Course-Compiler_Design-orange.svg)

</div>

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [Lab 1 - Lexical Analyzer](#lab-1--lexical-analyzer)
- [Lab 2 - Regular Expression to NFA](#lab-2--regular-expression-to-nfa)
- [Lab 3 - NFA to DFA](#lab-3--nfa-to-dfa)
- [Lab 4 - Elimination of Ambiguity, Left Recursion and Left Factoring](#lab-4--elimination-of-ambiguity-left-recursion-and-left-factoring)
- [Lab 5 - FIRST and FOLLOW Sets](#lab-5--first-and-follow-sets)
- [Lab 6 - Predictive Parsing Table LL1](#lab-6--predictive-parsing-table-ll1)
- [Lab 7 - Shift Reduce Parsing SLR1](#lab-7--shift-reduce-parsing-slr1)
- [Lab 8 - LEADING and TRAILING Sets](#lab-8--leading-and-trailing-sets)
- [How to Run Any Lab](#how-to-run-any-lab)
- [Overall Compiler Flow](#overall-compiler-flow)

---

## Repository Structure

```text
COMPILER-DESIGN-LAB/
+-- Lab 1 Lexical analyzer/
|   +-- lexical.py
|   +-- Readme.md
+-- Lab 2 conversion from Regular Expression to NFA/
|   +-- Re_to_nfa.py
|   +-- Readme.md
+-- Lab 3 Conversion from NFA to DFA/
|   +-- Nfa_dfa.py
|   +-- Readme.md
+-- Lab 4 Elimation of Ambiguity, Left Recursion and Left Factoring/
|   +-- Lftrecursion.py
|   +-- Readme.md
+-- Lab 5 -FIRST AND FOLLOW computation/
|   +-- First-follow-func.py
|   +-- Readme.md
+-- Lab 6 Predictive Parsing Table/
|   +-- Parsetable.py
|   +-- Readme.md
+-- Lab 7 - Shift Reduce Parsing/
|   +-- Shiftreduce.py
|   +-- Readme.md
+-- Lab 8- Computation of LEADING AND TRAILING/
|   +-- lead&trailing.py
|   +-- Readme.md
+-- README.md
```

---

## Lab 1 - Lexical Analyzer

**File:** `lexical.py` | **Status:** Completed

The first phase of a compiler. It reads raw source code character by character and groups them into **tokens** (the smallest meaningful units). The implementation uses Python's `re` module to build a master regex from individual token patterns, then scans the input string in a single pass.

**What it recognizes:** Keywords, Identifiers, Integers, Floats, Operators, Delimiters, Strings, and Unknown tokens.

```mermaid
flowchart TD
    A[Raw Source Code] --> B[Compile Master Regex Pattern]
    B --> C[Run finditer over Source Code]
    C --> D{Match Found?}
    D -- Yes --> E{Token Type?}
    E -- WHITESPACE --> F[Skip / Ignore]
    F --> C
    E -- KEYWORD / IDENTIFIER / INTEGER / FLOAT / OPERATOR / DELIMITER / STRING --> G[Append Token Type + Value to Token List]
    G --> C
    E -- UNKNOWN --> H[Flag Unknown Token and Append]
    H --> C
    D -- No --> I[Return Final Token List]
    I --> J[Display Tokens in Table Format]
```

**Example:**

```
Input:  int x = 10 + y;
Output: KEYWORD(int)  IDENTIFIER(x)  OPERATOR(=)  INTEGER(10)  OPERATOR(+)  IDENTIFIER(y)  DELIMITER(;)
```

---

## Lab 2 - Regular Expression to NFA

**File:** `Re_to_nfa.py` | **Status:** Completed

Converts a Regular Expression into a **Non-deterministic Finite Automaton (NFA)** using **Thompson's Construction Algorithm**. The regex is first preprocessed to insert explicit concatenation operators, then parsed using a recursive descent parser that builds the NFA bottom-up.

**Supports:** Literals, Concatenation (`.`), Union (`|`), Kleene Star (`*`), One-or-More (`+`), Optional (`?`), and Parentheses.

```mermaid
flowchart TD
    A[Input Regular Expression] --> B[Insert Explicit Concat Operators]
    B --> C[Initialize Recursive Descent Parser]
    C --> D[Parse: expr]
    D --> E[Parse: term]
    E --> F[Parse: factor]
    F --> G[Parse: base]
    G --> H{Current Token?}
    H -- "(" --> I[Consume and Parse Sub-Expression]
    I --> J[Consume Closing Paren]
    H -- Literal Symbol --> K[Create Basic NFA: start --symbol--> accept]
    J --> L{Postfix Operator?}
    K --> L
    L -- "*" --> M[Apply Kleene Star: Add epsilon loops]
    L -- "+" --> N[Apply Plus: Must match once then loop]
    L -- "?" --> O[Apply Optional: Union with epsilon NFA]
    L -- None --> P[Return NFA Fragment]
    M --> P
    N --> P
    O --> P
    P --> Q{More factors to concat?}
    Q -- Yes --> R[Merge: nfa1.accept --epsilon--> nfa2.start]
    R --> F
    Q -- No --> S{More terms to union?}
    S -- Yes --> T[Create new start/accept with epsilon branches]
    T --> E
    S -- No --> U[Final NFA Constructed]
    U --> V[Display: Start, Accept, All Transitions]
```

**Example:**

```
Regex: (a|b)*
NFA: q0 --epsilon--> q1 (branch a), q2 (branch b)
     q1 --a--> q3, q2 --b--> q4
     q3,q4 --epsilon--> accept, accept --epsilon--> q0 (loop)
```

---

## Lab 3 - NFA to DFA

**File:** `Nfa_dfa.py` | **Status:** Completed

Converts an NFA to an equivalent **Deterministic Finite Automaton (DFA)** using the **Subset Construction (Powerset) Algorithm**. Each DFA state corresponds to a set of NFA states. The resulting DFA is then used to simulate input string acceptance.

```mermaid
flowchart TD
    A[Input NFA: states, alphabet, transitions, start, accept] --> B["Compute epsilon-closure of start state"]
    B --> C["DFA Start State = epsilon-closure set"]
    C --> D["Add to Unprocessed Queue"]
    D --> E{Queue Empty?}
    E -- No --> F["Pop current DFA state (set of NFA states)"]
    F --> G["For each symbol in alphabet"]
    G --> H["Compute MOVE: all NFA states reachable on symbol"]
    H --> I["Compute epsilon-closure of MOVE result"]
    I --> J{New DFA State?}
    J -- Yes --> K["Add new state to DFA states + Queue"]
    K --> L{Overlaps NFA accept states?}
    L -- Yes --> M[Mark as DFA Accept State]
    L -- No --> N[Continue]
    J -- No --> N
    M --> N
    N --> O["Record DFA transition: current --symbol--> new state"]
    O --> G
    G -- All symbols done --> E
    E -- Yes --> P[DFA Construction Complete]
    P --> Q[Display DFA Transition Table]
    Q --> R["Simulate DFA on Input Strings"]
    R --> S{For each input symbol}
    S --> T["Follow DFA transition from current state"]
    T --> U{Dead State?}
    U -- Yes --> V["REJECTED"]
    U -- No --> S
    S -- Input exhausted --> W{Current state is accept?}
    W -- Yes --> X["ACCEPTED"]
    W -- No --> V
```

**Example:**

```
NFA for (a|b)*abb:
  DFA State {q0,q1,q3} on input 'a' --> DFA state {q1,q2}
  Input "abb" --> ACCEPTED
  Input "ab"  --> REJECTED
```

---

## Lab 4 - Elimination of Ambiguity, Left Recursion and Left Factoring

**File:** `Lftrecursion.py` | **Status:** Completed

Prepares a Context-Free Grammar (CFG) for predictive parsing by applying three essential grammar transformations. Each transformation addresses a different problem that prevents deterministic top-down parsing.

### Part 1: Left Recursion Elimination

```mermaid
flowchart TD
    A["Input Grammar: A -> A alpha1 | A alpha2 | beta1 | beta2"] --> B["Separate productions into two groups"]
    B --> C["Alpha group: Productions starting with A (left-recursive)"]
    B --> D["Beta group: Productions NOT starting with A"]
    C --> E{Alpha group empty?}
    E -- Yes --> F["No left recursion - keep original"]
    E -- No --> G["Create new non-terminal A-prime"]
    G --> H["A  -> beta1 A-prime | beta2 A-prime"]
    G --> I["A-prime -> alpha1 A-prime | alpha2 A-prime | epsilon"]
    H --> J[Output Transformed Grammar]
    I --> J
```

### Part 2: Left Factoring

```mermaid
flowchart TD
    A["Input Productions for A: A -> alpha beta1 | alpha beta2 | gamma"] --> B["Group productions by first symbol"]
    B --> C{Any group with more than 1 production?}
    C -- Yes --> D["Find Longest Common Prefix in group"]
    D --> E["Create new non-terminal A-prime"]
    E --> F["A -> prefix A-prime"]
    E --> G["A-prime -> suffix1 | suffix2 | epsilon"]
    F --> H[Output Factored Grammar]
    G --> H
    C -- No --> I["No factoring needed - keep original"]
```

### Part 3: Ambiguity

The program demonstrates two classic examples of ambiguous grammars (Dangling-Else and Expression Grammar) and shows the unambiguous restructured versions with enforced precedence and associativity.

---

## Lab 5 - FIRST and FOLLOW Sets

**File:** `First-follow-func.py` | **Status:** Completed

Computes **FIRST** and **FOLLOW** sets for all non-terminals in a grammar using iterative fixed-point algorithms. These sets are essential for constructing LL(1) parsing tables.

### FIRST Set Computation

```mermaid
flowchart TD
    A["Initialize FIRST sets as empty for all non-terminals"] --> B["Set changed = true"]
    B --> C{changed?}
    C -- Yes --> D["Set changed = false"]
    D --> E["For each production A -> X1 X2 ... Xn"]
    E --> F{X1 is terminal?}
    F -- Yes --> G["Add X1 to FIRST of A"]
    F -- No --> H["Add FIRST of X1 minus epsilon to FIRST of A"]
    H --> I{epsilon in FIRST of X1?}
    I -- Yes --> J["Move to X2, repeat check"]
    I -- No --> K[Stop for this production]
    J --> L{All Xi derive epsilon?}
    L -- Yes --> M["Add epsilon to FIRST of A"]
    L -- No --> K
    G --> N{FIRST set changed?}
    K --> N
    M --> N
    N -- Yes --> O["Set changed = true"]
    N -- No --> E
    E -- All productions done --> C
    C -- No --> P["Return Final FIRST Sets"]
```

### FOLLOW Set Computation

```mermaid
flowchart TD
    A["Initialize FOLLOW sets as empty"] --> B["Add $ to FOLLOW of Start Symbol"]
    B --> C["Set changed = true"]
    C --> D{changed?}
    D -- Yes --> E["Set changed = false"]
    E --> F["For each production A -> alpha B beta"]
    F --> G["Add FIRST of beta minus epsilon to FOLLOW of B"]
    G --> H{epsilon in FIRST of beta OR beta is empty?}
    H -- Yes --> I["Add FOLLOW of A to FOLLOW of B"]
    H -- No --> J[Continue]
    I --> K{FOLLOW set changed?}
    J --> K
    K -- Yes --> L["Set changed = true"]
    K -- No --> F
    F -- All productions done --> D
    D -- No --> M["Return Final FOLLOW Sets"]
```

**Example Output:**

```
Non-Terminal    FIRST                  FOLLOW
E               { (, id }              { $, ) }
E'              { +, epsilon }         { $, ) }
T               { (, id }              { $, ), + }
```

---

## Lab 6 - Predictive Parsing Table (LL1)

**File:** `Parsetable.py` | **Status:** Completed

Constructs the **LL(1) Predictive Parsing Table** from FIRST and FOLLOW sets, then simulates stack-based top-down parsing with a step-by-step trace.

### Table Construction

```mermaid
flowchart TD
    A["Input Grammar"] --> B["Compute FIRST Sets"]
    B --> C["Compute FOLLOW Sets"]
    C --> D["Initialize Empty Parsing Table"]
    D --> E["For each production A -> alpha"]
    E --> F["Compute FIRST of alpha"]
    F --> G["For each terminal a in FIRST of alpha"]
    G --> H["Set Table at M A a = A -> alpha"]
    F --> I{epsilon in FIRST of alpha?}
    I -- Yes --> J["For each terminal b in FOLLOW of A"]
    J --> K["Set Table at M A b = A -> alpha"]
    I -- No --> L[Continue]
    K --> M{Entry already exists?}
    H --> M
    M -- Yes --> N["Report Conflict: Grammar is NOT LL1"]
    M -- No --> L
    L --> E
    E -- Done --> O["Return Parsing Table"]
```

### Stack-Based LL(1) Parsing Simulation

```mermaid
flowchart TD
    A["Input: Token Stream + Parsing Table"] --> B["Initialize Stack with $ and Start Symbol"]
    B --> C["Set input pointer to first token"]
    C --> D{Stack Top == $ AND Current Token == $?}
    D -- Yes --> E["ACCEPT - Parsing Successful"]
    D -- No --> F{Stack Top is terminal?}
    F -- Yes --> G{Top matches Current Token?}
    G -- Yes --> H["Pop stack, advance input pointer"]
    G -- No --> I["ERROR: Terminal mismatch"]
    F -- No --> J["Lookup Table at M Top Current-Token"]
    J --> K{Entry exists?}
    K -- Yes --> L["Pop Top from stack"]
    L --> M["Push production body in reverse order"]
    M --> N["Print step: Stack | Input | Action"]
    K -- No --> O["ERROR: No table entry"]
    H --> N
    N --> D
```

**Example Parsing Trace:**

```
STACK                       INPUT                ACTION
$ E' T E                    id + id * id $       E -> T E'
$ E' T' F T                 id + id * id $       T -> F T'
$ E' T' id F                id + id * id $       F -> id
...                                              ACCEPT
```

---

## Lab 7 - Shift Reduce Parsing (SLR1)

**File:** `Shiftreduce.py` | **Status:** Completed

Implements a full **SLR(1) Bottom-Up parser**. It augments the grammar, builds the LR(0) canonical collection of item sets, constructs the ACTION/GOTO tables using FOLLOW sets, and simulates shift-reduce parsing.

### LR(0) Automaton Construction

```mermaid
flowchart TD
    A["Augment Grammar: Add S-prime -> S"] --> B["Create Initial Item: S-prime -> dot S"]
    B --> C["Compute Closure of Initial Item Set"]
    C --> D["Add to States and Queue"]
    D --> E{Queue Empty?}
    E -- No --> F["Pop State from Queue"]
    F --> G["For each grammar symbol X"]
    G --> H["Compute GOTO: advance dot past X in all items"]
    H --> I["Compute Closure of resulting set"]
    I --> J{Result is non-empty?}
    J -- Yes --> K{New state?}
    K -- Yes --> L["Add to States and Queue"]
    K -- No --> M["Record Transition: State --X--> Existing State"]
    L --> M
    J -- No --> G
    M --> G
    G -- All symbols done --> E
    E -- Yes --> N["LR0 Automaton Complete"]
```

### SLR(1) Table Construction and Parsing

```mermaid
flowchart TD
    A["LR0 Automaton + FOLLOW Sets"] --> B["For each state and each item in that state"]
    B --> C{Dot before terminal a?}
    C -- Yes --> D["ACTION state a = Shift to GOTO state"]
    C -- No --> E{Dot before non-terminal A?}
    E -- Yes --> F["GOTO state A = target state"]
    E -- No --> G{Item is S-prime -> S dot?}
    G -- Yes --> H["ACTION state $ = Accept"]
    G -- No --> I["Item A -> alpha dot is complete"]
    I --> J["For each terminal b in FOLLOW of A"]
    J --> K["ACTION state b = Reduce by A -> alpha"]
    D --> L{Conflict detected?}
    K --> L
    L -- Yes --> M["Report Shift-Reduce or Reduce-Reduce conflict"]
    L -- No --> N[Continue]
    N --> B
    B -- Done --> O["SLR Table Complete"]
    O --> P["Simulate Shift-Reduce Parsing"]
    P --> Q["Initialize Stack with State 0"]
    Q --> R{Look at ACTION for current state and lookahead}
    R -- Shift --> S["Push symbol and new state onto stack"]
    R -- Reduce --> T["Pop RHS symbols from stack"]
    T --> U["Look up GOTO for revealed state and LHS"]
    U --> V["Push LHS and GOTO state"]
    R -- Accept --> W["ACCEPT - Parsing Successful"]
    R -- Error --> X["ERROR - Reject Input"]
    S --> R
    V --> R
```

**Example Parsing Trace:**

```
STACK                   INPUT              ACTION
$ 0                     id + id $          Shift id -> state 5
$ 0 id 5                + id $             Reduce by F -> id
$ 0 F 3                 + id $             Reduce by T -> F
...                                        ACCEPT
```

---

## Lab 8 - LEADING and TRAILING Sets

**File:** `lead&trailing.py` | **Status:** Completed

Computes **LEADING** and **TRAILING** sets for Operator Grammars using iterative fixed-point algorithms, then derives **Operator Precedence Relations** between terminal symbols.

### LEADING and TRAILING Computation

```mermaid
flowchart TD
    A["Input Operator Grammar"] --> B["Initialize LEADING and TRAILING sets as empty"]
    B --> C["LEADING Computation: Scan each production LEFT to RIGHT"]
    C --> D{Current symbol is terminal?}
    D -- Yes --> E["Add terminal to LEADING of LHS, stop scanning"]
    D -- No --> F["Current symbol is non-terminal B"]
    F --> G["Add all of LEADING of B into LEADING of LHS"]
    G --> H{Next symbol is terminal a?}
    H -- Yes --> I["Add a to LEADING of LHS"]
    H -- No --> J{B can derive epsilon?}
    J -- Yes --> K["Continue scanning next symbol"]
    J -- No --> L["Stop scanning this production"]
    I --> L
    E --> M["Repeat until no changes - fixed point"]
    L --> M

    M --> N["TRAILING Computation: Scan each production RIGHT to LEFT"]
    N --> O{Current symbol is terminal?}
    O -- Yes --> P["Add terminal to TRAILING of LHS, stop scanning"]
    O -- No --> Q["Current symbol is non-terminal B"]
    Q --> R["Add all of TRAILING of B into TRAILING of LHS"]
    R --> S{Previous symbol is terminal a?}
    S -- Yes --> T["Add a to TRAILING of LHS"]
    S -- No --> U{B can derive epsilon?}
    U -- Yes --> V["Continue scanning previous symbol"]
    U -- No --> W["Stop scanning this production"]
    T --> W
    P --> X["Repeat until no changes - fixed point"]
    W --> X
```

### Operator Precedence Relations

```mermaid
flowchart TD
    A["LEADING and TRAILING Sets Computed"] --> B["Scan all productions for adjacent symbol pairs"]
    B --> C{"Pattern: terminal a followed by non-terminal B?"}
    C -- Yes --> D["For each b in LEADING of B: a yields-precedence b"]
    B --> E{"Pattern: non-terminal B followed by terminal b?"}
    E -- Yes --> F["For each a in TRAILING of B: a takes-precedence b"]
    B --> G{"Pattern: terminal a followed by terminal b?"}
    G -- Yes --> H["a equal-precedence b"]
    B --> I{"Pattern: terminal a, non-terminal B, terminal b?"}
    I -- Yes --> J["a equal-precedence b"]
    D --> K["Output: All Precedence Relations"]
    F --> K
    H --> K
    J --> K
```

**Example Output:**

```
Non-Terminal    LEADING              TRAILING
E               { (, +, *, id }      { ), +, *, id }
T               { (, *, id }         { ), *, id }
F               { (, id }            { ), id }

Operator a      Relation      Operator b
+               yields        (
*               takes         +
```

---

## How to Run Any Lab

These scripts are built in **pure Python 3** with **zero external dependencies**.

```bash
# 1. Clone the repository
git clone https://github.com/ShivamKSah/ShivamKSah-Compiler-Design-Lab.git
cd ShivamKSah-Compiler-Design-Lab

# 2. Run any lab directly
python "Lab 1 Lexical analyzer/lexical.py"
python "Lab 2 conversion from Regular Expression to NFA/Re_to_nfa.py"
python "Lab 3 Conversion from NFA to DFA/Nfa-dfa.py"
python "Lab 4 Elimation of Ambiguity, Left Recursion and Left Factoring/Lftrecursion.py"
python "Lab 5 -FIRST AND FOLLOW computation/First-follow-func.py"
python "Lab 6 Predictive Parsing Table/Parsetable.py"
python "Lab 7 - Shift Reduce Parsing/Shiftreduce.py"
python "Lab 8- Computation of LEADING AND TRAILING/lead&trailing.py"
```

**Requirements:** Python 3.6+

---

## Overall Compiler Flow

This repository maps directly to the stages of a modern compiler front-end:

```mermaid
graph LR
    subgraph "Lexical Analysis"
        A[Source Code] -->|Lab 1| B(Token Stream)
    end

    subgraph "Lexical Generator Pipeline"
        C[Regular Expression] -->|Lab 2| D[NFA]
        D -->|Lab 3| E[DFA]
        E -.->|Drives| B
    end

    subgraph "Syntax Analysis"
        B --> F{Grammar Prep}
        F -->|Lab 4| G[Clean CFG]
        G -->|Lab 5| H[FIRST and FOLLOW]
        H -->|Lab 6| I[LL1 Top-Down Parser]
        H -->|Lab 7| J[SLR1 Bottom-Up Parser]
        G -->|Lab 8| K[Operator Precedence Parser]
    end

    I --> L[Parse Tree]
    J --> L
    K --> L
```

---

<div align="center">

Built with love by **Shivam Kumar Sah** for Compiler Design

</div>
