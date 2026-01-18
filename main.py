import os, time
from src.parser import parse_instance
from src.greedy import greedy_solve
from src.vns import vns_solve
from src.sa import sa_solve

def run_experiment():
    instances = {"i1": "inst1[1].TXT", "i2": "inst2[1].TXT", "i3": "inst3[1].TXT"}
    configs = [("1m", 60), ("5m", 300)]
    algos = ["VNS", "SA"]

    # Parametri za VNS (k_max vrijednosti)
    vns_configs = {1: 5, 2: 10, 3: 20, 4: 40, 5: 60}
    
    # Parametri za SA (Temperatura, Alpha)
    sa_configs = {
        1: (100.0, 0.99),    # Brzo hlađenje
        2: (500.0, 0.995),   # Srednje
        3: (1000.0, 0.997),  # Sporo
        4: (5000.0, 0.999),  # Vrlo sporo
        5: (10000.0, 0.9995) # Ekstremno sporo (za duge testove)
    }

    for inst_id, file_name in instances.items():
        path = os.path.join("instances", file_name)
        if not os.path.exists(path): 
            print(f"File not found: {path}")
            continue
            
        instance = parse_instance(path)
        initial = greedy_solve(instance)
        
        for t_label, t_sec in configs:
            for algo_name in algos:
                for p_num in range(1, 6):
                    print(f"Running {inst_id}-{t_label}-{algo_name}-p{p_num}...")
                    
                    if algo_name == "VNS":
                        k_val = vns_configs[p_num]
                        res, dist, detailed, evals = vns_solve(instance, initial, t_sec, k_max_param=k_val)
                    else:
                        temp, alpha_val = sa_configs[p_num]
                        res, dist, detailed, evals = sa_solve(instance, initial, t_sec, T_init=temp, alpha_param=alpha_val)
                    
                    out_name = f"res-{t_label}-{inst_id}-{algo_name}-p{p_num}.txt"
                    save_solution(out_name, res, dist, detailed, evals)

def save_solution(name, routes, dist, detailed, evals):
    os.makedirs("solutions", exist_ok=True)
    with open(os.path.join("solutions", name), "w") as f:
        f.write(f"{len(routes)}\n")
        for i, path in enumerate(detailed, 1):
            # Dodan simbol $ na početak i kraj prema uputama
            f.write(f"{i}: ${path}$\n")
        f.write(f"{dist:.2f}")
    print(f"    Saved: {name} | Evals: {evals} | Dist: {dist}")

if __name__ == "__main__":
    run_experiment()