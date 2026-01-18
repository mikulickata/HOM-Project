import time, random, copy
from .utils import relocate_move, swap_move, two_opt_move
from .evaluator import check_constraints_and_fitness

def vns_solve(instance, initial, time_limit, k_max, full_set=False):
    best_routes = initial
    _, best_f, best_d, best_det = check_constraints_and_fitness(best_routes, instance)
    start_time = time.time()
    
    while (time.time() - start_time) < time_limit:
        k = 1
        while k <= k_max:
            if not full_set:
                # Basic: Samo Relocate i Swap
                cand = relocate_move(best_routes) if k % 2 == 0 else swap_move(best_routes)
            else:
                # Full: Relocate, Swap, 2-opt
                op = random.choice([relocate_move, swap_move, two_opt_move])
                cand = op(best_routes)

            v, f, d, det = check_constraints_and_fitness(cand, instance)
            if v and f < best_f:
                best_routes, best_f, best_d, best_det = cand, f, d, det
                k = 1
            else:
                k += 1
            if (time.time() - start_time) >= time_limit: break
    return best_routes, best_d, best_det, 0