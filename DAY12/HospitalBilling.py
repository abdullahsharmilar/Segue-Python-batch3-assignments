
from abc import ABC, abstractmethod
from enum import Enum


# ==========================================================
# 1. VISIT TYPE ENUM
# ==========================================================

class VisitType(Enum):
    OUTPATIENT = "Outpatient"
    INPATIENT = "Inpatient"
    EMERGENCY = "Emergency"


# ==========================================================
# 2. PATIENT CLASS
# ==========================================================

class Patient:

    def __init__(self, patient_id, name, age):

        self.__patient_id = patient_id
        self.name = name
        self.age = age

    # Read-only property

    @property
    def patient_id(self):
        return self.__patient_id


# ==========================================================
# 3. DOCTOR CLASS
# ==========================================================

class Doctor:

    def __init__(self, doctor_id, name, department):

        self.doctor_id = doctor_id
        self.name = name
        self.department = department


# ==========================================================
# 4. ABSTRACT VISIT CLASS
# ==========================================================

class Visit(ABC):

    def __init__(self, visit_id, patient, doctor,
                 visit_type, month):

        self.visit_id = visit_id
        self.patient = patient
        self.doctor = doctor
        self.visit_type = visit_type
        self.month = month

    @abstractmethod
    def calculate_bill(self):
        pass

    # Common invoice format

    def print_invoice(self):

        print("\n-------------------------------------------")
        print("              HOSPITAL INVOICE")
        print("-------------------------------------------")

        print(f"Visit ID       : {self.visit_id}")
        print(f"Patient ID     : {self.patient.patient_id}")
        print(f"Patient Name   : {self.patient.name}")
        print(f"Patient Age    : {self.patient.age}")
        print(f"Doctor Name    : {self.doctor.name}")
        print(f"Department     : {self.doctor.department}")
        print(f"Visit Type     : {self.visit_type.value}")
        print(f"Month          : {self.month}")

        print("-------------------------------------------")
        print(f"TOTAL BILL     : Rs. {self.calculate_bill():.2f}")
        print("-------------------------------------------")


# ==========================================================
# 5. OUTPATIENT VISIT
# ==========================================================

class OutPatientVisit(Visit):

    def calculate_bill(self):

        return 800


# ==========================================================
# 6. INPATIENT VISIT
# ==========================================================

class InPatientVisit(Visit):

    def __init__(self, visit_id, patient, doctor,
                 visit_type, month, days):

        super().__init__(
            visit_id, patient, doctor, visit_type, month
        )

        self.days = days

    def calculate_bill(self):

        return self.days * 3000


# ==========================================================
# 7. EMERGENCY VISIT
# ==========================================================

class EmergencyVisit(Visit):

    def calculate_bill(self):

        base_fee = 1000
        emergency_surcharge = 2500

        return base_fee + emergency_surcharge


# ==========================================================
# 8. INPUT VALIDATION
# ==========================================================

def get_integer(prompt):

    while True:

        value = input(prompt).strip()

        try:

            return int(value)

        except ValueError:

            print("Invalid input! Enter a valid integer.")


# ==========================================================
# 9. CREATE VISIT
# ==========================================================

def create_visit(index):

    print(f"\n========== VISIT {index} ==========")

    patient_id = input("Enter patient ID: ").strip()

    if not patient_id:
        raise ValueError("Patient ID cannot be empty")

    patient_name = input("Enter patient name: ").strip()

    if not patient_name:
        raise ValueError("Patient name cannot be empty")

    age = get_integer("Enter patient age: ")

    if age <= 0:
        raise ValueError("Age must be positive")

    doctor_id = input("Enter doctor ID: ").strip()

    if not doctor_id:
        raise ValueError("Doctor ID cannot be empty")

    doctor_name = input("Enter doctor name: ").strip()

    if not doctor_name:
        raise ValueError("Doctor name cannot be empty")

    department = input("Enter department: ").strip()

    if not department:
        raise ValueError("Department cannot be empty")

    month_number = get_integer("Enter month (1-12): ")

    if month_number < 1 or month_number > 12:
        raise ValueError("Month must be between 1 and 12")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    month = months[month_number - 1]

    patient = Patient(patient_id, patient_name, age)

    doctor = Doctor(doctor_id, doctor_name, department)

    print("\nSelect Visit Type")
    print("1. Outpatient")
    print("2. Inpatient")
    print("3. Emergency")

    choice = input("Enter choice: ").strip()

    visit_id = f"V{index:03d}"

    if choice == "1":

        return OutPatientVisit(
            visit_id, patient, doctor,
            VisitType.OUTPATIENT, month
        )

    elif choice == "2":

        days = get_integer("Enter number of inpatient days: ")

        if days <= 0:
            raise ValueError("Days must be positive")

        return InPatientVisit(
            visit_id, patient, doctor,
            VisitType.INPATIENT, month, days
        )

    elif choice == "3":

        return EmergencyVisit(
            visit_id, patient, doctor,
            VisitType.EMERGENCY, month
        )

    else:

        raise ValueError("Invalid visit type")


