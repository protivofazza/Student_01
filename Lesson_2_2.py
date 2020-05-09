class Shop:
    total_sold_products = 0

    def __init__(self, name, sold_products=0):
        self.name = name
        self.sold_products = sold_products
        Shop.total_sold_products += self.sold_products
        self.sold_products = 0

    def sale_progress(self, value=0):
        if value == 0:  # При введенні від'ємного числа вважається, що клієнт здав товар у магазин
            try:
                self.sold_products += int(input('Введіть кількість проданих товарів: '))
            except ValueError:
                print('Введене значення має бути цілим числом. Запустіть програму ще раз.')
                exit(21)
        else:
            self.sold_products += value
        Shop.total_sold_products += self.sold_products
        self.sold_products = 0

    @staticmethod
    def check_sales():
        print('загальна кількість товарів, проданих всіма магазинами:', Shop.total_sold_products)


print('Етап 0 - загальна кількість проданих товарів:', Shop.total_sold_products)
shop_1 = Shop('Магазин №1', 1)
shop_2 = Shop('Магазин №2')
print('Етап 1 - ', end='')
Shop.check_sales()
shop_1.sale_progress()
print('Етап 2 - ',  end='')
Shop.check_sales()
shop_1.sale_progress(10)
print('Етап 3 - загальна кількість проданих товарів:', Shop.total_sold_products)
