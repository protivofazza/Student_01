import mongoengine as me

me.connect('Shop_Lesson_10_hw')


class Category(me.Document):
    name = me.StringField(required=True, min_length=2, max_length=256)
    description = me.StringField(min_length=1, max_length=4096)
    parent_category = me.ReferenceField("self")

    def __str__(self):
        return f"{self.name}"


class Products(me.Document):
    name = me.StringField(required=True, min_length=1, max_length=256)
    model = me.StringField(required=True, min_length=1, max_length=512)
    in_stock = me.IntField(required=True, min_value=0)
    category = me.ReferenceField(Category, required=True)
    price = me.IntField(required=True, min_value=0)
    number_of_views = me.IntField(min_value=0, default=0)

    def __str__(self):
        return f"{self.name} (Category: {self.category}) -- price: {self.price} грн"
