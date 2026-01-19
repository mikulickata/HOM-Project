import os, time
import src.evaluator as evaluator
from src.ga import ga_solve
from src.ils import ils_solve
from src.lns import lns_solve
from src.parser import parse_instance
from src.greedy import greedy_solve
from src.vnd import vnd_solve
from src.vns import vns_solve
from src.sa import sa_solve
from src.tabu import tabu_solve
from src.hgs import hgs_solve
from src.alns import alns_solve
from src.aco import aco_solve
from src.memetic import memetic_solve
from src.evaluator import check_constraints_and_fitness

def save_solution(name, routes, dist, detailed):
    # Čistimo ime datoteke od znakova koji nisu dopušteni u Windows/Linux sustavima
    clean_name = name.replace("{", "").replace("}", "").replace("'", "").replace(":", "-").replace(" ", "")
    os.makedirs("solutions", exist_ok=True)
    with open(os.path.join("solutions", clean_name), "w") as f:
        f.write(f"{len(detailed)}\n")
        for i, path in enumerate(detailed, 1):
            f.write(f"{i}: {path}\n")
        f.write(f"{dist:.2f}")

def run_experiment():
    instances = {f"i{i}": f"inst{i}[1].TXT" for i in range(1, 7)}
    configs = [("1m", 60), ("5m", 300), ("un", 900)] 
    
    # Parametri
    sa_configs      = {1: (100.0, 0.99), 2: (500.0, 0.995), 3: (1000.0, 0.997), 4: (5000.0, 0.999), 5: (10000.0, 0.9995)}
    vns_configs     = {1: 5, 2: 10, 3: 20, 4: 40, 5: 60}
    ils_configs     = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
    lns_configs     = {1: 0.15, 2: 0.20, 3: 0.25, 4: 0.30, 5: 0.35}
    ga_configs      = {1: 30, 2: 40, 3: 50, 4: 60, 5: 70}
    tabu_configs    = {1: 20, 2: 40, 3: 60, 4: 80, 5: 100}
    hybrid_configs  = {1: (200, 0.92), 2: (500, 0.95), 3: (1000, 0.97), 4: (2000, 0.98), 5: (5000, 0.99)}
    hgs_configs     = {1: 20, 2: 40, 3: 60, 4: 80, 5: 100}
    alns_configs    = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5}
    aco_configs     = {1: 5, 2: 10, 3: 15, 4: 20, 5: 30}
    memetic_configs = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25}

    for inst_id, file_name in instances.items():
        path = os.path.join("instances", file_name)
        if not os.path.exists(path): continue
        
        instance = parse_instance(path)
        initial = greedy_solve(instance)
        _, _, g_dist, g_det = check_constraints_and_fitness(initial, instance)
        
        print(f"\n" + "="*100)
        print(f" PROCESSING: {inst_id} | Greedy Dist: {g_dist:.2f}")
        print("="*100)

        for t_label, t_sec in configs:
            if not inst_id == 'i2' or not inst_id == 'i1':
                print(f"\n--- TIME LIMIT: {t_label} ({t_sec}s) ---")

                # 1. FIKSNI ALGORITMI
                for name, func in [("VNS_FULL", vns_solve), ("VND", vnd_solve)]:
                    evaluator.evaluation_count = 0
                    if name == "VNS_FULL":
                        res, dist, det, _ = func(instance, initial, t_sec, full_set=True, k_max=25)
                        cfg_info = "full=True,k=25"
                    else:
                        res, dist, det, _ = func(instance, initial, t_sec)
                        cfg_info = "default"
                    
                    save_solution(f"res-{t_label}-{inst_id}-{name}-{cfg_info}.txt", res, dist, det)
                    print(f"    {name:11} | {cfg_info:20} | Evals: {evaluator.evaluation_count:8} | Veh: {len(det):2} | Dist: {dist:.2f}")

                # 2. PARAMETARSKI ALGORITMI (p1-p5)
                for p in range(1, 6):
                        methods = [
                            ("HYBRID", sa_solve, {"T_init": hybrid_configs[p][0], "alpha_param": hybrid_configs[p][1], "hybrid": True}),
                            ("SA", sa_solve, {"T_init": sa_configs[p][0], "alpha_param": sa_configs[p][1]}),
                            ("VNS_B", vns_solve, {"k_max": vns_configs[p], "full_set": False}),
                            ("GA", ga_solve, {"population_size": ga_configs[p]}),
                            ("TABU", tabu_solve, {"list_size": tabu_configs[p]}),
                            ("ILS", ils_solve, {"n_perturbations": ils_configs[p]}),
                            ("LNS", lns_solve, {"ruin_factor": lns_configs[p]}),
                            ("HGS", hgs_solve, {"pop_size": hgs_configs[p]}),
                            ("ALNS", alns_solve, {"intensity": alns_configs[p]}),
                            ("ACO", aco_solve, {"n_ants": aco_configs[p]}),
                            ("MEMETIC", memetic_solve, {"ls_intensity": memetic_configs[p]})
                        ]

                        for m_name, m_func, m_params in methods:
                            # Kreiranje čitljivog stringa konfiguracije: "param1=val1,param2=val2"
                            cfg_str = ",".join([f"{k}={v}" for k, v in m_params.items()])
                            
                            evaluator.evaluation_count = 0
                            r, d, dt, _ = m_func(instance, initial, t_sec, **m_params)
                            
                            save_solution(f"res-{t_label}-{inst_id}-{m_name}-{cfg_str}.txt", r, d, dt)
                            print(f"      {m_name:10} | {cfg_str:30} | Evals: {evaluator.evaluation_count:8} | Veh: {len(dt):2} | Dist: {d:.2f}")

if __name__ == "__main__":
    run_experiment()