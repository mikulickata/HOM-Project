import time
from .utils import relocate_move, swap_move, two_opt_move
from .evaluator import check_constraints_and_fitness

def vnd_solve(instance, initial, time_limit):
    curr_r = initial
    _, best_f, best_d, best_det = check_constraints_and_fitness(curr_r, instance)
    start_time = time.time()
    
    ops = [relocate_move, swap_move, two_opt_move]
    
    while (time.time() - start_time) < time_limit:
        i = 0
        improved = False
        while i < len(ops):
            cand = ops[i](curr_r)
            v, f, d, det = check_constraints_and_fitness(cand, instance)
            if v and f < best_f:
                curr_r, best_f, best_d, best_det = cand, f, d, det
                i = 0 # Reset na prvo susjedstvo
                improved = True
            else:
                i += 1
        if not improved: 
            # break # Lokalni optimum za sva susjedstva
            curr_r = relocate_move(curr_r)
        
    return curr_r, best_d, best_det, 0