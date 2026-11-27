
from abc import ABC, abstractmethod
from enum import Enum


# ==========================================================
# 1. VEHICLE TYPE ENUM
# ==========================================================

class VehicleType(Enum):
    CAR = "Car"
    BIKE = "Bike"
    VAN = "Van"


# ==========================================================
# 2. ABSTRACT VEHICLE CLASS
# ==========================================================

class Vehicle(ABC):

    def __init__(self, registration_number, mileage):

        self.registration_number = registration_number
        self.mileage = mileage

    # Encapsulation: registration number

    @property
    def registration_number(self):
        return self.__registration_number

    @registration_number.setter
    def registration_number(self, value):

        if not isinstance(value, str) or not value.strip():
            raise ValueError("Invalid registration number")

        self.__registration_number = value

    # Encapsulation: mileage

    @property
    def mileage(self):
        return self.__mileage

    @mileage.setter
    def mileage(self, value):

        if value < 0:
            raise ValueError("Mileage cannot be negative")

        self.__mileage = value

    # Abstract methods

    @abstractmethod
    def daily_rate(self):
        pass

    @abstractmethod
    def late_fee(self, days):
        pass


# ==========================================================
# 3. CAR SUBCLASS
# ==========================================================

class Car(Vehicle):

    def daily_rate(self):
        return 2000

    def late_fee(self, days):
        return days * 500


# ==========================================================
# 4. BIKE SUBCLASS
# ==========================================================

class Bike(Vehicle):

    def daily_rate(self):
        return 500

    def late_fee(self, days):
        return days * 100


# ==========================================================
# 5. VAN SUBCLASS
# ==========================================================

class Van(Vehicle):

    def daily_rate(self):
        return 3000

    def late_fee(self, days):
        return days * 700


# ==========================================================
# 6. CUSTOMER CLASS
# ==========================================================

class Customer:

    def __init__(self, customer_id, name):

        if not name.strip():
            raise ValueError("Customer name cannot be empty")

        self.customer_id = customer_id
        self.name = name


# ==========================================================
# 7. BILLING CLASS
# ==========================================================

class BillingService:

    @staticmethod
    def calculate_bill(rental):

        base_amount = (
            rental.vehicle.daily_rate() * rental.days
        )

        late_amount = rental.vehicle.late_fee(
            rental.late_days
        )

        return base_amount + late_amount


# ==========================================================
# 8. RENTAL CLASS - COMPOSITION (HAS-A)
# ==========================================================

class Rental:

    def __init__(self, vehicle, customer, days, late_days):

        if days <= 0 or late_days < 0:
            raise ValueError("Invalid rental or late days")

        self.vehicle = vehicle
        self.customer = customer
        self.days = days
        self.late_days = late_days

    def calculate_amount(self):

        return BillingService.calculate_bill(self)


# ==========================================================
# 9. RENTAL MANAGER CLASS
# ==========================================================

class RentalManager:

    def __init__(self):

        self.rentals = []

    def add_rental(self, rental):

        self.rentals.append(rental)

    def total_revenue(self):

        total = 0

        # Single loop for all vehicle types

        for rental in self.rentals:

            total += rental.calculate_amount()

        return total


# ==========================================================
# 10. REPORT CLASS - PRINTING
# ==========================================================

class RentalReport:

    @staticmethod
    def print_report(manager):

        print("\n")
        print("=" * 85)
        print("                    VEHICLE RENTAL REPORT")
        print("=" * 85)

        print(
            f"{'Customer':<15}"
            f"{'Vehicle':<12}"
            f"{'Registration':<18}"
            f"{'Days':<8}"
            f"{'Late Fee':<12}"
            f"{'Total':<12}"
        )

        print("-" * 85)

        for rental in manager.rentals:

            vehicle_name = type(rental.vehicle).__name__

            late_amount = rental.vehicle.late_fee(
                rental.late_days
            )

            print(
                f"{rental.customer.name:<15}"
                f"{vehicle_name:<12}"
                f"{rental.vehicle.registration_number:<18}"
                f"{rental.days:<8}"
                f"{late_amount:<12.2f}"
                f"{rental.calculate_amount():<12.2f}"
            )

        print("-" * 85)

        print(
            f"{'TOTAL REVENUE':<65}"
            f"Rs. {manager.total_revenue():.2f}"
        )

        print("=" * 85)


# ==========================================================
# 11. INPUT FUNCTION
# ==========================================================

def get_integer(prompt):

    while True:

        value = input(prompt).strip()

        try:

            number = int(value)

            return number

        except ValueError:

            print("Invalid input! Enter a valid integer.")


# ==========================================================
# 12. CREATE VEHICLE
# ==========================================================

def create_vehicle():

    print("\nSelect Vehicle Type")
    print("1. Car")
    print("2. Bike")
    print("3. Van")

    choice = input("Enter choice: ").strip()

    reg_no = input("Enter registration number: ").strip()

    mileage = get_integer("Enter mileage: ")

    if choice == "1":

        return Car(reg_no, mileage)

    elif choice == "2":

        return Bike(reg_no, mileage)

    elif choice == "3":

        return Van(reg_no, mileage)

    else:

        raise ValueError("Invalid vehicle type")


# ==========================================================
# 13. MAIN PROGRAM
# ==========================================================

def main():

    manager = RentalManager()

    print("\n")
    print("=" * 60)
    print("               VEHICLE RENTAL SYSTEM")
    print("=" * 60)

    count = get_integer("Enter number of rentals: ")

    if count <= 0:
        print("Number of rentals must be positive.")
        return

    for i in range(1, count + 1):

        print(f"\n========== RENTAL {i} ==========")

        try:

            customer_id = input("Enter customer ID: ").strip()

            if not customer_id:
                raise ValueError("Customer ID cannot be empty")

            name = input("Enter customer name: ").strip()

            customer = Customer(customer_id, name)

            vehicle = create_vehicle()

            days = get_integer("Enter rental days: ")

            late_days = get_integer("Enter late return days: ")

            rental = Rental(
                vehicle,
                customer,
                days,
                late_days
            )

            manager.add_rental(rental)

            print("Rental added successfully!")

        except ValueError as e:

            print("Error:", e)
            print("This rental was skipped.")

    # Print final report

    RentalReport.print_report(manager)


# ==========================================================
# PROGRAM EXECUTION
# ==========================================================

if __name__ == "__main__":

    main()
