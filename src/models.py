import math

class Customer:
    def __init__(self, data):
        self.id = int(data[0])
        self.x = int(data[1])
        self.y = int(data[2])
        self.demand = int(data[3])
        self.ready_time = int(data[4])
        self.due_date = int(data[5])
        self.service_time = int(data[6])

def get_distance(c1, c2):
    # Puna preciznost za fitness
    return math.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)

def get_travel_time(c1, c2):
    # Vrijeme je zaokružena distanca (prema uputama projekta)
    return math.ceil(get_distance(c1, c2))

class Instance:
    def __init__(self, name, v_num, capacity, nodes):
        self.name = name
        self.vehicle_num = v_num
        self.capacity = capacity
        self.depot = nodes[0]
        self.customers = nodes[1:]
        self.all_nodes = {n.id: n for n in nodes}