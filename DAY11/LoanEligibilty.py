
from dataclasses import dataclass


# --------------------------------------------------
# APPLICANT DATA MODEL
# --------------------------------------------------

@dataclass
class Applicant:
    applicant_id: str
    name: str
    age: int
    monthly_income: float
    credit_score: int
    employment_type: str
    existing_loans: int
    existing_emi: float
    proposed_emi: float


# --------------------------------------------------
# RULE 1: AGE ELIGIBILITY
# --------------------------------------------------

def check_age(age: int) -> bool:
    if age < 21:
        return False
    elif age <= 60:
        return True
    else:
        return False


# --------------------------------------------------
# RULE 2: INCOME TO EMI RATIO
# --------------------------------------------------

def check_emi_ratio(income: float,
                    existing_emi: float,
                    proposed_emi: float) -> bool:

    if income <= 0:
        return False

    total_emi: float = existing_emi + proposed_emi

    emi_ratio: float = (total_emi / income) * 100

    if emi_ratio <= 40:
        return True
    else:
        return False


# --------------------------------------------------
# RULE 3: CREDIT SCORE ELIGIBILITY
# --------------------------------------------------

def check_credit_score(score: int) -> bool:

    if score >= 750 and score <= 900:
        return True
    elif score >= 700 and score <= 749:
        return True
    elif score >= 650 and score <= 699:
        return True
    else:
        return False


# --------------------------------------------------
# RULE 4: EMPLOYMENT TYPE
# --------------------------------------------------

def check_employment(employment: str) -> bool:

    if employment.lower() == "salaried":
        return True
    elif employment.lower() == "self-employed":
        return True
    else:
        return False


# --------------------------------------------------
# RULE 5: EXISTING LOAN LIMIT
# --------------------------------------------------

def check_existing_loans(loan_count: int) -> bool:

    if loan_count < 0:
        return False
    elif loan_count <= 2:
        return True
    else:
        return False


# --------------------------------------------------
# RULE 6: CREDIT SCORE BAND USING MATCH-CASE
# --------------------------------------------------

def get_loan_product(score: int) -> tuple[str, float | None]:

    match score:
        case s if 750 <= s <= 900:
            return "Premium Loan", 8.5

        case s if 700 <= s <= 749:
            return "Standard Loan", 10.0

        case s if 650 <= s <= 699:
            return "Basic Loan", 12.0

        case _:
            return "Not Eligible", None


# --------------------------------------------------
# INPUT VALIDATION
# --------------------------------------------------

def validate_applicant(applicant: Applicant) -> str:

    if applicant.age < 0:
        return "Negative age"

    elif applicant.age == 0:
        return "Invalid age"

    elif applicant.monthly_income <= 0:
        return "Invalid income"

    elif applicant.credit_score < 300 or applicant.credit_score > 900:
        return "Credit score out of range"

    elif applicant.existing_loans < 0:
        return "Invalid existing loan count"

    elif applicant.existing_emi < 0 or applicant.proposed_emi < 0:
        return "Invalid EMI amount"

    return "Valid"


# --------------------------------------------------
# FINAL LOAN ELIGIBILITY DECISION
# --------------------------------------------------

def evaluate_applicant(applicant: Applicant) -> tuple[str, str, float | None]:

    validation: str = validate_applicant(applicant)

    if validation != "Valid":
        return "INVALID", validation, None

    age_result: bool = check_age(applicant.age)

    emi_result: bool = check_emi_ratio(
        applicant.monthly_income,
        applicant.existing_emi,
        applicant.proposed_emi
    )

    credit_result: bool = check_credit_score(applicant.credit_score)

    employment_result: bool = check_employment(
        applicant.employment_type
    )

    loan_result: bool = check_existing_loans(
        applicant.existing_loans
    )

    product: str
    interest_rate: float | None

    product, interest_rate = get_loan_product(
        applicant.credit_score
    )

    if age_result and emi_result:
        if credit_result and employment_result and loan_result:
            return "APPROVED", product, interest_rate
        else:
            return "REJECTED", "Failed eligibility rule", None
    else:
        return "REJECTED", "Failed eligibility rule", None


