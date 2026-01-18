import math

evaluation_count = 0

# src/evaluator.py - Nadogradnja s kaznenim funkcijama
def check_constraints_and_fitness(routes, instance, penalty_capacity=1000, penalty_time=100):
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
        service_time = 0
        prev_node = instance.depot
        route_str = "0(0)"
        
        for cust_id in route:
            node = instance.all_nodes[cust_id]
            visited.add(cust_id)
            curr_load += node.demand
            
            d_ij = math.sqrt((prev_node.x - node.x)**2 + (prev_node.y - node.y)**2)
            arrival_time = curr_time + service_time + math.ceil(d_ij)
            
            # Ako zakasni, bilježimo kršenje
            if arrival_time > node.due_date:
                total_time_violation += (arrival_time - node.due_date)
            
            start_service_time = max(arrival_time, node.ready_time)
            total_dist += d_ij
            route_str += f"->{node.id}({int(start_service_time)})"
            
            curr_time = start_service_time
            service_time = node.service_time
            prev_node = node

        # Kapacitet rute
        if curr_load > instance.capacity:
            total_excess_load += (curr_load - instance.capacity)
            
        # Povratak u depo
        d_to_depot = math.sqrt((prev_node.x - instance.depot.x)**2 + (prev_node.y - instance.depot.y)**2)
        return_time = curr_time + service_time + math.ceil(d_to_depot)
        if return_time > instance.depot.due_date:
            total_time_violation += (return_time - instance.depot.due_date)
        
        total_dist += d_to_depot
        detailed_routes.append(route_str + f"->0({int(return_time)})")

    # Provjera jesu li svi posluženi (ovo ostaje strogo)
    is_valid = (len(visited) == len(instance.customers)) and (total_excess_load == 0) and (total_time_violation == 0)
    
    # FITNESS formula koja dopušta "istraživanje" nevalidnih područja
    # Broj vozila (najbitnije) + distanca + kazne
    fitness = (len(detailed_routes) * 10**7) + total_dist + (total_excess_load * penalty_capacity) + (total_time_violation * penalty_time)
    
    return is_valid, fitness, round(total_dist, 2), detailed_routes