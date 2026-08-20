
x = 0
y = 0
matches3 = []
matches5 = []
while x < 30:
    y += 1
    x = 5 * y
    matches5.append(x)
    x = 3 * y
    matches3.append(x)
    

for i in range(1, 31, 1):
    if i in matches3:
        if i in matches5:
            print(f"Fizzbuzz {i}")
        else: 
            print(f"Fizz {i}")
    elif i in matches5:
        print(f"Buzz {i}")
    else:
        print(i)