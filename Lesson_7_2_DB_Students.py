import sqlite3


STUD_DB = "Student_DB.db"


class ContextManagerForDBConnect:
    """Контекстний менеджер для відкриття та закриття бази даних SQL"""

    def __init__(self, name_db):
        self._name_db = name_db

    def __enter__(self):
        self._connect = sqlite3.connect(self._name_db)
        return self._connect

    def __exit__(self, *args):
        self._connect.close()


def read_query_list(query="", *args):
    """Функція для зчитування даних з бази"""
    with ContextManagerForDBConnect(STUD_DB) as connection:
        cursor = connection.cursor()
        result = []
        try:
            cursor.execute(query, list(args))
            result = cursor.fetchall()
        except Exception as e:
            print("Error while reading data: " + query)
            print(e)
        finally:
            return result


def update_query(params, query=""):
    """Функція для запису даних в базу"""
    with ContextManagerForDBConnect(STUD_DB) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            print("Error while downloading data: " + query)
            print(e)


class User:
    def __init__(self):
        self._id = student_title_list[0]
        self._student_id = student_title_list[1]
        self._stud_name = student_title_list[2]
        self._stud_surname = student_title_list[3]
        self._stud_faculty = student_title_list[4]
        self._stud_group = student_title_list[5]

    @staticmethod
    def get_list_of_subjects(char=''):
        """Метод повертає список предметів, оцінки з яких можуть зберігатись базі"""
        return [(x[1] + char) for x in read_query_list("pragma table_info(student_grades)")][1:]

    @staticmethod
    def print_excellent_student(subj):
        """Метод виводить на екран список з іменем та прізвищем відмінників по предмету, переданому в якості
                аргумента"""
        extract = tuple([(x[0]) for x in read_query_list("SELECT id FROM student_grades WHERE " + subj + " = 5")])
        for x in range(len(extract)):
            print('-', *read_query_list("SELECT stud_name FROM students WHERE id = " + str(extract[x]))[0], end=' ')
            print(*read_query_list("SELECT stud_surname FROM students WHERE id = " + str(extract[x]))[0])

    @staticmethod
    def get_excellent_student(subj):
        """Метод повертає список кортежів з іменем та прізвищем відмінників по предмету, переданому в якості
        аргумента"""
        extract = tuple([(x[0]) for x in read_query_list("SELECT id FROM student_grades WHERE " + subj + " = 5")])
        list_person = []
        for x in range(len(extract)):
            list_person = [x for x in
                           read_query_list("SELECT stud_name, stud_surname FROM students WHERE id in " + str(extract))]
        return list_person

    @staticmethod
    def get_students_list():
        """Метод повертає список з імен та прізвищ студентів з бази"""
        return read_query_list("SELECT stud_name, stud_surname FROM students")

    @staticmethod
    def find_a_student_by_id(student_id):
        """Метод повертає ім'я та прізвище студенту за переданими номером студентського квитка в якості аргумента"""
        return read_query_list('SELECT stud_name, stud_surname FROM students WHERE students.student_id = "'
                               + student_id + '"')

    @staticmethod
    def get_info_about_student(name_s, surname_s):
        """Метод повертає всі дані по студенту за переданими іменем та прізвищем студента в якості аргументів"""
        return read_query_list(f'SELECT * FROM students INNER JOIN student_grades ON students.id = student_grades.id '
                               f'WHERE students.stud_name = "{name_s}" AND students.stud_surname = "{surname_s}"')

    @staticmethod
    def print_info_about_student(all_info_list):
        """Метод виводить на екран всі дані з бази про студента. В якості аргумента може приймати кортеж або список
        в програмі приймає розпакований результат методу get_info_about_student()"""
        print(f"\nУ базі даних знайдено дані на студента із зазначеними іменем та прізвищем:\n"
              f"\t\t№ запису в базі:  -{all_info_list[0]}-\t| {all_info_list[2]} {all_info_list[3]} |\n"
              f"\t\tСтудентський квиток:\t| {all_info_list[1]} |\n"
              f"\t\tФакультет {all_info_list[4]}, група {all_info_list[5]}\n"
              f"На даний момент в базі проставлені такі оцінки:")
        print("|", *User.get_list_of_subjects(' |'))
        print("|", end='')
        for i in range(len(all_info_list[7:])):
            if all_info_list[i + 7]:
                print(" " * (len(
                    [(x[1] + '\n') for x in read_query_list("pragma table_info(student_grades)")][1:][i]) - 1),
                      all_info_list[i + 7], " |", sep='', end='')
            else:
                print(" ", "-" * (len(
                    [(x[1] + '\n') for x in read_query_list("pragma table_info(student_grades)")][1:][i]) - 1), " |",
                      sep='', end='')
        print("\n")

    @staticmethod
    def add_student_personal_info(stud_id_, stud_name_, stud_surname_, stud_faculty_, stud_group_):
        """Метод додає анкетні дані в базу студентів, приймаючи в якості аргументів ці значення. В програмі їх вводить
        користувач"""
        list_of_params = stud_id_, stud_name_, stud_surname_, stud_faculty_, stud_group_
        update_query(list_of_params, "INSERT INTO students ('student_id', 'stud_name', 'stud_surname', 'stud_faculty', "
                                     "'stud_group') VALUES (?, ?, ?, ?, ?)")

    @staticmethod
    def add_student_personal_grades(param):
        """Метод додає оцінки в базу студентів, приймаючи в якості аргументів список цих значень. В програмі їх вводить
                користувач"""
        update_query(param, "INSERT INTO student_grades (" + str(User.get_list_of_subjects())[1:-1] + ") VALUES (" +
                     "?, " * (len(User.get_list_of_subjects()) - 1) + "?)")

    def change_student_info(self, id_, student_id_, stud_name_, stud_surname_, stud_faculty_, stud_group_):
        """Метод змінює анкетні дані в базі студентів, приймаючи в якості аргументів ці значення. В програмі їх вводить
                користувач"""
        self._id = id_
        self._student_id = student_id_
        self._stud_name = stud_name_
        self._stud_surname = stud_surname_
        self._stud_faculty = stud_faculty_
        self._stud_group = stud_group_
        params = self._student_id, self._stud_name, self._stud_surname, self._stud_faculty, self._stud_group, self._id

        update_query(params, f"UPDATE students SET student_id = ?, "
                             f"stud_name = ?, "
                             f"stud_surname = ?, "
                             f"stud_faculty = ?, "
                             f"stud_group = ?"
                             f"WHERE id = ?")

    def change_student_personal_grades(self, id_, title, value):
        """Метод змінює оцінку в базі студентів, приймаючи в якості аргументів це значення. В програмі їх вводить
                        користувач. Також в якості аргумента програма приймає заголовок стовбця (назва предмету) та
                        унікальний id студента"""
        self._id = id_
        list_of_params = []

        update_query(list_of_params,
                     f"UPDATE student_grades SET {title} = {value} WHERE student_grades.id = {self._id}")


