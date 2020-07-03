"""
1) Создать базу данных студентов (ФИО, группа, оценки, куратор студента, факультет).
Написать РЕСТ ко всем сущностям в бд (работа со студентами, оценками, кураторами, факультетами).
Создать отдельный контроллер, который будет выводить отличников по факультету.
2) Создать модуль, который будет заполнять базу данных
случайными валидными значениями (минимум 100 студентов).
"""

from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)
STUD_DB = "Student_DB_09.db"


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
        except sqlite3.OperationalError as e:
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
        except sqlite3.OperationalError as e:
            print("Error while downloading data: " + query)
            print(e)


@app.route('/students', methods=['GET', 'POST'])
@app.route('/students/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def students(user_id=None):
    if request.method == 'GET':
        if user_id:
            try:
                list_data = read_query_list(f"SELECT students.id, stud_name, stud_surname, "
                                            f"name_of_faculty, name_of_group, "
                                            f"name_curator, surname_curator "
                                            f"FROM students "
                                            f"INNER JOIN faculty "
                                            f"ON students.id_stud_faculty = faculty.id "
                                            f"INNER JOIN groups "
                                            f"ON students.id_stud_group = groups.id "
                                            f"INNER JOIN curators "
                                            f"ON students.id_curator = curators.id "
                                            f"WHERE students.id = {user_id}")[0]

                data = {'stud_name': list_data[1], 'stud_surname': list_data[2],
                        "name_of_faculty": list_data[3], "name_of_group": list_data[4],
                        "name_curator": list_data[5], "surname_curator": list_data[6]}
            except IndexError:
                data = f"Error 404: За вказаним ID стдента '{user_id}' немає записів в базі"
        else:
            data = dict(
                [(x[0], {'stud_name': x[1], 'stud_surname': x[2]}) for x in read_query_list("SELECT id, stud_name, "
                                                                                            "stud_surname "
                                                                                            "FROM students")])
        return jsonify(data)

    elif request.method == 'POST':
        # В графе body в postman вводить такой текст:
        # {
        #     "id_stud_faculty": 3,
        #     "id_stud_group": 1,
        #     "id_curator": 5,
        #     "stud_name": "Марк",
        #     "stud_surname": "Ткачов"
        # }
        params_dict = request.json
        list_of_params = [params_dict['stud_name'], params_dict['stud_surname'], params_dict['id_stud_faculty'],
                          params_dict['id_stud_group'], params_dict['id_curator']]

        update_query(list_of_params, "INSERT INTO students ('stud_name', 'stud_surname', 'id_stud_faculty', "
                                     "'id_stud_group', 'id_curator') VALUES (?, ?, ?, ?, ?)")
        return jsonify(request.json)

    elif request.method == 'PUT':

        params_dict = request.json
        for param in params_dict.items():
            params = param[1],
            update_query(params, f"UPDATE students SET '{param[0]}' = ? WHERE id = {user_id}")
        return jsonify(request.json)

    elif request.method == 'DELETE':
        params = []
        update_query(params, f"DELETE FROM students WHERE id = {user_id}")
        return jsonify(request.json)


@app.route('/marks/<int:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def marks(user_id=None):
    if request.method == 'GET':
        data_marks = read_query_list(f"SELECT students.id, stud_name, stud_surname, name_subject, grade "
                                     f"FROM students "
                                     f"INNER JOIN grades "
                                     f"ON students.id = grades.stud_id "
                                     f"INNER JOIN subjects "
                                     f"ON grades.subj_id = subjects.id "
                                     f"WHERE students.id = {user_id}")

        subj_list = list(set([x[3] for x in data_marks]))
        subj_list.sort()

        marks_list = [(x, [y[1] for y in [(x[3], x[4]) for x in data_marks] if y[0] == x]) for x in subj_list]
        data = dict([("stud_name", data_marks[0][1]), ("stud_surname", data_marks[0][2]), *marks_list])
        return jsonify(data)

    elif request.method == 'POST':
        # В графе body в postman вводить данные в такой форме:
        # {
        #     "БЖД": 3,
        #     "Вища математика": 4,
        #     "ТММ": 4,
        #     "Хімія загальна": 5
        # }

        marks_dict = request.json
        subjects_dict = dict(read_query_list(f"SELECT name_subject, id FROM subjects "))
        for mark in marks_dict.items():
            params = mark[1], int(user_id), subjects_dict[mark[0]]
            update_query(params, f"INSERT INTO grades ('grade', 'stud_id', subj_id) VALUES (?, ?, ?)")
        return jsonify(request.json)

    elif request.method == 'PUT':
        # В графе body в postman вводить данные в такой форме:
        # {
        #     "subject": "БЖД",
        #     "new_data": 3,
        #     "old_data": 5
        # }

        mark_dict = request.json
        mark_list = list(mark_dict.values())
        subjects_dict = dict(read_query_list(f"SELECT name_subject, id FROM subjects "))
        id_mark = read_query_list(f"SELECT id "
                                  f"FROM grades "
                                  f"WHERE grades.subj_id = {subjects_dict[mark_list[0]]} "
                                  f"AND grades.stud_id = {int(user_id)} AND grade = {mark_list[2]} LIMIT 1")[0][0]

        params = [mark_list[1], ]
        update_query(params,
                     f"UPDATE grades SET 'grade' = ? WHERE grades.subj_id = {subjects_dict[mark_list[0]]} "
                     f"AND grades.stud_id = {int(user_id)} AND grade = {mark_list[2]} AND id = {id_mark}")
        return jsonify(request.json)

    elif request.method == 'DELETE':
        # В графе body в postman вводить данные в такой форме:
        # {
        #     "subject": "БЖД",
        #     "del_data": 3
        # }

        mark_dict = request.json
        mark_list = list(mark_dict.values())
        subjects_dict = dict(read_query_list(f"SELECT name_subject, id FROM subjects "))
        id_mark = read_query_list(f"SELECT id "
                                  f"FROM grades "
                                  f"WHERE grades.subj_id = {subjects_dict[mark_list[0]]} "
                                  f"AND grades.stud_id = {int(user_id)} AND grade = {mark_list[1]} LIMIT 1")[0][0]

        params = []
        update_query(params, f"DELETE FROM grades "
                             f"WHERE grades.subj_id = {subjects_dict[mark_list[0]]} "
                             f"AND grades.stud_id = {int(user_id)} AND grade = {mark_list[1]} AND id = {id_mark}")
        return jsonify(request.json)


@app.route('/curators', methods=['GET', 'POST'])
@app.route('/curators/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def curators(user_id=None):
    if request.method == 'GET':
        if user_id:
            students_of_curator = read_query_list(f"SELECT name_curator, surname_curator, stud_name, "
                                                  f"stud_surname, students.id "
                                                  f"FROM curators "
                                                  f"INNER JOIN students "
                                                  f"ON curators.id = students.id_curator "
                                                  f"WHERE curators.id = {user_id}")
            try:
                if students_of_curator:
                    data = dict([('name_curator', students_of_curator[0][0]),
                                 ('surname_curator', students_of_curator[0][1]),
                                 ('students', dict([(x[4],
                                                     dict((('stud_name', x[2]), ('stud_surname', x[3])))) for x in
                                                    students_of_curator]))])
                else:
                    curator_name = read_query_list(f"SELECT name_curator, surname_curator "
                                                   f"FROM curators "
                                                   f"WHERE curators.id = {user_id}")
                    data = dict([('name_curator', curator_name[0][0]),
                                 ('surname_curator', curator_name[0][1]),
                                 ('students', "У куратора немає студентів")])
            except IndexError:
                data = "Error 404: Немає записів про кураторів за вказаним індексом"
        else:
            data = dict(
                [(x[0],
                  {'name_curator': x[1], 'surname_curator': x[2]}) for x in read_query_list("SELECT curators.id, "
                                                                                            "name_curator, "
                                                                                            "surname_curator "
                                                                                            "FROM curators")])
        return jsonify(data)

    elif request.method == 'POST':
        # В графе body в postman вводить такой текст:
        # {
        #     "name_curator": "Владислав",
        #     "surname_curator": "Гопко"
        # }
        params_dict = request.json
        list_of_params = params_dict['name_curator'], params_dict['surname_curator']

        update_query(list_of_params, "INSERT INTO curators ('name_curator', 'surname_curator') VALUES (?, ?)")
        return jsonify(request.json)

    elif request.method == 'PUT':
        # В графе body в postman вводить данные в такой форме:
        # {
        #     "name_curator": "Влада",
        #     "surname_curator": "Гопко"
        # }

        params_dict = request.json
        for param in params_dict.items():
            params = param[1],
            update_query(params, f"UPDATE curators SET '{param[0]}' = ? WHERE id = {user_id}")
        return jsonify(request.json)

    elif request.method == 'DELETE':
        params = []
        update_query(params, f"DELETE FROM curators WHERE id = {user_id}")
        return jsonify(request.json)


@app.route('/faculty', methods=['GET', 'POST'])
@app.route('/faculty/<int:subj_id>', methods=['GET', 'PUT', 'DELETE'])
def faculty(subj_id=None):
    if request.method == 'GET':
        if subj_id:
            students_on_faculty = read_query_list(f"SELECT faculty.id, name_of_faculty, stud_name, "
                                                  f"stud_surname, students.id "
                                                  f"FROM faculty "
                                                  f"INNER JOIN students "
                                                  f"ON faculty.id = students.id_stud_faculty "
                                                  f"WHERE faculty.id = {subj_id}")
            try:
                if students_on_faculty:
                    data = dict([('name_of_faculty', students_on_faculty[0][1]),
                                 ('students', dict([(x[4],
                                                     dict((('stud_name', x[2]), ('stud_surname', x[3])))) for x in
                                                    students_on_faculty]))])
                else:
                    faculty_name = read_query_list(f"SELECT name_of_faculty "
                                                   f"FROM faculty "
                                                   f"WHERE faculty.id = {subj_id}")
                    data = dict([('name_of_faculty', faculty_name[0][0]),
                                 ('students', "Поки що немає внесених даних про студентів на факультеті")])
            except IndexError:
                data = "Error 404: Немає записів про факультети за вказаним індексом"
        else:
            data = dict(
                [(x[0],
                  {'name_of_faculty': x[1]}) for x in read_query_list("SELECT faculty.id, "
                                                                      "name_of_faculty "
                                                                      "FROM faculty")])
        return jsonify(data)

    elif request.method == 'POST':
        # В графе body в postman вводить такой текст:
        # {
        #     "name_of_faculty": "АКС",
        # }
        params_dict = request.json
        list_of_params = [params_dict['name_of_faculty'], ]

        update_query(list_of_params, "INSERT INTO faculty ('name_of_faculty') VALUES (?)")
        return jsonify(request.json)

    elif request.method == 'PUT':
        # В графе body в postman вводить данные в такой форме:
        # {
        #     "name_of_faculty": "ІТ"
        # }
        params_dict = request.json
        for param in params_dict.items():
            params = param[1],
            update_query(params, f"UPDATE faculty SET '{param[0]}' = ? WHERE id = {subj_id}")
        return jsonify(request.json)

    elif request.method == 'DELETE':
        params = []
        update_query(params, f"DELETE FROM faculty WHERE id = {subj_id}")
        return jsonify(request.json)


@app.route('/excellent/<int:faculty_id>', methods=['GET'])
def excellent(faculty_id=None):
    if request.method == 'GET':
        required_average_mark = 4.7
        list_of_excellent = read_query_list(f"SELECT id, name, surname, avg_mark, faculty FROM "
                                            f"(SELECT AVG (grade) AS avg_mark, students.id AS id, "
                                            f"stud_name AS name, stud_surname AS surname, name_of_faculty AS faculty "
                                            f"FROM students "
                                            f"INNER JOIN faculty "
                                            f"ON students.id_stud_faculty = faculty.id "
                                            f"INNER JOIN grades "
                                            f"ON students.id = grades.stud_id "
                                            f"WHERE students.id_stud_faculty = {faculty_id} "
                                            f"GROUP BY students.id) "
                                            f"WHERE avg_mark >= {required_average_mark}")
        try:
            if list_of_excellent:
                data = dict([(x[0], {"stud_name": x[1], "stud_surname": x[2], "average_mark": x[3]})
                             for x in list_of_excellent])
            else:
                data = f"На жаль, на факультеті " \
                       f"'{read_query_list(f'SELECT name_of_faculty FROM faculty WHERE id = {faculty_id}')[0][0]}' " \
                       f"немає студентів з середнім балом рівним або вище {required_average_mark}"
        except IndexError:
            data = "Error 404: Немає записів про факультети за вказаним індексом"
        return jsonify(data)


app.run(debug=True)
