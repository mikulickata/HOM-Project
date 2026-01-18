import time, copy, random
from .evaluator import check_constraints_and_fitness

def lns_solve(instance, initial, time_limit, ruin_factor):
    best_routes = initial
    _, best_f, best_d, best_det = check_constraints_and_fitness(best_routes, instance)
    start_time = time.time()

    while (time.time() - start_time) < time_limit:
        # 1. RUIN: Ukloni kupce koji su prostorno blizu (povećava šansu za bolji Recreate)
        all_cust_objects = instance.customers
        seed_cust = random.choice(all_cust_objects)
        # Sortiraj ostale po udaljenosti od seed kupca
        sorted_by_dist = sorted(all_cust_objects, 
                               key=lambda c: (c.x - seed_cust.x)**2 + (c.y - seed_cust.y)**2)
        
        num_to_remove = int(len(instance.customers) * ruin_factor)
        to_remove_ids = [c.id for c in sorted_by_dist[:num_to_remove]]
        
        curr_routes = [[c for c in r if c not in to_remove_ids] for r in best_routes]
        curr_routes = [r for r in curr_routes if r]

        # 2. RECREATE: Greedy insertion s Education fazom
        for cust_id in to_remove_ids:
            best_ins_f = 1e25
            best_temp_routes = curr_routes + [[cust_id]]
            
            for r_idx in range(len(curr_routes)):
                for pos in range(len(curr_routes[r_idx]) + 1):
                    test_r = [list(r) for r in curr_routes]
                    test_r[r_idx].insert(pos, cust_id)
                    v, f, _, _ = check_constraints_and_fitness(test_r, instance)
                    if f < best_ins_f:
                        best_ins_f, best_temp_routes = f, test_r
            curr_routes = best_temp_routes

        # 3. EDUCATION: Obavezno poliranje nakon Recreate-a
        curr_routes, f = local_search_hill_climb(curr_routes, instance, best_ins_f)
        
        v, f, d, det = check_constraints_and_fitness(curr_routes, instance)
        if v and f < best_f:
            best_routes, best_f, best_d, best_det = curr_routes, f, d, det
            
    return best_routes, best_d, best_det, 0