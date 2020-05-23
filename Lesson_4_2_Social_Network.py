from datetime import datetime
# import getpass
import pickle

accounts_list = []
posts = [[0, 'Title', 'Text', datetime.now().date(), 'Author'], ]


class User:
    def __init__(self, login, user_password, is_admin, date_of_reg=datetime.now().date(), name=None, surname=None,
                 nickname=None):
        self._login = login
        self._password = user_password
        self._is_admin = is_admin
        self._date_of_reg = date_of_reg
        self._name = name
        self._surname = surname
        self._nickname = nickname

    def set_personal_data(self):
        self._name = input("Введіть ім'я (або пропустіть, натиснувши Enter): ")
        if self._name == '':
            self._name = None
        self._surname = input("Введіть прізвище (або пропустіть, натиснувши Enter): ")
        if self._surname == '':
            self._surname = None
        self._nickname = input("Введіть нікнейм (або пропустіть, натиснувши Enter): ")
        if self._nickname == '':
            self._nickname = None
        accounts_list.append([self._login, self._password, self._is_admin, self._date_of_reg, self._name,
                              self._surname, self._nickname])

    def creating_post(self, ):
        num_of_post = posts[-1][0] + 1
        print(f"Знайти пост в ленті можна буде за ідентифікатором id: {num_of_post}")
        title_of_post = input("Введіть заголовок посту: ")
        data_of_post = input("Введіть текст:\n")
        date_of_creating = datetime.now().date()
        post_author = self._login
        posts.append([num_of_post, title_of_post, data_of_post, date_of_creating, post_author])

    def print_info(self):
        len_list = []
        for j, attributes in enumerate(accounts_list, 1):
            len_list.append(attributes[0])
        max_len = len(max(len_list, key=len))
        for j, attributes in enumerate(accounts_list, 1):
            print(f"\n{' ' * (3 - len(str(j)))} {j} | {attributes[0]}{' ' * (max_len - len(attributes[0]))} | "
                  f"дата реєстрації: {attributes[3]} | Пости з номерами:    ", end='')
            for k in posts:
                if attributes[0] == k[4]:
                    print(k[0], '    ', end='', sep='')
        print('\n\n')

    @property
    def is_admin(self):
        return self._is_admin


class Registration:
    admin_pass = '123'

    def __init__(self):
        self._login = None
        self._password = None
        self.is_admin = None
        self.set_login()
        self.set_password()
        self.create_new_user(self._login, self._password)

    def set_login(self, ):
        while self._login is None:
            login = input("Введіть логін користувача: ")
            for account in accounts_list:
                if account[0] == login:
                    print(f"Введений логін '{login}' вже зайнятий іншим користувачем. Спробуйте інший.\n")
                    break
            else:
                self._login = login

    def set_password(self, char_min=8, char_max=16):
        while self._password is None:
            # password = getpass.getpass() - На жаль, імпортована фунція не працює
            password_s = input("Введіть майбутній пароль користувача: ")
            if char_min <= len(password_s) <= char_max:
                if set(password_s) & set('1234567890'):
                    if password_s != password_s.lower() and password_s != password_s.upper():
                        if input('Пароль прияйнято, для остаточної реєстрації введіть його повторно: ') == password_s:
                            # на жаль, імпортована фунція getpass.getpass() не працює
                            self._password = password_s
                            print('---------------------- Пароль зарєєстровано ----------------------\n')
                        else:
                            print("\nЗафіксовано розбіжності при повторному введенні паролю. Спробуйте ще раз.\n")
                    else:
                        print('\nПароль має включати від 8 до 16 символів, і складатися з цифр та літер як верхнього, '
                              'так і нижнього регістру! \nПароль відхилено через відсутність літер різних регістрів.'
                              '\nЗмініть пароль та спробуйте ввести його знову.\n')
                else:
                    print('\nПароль має включати від 8 до 16 символів, і складатися з цифр та літер як верхнього, '
                          'так і нижнього регістру! \nПароль відхилено через відсутність цмфр.'
                          '\nЗмініть пароль та спробуйте ввести його знову.\n')
            else:
                print('\nПароль має включати від 8 до 16 символів, і складатися з цифр та літер як верхнього, '
                      'так і нижнього регістру! \nПароль відхилено через невідповідну кількість знаків.'
                      '\nЗмініть пароль та спробуйте ввести його знову.\n')

    def create_new_user(self, login, password_c):
        if input("Для створення аккаунту користувача просто натисніть 'Enter'\n"
                 "Якщо ви створюєте новий аккаунт адміністратора - введіть код доступу: ") == Registration.admin_pass:
            self.is_admin = True
            print(f"\nКод доступу вірний. Створено аккаунт адміна з логіном {login}")
        else:
            self.is_admin = False
            print(f"\nСтворено аккаунт користувача з логіном {login}")
        user_from_reg = User(login, password_c, self.is_admin)
        user_from_reg.set_personal_data()


