
# ============================================================
# SET 3 - INSURANCE PREMIUM BANDS
# ============================================================


# ------------------------------------------------------------
# RULE 1: BMI CALCULATION AND CLASSIFICATION
# ------------------------------------------------------------

def calculate_bmi(weight, height):

    if weight <= 0 or height <= 0:
        return None, "Invalid", 0

    bmi = weight / (height ** 2)

    # Nested if statements for BMI classification

    if bmi > 0:

        if bmi < 18.5:
            category = "Underweight"
            loading = 0.05

        elif bmi < 25:
            category = "Normal"
            loading = 0.00

        elif bmi < 30:
            category = "Overweight"
            loading = 0.10

        else:
            category = "Obese"
            loading = 0.20

    else:
        category = "Invalid"
        loading = 0

    return bmi, category, loading


# ------------------------------------------------------------
# RULE 2: BASE PREMIUM USING MATCH-CASE WITH GUARDS
# ------------------------------------------------------------

def get_base_premium(age):

    match age:

        case a if 18 <= a <= 30:
            return 5000

        case a if 31 <= a <= 45:
            return 7000

        case a if 46 <= a <= 60:
            return 10000

        case a if 61 <= a <= 70:
            return 15000

        case _:
            return None


# ------------------------------------------------------------
# POLICY TERM MULTIPLIER USING MATCH-CASE
# ------------------------------------------------------------

def get_term_multiplier(term):

    match term:

        case t if t == 1:
            return 1.0

        case t if t == 5:
            return 4.5

        case t if t == 10:
            return 8.0

        case _:
            return None


# ------------------------------------------------------------
# RULE 3: FINAL PREMIUM CALCULATION
# ------------------------------------------------------------

def calculate_premium(base, multiplier, bmi_loading, smoker):

    smoker_loading = 0.20 if smoker else 0.00

    # Operator precedence:
    # 1. Parentheses are evaluated first.
    # 2. Multiplication is performed next.
    # 3. The final result is calculated.

    final_premium = base * multiplier * (1 + bmi_loading + smoker_loading)

    return final_premium, smoker_loading


# ------------------------------------------------------------
# INPUT FUNCTIONS: TYPE CONVERSION ERROR HANDLING
# ------------------------------------------------------------

def get_integer(prompt):

    while True:

        value = input(prompt).strip()

        if value == "":
            print("Error: Empty input is not allowed.")
            continue

        try:
            number = int(value)
            return number

        except ValueError:
            print("Error: Please enter a valid integer.")


def get_float(prompt):

    while True:

        value = input(prompt).strip()

        if value == "":
            print("Error: Empty input is not allowed.")
            continue

        try:
            number = float(value)
            return number

        except ValueError:
            print("Error: Please enter a valid number.")


# ------------------------------------------------------------
# RULE 4: PROCESS EIGHT APPLICANTS USING FOR LOOP
# ------------------------------------------------------------

def process_applicants():

    print("\n")
    print("=" * 75)
    print("                  INSURANCE PREMIUM CALCULATOR")
    print("=" * 75)

    applicant_count = 8

    approved_count = 0

    total_premium = 0

    for i in range(1, applicant_count + 1):

        print(f"\n========== APPLICANT {i} ==========")

        name = input("Enter applicant name: ").strip()

        if name == "":
            print("Error: Name cannot be empty.")
            print("Batch stopped due to invalid applicant.")
            break

        age = get_integer("Enter age: ")

        # Age eligibility check
        if age < 18 or age > 70:
            print(f"{name} is INELIGIBLE due to age.")
            print("Batch validation stopped.")
            break

        weight = get_float("Enter weight in KG: ")

        height = get_float("Enter height in meters: ")

        if weight <= 0 or height <= 0:
            print("Invalid weight or height.")
            print("Batch validation stopped.")
            break

        smoker_input = input("Is the applicant a smoker? (yes/no): ").strip().lower()

        if smoker_input not in ("yes", "no"):
            print("Invalid smoker status. Enter yes or no.")
            print("Batch validation stopped.")
            break

        smoker = smoker_input == "yes"

        term = get_integer("Enter policy term (1/5/10 years): ")

        multiplier = get_term_multiplier(term)

        if multiplier is None:
            print("Invalid policy term.")
            print("Batch validation stopped.")
            break

        # Calculate BMI
        bmi, bmi_category, bmi_loading = calculate_bmi(weight, height)

        # Calculate base premium
        base = get_base_premium(age)

        if base is None:
            print("Applicant is ineligible.")
            break

        # Calculate final premium
        premium, smoker_loading = calculate_premium(
            base,
            multiplier,
            bmi_loading,
            smoker
        )

        approved_count += 1

        total_premium += premium

        # Display applicant result
        print("\n---------- INSURANCE RESULT ----------")

        print(f"Applicant Name    : {name}")
        print(f"Age               : {age}")
        print(f"BMI               : {bmi:.2f}")
        print(f"BMI Category      : {bmi_category}")
        print(f"BMI Loading       : {bmi_loading * 100:.2f}%")
        print(f"Smoker Loading    : {smoker_loading * 100:.2f}%")
        print(f"Base Premium      : Rs. {base:.2f}")
        print(f"Policy Term       : {term} years")
        print(f"Term Multiplier   : {multiplier}")
        print("--------------------------------------")
        print(f"FINAL PREMIUM     : Rs. {premium:.2f}")

    else:
        # Executes only when all eight applicants are processed
        print("\nAll eight applicants passed batch validation.")

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print("\n")
    print("=" * 75)
    print("                    BATCH SUMMARY")
    print("=" * 75)

    print(f"Total Applicants       : {applicant_count}")
    print(f"Successfully Processed : {approved_count}")
    print(f"Total Premium Amount   : Rs. {total_premium:.2f}")

    print("=" * 75)


# ------------------------------------------------------------
# RULE 5: TYPE CONVERSION ERROR DEMONSTRATION
# ------------------------------------------------------------

def demonstrate_errors():

    print("\n")
    print("=" * 60)
    print("             TYPE CONVERSION ERROR DEMO")
    print("=" * 60)

    # String to integer conversion

    try:
        age = int("twenty")

    except ValueError as e:
        print("String to integer error:", e)

    # Empty string conversion

    try:
        age = int("")

    except ValueError as e:
        print("Empty input conversion error:", e)

    print("\nBoth errors were handled using try-except.")


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

def main():

    demonstrate_errors()

    process_applicants()


# ------------------------------------------------------------
# PROGRAM EXECUTION
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
