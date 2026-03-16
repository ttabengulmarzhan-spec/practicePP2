# enumerate
names = ["Alice","Bob","Charlie"]
for i, name in enumerate(names):
    print(i, name)

# zip
ages = [20,21,22]
for name, age in zip(names, ages):
    print(name, age)

# type conversion
a = "123"
print(type(a))
b = int(a)
print(type(b))
