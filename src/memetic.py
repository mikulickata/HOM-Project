import time, random, copy
from .evaluator import check_constraints_and_fitness
from .utils import local_search_hill_climb

def broken_pairs_dist(r1, r2):
    def get_edges(routes):
        edges = set()
        for r in routes:
            prev = 0
            for c in r:
                edges.add((prev, c))
                prev = c
            edges.add((prev, 0))
        return edges
    e1, e2 = get_edges(r1), get_edges(r2)
    return len(e1 - e2)

def memetic_solve(instance, initial, time_limit, ls_intensity):
    pop = [initial]
    # Inicijalizacija male populacije bazirane na inicijalnom rješenju
    for _ in range(9):
        pop.append(initial)
    
    best_r = initial
    _, best_f, best_d, best_det = check_constraints_and_fitness(initial, instance)
    start_time = time.time()
    
    while (time.time() - start_time) < time_limit:
        p1, p2 = random.sample(pop, 2)
        # Crossover: uzmi pola ruta od jednog, pola od drugog
        child = copy.deepcopy(p1[:len(p1)//2] + p2[len(p2)//2:])
        
        # Popravak duplikata/nedostajućih kupaca
        all_c = set(c.id for c in instance.customers)
        child_c = [c for r in child for c in r]
        missing = list(all_c - set(child_c))
        # (Pojednostavljeno: samo dodajemo nedostajuće kao nove rute)
        if missing: child.append(missing)
        
        # Edukacija djeteta: ls_intensity određuje broj ciklusa poliranja
        curr_child = child
        for _ in range(ls_intensity):
            v, f, _, _ = check_constraints_and_fitness(curr_child, instance)
            curr_child, _ = local_search_hill_climb(curr_child, instance, f)
        
        v, f, d, det = check_constraints_and_fitness(curr_child, instance)
        if v:
            if f < best_f:
                best_f, best_d, best_det, best_r = f, d, det, curr_child
            # Zamijeni najlošijeg ili nasumičnog
            pop[random.randint(0, len(pop)-1)] = curr_child
            
    return best_r, best_d, best_det, 0