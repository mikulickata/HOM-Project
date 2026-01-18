import time, collections, copy
from .utils import relocate_move
from .evaluator import check_constraints_and_fitness

def tabu_solve(instance, initial, time_limit, list_size):
    curr_routes = initial
    _, curr_f, curr_d, curr_det = check_constraints_and_fitness(curr_routes, instance)
    best_routes, best_f, best_d, best_det = curr_routes, curr_f, curr_d, curr_det
    
    tabu_list = collections.deque(maxlen=list_size)
    start_time = time.time()

    while (time.time() - start_time) < time_limit:
        best_neighbor = None
        best_neighbor_f = 1e20
        neighbor_repr = ""
        
        for _ in range(100): 
            cand = relocate_move(curr_routes)
            v, f, d, det = check_constraints_and_fitness(cand, instance)
            if v:
                state_repr = str(det)
                # Aspiration criteria: dopusti potez ako je bolji od najboljeg ikad, čak i ako je Tabu
                if f < best_f or state_repr not in tabu_list:
                    if f < best_neighbor_f:
                        best_neighbor, best_neighbor_f = cand, f
                        neighbor_repr = state_repr
        
        if best_neighbor:
            curr_routes = best_neighbor
            tabu_list.append(neighbor_repr)
            if best_neighbor_f < best_f:
                best_routes, best_f, best_d, best_det = check_constraints_and_fitness(best_neighbor, instance)[0:4]

    return best_routes, best_d, best_det, 0