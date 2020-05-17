import abc
import datetime


class AbstractPerson(abc.ABC):

    def __init__(self, surname, yy_btd, mm_btd, dd_btd, faculty):
        self._surname = surname
        self._date_of_btd = datetime.datetime(yy_btd, mm_btd, dd_btd)
        self._faculty = faculty
        self.calculate_age()

    @abc.abstractmethod
    def get_info(self):
        print('|', ' '*(30-len(self._surname)), end='')
        print(f"{self._surname} | д/н: {self._date_of_btd.date()} | ф-т: {self._faculty}", end='')

    @abc.abstractmethod
    def calculate_age(self):
        if (self._date_of_btd.month, self._date_of_btd.day) <= \
                (datetime.datetime.now().month, datetime.datetime.now().day):
            self.age = datetime.datetime.now().year - self._date_of_btd.year
        else:
            self.age = datetime.datetime.now().year - self._date_of_btd.year - 1


class Enrollee(AbstractPerson):

    def get_info(self):
        print('\nАбітуріент', end='')
        super().get_info()
        print(' ' * (35 - len(self._faculty)), '| -подані документи- |', end='')

    def calculate_age(self):
        super().calculate_age()
        # print(f'На сьогоднішню дату, {datetime.datetime.now().date()}, вік абітуріента {self._surname} '
        #       f'становить {self.age} р')


class Student(AbstractPerson):

    def __init__(self, surname, yy_btd, mm_btd, dd_btd, faculty, year_of_study):
        super().__init__(surname, yy_btd, mm_btd, dd_btd, faculty)
        self._year_of_study = year_of_study

    def get_info(self):
        print('\n   Студент', end='')
        super().get_info()
        print(' '*(35 - len(self._faculty)), end='')
        print(f' | рік навчання:  {self._year_of_study}-й |', end='')

    def calculate_age(self):
        super().calculate_age()
        # print(f'На сьогоднішню дату, {datetime.datetime.now().date()}, вік студента {self._surname} '
        #       f'становить {self.age} р')

    def __str__(self):
        self.get_info()


class Professor(AbstractPerson):

    def __init__(self, surname, yy_btd, mm_btd, dd_btd, faculty, position, experience):
        super().__init__(surname, yy_btd, mm_btd, dd_btd, faculty)
        self._position = position
        self._experience = experience

    def get_info(self):
        print('\n  Викладач', end='')
        super().get_info()
        print(' ' * (35 - len(self._faculty)), '| стаж в роках:', ' ' * (2 - len(str(self._experience))), end='')
        print(f'{self._experience} р | посада: {self._position}', end='')

    def calculate_age(self):
        super().calculate_age()
        # print(f'На сьогоднішню дату, {datetime.datetime.now().date()}, вік викладача {self._surname} '
        #       f'становить {self.age} р')


enrollee = Enrollee('Smith', 2001, 5, 18, 'Organic chemistry')
student_01 = Student('Gaponenko', 1991, 12, 30, 'Inorganic chemistry', 2)
professor_01 = Professor('Черненко', 1983, 2, 22, 'Електроспоживання', 'Доцент', 13)
student_02 = Student('Вавілова', 1999, 10, 3, 'Inorganic chemistry', 3)
student_03 = Student('Бондар', 1998, 1, 14, 'Inorganic chemistry', 5)

list_of_person = [enrollee, student_01, student_02, student_03, professor_01]

print("\nПовний список зі всією інформацією про зареєстроаних осіб:")
for person in list_of_person:
    person.get_info()

check_input = True
while check_input:
    try:
        # global age_min, age_max
        age_min = int(input("\n\nДля пошуку особи за заданими рамками віку введіть: "
                            "\n\t\t\t\t\t\t\t\t\t\t\t\t  -  нижню вікову межу років: "))
        age_max = int(input("\t\t\t\t\t\t\t\t\t\t\t\t  - верхню вікову межу років: "))
        check_input = False
    except ValueError:
        print('*'*39, '\nВведене значення має бути цілим числом!\nСпробуйте ввести дані ще раз.\n', '*'*39,
              sep='', end='')

for person in list_of_person:
    if age_min <= person.age <= age_max:
        person.get_info()
