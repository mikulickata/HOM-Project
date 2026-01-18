import time
from .utils import shaking, local_search_2opt
from .evaluator import check_constraints_and_fitness

def vns_solve(instance, initial_routes, time_limit, k_max_param):
    best_routes = initial_routes
    valid, best_f, best_dist, best_detailed = check_constraints_and_fitness(best_routes, instance)
    
    start_time = time.time()
    eval_count = 1
    k_max = k_max_param 

    while (time.time() - start_time) < time_limit:
        k = 1
        while k <= k_max and (time.time() - start_time) < time_limit:
            candidate = shaking(best_routes, k)
            
            # Local search vraća najbolju verziju rute i fitness
            candidate, f_ls = local_search_2opt(candidate, instance, best_f)
            
            is_valid, f_cand, d_cand, det_cand = check_constraints_and_fitness(candidate, instance)
            eval_count += 10 # 2-opt radi mnogo internih evaluacija
            
            if is_valid and f_cand < best_f:
                best_routes = candidate
                best_f = f_cand
                best_dist = d_cand
                best_detailed = det_cand
                k = 1 # Resetiramo k jer smo našli poboljšanje
            else:
                k += 1
                
    return best_routes, best_dist, best_detailed, eval_count