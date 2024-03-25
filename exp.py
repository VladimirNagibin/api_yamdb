import re




"""
string = re.sub(r'^[\w.@+-]+$', 'Неккоректное имя', 'Tantal()')
print(string)
"""



value = re.match(r'^[\w.@+-]+$', 'Tantal(')
print(value)
if value:
    print('Корректное имя')
else:
    print('Неккоректное имя')