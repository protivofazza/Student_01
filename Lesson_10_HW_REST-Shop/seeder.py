import random
from models import Category, Products
from schemas import CategorySchema, ProductsSchema

CATEGORIES = (
    {"name": "Ноутбуки та компьютери", "description": "Опис 001"},
    {"name": "Ноутбуки", "parent_category": "Ноутбуки та компьютери", "description": "Опис 001/1"},
    {"name": "Аксесуари", "parent_category": "Ноутбуки та компьютери", "description": "Опис 001/2"},
    {"name": "Планшети", "parent_category": "Ноутбуки та компьютери", "description": "Опис 001/3"},
    {"name": "Оргтехніка", "parent_category": "Ноутбуки та компьютери", "description": "Опис 001/4"},
    {"name": "Компьютери", "parent_category": "Ноутбуки та компьютери", "description": "Опис 001/5"},
    {"name": "Оргтехніка", "parent_category": "Ноутбуки та компьютери", "description": "Опис 001/6"},
    {"name": "Побутова техніка", "description": "Опис 002"},
    {"name": "Велика побутова техніка", "parent_category": "Побутова техніка", "description": "Опис 002/1"},
    {"name": "Кліматична побутова техніка", "parent_category": "Побутова техніка", "description": "Опис 002/2"},
    {"name": "Вбудована побутова техніка", "parent_category": "Побутова техніка", "description": "Опис 002/3"},
    {"name": "Сантехнічна побутова техніка", "parent_category": "Побутова техніка", "description": "Опис 002/4"},
    {"name": "Догляд та прибирання", "parent_category": "Побутова техніка", "description": "Опис 002/5"},
    {"name": "Товари для дому", "description": "Опис 003"},
    {"name": "Декор", "parent_category": "Товари для дому", "description": "Опис 003/1"},
    {"name": "Меблі", "parent_category": "Товари для дому", "description": "Опис 003/2"},
    {"name": "Посуд", "parent_category": "Товари для дому", "description": "Опис 003/3"},
    {"name": "Текстиль", "parent_category": "Товари для дому", "description": "Опис 003/4"},
)


def add_categories():
    for category in CATEGORIES:
        if not category.get("parent_category"):
            if not Category.objects.filter(**category):
                category = CategorySchema().load(category)
                print(f"Category = {Category.objects.create(**category).save()}")


def add_subcategories():
    for category in CATEGORIES:
        if category.get("parent_category"):
            parent_category = Category.objects.filter(name=category['parent_category'])
            category['parent_category'] = str(parent_category[0].id)
            category = CategorySchema().load(category)
            print(f"Subcategory = {Category.objects.create(**category).save()}")


def add_products():
    categories = Category.objects
    for category in categories:
        if category.parent_category:
            for x in range(1, 6):
                product_dict = {}
                product_dict['category'] = category
                product_dict['name'] = 'Товар 00' + product_dict['category'].description[5:] + ' B0' + str(x*100)
                product_dict['model'] = 'Модель Pro ' + product_dict['category'].description[5:] + ' HW_' + str(x*12)
                product_dict['in_stock'] = random.randint(5-x, (50-x*5))
                product_dict['price'] = random.randint(50, 128) * 27
                print(f"Products = {Products.objects.create(**product_dict).save()}")


if __name__ == '__main__':
    add_categories()
    add_subcategories()
    add_products()

    # Category.objects.delete()
    # Products.objects.delete()
