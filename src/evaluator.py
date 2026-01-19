import math

evaluation_count = 0

def check_constraints_and_fitness(routes, instance, penalty_capacity=2000, penalty_time=500):
    global evaluation_count
    evaluation_count += 1
    
    total_dist = 0.0
    total_excess_load = 0
    total_time_violation = 0
    visited = set()
    detailed_routes = []

    for route in routes:
        if not route: continue
        curr_load = 0
        curr_time = 0
        prev_node = instance.depot
        route_str = "0(0)"
        
        for cust_id in route:
            node = instance.all_nodes[cust_id]
            visited.add(cust_id)
            curr_load += node.demand
            
            d_ij = math.sqrt((prev_node.x - node.x)**2 + (prev_node.y - node.y)**2)
            arrival_time = curr_time + prev_node.service_time + d_ij
            
            if arrival_time > node.due_date:
                total_time_violation += (arrival_time - node.due_date)
            
            start_service_time = max(arrival_time, node.ready_time)
            total_dist += d_ij
            route_str += f"->{node.id}({int(start_service_time)})"
            
            curr_time = start_service_time
            prev_node = node

        if curr_load > instance.capacity:
            total_excess_load += (curr_load - instance.capacity)
            
        d_to_depot = math.sqrt((prev_node.x - instance.depot.x)**2 + (prev_node.y - instance.depot.y)**2)
        return_time = curr_time + prev_node.service_time + d_to_depot
        if return_time > instance.depot.due_date:
            total_time_violation += (return_time - instance.depot.due_date)
        
        total_dist += d_to_depot
        detailed_routes.append(route_str + f"->0({int(return_time)})")

    # BROJ VOZILA mora imati najveći ponder u fitnessu
    num_vehicles = len(detailed_routes)
    all_served = (len(visited) == len(instance.customers))
    
    # Ako nisu svi posluženi, fitness je beskonačan
    if not all_served:
        return False, 1e25, 0, []

    # Fitness: Kazne su uključene tako da algoritam može "evoluirati" kroz nevalidna rješenja
    penalty = (total_excess_load * penalty_capacity) + (total_time_violation * penalty_time)
    fitness = (num_vehicles * 1000000) + total_dist + penalty
    
    # Validno je samo ako nema nikakvih kršenja
    is_valid = (total_excess_load == 0 and total_time_violation == 0)
    
    return is_valid, fitness, round(total_dist, 2), detailed_routes