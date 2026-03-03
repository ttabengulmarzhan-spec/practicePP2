import re

a = input()
x1 = re.search(r"^ab*$",a)
x2 = re.search(r"^ab{2,3}$",a)
x3 = re.search(r"[a-z]+_[a-z]+",a)
x4 = re.search(r"[A-Z][a-z]+",a)
x5 = re.search(r"^a.*b$",a)
x6 = re.sub(r"[,\.]",":",a)
x7 = re.sub(r"_([a-z])",lambda x: x.group(1).upper(),a)
x8 = re.findall(r"[A-Z][a-z]*",a)
x9 = re.sub(r"([A-Z])", r" \1",a).strip()
x10 = re.sub(r"([A-Z])",r"_\1", a).lower()
if x1:
    print("Yes")
else:
    print("No")
if x2:
    print("Yes")
else:
    print("No")
if x3:
    print("Yes")
else:
    print("No")
if x4:
    print("Yes")
else:
    print("No")
if x5:
    print("Yes")
else:
    print("No")
print(x6)
print(x7)
print(x8)
print(x9)
print(x10)
