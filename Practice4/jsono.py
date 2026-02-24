#JSON is a syntax for storing and exchanging data.
#JSON is text, written with JavaScript object notation.
import json

x = '{"name":"John", "age":30, "city":"New York"}'

#parse = разобрать / распарсить / проанализировать текст и превратить его в структуру данных.

y = json.loads(x)

print(y["age"])


x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

y = json.dumps(x)

print(y)

print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))



x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

# use four indents to make it easier to read the result:
print(json.dumps(x, indent=4, separators=(". ", " = ")))
print("sorted")
print(json.dumps(x, indent=4, sort_keys=True))

#writing json files

data = {
    "name": "John",
    "age": 30
}

with open("file.json", "w") as f:
    json.dump(data, f, indent=4)

print("File created!")

#reading json files

with open("file.json", "r") as f:
    data = json.load(f)

print(data)
