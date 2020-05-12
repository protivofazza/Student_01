# У файлі створено два класи Point та PointUpdated. Обидва описують клас точки, проте клас PointUpdated виконує цю
# роботу "красивіше" та "чистіше" з точки зору користувача програми. Втім, обидва класи відповідають умовам задачі.


class Point:
    def __init__(self, name='Точка', x=0, y=0, z=0):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def set_point(self):
        self.x = int(input('Введіть координату по осі X: '))
        self.y = int(input('Введіть координату по осі Y: '))
        self.z = int(input('Введіть координату по осі Z: '))

    def get_point(self):
        print('Координати', self.name, ':\nПо осі X:', self.x, '\nПо осі Y:', self.y, '\nПо осі Z:', self.z)

    def __add__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        self.z = self.z + other.z
        return self.x, self.y, self.z

    def __sub__(self, other):
        self.x = self.x - other.x
        self.y = self.y - other.y
        self.z = self.z - other.z
        return self.x, self.y, self.z

    def __mul__(self, other):
        self.x = self.x * other.x
        self.y = self.y * other.y
        self.z = self.z * other.z
        return self.x, self.y, self.z

    def __truediv__(self, other):
        self.x = int(self.x / other.x)
        self.y = int(self.y / other.y)
        self.z = int(self.z / other.z)
        return self.x, self.y, self.z

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self.x, self.y, self.z


class PointUpdated(Point):

    def set_point(self):
        self.name = input("Введіть назву для цєї точки (наприклад 'Точка 1'): ")
        super().set_point()

    def change_name(self):
        print(f"Поточна назва точки з координатами ({self.x}, {self.y}, {self.z}) - '{self.name}'.")
        self.name = input("Введіть нову назву для цієї точки: ")

    def get_point(self):
        print("Координати '", self.name, "':\n\t\t\t\t\tПо осі X: ", self.x, '\n\t\t\t\t\tПо осі Y: ', self.y,
              '\n\t\t\t\t\tПо осі Z: ', self.z, sep='')

    def __add__(self, other):
        return PointUpdated(self.name + ' + ' + other.name, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return PointUpdated(self.name + ' - ' + other.name, self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return PointUpdated(self.name + ' * ' + other.name, self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other):
        return PointUpdated(self.name + ' / ' + other.name, int(self.x / other.x), int(self.y / other.y), int(self.z / other.z))

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        self.name = '-' + self.name
        return PointUpdated(self.name, self.x, self.y, self.z)


# Блок коду для перевірки фунціональності класу Point
print('\n\nНижче програма виконує код для перевірки фунціонау класу Point: \n')
point_0 = Point()
point_1 = Point('Точка 1')
point_2 = Point('Точка 2', 2, 2, 2)
point_3 = Point('Точка 3')
print('Введемо значення координат для Точки 3:')
point_3.set_point()
print("Також попередньо були задані значення координат для Точка 1 (Ім'я + дефолтні) і Точка 2 (передані параметри):")
point_1.get_point()
point_2.get_point()

print(f"Перегружений метод додавання '+' для {point_2.name} і {point_3.name} дає такий результат для {point_2.name} :")
point_2 + point_3
point_2.get_point()

print(f"Перегружений метод віднімання '-' для {point_2.name} і {point_3.name} дає такий результат для {point_2.name} :")
point_2 - point_3
point_2.get_point()

print(f"Перегружений метод множення '*' для {point_2.name} і {point_3.name} дає такий результат для {point_2.name} :")
point_2 * point_3
point_2.get_point()

print(f"Перегружений метод ділення '/' для {point_2.name} і {point_3.name} дає такий результат для {point_2.name} :")
point_2 / point_3
point_2.get_point()

print(f"Перегружений метод 'Унарний мінус' для {point_2.name} дає такий результат:")
-point_2
point_2.get_point()
-point_2

point_4 = PointUpdated('Точка 4')
point_4 = point_2 + point_3
print(point_4)


# Блок коду для перевірки фунціональності класу PointUpdated
print('\n\nНижче програма виконує код для перевірки фунціонау класу PointUpdated: \n')
point_0 = PointUpdated()
point_1 = PointUpdated('Точка 1')
point_2 = PointUpdated('Точка 2', 2, 2, 2)
point_3 = PointUpdated('Точка 3')
print('Введемо значення координат для Точки 3:')
point_3.set_point()
print("\nТакож попередньо були задані значення координат для Точка 1 (Ім'я + дефолтні) і Точка 2 (передані параметри):")
point_1.get_point()
point_2.get_point()

print(f"\nПерегружений метод додавання '+' для '{point_2.name}' і '{point_3.name}' дає такий результат:")
point_5 = point_2 + point_3
point_5.get_point()
point_5.change_name()
point_5.get_point()

print(f"Перегружений метод віднімання '-' для '{point_5.name}' і '{point_3.name}' дає такий результат:")
point_6 = point_5 - point_3
point_6.get_point()
point_6.change_name()
point_6.get_point()

print(f"Перегружений метод множення '*' для '{point_2.name}' і '{point_3.name}' дає такий результат")
point_7 = point_2 * point_3
point_7.get_point()

print(f"Перегружений метод ділення '/' для '{point_7.name}' і '{point_3.name}' дає такий результат:")
point_8 = point_7 / point_3
point_8.get_point()

print(f"Перегружений метод 'Унарний мінус' для '{point_2.name}' дає такий результат:")
-point_2
point_2.get_point()
-point_2


point_4 = point_7 + point_8
point_4.change_name()
point_4.get_point()
