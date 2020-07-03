import random
import sqlite3


STUD_DB = "Student_DB_09v_test_3.db"
FACULTIES = ['InOrgChemistry', 'OrgChemistry', 'Bio', 'Energetic', 'Mechanical', 'Physical']
SUBJECTS = ['Inorganic Chemistry', 'Organic Chemistry', 'Physics', 'Mechanics', 'Electrical Engineering', 'ACS', 'ITT',
            'Biology', 'Economy', 'Philosophy', 'History', 'Psychology', 'Jurisprudence', 'TMB', 'TS']


class ContextManagerForDBConnect:
    """Контекстний менеджер для відкриття та закриття бази даних SQL"""

    def __init__(self, name_db):
        self._name_db = name_db

    def __enter__(self):
        self._connect = sqlite3.connect(self._name_db)
        return self._connect

    def __exit__(self, *args):
        self._connect.close()


def update_query(params, query=""):
    """Функція для запису даних в базу"""
    with ContextManagerForDBConnect(STUD_DB) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
        except sqlite3.OperationalError as e:
            print("Error while downloading data: " + query)
            print(e)


with open("name.txt") as file:
    lines_name = file.readlines()
with open("surname.txt") as file:
    lines_surname = file.readlines()

list_of_group = []
for faculty in FACULTIES:
    update_query([faculty], "INSERT INTO faculty ('name_of_faculty') VALUES (?)")
    list_of_group.extend([faculty[:1]+'-20-1', faculty[:1]+'-20-2'])
for group in list_of_group:
    update_query([group], "INSERT INTO groups ('name_of_group') VALUES (?)")

for SUBJECT in SUBJECTS:
    update_query([SUBJECT], "INSERT INTO subjects ('name_subject') VALUES (?)")

curators_name = []
curators_surname = []
for i in range(15):
    name = lines_name[i][:-1]
    surname = lines_surname[i][:-1]
    curators_name.append(name)
    curators_surname.append(surname)
    lines_name.pop(i)
    lines_surname.pop(i)
for i in range(len(curators_name)):
    update_query([curators_name[i], curators_surname[i]], "INSERT INTO curators ('name_curator', 'surname_curator') "
                                                          "VALUES (?, ?)")

students_name = []
students_surname = []
for i in range(120):
    name = lines_name[i][:-1]
    surname = lines_surname[i][:-1]
    students_name.append(name)
    students_surname.append(surname)
    lines_name.pop(i)
    lines_surname.pop(i)

#  В наступному циклі при розподіленні на факультет группа обирається випадково, але з тих, що відповідають факультету
for i in range(len(students_name)):
    rand_faculty = random.randint(1, len(FACULTIES))
    list_of_params = [students_name[i], students_surname[i], rand_faculty,
                      (2*rand_faculty-random.randint(0, 1)), random.randint(1, len(curators_name))]
    update_query(list_of_params, "INSERT INTO students ('stud_name', 'stud_surname', 'id_stud_faculty', "
                                 "'id_stud_group', 'id_curator') VALUES (?, ?, ?, ?, ?)")

for student_id in range(1, (len(students_name)+1)):
    for subj_id in range(1, (len(SUBJECTS)+1)):
        for i in [3, 4, 4, 5, 5]:   # Для того, щоб середній бал студентів був більшим 4 знижуємо ймовірність трійок
            list_of_params = [random.randint(i, 5), student_id, subj_id]
            update_query(list_of_params, f"INSERT INTO grades ('grade', 'stud_id', subj_id) VALUES (?, ?, ?)")
