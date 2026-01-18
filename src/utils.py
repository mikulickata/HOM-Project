import random, copy
from .evaluator import check_constraints_and_fitness

def relocate_move(routes):
    new_routes = copy.deepcopy(routes)
    r1 = random.randrange(len(new_routes))
    if not new_routes[r1]: return routes
    cust = new_routes[r1].pop(random.randrange(len(new_routes[r1])))
    r2 = random.randrange(len(new_routes))
    new_routes[r2].insert(random.randint(0, len(new_routes[r2])), cust)
    return [r for r in new_routes if r]

def swap_move(routes):
    new_routes = copy.deepcopy(routes)
    if len(new_routes) < 2: return routes
    r1, r2 = random.sample(range(len(new_routes)), 2)
    if not new_routes[r1] or not new_routes[r2]: return routes
    idx1, idx2 = random.randrange(len(new_routes[r1])), random.randrange(len(new_routes[r2]))
    new_routes[r1][idx1], new_routes[r2][idx2] = new_routes[r2][idx2], new_routes[r1][idx1]
    return new_routes

def two_opt_move(routes):
    new_routes = copy.deepcopy(routes)
    r_idx = random.randrange(len(new_routes))
    if len(new_routes[r_idx]) < 2: return routes
    i, j = sorted(random.sample(range(len(new_routes[r_idx])), 2))
    new_routes[r_idx][i:j+1] = reversed(new_routes[r_idx][i:j+1])
    return new_routes

def or_opt_move(routes):
    new_routes = copy.deepcopy(routes)
    r_idx = random.randrange(len(new_routes))
    if len(new_routes[r_idx]) < 3: return routes
    # Uzmi segment od 2 kupca i pomakni ga unutar iste rute
    start = random.randint(0, len(new_routes[r_idx]) - 2)
    segment = [new_routes[r_idx].pop(start) for _ in range(2)]
    pos = random.randint(0, len(new_routes[r_idx]))
    for i, val in enumerate(segment):
        new_routes[r_idx].insert(pos + i, val)
    return new_routes

def local_search_hill_climb(routes, instance, current_f):
    best_r, best_f = routes, current_f
    improved = True
    
    # Umjesto 1000 nasumičnih, radimo dok god nalazimo poboljšanje (Greedy Descent)
    # Fokusiramo se na Relocate jer on najbolje smanjuje broj vozila
    while improved:
        improved = False
        
        # Pokušaj premjestiti svakog kupca na svako drugo mjesto
        for r1_idx in range(len(best_r)):
            for i in range(len(best_r[r1_idx])):
                cust = best_r[r1_idx][i]
                
                for r2_idx in range(len(best_r)):
                    for j in range(len(best_r[r2_idx]) + 1):
                        if r1_idx == r2_idx and (j == i or j == i + 1): continue
                        
                        # Napravi privremeni potez bez copy.deepcopy (radi brzine)
                        new_r = [list(r) for r in best_r]
                        new_r[r1_idx].pop(i)
                        new_r[r2_idx].insert(j, cust)
                        new_r = [r for r in new_r if r] # Ukloni prazne
                        
                        v, f, d, det = check_constraints_and_fitness(new_r, instance)
                        if f < best_f: # Dopušta i nevalidna s manjom kaznom (Strategic Oscillation)
                            best_r, best_f = new_r, f
                            improved = True
                            break
                    if improved: break
                if improved: break
    return best_r, best_f