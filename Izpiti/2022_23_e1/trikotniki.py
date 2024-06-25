import matplotlib.pyplot as plt
import random

# Definiranje oglišč trikotnika
A = (0, 0)
B = (1, 0)
C = (0.5, 0.866)  # C je na sredini med A in B na y-osi

# Začetna točka
current_point = A

# Seznam za shranjevanje točk
points = [current_point]

# Število točk
num_points = 10000

# Ustvarjanje točk
for _ in range(num_points):
    chosen_vertex = random.choice([A, B, C])
    current_point = ((current_point[0] + chosen_vertex[0]) / 2, 
                     (current_point[1] + chosen_vertex[1]) / 2)
    points.append(current_point)

# Razpakiranje točk za risanje
x_points, y_points = zip(*points)

# Risanje točk
plt.figure(figsize=(8, 8))
plt.scatter(x_points, y_points, s=0.1, color='blue')
plt.title("Sierpinski Triangle")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.axis('equal')

# Shranjevanje grafa v datoteko
plt.savefig("sierpinski.pdf")
plt.show()
