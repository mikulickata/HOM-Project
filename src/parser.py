import os
from .models import Customer, Instance

def parse_instance(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    v_num = 0
    v_cap = 0
    customers = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 1. Tražimo zaglavlje VEHICLE da izvučemo broj vozila i kapacitet
        if "VEHICLE" in line:
            i += 2  # Preskačemo "VEHICLE" i "NUMBER CAPACITY" redove
            parts = lines[i].split()
            if parts:
                v_num = int(parts[0])
                v_cap = int(parts[1])
        
        # 2. Tražimo sekciju CUSTOMER
        elif "CUSTOMER" in line:
            i += 2  # Preskačemo "CUSTOMER" i zaglavlje tablice (CUST NO. XCOORD...)
            # Čitamo sve do kraja datoteke
            while i < len(lines):
                parts = lines[i].split()
                # Ako red ima 7 elemenata (ID, X, Y, Demand, Ready, Due, Service)
                if len(parts) == 7:
                    customers.append(Customer(parts))
                i += 1
        i += 1

    # Čišćenje naziva instance (npr. "inst1[1].TXT" -> "i1")
    raw_name = os.path.basename(file_path).lower()
    name = raw_name.replace('.txt', '').replace('[1]', '').replace('inst', 'i')
    
    return Instance(name, v_num, v_cap, customers)