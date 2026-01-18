import math

class Customer:
    def __init__(self, data):
        # data dolazi kao lista stringova iz parsera
        self.id = int(data[0])
        self.x = int(data[1])
        self.y = int(data[2])
        self.demand = int(data[3])
        self.ready_time = int(data[4])
        self.due_date = int(data[5])
        self.service_time = int(data[6])

    def __repr__(self):
        return f"C{self.id}"

def get_distance(c1, c2):
    """Euklidska udaljenost bez zaokruživanja (za fitness)."""
    return math.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)

def get_travel_time(c1, c2):
    """Ceiling udaljenosti (za provjeru vremenskih prozora)."""
    return math.ceil(get_distance(c1, c2))

class Instance:
    def __init__(self, name, v_num, capacity, customers):
        self.name = name
        self.vehicle_num = v_num
        self.capacity = capacity
        self.depot = customers[0]
        self.customers = customers[1:]  # Samo pravi kupci
        self.all_nodes = {c.id: c for c in customers} # Brzi dohvat po ID-u