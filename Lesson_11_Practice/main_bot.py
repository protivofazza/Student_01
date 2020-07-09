from telebot import TeleBot, types
from config import TOKEN
from models import Person, Status
from schemas import PersonSchema, StatusSchema
from mongoengine import DoesNotExist

bot = TeleBot(TOKEN)

STATUS_TABLE = (
    {
        'text': "Будь ласка, введіть ваше ім'я",
        'title': 'name'
    },
    {
        'text': 'Будь ласка, введіть ваше прізвище',
        'title': 'surname'
    },
    {
        'text': 'Будь ласка, введіть ваш телефон у форматі +380xxxxxxxxx',
        'title': 'phone_number'
    },
    {
        'text': 'Будь-ласка, введіть ваш e-mail у форматі email@site.com',
        'title': 'email'
    },
    {
        'text': 'Будь-ласка, введіть вашу адресу',
        'title': 'address'
    },
    {
        'text': 'Будь-ласка, напишіть ваші примітки, які ви, можливо, хочете додати до цієї інформації',
        'title': 'info'
    }
)


def add_new_data_in_db(person, id_):
    global status
    if status.status == 6:
        status.status = -1
        status.update(status=status.status)
        # new_person = {}
    person_upd = Person.objects.filter(id=id_)
    person_upd.update(**person)


def info_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("Без додаткової інформації", callback_data="no_info")
    ]
    kb.add(*buttons)
    return kb


def is_email_valid(email: str):
    s = email.find('@', 1, -4)
    if s == -1:
        return False
    d = email.find('.', s + 2, len(email) - 2)
    if d == -1:
        return False
    if email[s-1] == '.' or email[0] == '.':
        return False
    for i in range(s):
        if not any([email[i].isdigit(), email[i].isalpha(), email[i] == '.']):
            return False
    for i in range(s+1, len(email)):
        if not any([email[i].isdigit(), email[i].isalpha(), email[i] == '.']):
            return False
    return True


def is_phone_valid(phone: str):
    if not phone[0] == '+':
        return False
    if not len(phone) == 13:
        return False
    if not phone[1:].isdigit():
        return False
    return True


class Send:

    @staticmethod
    def request_new_data(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text=f'{STATUS_TABLE[status.status]["text"]}',
            reply_markup=info_kb() if STATUS_TABLE[status.status]["title"] == "info" else None
        )

    @staticmethod
    def report_success(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text="Дані про щойно анкетованого успішно додані в базу\n"
                 "Натисніть /start, щоб внести нові дані"
        )

    @staticmethod
    def greetings(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text="Привіт, це бот для заповнення анкетних даних"
        )

    @staticmethod
    def invitation(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text="Введіть /start"
        )

    @staticmethod
    def continuation(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text="Роботу бота було перервано. Продовжимо з останнього пункту"
        )

    @staticmethod
    def error_phone_message(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text=f'Невірний формат телефонного номеру: \n{STATUS_TABLE[2]["text"]}'
        )

    @staticmethod
    def error_email_message(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text=f'Невірний формат e-mail: \n{STATUS_TABLE[3]["text"]}'
        )


try:
    status = Status.objects.get()
except DoesNotExist:
    status = Status.objects.create(status=-1).save()


if status.status != -1:
    print("Виявлено незакінчене введення на етапі", status.status)
    person_obj = Person.objects.filter(id=status.person_id.id)[0]

new_person = {}


@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    global status
    if status.status == -1:
        status.status = 0
        status.update(status=status.status)
        Send.greetings(message.chat.id)
        global new_person
        new_person = {}
        global person
        person = PersonSchema().load(new_person)
        global person_obj
        person_obj = Person.objects.create(**person).save()
        status.update(person_id=person_obj.id)
        Send.request_new_data(message.chat.id)
    else:
        Send.continuation(message.chat.id)


@bot.message_handler(content_types=['text'])
def data_handler(message: types.Message):
    global status
    if status.status == -1:
        Send.invitation(message.chat.id)
    elif status.status < len(STATUS_TABLE):
        if STATUS_TABLE[status.status]['title'] == 'phone_number':
            if not is_phone_valid(message.text):
                Send.error_phone_message(message.chat.id)
                return None
        elif STATUS_TABLE[status.status]['title'] == 'email':
            if not is_email_valid(message.text):
                Send.error_email_message(message.chat.id)
                return None
        global new_person
        new_person = {}
        new_person[STATUS_TABLE[status.status]['title']] = message.text
        add_new_data_in_db(new_person, person_obj.id)
        status.status += 1
        status.update(status=status.status)
        if status.status < len(STATUS_TABLE):
            Send.request_new_data(message.chat.id)
        else:
            add_new_data_in_db(new_person, person_obj.id)
            status.status = -1
            status.update(status=status.status)
            Send.report_success(message.chat.id)


@bot.callback_query_handler(func=lambda x: x.data == 'no_info')
def no_info_callback_handler(call):
    new_person['info'] = "Без додаткової інформації"
    add_new_data_in_db(new_person, person_obj.id)
    Send.report_success(call.message.chat.id)
    status.status = -1
    status.update(status=status.status)


bot.polling()
