
from abc import ABC, abstractmethod
from enum import Enum


# ==========================================================
# 1. ENUM CLASS
# ==========================================================

class PolicyStatus(Enum):
    DRAFT = "Draft"
    ACTIVE = "Active"
    LAPSED = "Lapsed"
    CANCELLED = "Cancelled"


# ==========================================================
# 2. ABSTRACT BASE CLASS
# ==========================================================

class Policy(ABC):

    def __init__(self, policy_number, customer_name, status):

        self.policy_number = policy_number
        self.customer_name = customer_name
        self.status = status

    # Encapsulation using property

    @property
    def policy_number(self):
        return self.__policy_number

    @policy_number.setter
    def policy_number(self, value):

        if not isinstance(value, str) or not value.strip():
            raise ValueError("Invalid policy number")

        self.__policy_number = value

    # Abstract method

    @abstractmethod
    def calculate_premium(self):
        pass

    # Common reporting interface

    def report(self):

        print("\n--------------------------------------")
        print("Policy Number :", self.policy_number)
        print("Customer Name :", self.customer_name)
        print("Policy Status :", self.status.value)
        print("Policy Type   :", type(self).__name__)
        print("Premium       : Rs.", f"{self.calculate_premium():.2f}")


# ==========================================================
# 3. MOTOR POLICY
# ==========================================================

class MotorPolicy(Policy):

    def __init__(self, policy_number, customer_name,
                 vehicle_value, status):

        super().__init__(policy_number, customer_name, status)

        self.vehicle_value = vehicle_value

    def calculate_premium(self):

        return self.vehicle_value * 0.03


# ==========================================================
# 4. HEALTH POLICY
# ==========================================================

class HealthPolicy(Policy):

    def __init__(self, policy_number, customer_name,
                 age, status):

        super().__init__(policy_number, customer_name, status)

        self.age = age

    def calculate_premium(self):

        return 5000 + (self.age * 100)


# ==========================================================
# 5. TRAVEL POLICY
# ==========================================================

class TravelPolicy(Policy):

    def __init__(self, policy_number, customer_name,
                 travel_days, status):

        super().__init__(policy_number, customer_name, status)

        self.travel_days = travel_days

    def calculate_premium(self):

        return self.travel_days * 100


# ==========================================================
# 6. HOME POLICY - NEW SUBCLASS
# ==========================================================

class HomePolicy(Policy):

    def __init__(self, policy_number, customer_name,
                 property_value, status):

        super().__init__(policy_number, customer_name, status)

        self.property_value = property_value

    def calculate_premium(self):

        return self.property_value * 0.001


# ==========================================================
# 7. GET POLICY STATUS
# ==========================================================

def get_status():

    while True:

        value = input(
            "Enter status (DRAFT/ACTIVE/LAPSED/CANCELLED): "
        ).strip().upper()

        try:
            return PolicyStatus[value]

        except KeyError:
            print("Invalid status! Try again.")


# ==========================================================
# 8. CREATE POLICY USING USER INPUT
# ==========================================================

def create_policy(policy_number):

    print("\n1. Motor Policy")
    print("2. Health Policy")
    print("3. Travel Policy")

    choice = input("Choose policy type: ").strip()

    name = input("Enter customer name: ").strip()

    if not name:
        raise ValueError("Customer name cannot be empty")

    status = get_status()

    if choice == "1":

        value = float(input("Enter vehicle value: "))

        if value <= 0:
            raise ValueError("Vehicle value must be positive")

        return MotorPolicy(
            policy_number, name, value, status
        )

    elif choice == "2":

        age = int(input("Enter customer age: "))

        if age <= 0:
            raise ValueError("Age must be positive")

        return HealthPolicy(
            policy_number, name, age, status
        )

    elif choice == "3":

        days = int(input("Enter travel days: "))

        if days <= 0:
            raise ValueError("Travel days must be positive")

        return TravelPolicy(
            policy_number, name, days, status
        )

    else:

        raise ValueError("Invalid policy choice")


# ==========================================================
# 9. ADD FIVE POLICIES TO A LIST
# ==========================================================

def policy_management():

    policies = []

    print("\n========== INSURANCE POLICY SYSTEM ==========")

    for i in range(1, 6):

        print(f"\n========== POLICY {i} ==========")

        while True:

            try:

                policy = create_policy(f"POL{i:03d}")

                policies.append(policy)

                break

            except ValueError as e:

                print("Error:", e)
                print("Please enter the policy details again.")

    # ======================================================
    # 10. SINGLE REPORT LOOP - RUNTIME POLYMORPHISM
    # ======================================================

    print("\n========== POLICY REPORT ==========")

    for policy in policies:

        policy.report()

    # ======================================================
    # 11. ADD HOME POLICY
    # ======================================================

    print("\n========== ADD NEW HOME POLICY ==========")

    try:

        name = input("Enter customer name: ").strip()

        if not name:
            raise ValueError("Customer name cannot be empty")

        value = float(input("Enter property value: "))

        if value <= 0:
            raise ValueError("Property value must be positive")

        status = get_status()

        home = HomePolicy(
            "HOME001",
            name,
            value,
            status
        )

        policies.append(home)

        print("\nHome policy added successfully!")

    except ValueError as e:

        print("Error:", e)

    # Display all policies again

    print("\n========== UPDATED POLICY REPORT ==========")

    for policy in policies:

        policy.report()

    return policies


# ==========================================================
# 12. TWO-DIMENSIONAL LIST - MONTHLY COLLECTION
# ==========================================================

def monthly_collection():

    regions = ["Chennai", "Mumbai", "Bangalore"]

    months = ["January", "February", "March", "April"]

    collection = [

        [10000, 12000, 15000, 11000],

        [15000, 18000, 14000, 16000],

        [12000, 11000, 13000, 17000]

    ]

    print("\n========== MONTHLY PREMIUM COLLECTION ==========")

    print(f"{'Region':<15}", end="")

    for month in months:

        print(f"{month:<12}", end="")

    print(f"{'Total':<12}")

    # Row totals

    column_totals = [0] * len(months)

    for i in range(len(collection)):

        row_total = 0

        print(f"{regions[i]:<15}", end="")

        for j in range(len(collection[i])):

            value = collection[i][j]

            print(f"{value:<12}", end="")

            row_total += value

            column_totals[j] += value

        print(f"{row_total:<12}")

    # Column totals

    print("-" * 85)

    print(f"{'Total':<15}", end="")

    for total in column_totals:

        print(f"{total:<12}", end="")

    print(f"{sum(column_totals):<12}")


# ==========================================================
# 13. MAIN FUNCTION
# ==========================================================

def main():

    policies = policy_management()

    monthly_collection()

    print("\n========== PROGRAM COMPLETED ==========")


if __name__ == "__main__":

    main()
