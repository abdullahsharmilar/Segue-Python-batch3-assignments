
# ============================================================
# SET 2 - UTILITY BILLING CALCULATOR
# ============================================================


# ------------------------------------------------------------
# RULE 1: CALCULATE ELECTRICITY BILL USING FOUR SLABS
# ------------------------------------------------------------

def calculate_energy_charge(units):

    if units < 0:
        return 0

    elif units <= 100:
        bill = units * 2

    elif units <= 200:
        bill = (100 * 2) + ((units - 100) * 3)

    elif units <= 400:
        bill = (100 * 2) + (100 * 3) + ((units - 200) * 5)

    else:
        bill = (100 * 2) + (100 * 3) + (200 * 5) + ((units - 400) * 7)

    return bill


# ------------------------------------------------------------
# RULE 2: CONSUMER CATEGORY USING MATCH-CASE
# ------------------------------------------------------------

def get_fixed_charge(category):

    match category.lower():

        case "domestic":
            return 100

        case "commercial":
            return 300

        case "industrial":
            return 500

        case _:
            return None


# ------------------------------------------------------------
# RULE 3: LATE SURCHARGE AND ONLINE REBATE
# ------------------------------------------------------------

def calculate_final_bill(base_bill, late_payment, online_payment):

    late_surcharge = 0.05
    online_rebate = 0.02

    surcharge_amount = 0
    rebate_amount = 0

    if late_payment:
        surcharge_amount = base_bill * late_surcharge

    if online_payment:
        rebate_amount = base_bill * online_rebate

    # Operator precedence:
    # Multiplication is evaluated before addition/subtraction.
    final_bill = base_bill + (base_bill * late_surcharge if late_payment else 0) - (base_bill * online_rebate if online_payment else 0)

    return final_bill, surcharge_amount, rebate_amount


# ------------------------------------------------------------
# COMPLETE BILL CALCULATION
# ------------------------------------------------------------

def calculate_bill(units, category, late_payment=False, online_payment=False):

    energy_charge = calculate_energy_charge(units)

    fixed_charge = get_fixed_charge(category)

    if fixed_charge is None:
        return None

    base_bill = energy_charge + fixed_charge

    final_bill, surcharge, rebate = calculate_final_bill(
        base_bill,
        late_payment,
        online_payment
    )

    return energy_charge, fixed_charge, surcharge, rebate, final_bill


# ------------------------------------------------------------
# RULE 4: 12-MONTH CONSUMPTION STATEMENT USING FOR LOOP
# ------------------------------------------------------------

def monthly_statement():

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    # Sample monthly electricity consumption
    readings = [
        80, 120, 150, 180,
        220, 250, 300, 350,
        400, 420, 450, 500
    ]

    category = "domestic"

    print("\n")
    print("=" * 75)
    print("              12-MONTH ELECTRICITY CONSUMPTION STATEMENT")
    print("=" * 75)

    print(f"{'MONTH':<15}{'UNITS':>10}{'ENERGY CHARGE':>20}{'TOTAL BILL':>20}")

    print("-" * 75)

    annual_total = 0

    for i in range(12):

        month = months[i]
        units = readings[i]

        result = calculate_bill(units, category)

        energy_charge = result[0]
        final_bill = result[4]

        annual_total += final_bill

        print(
            f"{month:<15}"
            f"{units:>10}"
            f"{energy_charge:>20.2f}"
            f"{final_bill:>20.2f}"
        )

    print("-" * 75)

    print(f"{'ANNUAL TOTAL':<15}{sum(readings):>10}{'':>20}{annual_total:>20.2f}")

    print("=" * 75)


# ------------------------------------------------------------
# RULE 5: DISPLAY INDIVIDUAL ELECTRICITY BILL
# ------------------------------------------------------------

def display_bill(units, category, late_payment, online_payment):

    result = calculate_bill(
        units,
        category,
        late_payment,
        online_payment
    )

    if result is None:
        print("Invalid consumer category!")
        return

    energy_charge, fixed_charge, surcharge, rebate, final_bill = result

    print("\n")
    print("=" * 50)
    print("             ELECTRICITY BILL")
    print("=" * 50)

    print(f"{'Units Consumed':<25}: {units}")
    print(f"{'Consumer Category':<25}: {category}")
    print("-" * 50)

    print(f"{'Energy Charge':<25}: Rs. {energy_charge:>10.2f}")
    print(f"{'Fixed Charge':<25}: Rs. {fixed_charge:>10.2f}")
    print(f"{'Late Surcharge':<25}: Rs. {surcharge:>10.2f}")
    print(f"{'Online Rebate':<25}: Rs. {rebate:>10.2f}")

    print("-" * 50)

    print(f"{'FINAL BILL':<25}: Rs. {final_bill:>10.2f}")

    print("=" * 50)


# ------------------------------------------------------------
# RULE 4: WHILE LOOP TO ACCEPT READINGS UNTIL Q
# ------------------------------------------------------------

def accept_readings():

    print("\n")
    print("=" * 50)
    print("         INTERACTIVE BILLING SYSTEM")
    print("=" * 50)

    category = input(
        "Enter consumer category (domestic/commercial/industrial): "
    ).strip().lower()

    if get_fixed_charge(category) is None:
        print("Invalid consumer category!")
        return

    while True:

        reading = input(
            "\nEnter electricity units consumed (or q to quit): "
        ).strip()

        if reading.lower() == "q":
            print("Exiting billing system...")
            break

        try:
            units = int(reading)

            if units < 0:
                print("Invalid reading! Units cannot be negative.")
                continue

        except ValueError:
            print("Invalid input! Please enter a valid integer.")
            continue

        late = input("Is the payment late? (yes/no): ").strip().lower()

        online = input("Is this an online payment? (yes/no): ").strip().lower()

        if late not in ("yes", "no") or online not in ("yes", "no"):
            print("Invalid payment option! Please enter yes or no.")
            continue

        display_bill(
            units,
            category,
            late == "yes",
            online == "yes"
        )


# ------------------------------------------------------------
# BOUNDARY VALUE TESTING
# ------------------------------------------------------------

def boundary_testing():

    test_values = [100, 101, 200, 201, 400, 401]

    print("\n")
    print("=" * 50)
    print("             BOUNDARY VALUE TESTING")
    print("=" * 50)

    print(f"{'UNITS':<15}{'ENERGY CHARGE':>20}")

    print("-" * 35)

    for units in test_values:

        bill = calculate_energy_charge(units)

        print(f"{units:<15}{bill:>20.2f}")

    print("=" * 50)


# ------------------------------------------------------------
# MAIN DRIVER PROGRAM
# ------------------------------------------------------------

def main():

    print("\n")
    print("*" * 60)
    print("           UTILITY BILLING CALCULATOR")
    print("*" * 60)

    # Generate 12-month statement
    monthly_statement()

    # Test boundary values
    boundary_testing()

    # Accept user readings until q
    accept_readings()


# ------------------------------------------------------------
# PROGRAM EXECUTION
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
