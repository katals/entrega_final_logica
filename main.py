"""PetersonChecker: Verificación de algoritmo de exclusión mutua de Peterson (2 procesos)

Modela el protocolo clásico de Peterson y verifica:
  - Safety (exclusión mutua): nunca ambos procesos en sección crítica.
  - Liveness (progreso): no existe ciclo alcanzable donde un proceso queda para siempre en espera sin entrar a su sección crítica.

La verificación de liveness se implementa mediante detección de Componentes Fuertemente Conectados (SCC).
"""

from collections import defaultdict, deque

# Estados de los procesos
TRYP, WAITP, CSP = 'tryp', 'waitp', 'csp'
TRYQ, WAITQ, CSQ = 'tryq', 'waitq', 'csq'

# Estado inicial: ambos intentando, nadie quiere entrar aún, turno inicial favorece a P
initial_state = (TRYP, TRYQ, False, False, 1)  # (pc_p, pc_q, wantp, wantq, turn)

def enabled_transitions(state):
    """Genera transiciones activadas según código de Peterson correcto."""
    pc_p, pc_q, wantp, wantq, turn = state
    transitions = []

    # Proceso P
    if pc_p == TRYP:
        # intenta entrar: wantp=True; cede turno al otro (turn=2); pasa a waitp
        transitions.append((WAITP, pc_q, True, wantq, 2))
    elif pc_p == WAITP:
        # espera mientras wantq and turn == 2; puede avanzar si !wantq or turn == 1
        if (not wantq) or (turn == 1):
            transitions.append((CSP, pc_q, wantp, wantq, turn))
    elif pc_p == CSP:
        # sale de sección crítica: wantp=False; vuelve a tryp
        transitions.append((TRYP, pc_q, False, wantq, turn))

    # Proceso Q (simétrico)
    if pc_q == TRYQ:
        transitions.append((pc_p, WAITQ, wantp, True, 1))  # cede turno a P
    elif pc_q == WAITQ:
        if (not wantp) or (turn == 2):
            transitions.append((pc_p, CSQ, wantp, wantq, turn))
    elif pc_q == CSQ:
        transitions.append((pc_p, TRYQ, wantp, False, turn))

    return transitions

def build_state_space():
    """Explora el espacio de estados por BFS devolviendo grafo y conjunto de estados."""
    visited = set([initial_state])
    graph = defaultdict(list)
    queue = deque([initial_state])
    while queue:
        state = queue.popleft()
        for nxt in enabled_transitions(state):
            graph[state].append(nxt)
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    return graph, visited

def check_mutual_exclusion(states):
    """Verifica que nunca ambos procesos estén simultáneamente en sección crítica."""
    for s in states:
        if s[0] == CSP and s[1] == CSQ:
            print("Violación de exclusión mutua en estado:", s)
            return False
    print("Exclusión mutua verificada.")
    return True

# ---------- SCC (Tarjan) ----------
def strongly_connected_components(graph):
    """Devuelve lista de componentes fuertemente conectados usando Tarjan."""
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlink = {}
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph[v]:
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        # raíz de SCC
        if lowlink[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    for v in list(graph.keys()):  # asegurar iterar sobre todos nodos con aristas salientes
        if v not in indices:
            strongconnect(v)
    # incluir estados aislados sin aristas salientes
    for v in graph.keys():
        pass  # ya cubiertos; estados sin salida están en su propio SCC al visitar
    return sccs

def check_liveness(graph, states):
    """Verifica progreso: no existe SCC alcanzable que contenga WAIT perpetuo sin CS."""
    # Aseguramos que todos estados aparezcan como clave
    for s in states:
        graph.setdefault(s, [])
    sccs = strongly_connected_components(graph)

    violated_p = None
    violated_q = None
    for comp in sccs:
        # Condición de violación para P: algún WAITP y ningún CSP en el componente
        if any(st[0] == WAITP for st in comp) and all(st[0] != CSP for st in comp):
            # Además requiere que tenga al menos una arista cíclica (size>1 o self-loop)
            if len(comp) > 1 or any(st in graph[st] for st in comp):
                violated_p = comp
        # Condición de violación para Q
        if any(st[1] == WAITQ for st in comp) and all(st[1] != CSQ for st in comp):
            if len(comp) > 1 or any(st in graph[st] for st in comp):
                violated_q = comp

    if violated_p:
        print("Vivacidad violada para proceso P. SCC sin progreso:")
        for st in violated_p:
            print("  ", st)
        return False
    if violated_q:
        print("Vivacidad violada para proceso Q. SCC sin progreso:")
        for st in violated_q:
            print("  ", st)
        return False
    print("Vivacidad verificada (no hay SCC de espera perpetua).")
    return True

if __name__ == "__main__":
    print("Construyendo espacio de estados del algoritmo de Peterson...")
    graph, states = build_state_space()
    print(f"{len(states)} estados alcanzables generados.")

    print("\n[1/2] Verificando exclusión mutua...")
    safe = check_mutual_exclusion(states)

    print("\n[2/2] Verificando vivacidad...")
    live = check_liveness(graph, states)

    if safe and live:
        print("\n¡El algoritmo de Peterson es correcto!")
    else:
        print("\nSe detectaron violaciones de propiedades.")
