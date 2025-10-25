import random

# ====== ข้อมูลระยะทางระหว่างเมือง ======
distances = {
    ('A', 'B'): 2, ('B', 'A'): 2,
    ('A', 'C'): 8, ('C', 'A'): 8,
    ('A', 'D'): 5, ('D', 'A'): 5,
    ('B', 'C'): 3, ('C', 'B'): 3,
    ('B', 'D'): 4, ('D', 'B'): 4,
    ('C', 'D'): 7, ('D', 'C'): 7
}

cities = ['A', 'B', 'C', 'D']

# ====== ฟังก์ชันคำนวณระยะทางทั้งหมดของเส้นทาง ======
def total_distance(route):
    dist = 0
    for i in range(len(route) - 1):
        dist += distances[(route[i], route[i+1])]
    dist += distances[(route[-1], route[0])]  # กลับไปเมืองเริ่มต้น
    return dist

# ====== ฟังก์ชันเริ่มต้นประชากร ======
def create_population(size):
    population = []
    for _ in range(size):
        route = cities[:]
        random.shuffle(route)
        population.append(route)
    return population

# ====== เลือกพ่อแม่โดย roulette wheel ======
def select(population):
    weights = [1 / total_distance(route) for route in population]
    total = sum(weights)
    pick = random.uniform(0, total)
    current = 0
    for route, w in zip(population, weights):
        current += w
        if current > pick:
            return route

# ====== crossover ======
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(cities)), 2))
    child = parent1[start:end]
    for city in parent2:
        if city not in child:
            child.append(city)
    return child

# ====== mutation ======
def mutate(route, rate=0.1):
    for i in range(len(route)):
        if random.random() < rate:
            j = random.randint(0, len(route)-1)
            route[i], route[j] = route[j], route[i]
    return route

# ====== main genetic algorithm ======
def genetic_algorithm(generations=500, population_size=50):
    population = create_population(population_size)
    best_route = min(population, key=total_distance)
    best_distance = total_distance(best_route)

    for gen in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1 = select(population)
            parent2 = select(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
        current_best = min(population, key=total_distance)
        if total_distance(current_best) < best_distance:
            best_route = current_best
            best_distance = total_distance(best_route)

    return best_route, best_distance

# ====== Run ======
best_route, best_distance = genetic_algorithm()
print("🏆 เส้นทางที่ดีที่สุด:", " → ".join(best_route + [best_route[0]]))
print("📏 ระยะทางรวม:", best_distance)