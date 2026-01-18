import os
import time
from src.parser import parse_instance
from src.greedy import greedy_solve
from src.evaluator import check_constraints_and_fitness

# Globalna varijabla za praćenje evaluacija
EVAL_COUNT = 0

def save_solution(instance_name, time_label, detailed_routes, num_vehicles, total_dist, eval_count):
    """Sprema rješenje u formatu res-vrijeme-instanca.txt"""
    if not os.path.exists('solutions'):
        os.makedirs('solutions')
    
    filename = f"res-{time_label}-{instance_name}.txt"
    filepath = os.path.join('solutions', filename)
    
    with open(filepath, 'w') as f:
        # Prvi red: broj vozila
        f.write(f"{num_vehicles}\n")
        # Rute
        for i, route_str in enumerate(detailed_routes, 1):
            f.write(f"{i}: {route_str}\n")
        # Zadnji red: ukupna distanca (zaokružena na 2 decimale)
        f.write(f"{total_dist:.2f}")
    
    print(f"   [OK] Spremljeno: {filename} (Evala: {eval_count}, Dist: {total_dist})")

def run_experiment(instance_path):
    global EVAL_COUNT
    instance = parse_instance(instance_path)
    print(f"\n>>> Pokrećem instancu: {instance.name} ({instance_path})")
    
    # Lista vremenskih ograničenja koja profesor traži
    time_limits = [("1m", 60), ("5m", 300), ("un", 999999)]
    
    for label, limit in time_limits:
        EVAL_COUNT = 0
        start_time = time.time()
        
        # 1. KREIRAJ POČETNO RJEŠENJE (Greedy)
        # Za sada, greedy je brz pa ga odmah imamo
        current_routes = greedy_solve(instance)
        EVAL_COUNT += 1
        
        # 2. POBOLJŠAJ (Ovdje će doći tvoj VNS/Metaheuristika)
        # Dok god ima vremena, pokušavaj poboljšati...
        # lower_dist_solution = vns_improve(current_routes, instance, limit, start_time)
        
        # 3. EVALUACIJA I SPREMANJE
        is_valid, fitness, total_dist, detailed_routes = check_constraints_and_fitness(current_routes, instance)
        
        if is_valid:
            save_solution(instance.name, label, detailed_routes, len(current_routes), total_dist, EVAL_COUNT)
        else:
            print(f"   [ERROR] Rješenje za {instance.name} nije validno!")
        
        # Za 'un' (unlimited) vjerojatno ne želiš čekati vječno dok testiraš
        # pa možemo staviti break ako je ovo samo testiranje greedy-ja
        if label == "un": 
             print("   (unlimited opcija odrađena kao jedan prolaz greedy-ja)")

if __name__ == "__main__":
    # Folder gdje se nalaze instance
    instances_dir = "instances"
    
    if not os.path.exists(instances_dir):
        print(f"Greška: Folder '{instances_dir}' ne postoji!")
    else:
        # Uzmi sve .txt datoteke i sortiraj ih po imenu
        files = sorted([f for f in os.listdir(instances_dir) if f.upper().endswith(".TXT")])
        
        if not files:
            print("Nema pronađenih .txt instanci u folderu.")
        else:
            print(f"Pronađeno {len(files)} instanci. Krećem s radom...")
            for file_name in files:
                full_path = os.path.join(instances_dir, file_name)
                run_experiment(full_path)
            print("\nSve instance su obrađene!")