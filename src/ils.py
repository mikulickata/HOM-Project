import time, copy, random
from .utils import local_search_hill_climb, swap_move
from .evaluator import check_constraints_and_fitness

def ils_solve(instance, initial, time_limit, n_perturbations):
    curr_routes = initial
    _, curr_f, curr_d, curr_det = check_constraints_and_fitness(curr_routes, instance)
    best_routes, best_f, best_d, best_det = curr_routes, curr_f, curr_d, curr_det
    start_time = time.time()

    while (time.time() - start_time) < time_limit:
        # 1. Perturbacija: n_perturbations određuje jačinu "potresa"
        perturbed = copy.deepcopy(curr_routes)
        for _ in range(n_perturbations): 
            perturbed = swap_move(perturbed)
        
        # 2. Local Search (Hill Climb)
        refined, refined_f = local_search_hill_climb(perturbed, instance, 1e18)
        
        v, f, d, det = check_constraints_and_fitness(refined, instance)
        if v and f < best_f:
            best_routes, best_f, best_d, best_det = refined, f, d, det
            curr_routes = refined
        
    return best_routes, best_d, best_det, 0