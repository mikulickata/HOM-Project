import time, random, copy
from .evaluator import check_constraints_and_fitness

def alns_solve(instance, initial, time_limit, intensity):
    best_r = initial
    _, best_f, best_d, best_det = check_constraints_and_fitness(initial, instance)
    curr_r = initial
    
    operators = ["random", "worst"]
    weights = [1.0, 1.0]
    
    start_time = time.time()
    while (time.time() - start_time) < time_limit:
        op_idx = random.choices(range(len(operators)), weights=weights)[0]
        
        # RUIN faza - intensity određuje opseg razaranja
        all_c = [c for r in curr_r for c in r]
        num_to_remove = max(1, int(len(all_c) * intensity))
        
        removed = random.sample(all_c, num_to_remove)
            
        temp_r = [[c for c in r if c not in removed] for r in curr_r]
        temp_r = [r for r in temp_r if r]
        
        # REPAIR faza (Greedy Insertion)
        for c in removed:
            best_insert_f = 1e25
            best_state = temp_r + [[c]]
            for r_idx in range(len(temp_r)):
                for pos in range(len(temp_r[r_idx]) + 1):
                    test_r = copy.deepcopy(temp_r)
                    test_r[r_idx].insert(pos, c)
                    v, f, _, _ = check_constraints_and_fitness(test_r, instance)
                    if v and f < best_insert_f:
                        best_insert_f, best_state = f, test_r
            temp_r = best_state

        v, f, d, det = check_constraints_and_fitness(temp_r, instance)
        if v:
            if f < best_f:
                best_f, best_d, best_det, best_r = f, d, det, temp_r
                weights[op_idx] += 0.5
            curr_r = temp_r
            
    return best_r, best_d, best_det, 0