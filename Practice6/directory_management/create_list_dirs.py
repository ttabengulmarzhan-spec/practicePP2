import os

os.makedirs("project/data/files", exist_ok=True)

print("Files in current directory:")
print(os.listdir())


with open("a.txt","w") as f:
    f.write("I am pretty")
    
print("TXT files:")
for file in os.listdir():
    if file.endswith(".txt"):
        print(file)

