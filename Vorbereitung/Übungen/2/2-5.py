def fac(x):
    if x < 0:
        print("Fakultät für negative Zahlen ist nicht definiert")
        return None
    if x == 0 or x == 1:
        return 1
    return x * fac(x - 1)


x = int(input("Gib einen Int an: "))
print(f"Die Fakultät von {x} ist {fac(x)}")