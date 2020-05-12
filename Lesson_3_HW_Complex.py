class ComplexNumber:
    def __init__(self, r_part=0, i_part=0):
        self.r_part = r_part
        self.i_part = i_part

    def __str__(self):
        if self.i_part != 0:
            temp_sign = '-' if self.i_part/abs(self.i_part) == -1 else '+'
        else:
            temp_sign = '+'
        return f"{self.r_part} {temp_sign} {abs(self.i_part)}i"

    def set_number(self):
        r_b = True
        while r_b:
            r_part = input('Введіть дійсну частину комплексного числа: ')
            i_part = input('Введіть уявну частину комплексного числа: ')
            try:
                self.r_part = int(r_part)
                self.i_part = int(i_part)
                r_b = False
            except ValueError:
                try:
                    self.r_part = float(r_part)
                    self.i_part = float(i_part)
                    r_b = False
                except ValueError:
                    print('Введені значення мають бути числами')

    def get_number(self):
        print()
        return self.r_part, self.i_part

    def __add__(self, other):
        return ComplexNumber(self.r_part + other.r_part, self.i_part + other.i_part)

    def __sub__(self, other):
        return ComplexNumber(self.r_part - other.r_part, self.i_part - other.i_part)

    def __mul__(self, other):
        return ComplexNumber(self.r_part * other.r_part - self.i_part * other.i_part,
                             self.r_part * other.i_part + other.r_part * self.i_part)

    def __truediv__(self, other):
        return ComplexNumber(
                                (self.r_part * other.r_part + self.i_part * other.i_part) /
                                (other.r_part ** 2 + other.i_part ** 2),
                                (self.i_part * other.r_part - self.r_part *other.i_part) /
                                (other.r_part ** 2 + other.i_part ** 2)
                            )


complex_1 = ComplexNumber(2, -3)
complex_2 = ComplexNumber()
complex_2.set_number()
print(complex_1)
print(complex_2)
complex_3 = complex_1 + complex_2
print(complex_3)

complex_4 = complex_1 - complex_2
print(complex_4)

complex_5 = complex_1 * complex_2
print(complex_5)

complex_6 = complex_1 / complex_2
print(complex_6)
