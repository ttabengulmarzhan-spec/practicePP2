nums = [1,2,3,4,5]

squared = list(map(lambda x: x*x, nums))
even = list(filter(lambda x: x%2==0, nums))

print(squared)
print(even)


from functools import reduce

nums = [1,2,3,4]

result = reduce(lambda x,y: x+y, nums)

print(result)
