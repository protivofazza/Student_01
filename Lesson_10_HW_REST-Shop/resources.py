from flask_restful import Resource
from flask import request, jsonify
from models import Category, Products
from schemas import CategorySchema, ProductsSchema, ValidationError
import json
from mongoengine import DoesNotExist, ValidationError as Val_error


class CategoryResource(Resource):

    def get(self, cat_id=None):
        if cat_id:
            try:
                category = Category.objects.get(id=cat_id)
                category = CategorySchema().dump(category)
                return category
            except DoesNotExist as error:
                data = "За введеним ID наразі немає записів (або отриманий запис має посилання на " \
                   "інший неіснуючий): " + str(error)
                return jsonify(data)
            except Val_error as error:
                data = "Введений ID у невірному форматі: " + str(error)
                return jsonify(data)
        else:
            try:
                categories = Category.objects
                return CategorySchema().dump(categories, many=True)
            except DoesNotExist as error:
                data = "Один з отриманих записів має посилання на інший неіснуючий: " + str(error)
                return data

    def post(self, *args):
        try:
            json_data = json.dumps(request.json)
            result = CategorySchema().loads(json_data)
            res = json.loads(CategorySchema().dumps(result))

            category = Category.objects.filter(id=result['parent_category'])

            # Наступний if не дозволяє створювати підкатегорії другого рівня
            if not category[0].parent_category:
                Category.objects.create(**res).save().to_json()
            else:
                res = "Заборонено створювати підкатегорії другого рівня"
        except ValidationError as error:
            return error.messages
        return res

    def put(self, cat_id=None):
        if not cat_id:
            return "Відсутній id в url"
        json_data = json.dumps(request.json)
        try:
            try:
                category_data = CategorySchema().loads(json_data)
                category_data = json.loads(CategorySchema().dumps(category_data))

                category = Category(id=cat_id)
                parent_category = Category.objects.filter(id=category_data['parent_category'])

                # Наступний if не дозволяє створювати підкатегорії другого рівня
                if not parent_category[0].parent_category:
                    category.update(id=cat_id,
                                    parent_category=parent_category[0].id,
                                    description=category_data['description'],
                                    name=category_data['name'])
                else:
                    category_data = "Заборонено створювати підкатегорії другого рівня"
            except ValidationError as error:
                category_data = error.messages
            return category_data
        except Val_error as error:
            data = "Введений ID у невірному форматі або неіснуючий: " + str(error)
            return data

    def delete(self, cat_id=None):
        if not cat_id:
            return "Відсутній id в url"
        try:
            category_to_delete = Category.objects.get(id=cat_id)
            category_to_delete = CategorySchema().dump(category_to_delete)

            reference_list_child_cat = Category.objects.filter(parent_category=category_to_delete['id'])
            # При видаленні категорії в разі наявності в них підкатегорій наступний блок if/for видаляє всі їх також
            if reference_list_child_cat:
                for category in reference_list_child_cat:
                    # Продукти, що належать до підкатегорії видаляються в наступному циклі for
                    products_to_delete_list = Products.objects.filter(category=category.id)
                    for product in products_to_delete_list:
                        product.delete()
                    category.delete()

            category = Category(id=cat_id)
            # Продукти, що належать до підкатегорії видаляються також разом із нею
            products_to_delete_list = Products.objects.filter(category=category.id)
            for product in products_to_delete_list:
                product.delete()
            category.delete()
            return category_to_delete
        except DoesNotExist as error:
            data = "За введеним ID наразі немає записів: " + str(error)
            return data
        except Val_error as error:
            data = "Введений ID у невірному форматі: " + str(error)
            return data


class ProductsResource(Resource):

    def get(self, prod_id=None):
        if prod_id:
            try:
                products = Products.objects.get(id=prod_id)
                products.number_of_views += 1
                products.save()
                return ProductsSchema().dump(products)
            except DoesNotExist as error:
                data = "За введеним ID наразі немає записів (або отриманий запис має посилання на " \
                       "інший неіснуючий): " + str(error)
                return data
            except Val_error as error:
                data = "Введений ID у невірному форматі:" + str(error)
                return jsonify(data)
        else:
            try:
                return ProductsSchema().dump(Products.objects, many=True)
            except DoesNotExist as error:
                data = "Один з отриманих записів має посилання на інший неіснуючий: " + str(error)
                return data

    def post(self, *args):
        try:
            products = ProductsSchema().load(request.get_json())

            # Наступний if не дозволяє створювати товари в категоріях, лише в підкатегоріях
            category = Category.objects.filter(id=products['category'])
            if category[0].parent_category:
                res = ProductsSchema().dump(Products.objects.create(**products).save())
            else:
                res = "Продукти не можна створювати в категоріях, лише в підкатегоріях"

        except ValidationError as error:
            return error.messages
        except TypeError as error:
            return str(error)
        return res

    def put(self, prod_id=None):
        if not prod_id:
            return "Відсутній id в url"
        json_data = json.dumps(request.json)
        try:
            try:
                products_data = ProductsSchema().loads(json_data)
                products_data = json.loads(ProductsSchema().dumps(products_data))

                products = Products(id=prod_id)
                category = Category.objects.filter(id=products_data['category'])

                # Наступний if не дозволяє переміщати товари в категорії, лише в підкатегорії
                if category[0].parent_category:
                    products.update(id=prod_id,
                                    in_stock=products_data['in_stock'],
                                    category=category[0].id,
                                    model=products_data['model'],
                                    name=products_data['name'],
                                    price=products_data['price']
                                    )
                else:
                    products_data = "Продукти не можна переміщати в категорії, лише в підкатегорії"
            except ValidationError as error:
                products_data = error.messages
            return products_data
        except Val_error as error:
            data = "Введений ID у невірному форматі або неіснуючий: " + str(error)
            return data

    def delete(self, prod_id=None):
        if not prod_id:
            return "Відсутній id в url"
        try:
            product_to_delete = Products.objects.get(id=prod_id)
            product_to_delete = ProductsSchema().dump(product_to_delete)

            product = Products(id=prod_id)
            product.delete()
            return product_to_delete
        except DoesNotExist as error:
            data = "За введеним ID наразі немає записів: " + str(error)
            return data
        except Val_error as error:
            data = "Введений ID у невірному форматі: " + str(error)
            return data


class AmountResource(Resource):

    def get(self):
        products = Products.objects
        amount = 0
        for product in products:
            amount += product.price
        return f"Сума вартості всіх товарів, наявних у магазині становить: {amount} грн"
