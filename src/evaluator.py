import math

def check_constraints_and_fitness(routes, instance):
    """
    Vraća (is_valid, fitness, total_dist, detailed_routes)
    """
    total_dist = 0.0
    total_vehicles = len(routes)
    visited_customers = set()
    detailed_output = []

    for route_nodes in routes:
        current_time = 0
        current_load = 0
        prev_node = instance.depot
        route_str = "0(0)"
        
        for cust_id in route_nodes:
            customer = instance.all_nodes[cust_id]
            visited_customers.add(cust_id)
            
            # 1. Provjera kapaciteta
            current_load += customer.demand
            if current_load > instance.capacity:
                return False, 1e15, 0, []

            # 2. Izračun vremena (Strogo po formuli s math.ceil)
            d_ij = math.sqrt((prev_node.x - customer.x)**2 + (prev_node.y - customer.y)**2)
            arrival_time = current_time + prev_node.service_time + math.ceil(d_ij)
            
            start_service = max(arrival_time, customer.ready_time)
            
            # 3. Provjera vremenskog prozora
            if start_service > customer.due_date:
                return False, 1e15, 0, []
            
            # Update statistike (Fitness koristi pravu udaljenost bez ceil)
            total_dist += d_ij
            current_time = start_service
            route_str += f"->{customer.id}({int(current_time)})"
            prev_node = customer

        # Povratak u depo
        d_to_depot = math.sqrt((prev_node.x - instance.depot.x)**2 + (prev_node.y - instance.depot.y)**2)
        arrival_at_depot = current_time + prev_node.service_time + math.ceil(d_to_depot)
        
        if arrival_at_depot > instance.depot.due_date:
            return False, 1e15, 0, []
        
        total_dist += d_to_depot
        route_str += f"->0({int(arrival_at_depot)})"
        detailed_output.append(route_str)

    if len(visited_customers) != len(instance.customers):
        return False, 1e15, 0, []

    # Fitness: broj_vozila * 10^7 + distanca
    fitness_val = (total_vehicles * 10**7) + total_dist
    return True, fitness_val, round(total_dist, 2), detailed_output