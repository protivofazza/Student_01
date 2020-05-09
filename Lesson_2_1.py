class Vehicle:
    country_of_registration = 'Ukraine'

    def __init__(self, model, vin, maximum_mass):
        self.model = model
        self.vin = vin
        self.maximum_mass = maximum_mass

    def set_model(self, type_vehicle):
        self.model = type_vehicle

    def set_vin(self, id_number):
        self.vin = id_number

    def set_maximum_mass(self, mass):
        self.maximum_mass = mass

    def indicate_features(self):
        print('No features')


class Truck(Vehicle):
    def __init__(self, model, vin, maximum_mass, lift_capacity):
        super().__init__(model, vin, maximum_mass)
        self.lift_capacity = lift_capacity

    def indicate_features(self):
        print('It is possible to attach a trailer')

    def __str__(self):
        return f"Модель автомобіля: {self.model}, індивідуальний код кузова: {self.vin}, максимальна дозволена маса: " \
               f"{self.maximum_mass} кг, максимальний вантаж підйомника: {self.lift_capacity} кг, країна реєстрації: " \
               f"{Truck.country_of_registration}"


class Car(Vehicle):
    def __init__(self, model, vin, maximum_mass, pass_seats):
        super().__init__(model, vin, maximum_mass)
        self.pass_seats = pass_seats

    def indicate_features(self):
        print("Ви можете попередньо вибрати колір екстер'єру та інтер'єру авто ")


truck_01 = Truck('Volvo', '2464VCD005678', 22000, 3500)
print(truck_01.model, truck_01.vin, truck_01.maximum_mass, truck_01.lift_capacity)

print(truck_01)
