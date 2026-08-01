import numpy as np
import random
import time
import pandas as pd

def calculate_distance_matrix(data, n):
    """
    Şehirler arası mesafeleri içeren bir mesafe matrisi oluşturur.
    """
    distance = np.ones((n, n)) * np.inf
    for i in range(n):
        for j in range(n):
            if i != j:
                distance[i, j] = np.sqrt((data[i, 1] - data[j, 1]) ** 2 + (data[i, 2] - data[j, 2]) ** 2)
    return distance

# Berlin52 veri setini yükle
data = np.loadtxt("dataSets/berlin52.txt")
n = len(data)

# Mesafe matrisini oluştur
distance_matrix = calculate_distance_matrix(data, n)

def calculate_route_distance(route, distance_matrix):
    """
    Verilen rotanın toplam mesafesini hesaplar.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += (distance_matrix[route[i], route[i + 1]])
    # Dönüş mesafesi
    total_distance += distance_matrix[route[-1], route[0]]
    return total_distance

def initialize_population(pop_size, num_cities):
    """
    Rastgele popülasyon oluşturur.
    """
    population = [random.sample(range(num_cities), num_cities) for _ in range(pop_size)]
    return population

def evaluate_population(population, distance_matrix):
    """
    Popülasyonu değerlendirir ve fitness değerlerini hesaplar.
    """
    fitness_durumu= []
    for route in population:
        distance = calculate_route_distance(route, distance_matrix)
        fitness_durumu.append(distance)  
    return fitness_durumu

def pilot_study(pop_sizes, iterations, distance_matrix):
    """
    Pilot çalışma: Belirli popülasyon büyüklükleri ve iterasyon sayıları ile algoritmanın performansını ölçer.
    """
    results = []
    
    for pop_size in pop_sizes:
        for iter_count in iterations:
            start_time = time.time()
            
            # Popülasyon oluştur
            population = initialize_population(pop_size, len(distance_matrix))
            
            # Popülasyonu değerlendir
            fitness_durumu = evaluate_population(population, distance_matrix)
            
            # En iyi fitness değerini bul
            best_fitness = (min(fitness_durumu))
            
            
            # Süreyi hesapla
            duration = time.time() - start_time
            
            # Sonuçları kaydet
            results.append({
                'Pop Size': pop_size,
                'Iterations': iter_count,
                'Best Fitness': best_fitness,
                'Duration (s)': duration
            })
    
    return results

def save_results_to_excel(results, filename):
    """
    Sonuçları Excel dosyasına kaydeder.
    """
    df = pd.DataFrame(results)
    df.to_excel(filename, index=False)
    print(f"Sonuçlar {filename} dosyasına kaydedildi.")

# Pilot çalışma parametreleri
POP_SIZES = [30, 40, 50]
ITERATIONS = [10000, 50000, 100000]

# Pilot çalışmayı Berlin52 veri seti ile çalıştır
pilot_results = pilot_study(POP_SIZES, ITERATIONS, distance_matrix)


# Sonuçları kaydet
save_results_to_excel(pilot_results, "Pilot_Study_Results1.xlsx")

print(pilot_results)
