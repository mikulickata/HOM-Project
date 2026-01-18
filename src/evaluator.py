import math

def check_constraints_and_fitness(routes, instance):
    """
    CHECKER funkcija koja provjerava:
    1. Svi kupci posjećeni točno jednom?
    2. Demand <= Capacity?
    3. Start servisa unutar [Ready Time, Due Date]?
    4. Povratak u depo do Due Date depoa?
    """
    total_dist = 0.0
    visited = set()
    detailed_routes = []
    
    for route in routes:
        if not route: continue
        
        t_i = 0      # Vrijeme početka servisa na prethodnom čvoru (depo = 0)
        st_i = 0     # Service time prethodnog čvora
        curr_load = 0
        prev_node = instance.depot
        route_str = "0(0)"
        
        for cust_id in route:
            node = instance.all_nodes[cust_id]
            visited.add(cust_id)
            curr_load += node.demand
            
            # 1. Provjera kapaciteta
            if curr_load > instance.capacity: 
                return False, 1e18, 0, []
            
            # 2. Izračun vremena: tj = max(ti + STi + ceil(dij), RTj)
            d_ij = math.sqrt((prev_node.x - node.x)**2 + (prev_node.y - node.y)**2)
            arrival_time = t_i + st_i + math.ceil(d_ij)
            t_j = max(arrival_time, node.ready_time)
            
            # 3. Provjera vremenskog prozora (Due Date je krajnja granica za START servisa)
            if t_j > node.due_date: 
                return False, 1e18, 0, []
            
            total_dist += d_ij  # Suma bez zaokruživanja
            route_str += f"->{node.id}({int(t_j)})"
            
            t_i, st_i = t_j, node.service_time
            prev_node = node
            
        # Povratak u depo
        d_to_depot = math.sqrt((prev_node.x - instance.depot.x)**2 + (prev_node.y - instance.depot.y)**2)
        return_time = t_i + st_i + math.ceil(d_to_depot)
        
        # 4. Povratak u depo do Due Date depoa
        if return_time > instance.depot.due_date: 
            return False, 1e18, 0, []
        
        total_dist += d_to_depot
        route_str += f"->0({int(return_time)})"
        detailed_routes.append(route_str)
        
    if len(visited) != len(instance.customers): 
        return False, 1e18, 0, []
    
    # Ciljevi: 1. Min broj vozila, 2. Min distanca
    fitness = (len(detailed_routes) * 10**7) + total_dist
    return True, fitness, round(total_dist, 2), detailed_routes