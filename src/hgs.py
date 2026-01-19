import time, random, copy, math
from .evaluator import check_constraints_and_fitness

def vidal_split(giant_tour, instance):
    n = len(giant_tour)
    d = [1e18] * (n + 1)
    parent = [0] * (n + 1)
    d[0] = 0
    
    for i in range(1, n + 1):
        load = 0
        time_curr = 0
        for j in range(i, n + 1):
            cust = instance.all_nodes[giant_tour[j-1]]
            load += cust.demand
            if load > instance.capacity: break
            
            if i == j:
                arrival = max(math.ceil(math.dist((instance.depot.x, instance.depot.y), (cust.x, cust.y))), cust.ready_time)
                time_curr = arrival + cust.service_time
            else:
                prev = instance.all_nodes[giant_tour[j-2]]
                travel = math.ceil(math.dist((prev.x, prev.y), (cust.x, cust.y)))
                arrival = max(time_curr + travel, cust.ready_time)
                if arrival > cust.due_date: break
                time_curr = arrival + cust.service_time
            
            back_to_depot = math.ceil(math.dist((cust.x, cust.y), (instance.depot.x, instance.depot.y)))
            if time_curr + back_to_depot > instance.depot.due_date: break
            
            # Računanje distance rute
            dist_seg = math.dist((instance.depot.x, instance.depot.y), (instance.all_nodes[giant_tour[i-1]].x, instance.all_nodes[giant_tour[i-1]].y))
            for k in range(i, j):
                n1, n2 = instance.all_nodes[giant_tour[k-1]], instance.all_nodes[giant_tour[k]]
                dist_seg += math.dist((n1.x, n1.y), (n2.x, n2.y))
            last_n = instance.all_nodes[giant_tour[j-1]]
            dist_seg += math.dist((last_n.x, last_n.y), (instance.depot.x, instance.depot.y))
            
            cost = d[i-1] + 1e7 + dist_seg
            if cost < d[j]:
                d[j] = cost
                parent[j] = i - 1

    routes = []
    curr = n
    while curr > 0:
        routes.append(giant_tour[parent[curr]:curr])
        curr = parent[curr]
    return routes[::-1]

def hgs_solve(instance, initial, time_limit, pop_size):
    # Generiraj početnu populaciju s varijacijama
    gt_base = [c for r in initial for c in r]
    population = []
    for _ in range(pop_size):
        individual = list(gt_base)
        if len(population) > 0: random.shuffle(individual)
        population.append(individual)

    best_routes = initial
    v, best_f, best_d, best_det = check_constraints_and_fitness(initial, instance)
    
    start_time = time.time()
    while (time.time() - start_time) < time_limit:
        p1, p2 = random.sample(population, 2)
        # OX Crossover
        size = len(p1)
        a, b = sorted(random.sample(range(size), 2))
        child = [None] * size
        child[a:b] = p1[a:b]
        p2_remaining = [item for item in p2 if item not in child[a:b]]
        
        curr = 0
        for i in range(size):
            if child[i] is None:
                child[i] = p2_remaining[curr]
                curr += 1
        
        # Split i Local Search (obrazovanje djeteta)
        cand_routes = vidal_split(child, instance)
        # MALA TAJNA: Dodaj Local Search ovdje da polira dijete prije evaluacije!
        
        v, f, d, det = check_constraints_and_fitness(cand_routes, instance)
        
        # Čak i ako je nevalidno, fitness će ga rangirati
        population.append(child)
        if v and f < best_f:
            best_f, best_d, best_det, best_routes = f, d, det, cand_routes
            
        if len(population) > pop_size * 2:
            # Preživljavanje: izbaci najgore po fitnessu
            population.sort(key=lambda x: check_constraints_and_fitness(vidal_split(x, instance), instance)[1])
            population = population[:pop_size]

    return best_routes, best_d, best_det, 0