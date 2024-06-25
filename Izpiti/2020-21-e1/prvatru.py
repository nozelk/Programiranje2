from random import sample

arr = sample(range(10**12), 10**6)
m = [0] * 8

for i in arr:
    if i % 2 == 0 and i > min(m):
        m[m.index(min(m))] = i



for i in range(8):
    print(max(m))
    m.remove(max(m))

print('s_s')
s_s = [stevilo for stevilo in arr if stevilo % 2 == 0]

for i in range(8):
    print(max(s_s))
    s_s.remove(max(s_s))

soda_stevila = sorted([stevilo for stevilo in arr if stevilo % 2 == 0], reverse=True)

print("Sort")
for stevilo in soda_stevila[:8]:
    print(stevilo)