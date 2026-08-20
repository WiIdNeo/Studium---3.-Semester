def fib(x):
    if x == 0:
        return 1
    if x == 1:
        return 2
    else: 
        return x + x-1       

x = int(input("Gib eine natürliche Zahl an."))
print(f"Die {x}. Fibonacci-Zahl ist {fib(x)}.")

