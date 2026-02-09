# Пример строки
a = "Hello, World!" 

# upper() — превращает все буквы в верхний регистр
print(a.upper())  # HELLO, WORLD!

# lower() — превращает все буквы в нижний регистр
print(a.lower())  # hello, world!

# replace() — заменяет указанную букву или подстроку
print(a.replace("H", "J"))  # Jello, World!

# split() — разбивает строку на список по разделителю (по умолчанию пробел)
print(a.split(","))  # ['Hello', ' World!']

# Склеивание строк с +
x = "Hello"
y = "World"
z = x + " " + y  # добавляем пробел между словами
print(z)  # Hello World

# f-string — форматированные строки
num = 36
txt = f"My name is John, I am {num}"          # вставка переменной
txt1 = f"The price is {num:.2f} dollars"      # .2f — 2 знака после запятой
print(txt)   # My name is John, I am 36
print(txt1)  # The price is 36.00 dollars

# Методы для работы с регистром и проверками
text = "hello world"
print(text.capitalize())   # Делает первую букву большой -> Hello world
print(text.title())        # Делает первую букву каждого слова большой -> Hello World
print(text.swapcase())     # Меняет регистр всех букв на противоположный -> HELLO WORLD
print(text.islower())      # True, все буквы маленькие
print(text.isupper())      # False, не все буквы большие
print(text.isalpha())      # False, есть пробел
print("Hello".isalpha())   # True, только буквы
print("123".isdigit())     # True, только цифры
print("Hello123".isalnum())# True, буквы и цифры

# Поиск и подсчёт
print(text.find("world"))   # 6, позиция первого символа подстроки
print(text.index("world"))  # 6, то же самое, но выдаст ошибку, если нет подстроки
print(text.count("l"))      # 3, сколько раз встречается буква "l"

# Проверка начала и конца строки
print(text.startswith("hello"))  # True, строка начинается с hello
print(text.endswith("world"))    # True, строка заканчивается на world

# split() — разбивает строку на список слов
text1 = "Hello World Python"
words = text1.split()
print(words)  # ['Hello', 'World', 'Python']

# join() — соединяет список слов в одну строку с указанным разделителем
joined = "-".join(words)
print(joined)  # Hello-World-Python

# Работа с пробелами
msg = "   Hello, World!   "

# strip() — убирает пробелы с обеих сторон
print("strip: '" + msg.strip() + "'")  # 'Hello, World!'

# lstrip() — убирает пробелы только слева
print("lstrip: '" + msg.lstrip() + "'")  # 'Hello, World!   '

# rstrip() — убирает пробелы только справа
print("rstrip: '" + msg.rstrip() + "'")  # '   Hello, World!'

