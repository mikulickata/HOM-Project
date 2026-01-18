import time, random, copy
from .utils import local_search_hill_climb, relocate_move
from .evaluator import check_constraints_and_fitness

def ga_solve(instance, initial, time_limit, population_size):
    population = [initial]
    # Inicijalizacija populacije s varijacijama
    for _ in range(population_size - 1):
        population.append(relocate_move(initial)) 

    _, best_f, best_d, best_det = check_constraints_and_fitness(initial, instance)
    best_routes = initial
    start_time = time.time()

    while (time.time() - start_time) < time_limit:
        parent = random.choice(population)
        child = copy.deepcopy(parent)
        
        # Mutacija + Edukacija (Memetički dio)
        child = relocate_move(child)
        child, _ = local_search_hill_climb(child, instance, 1e20)
        
        v, f, d, det = check_constraints_and_fitness(child, instance)
        if v:
            # Zamjena nasumičnog člana
            population[random.randint(0, population_size-1)] = child
            if f < best_f:
                best_routes, best_f, best_d, best_det = child, f, d, det
                
    return best_routes, best_d, best_det, 0