x = 5
y = "John"
x = "Sally" #x is now of type str
print(x)
print(y)
print(type(x))
print(type(y))

myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"


print(myvar)
print(my_var)
print(_my_var)
print(myVar)
print(MYVAR)
print(myvar2)

a, b, z = "Orange", "Banana", "Cherry"
print(a)
print(b)
print(z)

fruits = ["apple", "banana", "cherry"]
c, v, n = fruits
print(c)
print(b)
print(n)

def myfunc():
  global x
  x = "fantastic"
  print("Python is " + x)
myfunc()

print("Python is " + x)