student_title_list = ["№ запису в базі", "Студентський квиток", "Ім'я", "Прізвище", "Факультет", "Група"]
check_exit = True
while check_exit:
    login_obj = User()
    radio_button = input("\nВиберіть подальший варіант дій:"
                         "\n                               - Зайти як користувач:_______________ 1"
                         "\n                               - Зайти як адміністратор:____________ 2"
                         "\n                               - Завершити роботу:__________________ 3"
                         "\n\nВведіть цифру для вашого варіанту дій: ")

    if radio_button == '1':
        print('\nВи вибрали пункт "Зайти як користувач"...')
        check_exit_user = True
        while check_exit_user:
            r_b_user = input("\nВиберіть подальший варіант дій:"
                             "\n                           - Отримати список відмінників:_____________________ 1"
                             "\n                           - Отримати список всіх студентів:__________________ 2"
                             "\n                           - Знайти студента за номером студентьского:________ 3"
                             "\n                           - Отримати повну інформацію про певного студента:__ 4"
                             "\n                           - Вийти в загальне меню:___________________________ 5"
                             "\n\nВведіть цифру для вашого варіанту дій: ")

            if r_b_user == '1':
                print("\nСтуденти, дані яких внесені в базу, мають оцінки з таких предметів:\n\n",
                      "*" * (len(max(User.get_list_of_subjects("\n"), key=len)) - 1), "\n",
                      *User.get_list_of_subjects("\n"), "*" * (len(max(User.get_list_of_subjects("\n"), key=len)) - 1),
                      "\n")
                ex_stud = ' '
                while ex_stud:
                    ex_stud = input("Впишіть або скопіюйте назву предмету, щоб отримати список відмінників з нього\n"
                                    "(для виходу в меню вищого рівня введіть пустий рядок): ")
                    if not ex_stud:
                        print("\nВибрано перехід в меню вищого рівня...")
                        continue
                    if ex_stud not in User.get_list_of_subjects():
                        print("\nВи ввели неіснучу дисципліну або припустилися помилки в написанні. \n"
                              "Спробуйте ще раз (або введіть пустий рядок, якщо бажаєте вийти в меню рівнем вище).\n")
                        continue
                    if ex_stud:
                        # print(login_obj.get_excellent_student(ex_stud))
                        # if len(login_obj.get_excellent_student(ex_stud)):
                        #     print("\nНа жаль, жоден студент не має оцінки відмнно з предмету", ex_stud)
                        #     continue
                        print(f"\nСписок відмінників з предмету '{ex_stud}':")
                        login_obj.print_excellent_student(ex_stud)
                        print("\n")

            elif r_b_user == '2':
                print("\nСписок імен та прізвищ всіх студентів, дані про яких внесені в базу:")
                for x in range(len(User.get_students_list())):
                    print("-", *User.get_students_list()[x])

            elif r_b_user == '3':
                print("\nВи вибрали пункт з пошуком студента за номером документа.")
                try:
                    print("У базі знайдено відповідність:\n-",
                          *login_obj.find_a_student_by_id(input("Введіть номер студентського квитка: "))[0])
                except IndexError:
                    print("За вказаним номером відповідностей не знайдено")

            elif r_b_user == '4':
                print("Ви вибрали пункт отримання повної інформації про студента.")
                name = input("Введіть ім'я студента: ")
                surname = input("Введіть прізвище студента: ")
                try:
                    User.print_info_about_student(*User.get_info_about_student(name, surname))
                except TypeError:
                    print("\n", "*" * 60, "\nЗа вказаними іменем та прізвищем записів в базі не знайдено.\n"
                                          "Перевірте правильність введених даних.\n", "*" * 60, sep='')

            elif r_b_user == '5':
                check_exit_user = False
                print("Вибрано варіант виходу в загальне меню.")

            else:
                print("\nВи ввели неіснучий варіант вибору. Спробуйте ще раз.")
                t = input("Для цього натисніть клавішу 'Enter'...")

    elif radio_button == '2':
        print('\nВи вибрали пункт "Зайти як адміністратор"...')
        check_exit_admin = True
        while check_exit_admin:
            r_b_admin = input("\nВиберіть подальший варіант дій:"
                              "\n                           - Додати в базу новий запис про студента___________ 1"
                              "\n                           - Змінити дані в існучому записі про студента:_____ 2"
                              "\n                           - Вийти в загальне меню:___________________________ 3"
                              "\n\nВведіть цифру для вашого варіанту дій: ")

            if r_b_admin == '1':
                print("Вибрано пункт введення нового запису.\n"
                      "Будь ласка, введіть акетні дані студента:")
                stud_name = input("\t\t- ім'я студента: ")
                stud_surname = input("\t\t- прізвище студента: ")
                login_obj.add_student_personal_info(
                    input("\t\t- номер студентського: "),
                    stud_name,
                    stud_surname,
                    input("\t\t- факультет студента: "),
                    input("\t\t- група студента: "))

                print("\nІнформацію внесено в базу. Далі необхідно ввести оцінки цього студента.\n"
                      "Якщо за запитаним предметом студент не має оцінок, вводити пустий рядок.\nРозпочнемо:")
                list_of_grades = [input(f"- введіть оцінку з предмету '{User.get_list_of_subjects()[x]}': ") for x in
                                  range(len(User.get_list_of_subjects()))]
                list_of_grades = [(int(list_of_grades[x]) if list_of_grades[x].isdigit() else None) for x in
                                  range(len(list_of_grades))]
                User.add_student_personal_grades(list_of_grades)

                print(f"\nПеревіряємо введену інформацію. Для цього шукаємо дані про щойно \n"
                      f"зареєстрованого студента за іменем '{stud_name}' та прізвищем '{stud_surname}'...")
                User.print_info_about_student(*User.get_info_about_student(stud_name, stud_surname))

            elif r_b_admin == '2':
                print("\nВибрано пункт зміни даних в існуючому записі про студента.\n"
                      "Загальний список студентів в базі:")
                for x in range(len(User.get_students_list())):
                    print("-", *User.get_students_list()[x])
                print("\nБудь ласка, введіть акетні дані студента, \nінформацію щодо якого треба змінити:")
                stud_name = input("\t\t- ім'я студента: ")
                stud_surname = input("\t\t- прізвище студента: ")
                try:
                    User.print_info_about_student(*User.get_info_about_student(stud_name, stud_surname))
                except TypeError:
                    print("\n", "*" * 60, "\nЗа вказаними іменем та прізвищем записів в базі не знайдено.\n"
                                          "Перевірте правильність введених даних.\n", "*" * 60, sep='')
                    continue

                zipped_list = list(zip(student_title_list,
                                       *User.get_info_about_student(stud_name, stud_surname),
                                       [x[1] for x in read_query_list("pragma table_info(students)")]
                                       ))
                list_of_values = [zipped_list[0][1], zipped_list[1][1], zipped_list[2][1], zipped_list[3][1],
                                  zipped_list[4][1], zipped_list[5][1], ]

                print("------------Виконаємо прохід по полям для зміни відповідних даних------------\n"
                      "- для того, щоб залишити в базі попередне значення, введіть пустий рядок\n"
                      "- для заміни даних - введіть нове значення\n\n - ",
                      zipped_list[0][0], ": ", zipped_list[0][1], "                          ...без змін...\n", sep='')
                id_for_csi_func = zipped_list.pop(0)

                for j, subj in enumerate(zipped_list, 1):
                    i = input(f"- наявні дані в графі '{subj[0]}': {subj[1]} | Введіть нове значення: ")
                    if i == "":
                        print("\t\t\t...запис залишається без змін...", subj[0], "=", list_of_values[j])
                    else:
                        list_of_values[j] = i
                login_obj.change_student_info(list_of_values[0], list_of_values[1], list_of_values[2],
                                              list_of_values[3], list_of_values[4], list_of_values[5])

                zipped_subjects_grades_list = (list(zip(
                    User.get_list_of_subjects(),
                    User.get_info_about_student(list_of_values[2], list_of_values[3])[0][7:])
                )
                )
                for subj in zipped_subjects_grades_list:
                    i = input(f"- наявна оцінка з '{subj[0]}': {subj[1]} | ")
                    if i == "":
                        print("\t\t\t...оцінка залишається без змін...", subj[0], "=", subj[1])
                    else:
                        login_obj.change_student_personal_grades(list_of_values[0], subj[0], int(i))
                print("Дані успішно змінено")

            elif r_b_admin == '3':
                check_exit_admin = False
                print("Вибрано варіант виходу в загальне меню.")
            else:
                print("\nВи ввели неіснучий варіант вибору. Спробуйте ще раз.")
                t = input("Для цього натисніть клавішу 'Enter'...")

    elif radio_button == '3':
        print('\nРобота програми завершується за вибором користувача.')
        check_exit = False

    else:
        print("\nВи ввели неіснучий варіант вибору. Спробуйте ще раз.")
        t = input("Для цього натисніть клавішу 'Enter'...")
