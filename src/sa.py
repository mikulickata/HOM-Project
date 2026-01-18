import time
import random
import math
from .utils import shaking
from .evaluator import check_constraints_and_fitness

def sa_solve(instance, initial_routes, time_limit, T_init, alpha_param):
    current_routes = initial_routes
    _, curr_f, curr_d, curr_det = check_constraints_and_fitness(current_routes, instance)
    
    best_routes = current_routes
    best_f = curr_f
    best_dist = curr_d
    best_detailed = curr_det
    
    T = T_init
    T_min = 0.05
    alpha = alpha_param 
    
    start_time = time.time()
    eval_count = 1

    while (time.time() - start_time) < time_limit and T > T_min:
        # Shaking s k=1 je zapravo standardni Move operator za SA
        candidate = shaking(current_routes, 1)
        is_valid, f_cand, d_cand, det_cand = check_constraints_and_fitness(candidate, instance)
        eval_count += 1
        
        if is_valid:
            delta = f_cand - curr_f
            if delta < 0 or random.random() < math.exp(-delta / T):
                current_routes = candidate
                curr_f = f_cand
                
                if f_cand < best_f:
                    best_routes = candidate
                    best_f = f_cand
                    best_dist = d_cand
                    best_detailed = det_cand
        
        T *= alpha
        # Mehanizam ponovnog zagrijavanja (re-heating) ako zapne prerano
        if T <= T_min and (time.time() - start_time) < (time_limit * 0.8):
            T = T_init * 0.1 
            
    return best_routes, best_dist, best_detailed, eval_count