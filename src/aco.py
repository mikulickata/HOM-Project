import time, random, math
from .evaluator import check_constraints_and_fitness
from .tabu import tabu_solve

def aco_solve(instance, initial, time_limit, n_ants):
    num_nodes = len(instance.all_nodes)
    pheromones = [[1.0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    best_r = initial
    _, best_f, best_d, best_det = check_constraints_and_fitness(initial, instance)
    
    start_time = time.time()
    while (time.time() - start_time) < time_limit:
        iteration_solutions = []
        
        # n_ants mrava gradi svoja rješenja
        for _ in range(n_ants):
            current_r = []
            unvisited = set(c.id for c in instance.customers)
            while unvisited:
                route = []
                curr = 0
                while unvisited:
                    nodes = list(unvisited)
                    probs = []
                    for n_id in nodes:
                        node = instance.all_nodes[n_id]
                        prev = instance.all_nodes[curr]
                        dist = math.sqrt((prev.x - node.x)**2 + (prev.y - node.y)**2)
                        probs.append(pheromones[curr][n_id] / (dist + 0.1))
                    
                    next_c = random.choices(nodes, weights=probs)[0]
                    route.append(next_c)
                    unvisited.remove(next_c)
                    curr = next_c
                    if random.random() > 0.8: break 
                current_r.append(route)
            iteration_solutions.append(current_r)
            
        # Odabir najboljeg mrava iz ove generacije za poliranje i update
        for sol in iteration_solutions:
            refined, d, det, _ = tabu_solve(instance, sol, time_limit=1, list_size=20)
            v, f, d, det = check_constraints_and_fitness(refined, instance)
            
            if v and f < best_f:
                best_f, best_d, best_det, best_r = f, d, det, refined
                # Pojačavanje feromona samo za najbolje rješenje (Elitist ACO)
                for r in best_r:
                    p = 0
                    for c in r:
                        pheromones[p][c] += 1.0
                        p = c
                    pheromones[p][0] += 1.0
                
    return best_r, best_d, best_det, 0