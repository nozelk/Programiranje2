# Program to display the Fibonacci sequence up to n-th term

nterms = int(input("How many terms? "))

# first two terms
n1, n2 = 0, 1
count = 0

if nterms <= 0:
   print("Please enter a positive integer")
elif nterms == 1:
   print("Fibonacci sequence upto",nterms,":")
   print(n1)
else:
   print("Fibonacci sequence:")
   while count <= nterms:
       print(f'F_{count} = {n1:,}')
       nth = n1 + n2
       # update values
       n1 = n2
       n2 = nth
       count += 1

def fibonacci(n):
    fib = [0, 1]  # Začetna vrednost Fibonaccijevega zaporedja
    if n <= 1:
        return fib[:n+1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])  # Dodajanje naslednjega Fibonaccijevega števila
    return fib

# Izračun in izpis prvih sto Fibonaccijevih števil
fib_sequence = fibonacci(100)
for i, fib_number in enumerate(fib_sequence):
    print(f'F_{i} = {fib_number:,}')