# ==========================================================
# 10. BILL SUMMARY - SINGLE POLYMORPHIC LOOP
# ==========================================================

def generate_bill_summary(visits):

    print("\n")
    print("=" * 90)
    print("                     HOSPITAL BILL SUMMARY")
    print("=" * 90)

    print(
        f"{'Patient':<15}"
        f"{'Visit Type':<15}"
        f"{'Doctor':<15}"
        f"{'Department':<18}"
        f"{'Month':<12}"
        f"{'Bill':<12}"
    )

    print("-" * 90)

    total_revenue = 0

    # Single polymorphic loop

    for visit in visits:

        bill = visit.calculate_bill()

        total_revenue += bill

        print(
            f"{visit.patient.name:<15}"
            f"{visit.visit_type.value:<15}"
            f"{visit.doctor.name:<15}"
            f"{visit.doctor.department:<18}"
            f"{visit.month:<12}"
            f"{bill:<12.2f}"
        )

    print("-" * 90)

    print(f"TOTAL HOSPITAL REVENUE: Rs. {total_revenue:.2f}")

    print("=" * 90)

    return total_revenue


# ==========================================================
# 11. DEPARTMENT-WISE MONTHLY TOTALS USING NESTED LIST
# ==========================================================

def department_monthly_totals(visits):

    departments = []

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    # Collect unique departments

    for visit in visits:

        department = visit.doctor.department

        if department not in departments:

            departments.append(department)

    # Create 2D nested list

    totals = []

    for i in range(len(departments)):

        totals.append([0] * 12)

    # Calculate department-wise monthly bills

    for visit in visits:

        row = departments.index(visit.doctor.department)

        column = months.index(visit.month)

        totals[row][column] += visit.calculate_bill()

    # Display nested list

    print("\n")
    print("=" * 100)
    print("             DEPARTMENT-WISE MONTHLY COLLECTION")
    print("=" * 100)

    print(f"{'Department':<18}", end="")

    for month in months:

        print(f"{month[:3]:<10}", end="")

    print(f"{'Total':<12}")

    print("-" * 100)

    column_totals = [0] * 12

    grand_total = 0

    for i in range(len(departments)):

        row_total = 0

        print(f"{departments[i]:<18}", end="")

        for j in range(12):

            amount = totals[i][j]

            print(f"{amount:<10.2f}", end="")

            row_total += amount

            column_totals[j] += amount

        print(f"{row_total:<12.2f}")

        grand_total += row_total

    # Column totals

    print("-" * 100)

    print(f"{'TOTAL':<18}", end="")

    for total in column_totals:

        print(f"{total:<10.2f}", end="")

    print(f"{grand_total:<12.2f}")

    print("=" * 100)


# ==========================================================
# 12. MAIN PROGRAM
# ==========================================================

def main():

    print("\n")
    print("=" * 60)
    print("                 HOSPITAL BILLING MODEL")
    print("=" * 60)

    visits = []

    count = get_integer("Enter number of visits: ")

    if count <= 0:
        print("Number of visits must be positive.")
        return

    # Store visits in a list

    for i in range(1, count + 1):

        while True:

            try:

                visit = create_visit(i)

                visits.append(visit)

                print("Visit added successfully!")

                break

            except ValueError as e:

                print("Error:", e)
                print("Please enter the visit details again.")

    # Print individual invoices

    print("\n========== INDIVIDUAL INVOICES ==========")

    for visit in visits:

        visit.print_invoice()

    # Common bill summary

    generate_bill_summary(visits)

    # Department-wise monthly totals

    department_monthly_totals(visits)

    print("\n========== PROGRAM COMPLETED ==========")


# ==========================================================
# PROGRAM EXECUTION
# ==========================================================

if __name__ == "__main__":

    main()
