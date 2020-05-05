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

    def indicate_features(self, notes):
        pass


class Truck(Vehicle):
    def __init__(self, model, vin, maximum_mass, lift_capacity):
        self.model = model
        self.vin = vin
        self.maximum_mass = maximum_mass
        self.lift_capacity = lift_capacity

    def indicate_features(self, presence_of_trailer):
        self.presence_of_trailer = presence_of_trailer


class Car(Vehicle):
    def __init__(self, model, vin, maximum_mass, pass_seats):
        self.model = model
        self.vin = vin
        self.maximum_mass = maximum_mass
        self.pass_seats = pass_seats

    def indicate_features(self, interior_color):
        self.interior_color = interior_color


truck = Truck('Volvo', '2464VCD005678', 22000, 3500)
print(truck.model, truck.vin, truck.maximum_mass, truck.lift_capacity)