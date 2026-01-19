import time, random, copy
from .evaluator import check_constraints_and_fitness

def alns_solve(instance, initial, time_limit, intensity):
    # Početno rješenje
    curr_r = initial
    v, curr_f, d, det = check_constraints_and_fitness(curr_r, instance)
    best_r, best_f, best_d, best_det = curr_r, curr_f, d, det
    
    start_time = time.time()
    while (time.time() - start_time) < time_limit:
        # RUIN: Slučajno ukloni kupce
        all_c = [c for r in curr_r for c in r]
        num_to_remove = max(2, int(len(all_c) * intensity))
        removed = random.sample(all_c, num_to_remove)
        
        # Stvori privremeno rješenje bez uklonjenih kupaca
        temp_r = [[c for c in r if c not in removed] for r in curr_r]
        temp_r = [r for r in temp_r if r] # Obriši prazne rute
        
        # REPAIR: Best Insertion
        random.shuffle(removed)
        for c in removed:
            best_ins_f = 1e25
            best_ins_state = None
            
            # 1. Pokušaj ubaciti u postojeće rute (ako ih ima)
            if temp_r:
                for r_idx in range(len(temp_r)):
                    for pos in range(len(temp_r[r_idx]) + 1):
                        # Optimizacija: koristimo plitku kopiju lista ruta za brzinu
                        test_r = [list(r) for r in temp_r]
                        test_r[r_idx].insert(pos, c)
                        _, f, _, _ = check_constraints_and_fitness(test_r, instance)
                        if f < best_ins_f:
                            best_ins_f = f
                            best_ins_state = test_r
            
            # 2. Pokušaj otvoriti potpuno novu rutu za tog kupca
            test_r_new = temp_r + [[c]]
            _, f_new, _, _ = check_constraints_and_fitness(test_r_new, instance)
            
            # 3. Odaberi bolju opciju
            if f_new < best_ins_f or best_ins_state is None:
                temp_r = test_r_new
            else:
                temp_r = best_ins_state

        # Evaluacija cijelog novog rješenja
        v, f, d, det = check_constraints_and_fitness(temp_r, instance)
        
        # Prihvaćanje rješenja (Hill Climbing s malim pragom tolerancije)
        if f < curr_f * 1.01: 
            curr_r, curr_f = temp_r, f
            if v and f < best_f:
                best_r, best_f, best_d, best_det = temp_r, f, d, det
                
    return best_r, best_d, best_det, 0