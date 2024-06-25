a=int(input("Prva"))
b=int(input("Druga"))
def euclid(a,b):
    x=a%b
    while x:
        a=b
        b=x
        x=a%b
    print(b)
euclid(a,b)