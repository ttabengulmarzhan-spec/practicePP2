x = 15
y = 4

print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y)
print(x ** y)
print(x // y)

numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3: #print(x := 3) --> x = 3  print(x)
    print(f"List has {count} elements")

print(6 & 3) #The & operator compares each bit and set it to 1 if both are 1, otherwise it is set to 0
print(6 | 3) #The | operator compares each bit and set it to 1 if one or both is 1, otherwise it is set to 0
print(6 ^ 3) #The ^ operator compares each bit and set it to 1 if only one is 1, otherwise (if both are 1 or both are 0) it is set to 0
print(~3) #Inverts all the bits
print(3 << 2) #Zero fill left shift
print(8 >> 2) #Signed right shift
