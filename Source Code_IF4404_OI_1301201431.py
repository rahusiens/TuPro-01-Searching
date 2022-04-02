import random
import math
import copy
import time

start_time = time.time()

def generate_kromosom(panjang: int):
    # Generate kromosom dalam bentuk dua list berisi integer 0 atau 1
    # Contoh :
    # [[0, 1, 0, 0, 1], [1, 1, 0, 1, 0]]
    x = random.choices([0, 1], k=panjang)
    y = random.choices([0, 1], k=panjang)
    return [x, y]

def generate_populasi(ukuran: int, panjang_kromosom: int):
    # Generate populasi dalam bentuk list berisi kromosom
    # Contoh :
    # [
    #   [[0, 1, 0], [1, 1, 1]],
    #   [[0, 0, 0], [1, 1, 0]]
    # ]
    return [generate_kromosom(panjang_kromosom) for _ in range(ukuran)]

def dekode_kromosom(kromosom: int):
    # Dekode kromosom dari bentuk biner menjadi float
    rmax = 5
    rmin = -5
    kro_x, kro_y = kromosom
    x = (rmax-rmin)/sum([2**-(i+1) for i in range(len(kro_x))])
    temp_x = 0
    for i in range(len(kro_x)):
        if kro_x[i] == 1:
            temp_x += 2**-(i+1)
    x *= temp_x
    x += rmin

    y = (rmax-rmin)/sum([2**-(i+1) for i in range(len(kro_y))])
    temp_y = 0
    for i in range(len(kro_y)):
        if kro_y[i] == 1:
            temp_y += 2**-(i+1)
    y *= temp_y
    y += rmin
    return [x, y]

def fitness(kromosom: int):
    # Menghitung nilai fitness dari satu kromosom
    x, y = dekode_kromosom(kromosom)
    return 1 / ( ((math.cos(x) + math.sin(y))**2 / (x**2 + y**2)) + 0.01 )

def fungsi(kromosom: int):
    x, y = dekode_kromosom(kromosom)
    return (math.cos(x) + math.sin(y))**2 / (x**2 + y**2)


def pemilihan_orangtua(populasi):
    # Memilih dua orangtua berbeda dari populasi
    a = random.choices(
        populasi,
        weights = [fitness(kromosom) for kromosom in populasi],
        k = 2
    )

    while a[0] == a[1]:
        a = random.choices(
            populasi,
            weights = [fitness(kromosom) for kromosom in populasi],
            k = 2
        )
    
    orangtua_a, orangtua_b = a[0], a[1]
    return orangtua_a, orangtua_b

def crossover(a: int, b: int):
    # Melakukan crossover antara dua orangtua dan mengembalikan dua offspring
    px = random.randint(1, len(a[0])-2)
    py = random.randint(1, len(a[1])-2)

    offspring_a = [a[0][0:px] + b[0][px:], a[1][0:px] + b[1][px:]]
    offspring_b = [b[0][0:py] + a[0][py:], b[1][0:py] + a[1][py:]]

    return offspring_a, offspring_b

def mutasi(kromosom: int, probability: float = 0.5):
    # Melakukan mutasi pada kromosom dengan kemungkinan 50%
    index1 = random.randrange(len(kromosom))
    index2 = random.randrange(len(kromosom))
    if random.uniform(0, 1) > probability:
        kromosom[0][index1] = abs(kromosom[0][index1] - 1)
    if random.uniform(0, 1) > probability:
        kromosom[1][index2] = abs(kromosom[1][index2] - 1)
    return kromosom

def evolusi(generation_limit: int, ukuran_populasi: int, panjang_kromosom: int, fitness_limit: float):
    # Evolusi untuk pergantian generasi
    populasi = generate_populasi(ukuran_populasi, panjang_kromosom)

    for i in range(generation_limit):
        # Sorting populasi sesuai dengan fitness
        populasi = sorted(
            populasi,
            key = lambda kromosom: fitness(kromosom),
            reverse = True
        )

        # Ketika sudah didapat hasil yang memuaskan, hentikan evolusi
        if fitness(populasi[0]) >= fitness_limit:
            break
    
        # Simpan elitism ke generasi selanjutnya
        next_generation = populasi[0:2]
        
        for j in range(int(len(populasi) / 2) -  1):
            # Buat populasi temporary untuk diambil parent agar nilai populasi asli tidak berubah
            temp_populasi = populasi[:]
            parent_a, parent_b = pemilihan_orangtua(temp_populasi)

            # Crossover kromosom dari kedua parent
            offspring_a, offspring_b = crossover(parent_a, parent_b)

            # Mutasi kedua offspring
            offspring_a = mutasi(offspring_a)
            offspring_b = mutasi(offspring_b)

            # Simpan offspring di generasi selanjutnya
            next_generation.extend([offspring_a, offspring_b])

        populasi = next_generation

    populasi = sorted(
        populasi,
        key = lambda kromosom: fitness(kromosom),
        reverse = True
    )

    return populasi, i
                                                                                                                          



populasi, generasi = evolusi(generation_limit=100, ukuran_populasi=100, panjang_kromosom=10, fitness_limit=99.999997)

print()
print("====================HASIL====================")
print("Kromosom :", populasi[0][0])
print("          ", populasi[0][1])
print("    X    :", dekode_kromosom(populasi[0])[0])
print("    Y    :", dekode_kromosom(populasi[0])[1])
print()
print(" h(x, y) :", fungsi(populasi[0]))
print(" Fitness :", fitness(populasi[0]))
print()
print("Generasi :", generasi)
print("  Waktu  :", (time.time() - start_time), "detik")