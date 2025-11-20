# PetersonCheker
from collections import defaultdict, deque

# Estados de los procesos
TRYP, WAITP, CSP = 'tryp', 'waitp', 'csp'
TRYQ, WAITQ, CSQ = 'tryq', 'waitq', 'csq'

# Estados iniciales
initial_state = (TRYP, TRYQ, False, False, 1)

# Construcción del espacio de estados
def enabled_transitions(state):
    pc_p, pc_q, wantp, wantq, turn = state
    transitions = []

    # Transiciones del proceso P
    if pc_p == TRYP:
        # tryp -> waitp: wantp = True; turn = 1
        transitions.append((WAITP, pc_q, True, wantq, 1))
    elif pc_p == WAITP:
        # waitp: espera (!wantq or turn == 2)
        if (not wantq) or (turn == 2):
            transitions.append((CSP, pc_q, wantp, wantq, turn))
    elif pc_p == CSP:
        # csp -> tryp: wantp = False
        transitions.append((TRYP, pc_q, False, wantq, turn))

    # Transiciones del proceso Q
    if pc_q == TRYQ:
        transitions.append((pc_p, WAITQ, wantp, True, 2))
    elif pc_q == WAITQ:
        if (not wantp) or (turn == 1):
            transitions.append((pc_p, CSQ, wantp, wantq, turn))
    elif pc_q == CSQ:
        transitions.append((pc_p, TRYP, wantp, False, turn))

    return transitions

# Verificación de Seguridad (Safety) 
def build_state_space():
    visited = set()
    graph = defaultdict(list)
    queue = deque([initial_state])
    visited.add(initial_state)

    # Construcción del grafo de estados
    while queue:
        state = queue.popleft()
        for next_state in enabled_transitions(state):
            graph[state].append(next_state)
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    return graph, visited

# Verificación de Exclusión Mutua (Mutual Exclusion)
def check_mutual_exclusion(state_space):
    for s in state_space:
        pc_p, pc_q, _, _, _ = s
        if pc_p == CSP and pc_q == CSQ:
            print("Violación de exclusión mutua en estado:", s)
            return False
    print("Exclusión mutua verificada.")
    return True

# Verificación de Vivacidad (Liveness) 
# Buscamos un ciclo alcanzable desde waitp donde csp nunca se cumple → violación
def dfs_for_liveness_violation(graph, start_states, bad_condition):
    
   # Busca un ciclo alcanzable desde start_states donde bad_condition es siempre cierta. 
    def dfs(u, stack_set, stack, visited_global):
        visited_global.add(u)
        stack.append(u)
        stack_set.add(u)

        for v in graph[u]:
            if not bad_condition(v):
                continue  # Solo seguimos si la condición mala se mantiene
            if v not in visited_global:
                if dfs(v, stack_set, stack, visited_global):
                    return True
            elif v in stack_set:
                # Ciclo encontrado dentro de la condición mala
                print("Ciclo de no-progreso detectado:", stack[stack.index(v):] + [v])
                return True

        stack.pop()
        stack_set.remove(u)
        return False

    visited_global = set()
    for s in start_states:
        if bad_condition(s):
            if dfs(s, set(), [], visited_global):
                return True
    return False

def check_liveness(graph, all_states):
    # waitp -> ◇csp  <=>  no existe ciclo con waitp ∧ □¬csp
    def in_waitp_and_never_csp(s):
        pc_p, _, _, _, _ = s
        return pc_p == WAITP  # y nunca llega a csp → lo manejamos en DFS

    def always_not_in_csp(s):
        pc_p, _, _, _, _ = s
        return pc_p != CSP

    # Estados con waitp que nunca alcanzan csp están en un ciclo sin csp
    waitp_states = [s for s in all_states if s[0] == WAITP]
    if dfs_for_liveness_violation(graph, waitp_states, always_not_in_csp):
        print("Vivacidad violada para proceso P.")
        return False

    waitq_states = [s for s in all_states if s[1] == WAITQ]
    def always_not_in_csq(s):
        _, pc_q, _, _, _ = s
        return pc_q != CSQ
    if dfs_for_liveness_violation(graph, waitq_states, always_not_in_csq):
        print("Vivacidad violada para proceso Q.")
        return False

    print("Vivacidad verificada (bajo suposición de fairness implícita en la búsqueda).")
    return True

# # Ejecución
if __name__ == "__main__":
    print("Construyendo espacio de estados del algoritmo de Peterson...")
    graph, states = build_state_space()
    print(f"{len(states)} estados alcanzables generados.")

    print("\n[1/2] Verificando exclusión mutua...")
    safe = check_mutual_exclusion(states)

    print("\n[2/2] Verificando vivacidad...")
    live = check_liveness(graph, states)

    if safe and live:
        print("\n ¡El algoritmo de Peterson es correcto!")
    else:
        print("\n ¡El algoritmo de Peterson tiene errores!")
