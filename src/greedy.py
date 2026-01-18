import math
from .models import get_distance, get_travel_time

def greedy_solve(instance):
    """
    Kreira početno rješenje koristeći Nearest Neighbor logiku 
    uz poštivanje kapaciteta i vremenskih prozora.
    """
    unvisited = list(instance.customers)  # Svi kupci koje moramo obići
    routes = []
    
    while unvisited:
        current_route = []
        current_load = 0
        current_time = 0
        last_node = instance.depot
        
        # Pokušaj napuniti trenutno vozilo
        while True:
            best_next_node = None
            min_dist = float('inf')
            
            for candidate in unvisited:
                # 1. Provjera kapaciteta
                if current_load + candidate.demand > instance.capacity:
                    continue
                
                # 2. Provjera vremena dolaska
                dist = get_distance(last_node, candidate)
                travel_time = math.ceil(dist)
                arrival_time = current_time + last_node.service_time + travel_time
                start_service = max(arrival_time, candidate.ready_time)
                
                # Smije li startati servis?
                if start_service <= candidate.due_date:
                    # 3. Provjera može li se vratiti u depo nakon ovog kupca
                    dist_to_depot = get_distance(candidate, instance.depot)
                    return_arrival = start_service + candidate.service_time + math.ceil(dist_to_depot)
                    
                    if return_arrival <= instance.depot.due_date:
                        # Ako je sve OK, tražimo najbližeg takvog
                        if dist < min_dist:
                            min_dist = dist
                            best_next_node = candidate
            
            if best_next_node:
                # Dodaj kupca u rutu
                current_route.append(best_next_node.id)
                current_load += best_next_node.demand
                
                # Updateaj vrijeme za sljedeći korak
                dist = get_distance(last_node, best_next_node)
                arrival_time = current_time + last_node.service_time + math.ceil(dist)
                current_time = max(arrival_time, best_next_node.ready_time)
                
                last_node = best_next_node
                unvisited.remove(best_next_node)
            else:
                # Nema više kupaca koji stanu u ovo vozilo
                break
        
        if current_route:
            routes.append(current_route)
        else:
            # Sigurnosni break ako je nemoguće uslužiti nekog kupca
            break
            
    return routes