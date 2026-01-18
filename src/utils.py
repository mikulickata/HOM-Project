import random
import copy

def shaking(routes, k):
    new_routes = copy.deepcopy(routes)
    for _ in range(k):
        if len(new_routes) < 1: break
        
        # Tip susjedstva: 0 = Move, 1 = Swap
        neighborhood_type = random.choice([0, 1])
        
        r1_idx = random.randrange(len(new_routes))
        if not new_routes[r1_idx]: continue
        
        if neighborhood_type == 0: # MOVE
            cust_idx = random.randrange(len(new_routes[r1_idx]))
            customer = new_routes[r1_idx].pop(cust_idx)
            
            r2_idx = random.randrange(len(new_routes))
            insert_pos = random.randint(0, len(new_routes[r2_idx]))
            new_routes[r2_idx].insert(insert_pos, customer)
            
        else: # SWAP
            r2_idx = random.randrange(len(new_routes))
            if not new_routes[r2_idx]: continue
            
            idx1 = random.randrange(len(new_routes[r1_idx]))
            idx2 = random.randrange(len(new_routes[r2_idx]))
            
            # Zamjena kupaca između (ili unutar) ruta
            new_routes[r1_idx][idx1], new_routes[r2_idx][idx2] = \
                new_routes[r2_idx][idx2], new_routes[r1_idx][idx1]
        
    return [r for r in new_routes if r]

def local_search_2opt(routes, instance, current_best_f):
    from .evaluator import check_constraints_and_fitness
    improved_routes = copy.deepcopy(routes)
    best_f = current_best_f
    
    # Fokusiramo se na 2-opt unutar ruta (Intensification)
    for i in range(len(improved_routes)):
        route = improved_routes[i]
        if len(route) < 3: continue
        
        for a in range(len(route) - 1):
            for b in range(a + 2, len(route) + 1):
                new_route = route[:a] + route[a:b][::-1] + route[b:]
                
                old_route = improved_routes[i]
                improved_routes[i] = new_route
                
                valid, f_cand, _, _ = check_constraints_and_fitness(improved_routes, instance)
                
                if valid and f_cand < best_f:
                    best_f = f_cand
                else:
                    improved_routes[i] = old_route
                    
    return improved_routes, best_f