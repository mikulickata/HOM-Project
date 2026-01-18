import random, copy, time
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

def local_search_hill_climb(routes, instance, current_f, start_time=None, time_limit=None):
    best_r, best_f = routes, current_f
    operators = [relocate_move, swap_move, two_opt_move, or_opt_move]
    
    # Ako nemamo start_time, stavit ćemo nešto da ne pukne, ali u GA proslijedi prave vrijednosti
    if start_time is None: start_time = time.time()
    if time_limit is None: time_limit = 1e9 

    for _ in range(1000): 
        # Ključni dodatak: prekid ako vrijeme isteče
        if (time.time() - start_time) > time_limit:
            break
            
        op = random.choice(operators)
        cand = op(best_r)
        v, f, d, det = check_constraints_and_fitness(cand, instance)
        if f < best_f:
            best_r, best_f = cand, f
            
    return best_r, best_f