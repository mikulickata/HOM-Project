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
    os.makedirs("solutions", exist_ok=True)
    with open(os.path.join("solutions", name), "w") as f:
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
        
        print(f"\n" + "="*85)
        print(f" PROCESSING: {inst_id} | Greedy Dist: {g_dist:.2f}")
        print("="*85)

        for t_label, t_sec in configs:
            print(f"\n--- TIME LIMIT: {t_label} ---")
            is_un = (t_label == "un")

            # 1. FIKSNI - VNS FULL (Uvijek)
            evaluator.evaluation_count = 0
            res, dist, det, _ = vns_solve(instance, initial, t_sec, full_set=True, k_max=25)
            save_solution(f"res-{t_label}-{inst_id}-VNS_FULL.txt", res, dist, det)
            print(f"    VNS_FULL    | Evals: {evaluator.evaluation_count:8} | Veh: {len(det):2} | Dist: {dist:.2f}")

            # 2. FIKSNI - VND (Samo ako NIJE unlimited)
            if not is_un:
                evaluator.evaluation_count = 0
                res, dist, det, _ = vnd_solve(instance, initial, t_sec)
                save_solution(f"res-{t_label}-{inst_id}-VND.txt", res, dist, det)
                print(f"    VND         | Evals: {evaluator.evaluation_count:8} | Veh: {len(det):2} | Dist: {dist:.2f}")

            # 3. PARAMETARSKI (p1-p5)
            for p in range(1, 6):
                print(f"    > p{p}:")

                # --- GRUPA: UVIJEK (1m, 5m, un) ---
                # HYBRID
                evaluator.evaluation_count = 0
                res, dist, det, _ = sa_solve(instance, initial, t_sec, T_init=hybrid_configs[p][0], alpha_param=hybrid_configs[p][1], hybrid=True)
                save_solution(f"res-{t_label}-{inst_id}-HYBRID-p{p}.txt", res, dist, det)
                print(f"      HYBRID-p{p}  | Veh: {len(det):2} | Dist: {dist:.2f}")

                # SA, VNS_BASIC, GA, TABU
                for name, func, cfg in [("SA", sa_solve, sa_configs[p]), ("VNS_B", vns_solve, vns_configs[p]), 
                                        ("GA", ga_solve, ga_configs[p]), ("TABU", tabu_solve, tabu_configs[p])]:
                    evaluator.evaluation_count = 0
                    if name == "SA": r, d, dt, _ = func(instance, initial, t_sec, T_init=cfg[0], alpha_param=cfg[1])
                    elif name == "VNS_B": r, d, dt, _ = func(instance, initial, t_sec, k_max=cfg, full_set=False)
                    elif name == "GA": r, d, dt, _ = func(instance, initial, t_sec, population_size=cfg)
                    elif name == "TABU": r, d, dt, _ = func(instance, initial, t_sec, list_size=cfg)
                    save_solution(f"res-{t_label}-{inst_id}-{name}-p{p}.txt", r, d, dt)
                    print(f"      {name:10}-p{p} | Veh: {len(dt):2} | Dist: {d:.2f}")

                # --- GRUPA: SAMO KAD NIJE UN ---
                if not is_un:
                    # ILS
                    evaluator.evaluation_count = 0
                    r, d, dt, _ = ils_solve(instance, initial, t_sec, n_perturbations=ils_configs[p])
                    save_solution(f"res-{t_label}-{inst_id}-ILS-p{p}.txt", r, d, dt)
                    print(f"      ILS-p{p:5}    | Veh: {len(dt):2} | Dist: {d:.2f}")
                    # LNS
                    evaluator.evaluation_count = 0
                    r, d, dt, _ = lns_solve(instance, initial, t_sec, ruin_factor=lns_configs[p])
                    save_solution(f"res-{t_label}-{inst_id}-LNS-p{p}.txt", r, d, dt)
                    print(f"      LNS-p{p:5}    | Veh: {len(dt):2} | Dist: {d:.2f}")

                # --- GRUPA: SAMO KAD JE UN ---
                else:
                    # HGS, ALNS, ACO, MEMETIC
                    heavy = [("HGS", hgs_solve, "pop_size", hgs_configs[p]), 
                             ("ALNS", alns_solve, "intensity", alns_configs[p]),
                             ("ACO", aco_solve, "n_ants", aco_configs[p]),
                             ("MEMETIC", memetic_solve, "ls_intensity", memetic_configs[p])]
                    for h_name, h_func, h_param, h_val in heavy:
                        evaluator.evaluation_count = 0
                        r, d, dt, _ = h_func(instance, initial, t_sec, **{h_param: h_val})
                        save_solution(f"res-{t_label}-{inst_id}-{h_name}-p{p}.txt", r, d, dt)
                        print(f"      {h_name:10}-p{p} | Veh: {len(dt):2} | Dist: {d:.2f}")

if __name__ == "__main__":
    run_experiment()