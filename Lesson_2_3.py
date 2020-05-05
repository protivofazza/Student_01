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
        self.z = self.z + other.z
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self.x, self.y, self.z

    def __sub__(self, other):
        self.z = self.z - other.z
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self.x, self.y, self.z

    def __mul__(self, other):
        self.z = self.z * other.z
        self.x = self.x * other.x
        self.y = self.y * other.y
        return self.x, self.y, self.z

    def __truediv__(self, other):
        self.z = int(self.z / other.z)
        self.x = int(self.x / other.x)
        self.y = int(self.y / other.y)
        return self.x, self.y, self.z

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self.x, self.y, self.z


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

