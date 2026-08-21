class book:
    def __init__(self):
        self.title = ""
        self.author = ""
        self.year = 0

x = book()
x.title = "Monster Manual"
x.author = "Wizards of the Coast"
x.year = 2014

y = book()
y.title = "Monster Manual"
y.author = "Wizards of the Coast"
y.year = 2024

print(f"{y.title}\n{y.author}\n{y.year}")