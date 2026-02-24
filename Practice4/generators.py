#iterations

mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))


for x in mytuple:
  print(x)

class mynum:
    def __iter__(self):
        self.num = 1
        return self
    def __next__(self):
        if self.num <=20:
            x = self.num
            self.num += 1
            return x
        else:
            raise StopIteration

a = mynum()
myiter = iter(a)

for x in myiter:
  print(x)


#generators
  
def a(num):
    cnt = 1
    while cnt <= num:
        yield cnt
        cnt += 1
        
ctr = a(5)
for i in ctr:
    print(i)


def fun():
    yield 1
    yield 2
    yield 3
    
for i in fun():
    print(i)

#Generator Expression
sq = (x*x for i in range(1,6))
for i in sq:
    print(i)
