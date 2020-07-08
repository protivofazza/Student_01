"""1) Создать свою структуру данных Список, которая поддерживает
индексацию. Методы pop, append, insert, remove, clear. Перегрузить
операцию сложения для списков, которая возвращает новый расширенный
объект."""


class MyList:

    def __init__(self, *args):
        self._list = [*args]
        self._length = len(args)

    def pop(self, key=0):
        if type(key) != int:
            raise TypeError
        if key < 0:
            key += self._length
        if 0 <= key < self._length:
            value = self._list[key]
            self._list = self._list[:key] + self._list[key + 1:]
            self._length -= 1
            return value
        else:
            raise IndexError

    def append(self, value):
        self._list += [value]
        self._length += 1

    def insert(self, key, value):
        if type(key) != int:
            raise TypeError
        if key < 0:
            key += self._length
        if 0 <= key < self._length:
            self._list = self._list[:key] + [value] + self._list[key:]
            self._length += 1
        else:
            raise IndexError

    def remove(self, value):
        for key, val in enumerate(self):
            if val == value:
                self.pop(key)

    def clear(self):
        self._list = []
        self._length = 0

    def __add__(self, other):
        return MyList(*self._list, *other._list)

    def __setitem__(self, key, value):
        if type(key) != int:
            raise TypeError
        if key < 0:
            key += self._length
        if 0 <= key < self._length:
            self._list[key] = value
        else:
            raise IndexError

    def __getitem__(self, item):
        if type(item) != int:
            raise TypeError
        if item < 0:
            item += self._length
        if 0 <= item < self._length:
            return self._list[item]
        else:
            raise IndexError

    def __len__(self):
        return self._length

    def __str__(self):
        return str(self._list)


list_1 = MyList(14)
list_2 = MyList(36, '28', 17)
list_3 = list_1 + list_2
print("list_3 =", list_3)
print("list_3[0], list_3[1], list_3[2], list_3[3] ---", list_3[0], list_3[1], list_3[2], list_3[3])
print("len(list_3) = ", len(list_3), "\n")

list_3.append("777")
print("list_3 =", list_3, "\n")

list_3[1] = 'gfro'
print("list_3 =", list_3, "\n")

list_3.insert(3, [998, 999])
print("list_3 =", list_3, "\n")

list_3.pop(3)
print("list_3 =", list_3, "\n")

list_3.remove('777')
print("list_3 =", list_3, "\n")

list_3.clear()
print("list_3 =", list_3, "\n")

try:
    print(list_1[1])
except IndexError:
    print("IndexError while running\n\n\n")


"""2) Создать свою структуру данных Словарь, которая поддерживает методы,
get, items, keys, values. Так же перегрузить операцию сложения для
словарей, которая возвращает новый расширенный объект.
Указанные методы описываем самостоятельно, без использования
стандартных."""


class MyDict:

    def __init__(self, dict_param):
        self._dict = dict_param
        self._length = len(dict_param)

    def get(self, key, default=None):
        if key in self._dict:
            return self._dict[key]
        else:
            return default

    def items(self):
        items = []
        for key in self._dict:
            items.append((key, self._dict[key],))
        return tuple(items)

    def keys(self):
        keys = []
        for key in self._dict:
            keys.append(key)
        return tuple(keys)

    def values(self):
        values = []
        for key in self._dict:
            values.append(self._dict[key])
        return tuple(values)

    def __add__(self, other):
        dictionary = MyDict(self._dict)
        for i in other._dict:
            dictionary[i] = other[i]
        return dictionary

    def __getitem__(self, item):
        if self.get(item):
            return self._dict[item]
        raise IndexError

    def __setitem__(self, key, value):
        if type(key) != int and type(key) != str:
            raise TypeError
        if key not in self._dict:
            self._length += 1
        self._dict[key] = value

    def __len__(self):
        return self._length

    def __str__(self):
        return str(self._dict)


dict_1 = MyDict({"pilot": "Mark Weber", "bolid": "RBR07", "engine_power": 860})
dict_2 = MyDict({"year": 2012, "city": "Melbourne"})

dict_3 = dict_1 + dict_2

print("dict_3 =", dict_3)

print("dict_3.get('city') =", dict_3.get('city'))
print("dict_3.get('car') =", dict_3.get('car'))

print("dict_3.items() =", dict_3.items())

print("dict_3['year'] =", dict_3['year'])

print("dict_3.values() =", dict_3.values())

print("dict_3.keys() =", dict_3.keys())