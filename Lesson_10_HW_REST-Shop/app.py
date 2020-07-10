from flask import Flask
from flask_restful import Api
from resources import CategoryResource, ProductsResource, AmountResource


"""Реализовать REST интернет магазина. Модель товар (цена,
доступность, кол-во доступных единиц, категория, кол-во просмотров),
Категория (описание, название). При обращении к конкретному товару
увеличивать кол-во просмотров на 1. Добавить модуль для заполнения
БД валидными данными. Реализовать подкатегории ( доп. Бал). Добавить
роут, который выводят общую стоимость товаров в магазине."""


app = Flask(__name__)
api = Api(app)
api.add_resource(CategoryResource, '/categories', '/categories/<cat_id>')
api.add_resource(ProductsResource, '/products', '/products/<prod_id>')
api.add_resource(AmountResource, '/amount')


if __name__ == '__main__':
    app.run(debug=True)
