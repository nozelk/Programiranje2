import matplotlib.pyplot as plt
import random

A = (0, 0)
B = (1, 0)
C = (0.5, 1)

tocke = [A]
while len(tocke) < 100000:
    nakljucno_oglisce = random.choice([A, B, C])
    zadnja_tocka = tocke[-1]
    nova_tocka = ((zadnja_tocka[0] + nakljucno_oglisce[0]) / 2, (zadnja_tocka[1] + nakljucno_oglisce[1]) / 2)
    tocke.append(nova_tocka)

vrednost_x = [point[0] for point in tocke]
vrednost_y = [point[1] for point in tocke]

plt.scatter(vrednost_x, vrednost_y, s=1, color='blue')
plt.title('Trikotnik Sierpinskega (100000 točk)')
plt.xlabel('X')
plt.ylabel('Y')

plt.savefig('sierpinski.pdf')
plt.show()
