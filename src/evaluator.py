import math

evaluation_count = 0

def check_constraints_and_fitness(routes, instance, penalty_capacity=2000, penalty_time=500):
    """
    Evaluira rješenje prema CVRPTW pravilima.
    Izračun vremena koristi math.ceil(udaljenost) prema uputama projekta.
    """
    global evaluation_count
    evaluation_count += 1
    
    total_dist = 0.0
    total_excess_load = 0
    total_time_violation = 0
    visited = set()
    detailed_routes = []

    for route in routes:
        if not route: 
            continue
            
        curr_load = 0
        curr_time = 0  # Početak u depou (Ready time depoa je 0)
        prev_node = instance.depot
        route_str = "0(0)"
        
        for cust_id in route:
            node = instance.all_nodes[cust_id]
            visited.add(cust_id)
            curr_load += node.demand
            
            # 1. Izračun euklidske udaljenosti
            d_ij = math.sqrt((prev_node.x - node.x)**2 + (prev_node.y - node.y)**2)
            total_dist += d_ij  # U ukupnu distancu ide precizni float
            
            # 2. VRIJEME DOLASKA: t(j) = t(i) + ST(i) + ceil(d_ij)
            # Ovo je ključni dio koji validator provjerava
            arrival_time = curr_time + prev_node.service_time + math.ceil(d_ij)
            
            # 3. KASNJENJE: Provjera Due Date-a (mora započeti servis najkasnije do Due Date)
            if arrival_time > node.due_date:
                total_time_violation += (arrival_time - node.due_date)
            
            # 4. POČETAK SERVISA: Ako dođe ranije, čeka do READY TIME
            start_service_time = max(arrival_time, node.ready_time)
            
            # Formatiranje ispisa za rješenje (mora biti cijeli broj u zagradi)
            route_str += f"->{node.id}({int(start_service_time)})"
            
            # Ažuriranje stanja za idućeg kupca
            curr_time = start_service_time
            prev_node = node

        # Provjera kapaciteta vozila za ovu rutu
        if curr_load > instance.capacity:
            total_excess_load += (curr_load - instance.capacity)
            
        # POVRATAK U DEPO
        d_to_depot = math.sqrt((prev_node.x - instance.depot.x)**2 + (prev_node.y - instance.depot.y)**2)
        total_dist += d_to_depot
        
        # Vrijeme povratka u depo (također koristi ceil udaljenosti)
        return_time = curr_time + prev_node.service_time + math.ceil(d_to_depot)
        
        # Provjera zatvaranja depoa (Due Date depoa)
        if return_time > instance.depot.due_date:
            total_time_violation += (return_time - instance.depot.due_date)
        
        detailed_routes.append(route_str + f"->0({int(return_time)})")

    # BROJ VOZILA (Primarni cilj)
    num_vehicles = len(detailed_routes)
    
    # Provjera jesu li svi kupci usluženi
    all_served = (len(visited) == len(instance.customers))
    if not all_served:
        # Penalizacija ako algoritam slučajno izbaci rješenje koje ne pokriva sve kupce
        return False, 1e25, 0, []

    # Validnost: nema kršenja kapaciteta ni vremenskih prozora
    is_valid = (total_excess_load == 0 and total_time_violation == 0)

    # FITNESS FUNKCIJA: 
    # Prioritet 1: Broj vozila (težina 1,000,000)
    # Prioritet 2: Kazne za nevalidna rješenja
    # Prioritet 3: Ukupna udaljenost
    penalty = (total_excess_load * penalty_capacity) + (total_time_violation * penalty_time)
    fitness = (num_vehicles * 1000000) + total_dist + penalty
    
    return is_valid, fitness, round(total_dist, 2), detailed_routes