class Authorization:

    def logging(self, login, password_a):
        for k, acc in enumerate(accounts_list):
            if login == acc[0]:
                if password_a == acc[1]:
                    return True, k
                else:
                    print("----------------------- Введено невірний пароль ----------------------")
                    return False, k
        else:
            print("----------------------- Введено неіснуючий логін ---------------------")
            return False, None


try:
    with open('accounts_list.pickle', 'rb') as f:
        accounts_list = pickle.load(f)
    with open('posts.pickle', 'rb') as f:
        posts = pickle.load(f)

except FileNotFoundError:
    print("При спробі програми завантажити попередньо збережені на диску дані контактів з файлів 'accounts_list.pickle'"
          "\nта 'posts.pickle' файли не було знайдено. При першому збереженні введених даних вказані файли з'являться"
          "\nу папці, в якій запущений срипт. В подальшому стартові дані контактів та постів, збережених при попередніх"
          "\nвиконаннях програми, будуть завантажуватись при запуску програми вже з файлів 'accounts_list.pickle' та "
          "\n'posts.pickle'")

check_exit = True
while check_exit:
    radio_button = input("\nВиберіть подальший варіант дій:"
                         "\n                               - Зайти в існуючий аккаунт:__________ 1"
                         "\n                               - Створити новий аккаунт:____________ 2"
                         "\n                               - Завершити роботу:__________________ 3"
                         "\n\nВведіть цифру для вашого варіанту дій: ")

    if radio_button == '1':
        print('\nВи вибрали пункт "Зайти в існуючий аккаунт"...')
        login_obj = Authorization()
        log = input('Введіть логін: ')
        password = input('Введіть пароль:')
        check_log_in, i = login_obj.logging(log, password)
        if check_log_in:
            print(f"Вхід в аккаунт '{log}' виконано..")
            user = User(accounts_list[i][0], accounts_list[i][1], accounts_list[i][2], accounts_list[i][3],
                        accounts_list[i][4], accounts_list[i][5], accounts_list[i][6])
            if not user.is_admin:
                check_exit_user = True
                while check_exit_user:
                    r_b_user = input("\nВиберіть подальший варіант дій:"
                                     "\n                               - Створити новий пост:_______________ 1"
                                     "\n                               - Вийти з аккаунту:__________________ 2"
                                     "\n\nВведіть цифру для вашого варіанту дій: ")

                    if r_b_user == '1':
                        user.creating_post()
                    elif r_b_user == '2':
                        check_exit_user = False
                        check_log_in = False
                        print("Виконано вихід з аккаунту.")
                    else:
                        print("\nВи ввели неіснучий варіант вибору. Спробуйте ще раз.")
                        t = input("Для цього натисніть клавішу 'Enter'...")

            elif user.is_admin:
                check_exit_admin = True
                while check_exit_admin:
                    r_b_admin = input("\nВиберіть подальший варіант дій:"
                                      "\n                               - Переглянути всіх користувачів______ 1"
                                      "\n                               - Переглянути пости користувачів:____ 2"
                                      "\n                               - Вийти з аккаунту:__________________ 3"
                                      "\n\nВведіть цифру для вашого варіанту дій: ")

                    if r_b_admin == '1':
                        user.print_info()
                    elif r_b_admin == '2':
                        num_post = int(input("Введіть номер посту, що необхідно роздрукувати: "))
                        for post in posts:
                            if num_post == post[0]:
                                print("\n", post[1], "\n", '=' * len(post[2]), "\n", post[2],
                                      "\n", '=' * len(post[2]), "\n", post[3], '\n', sep='')
                    elif r_b_admin == '3':
                        check_exit_admin = False
                        check_log_in = False
                        print("Виконано вихід з аккаунту.")
                    else:
                        print("\nВи ввели неіснучий варіант вибору. Спробуйте ще раз.")
                        t = input("Для цього натисніть клавішу 'Enter'...")

    elif radio_button == '2':
        print('\nВи вибрали пункт "Створити новий аккаунт"...\n')
        reg_id = Registration()
        print(f"\nВи успішно зареєстрували аккаунт. Для подальших дій зайдіть через відповідний пункт меню")

    elif radio_button == '3':
        check_exit = False
        print("Робота програми завершується за вибором користувача.")
        with open('accounts_list.pickle', 'wb') as f:
            pickle.dump(accounts_list, f)
        with open('posts.pickle', 'wb') as f:
            pickle.dump(posts, f)

    else:
        print("\nВи ввели неіснучий варіант вибору. Спробуйте ще раз.")
        t = input("Для цього натисніть клавішу 'Enter'...")
