import time, random, math
from .utils import relocate_move
from .evaluator import check_constraints_and_fitness
from .vns import vns_solve

def sa_solve(instance, initial, time_limit, T_init, alpha_param, hybrid=False):
    curr_r = initial
    _, curr_f, curr_d, curr_det = check_constraints_and_fitness(curr_r, instance)
    best_r, best_f, best_d, best_det = curr_r, curr_f, curr_d, curr_det
    
    T = T_init
    start_time = time.time()

    while (time.time() - start_time) < time_limit:
        if hybrid:
            # Hibrid koristi kratki VNS za istraživanje
            cand, _, _, _ = vns_solve(instance, curr_r, time_limit=0.5, k_max=5, full_set=False)
        else:
            cand = relocate_move(curr_r)
        
        v, f, d, det = check_constraints_and_fitness(cand, instance)
        if v:
            delta = f - curr_f
            if delta < 0 or random.random() < math.exp(-delta / T):
                curr_r, curr_f = cand, f
                if f < best_f:
                    best_r, best_f, best_d, best_det = cand, f, d, det
        
        T *= alpha_param
        if T < 0.1: T = T_init # Reheating
        
    return best_r, best_d, best_det, 0