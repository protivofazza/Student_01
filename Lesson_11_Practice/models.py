import mongoengine as me

me.connect("Practice_11")


class Person(me.Document):
    name = me.StringField(min_length=1, max_length=128)
    surname = me.StringField(min_length=1, max_length=128)
    phone_number = me.StringField(min_length=13, max_length=13)
    email = me.EmailField()
    address = me.StringField(min_length=2, max_length=512)
    info = me.StringField(min_length=2, max_length=4096)

    def __str__(self):
        return f"ім'я: {self.name} прізвище: {self.surname}\n" \
               f"тел.: {self.phone_number}\n" \
               f"e-mail: {self.email}\n" \
               f"адреса: {self.address}\n" \
               f"примітки: {self.info}"


class Status(me.Document):
    status = me.IntField()
    person_id = me.ReferenceField(Person)
