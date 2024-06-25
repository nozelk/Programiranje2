"""def shrani(ime, sosedi, oznake):
    if oznake == None:
        oznake = [None] * len(sosedi)
    with open(f"{ime}.adj","w") as f:
        j = 0
        for i in oznake:
            s = ""
            if i == None:
                s += '"",'
            else:
                s += f'"{i}",'
            h = 0
            while h < len(sosedi[j]):
                s += f"{sosedi[j][h]},"
                h += 1
            j += 1
            if j != len(oznake):
                f.write(f'{s[:-1]}\n')
            else:
                f.write(s[:-1])
    
shrani('demo', [[1], [0, 2, 2], [1, 1], []], ['foo', 'bar', 'baz', None])
shrani('demo2', [[1], [0, 2, 2], [1, 1], []], [None, 'foo', None, 'bar'])
shrani('cikel', [[7, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 0]], None)

def preberi(ime):
    g = [ime.split(".")[0],[],[]]
    s = 0
    with open(ime,"r") as dat:
        l = dat.readlines()
        for i in l:
            i = i.split(",")
            if i[0].strip('""') != "":
                g[2].append(i[0].strip('""'))
            else:
                g[2].append(None)
                s += 1
            i = i[1:]
            g[1].append([int(j) for j in i])
    if s == len(g[2]):
        g[2] = None
    return g

print(preberi("demo.adj"))
print(preberi("demo2.adj"))
print(preberi("cikel.adj"))
"""
import re
string = 'Split!!by,integers,123,and,45'

res = re.split(r"\W+", string)
print(res)