# --------------------------------------------------
# APPLICANT RECORDS - 10 APPLICANTS
# --------------------------------------------------

applicants: list[Applicant] = [

    Applicant("A101", "Arun", 30, 50000, 780,
              "Salaried", 0, 0, 10000),

    Applicant("A102", "Bala", 25, 0, 720,
              "Salaried", 0, 0, 5000),

    Applicant("A103", "Charan", 19, 40000, 760,
              "Salaried", 0, 0, 5000),

    Applicant("A104", "David", 42, 80000, 720,
              "Self-employed", 1, 10000, 15000),

    Applicant("A105", "Ezhil", 35, 60000, 620,
              "Salaried", 0, 0, 10000),

    Applicant("A106", "Farhan", 55, 100000, 760,
              "Salaried", 2, 10000, 15000),

    Applicant("A107", "Ganesh", 28, 45000, 680,
              "Salaried", 1, 5000, 10000),

    Applicant("A108", "Hari", 65, 90000, 800,
              "Self-employed", 0, 0, 15000),

    Applicant("A109", "Imran", 32, 70000, 850,
              "Salaried", 3, 10000, 10000),

    Applicant("A110", "John", -5, 50000, 750,
              "Salaried", 0, 0, 5000)
]


# --------------------------------------------------
# DRIVER SCRIPT
# --------------------------------------------------

def main() -> None:

    daily_approval_limit: int = 3

    approved_count: int = 0

    processed_count: int = 0

    results: list[tuple[str, str, str, str]] = []

    print(f"\n{'=' * 75}")
    print(f"{'BANK LOAN ELIGIBILITY ENGINE':^75}")
    print(f"{'=' * 75}")

    for applicant in applicants:

        processed_count += 1

        validation: str = validate_applicant(applicant)

        # Skip invalid records
        if validation != "Valid":

            print(
                f"Skipping {applicant.applicant_id}: {validation}"
            )

            results.append((
                applicant.applicant_id,
                applicant.name,
                "INVALID",
                validation
            ))

            continue

        # Evaluate valid applicants
        decision: str
        product: str
        rate: float | None

        decision, product, rate = evaluate_applicant(applicant)

        if decision == "APPROVED":

            approved_count += 1

            rate_display: str = f"{rate:.1f}%" if rate is not None else "N/A"

            results.append((
                applicant.applicant_id,
                applicant.name,
                decision,
                f"{product} ({rate_display})"
            ))

        else:

            results.append((
                applicant.applicant_id,
                applicant.name,
                decision,
                product
            ))

        # Stop when daily approval limit is reached
        if approved_count >= daily_approval_limit:

            print(
                f"\nDaily approval limit of "
                f"{daily_approval_limit} reached."
            )

            break

    else:

        print(
            f"\nAll {len(applicants)} applicants processed successfully."
        )

    # --------------------------------------------------
    # DECISION TABLE
    # --------------------------------------------------

    print(f"\n{'=' * 75}")
    print(f"{'LOAN DECISION TABLE':^75}")
    print(f"{'=' * 75}")

    print(
        f"{'ID':<12}"
        f"{'NAME':<15}"
        f"{'DECISION':<15}"
        f"{'PRODUCT / REASON':<35}"
    )

    print(f"{'-' * 75}")

    for applicant_id, name, decision, details in results:

        print(
            f"{applicant_id:<12}"
            f"{name:<15}"
            f"{decision:<15}"
            f"{details:<35}"
        )

    print(f"{'-' * 75}")

    print(f"Total applicants in list : {len(applicants)}")
    print(f"Applicants processed     : {processed_count}")
    print(f"Approved applicants      : {approved_count}")
    print(f"Daily approval limit     : {daily_approval_limit}")

    print(f"{'=' * 75}")


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()
