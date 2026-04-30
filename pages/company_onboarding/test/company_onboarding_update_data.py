"""
company_onboarding_update_data.py
----------------------------------
Random update data generators for Company Onboarding update tests.
Generates fresh random data on every import.

Step mapping (matches RhythmERP stepper):
  STEP1 = Company Details (contact_name, email, mobile_number)
  STEP2 = Promoters (promoter_name, promoter_remark)
  STEP3 = Address (address, pin_code)
  STEP4 = Business Details (business_model, market_linkages)
  STEP5 = Infrastructure (infra_location)
"""

import random
import string


UPDATE_COMPANY_NAME = "Orion Royal Systems"


def _random_name():
    first = random.choice([
        "Aarav", "Vedant", "Arjun", "Rohan", "Nikhil", "Prashant",
        "Suresh", "Mahesh", "Rajesh", "Priya", "Pooja", "Sneha",
        "Amit", "Vijay", "Manoj", "Deepak", "Sanjay", "Rakesh",
    ])
    last = random.choice([
        "Sharma", "Patil", "Desai", "Joshi", "Kulkarni", "Mehta",
        "Shah", "Pawar", "Jadhav", "Chavan", "Bhosale", "More",
    ])
    return f"{first} {last}"


def _random_mobile():
    return f"9{random.randint(100000000, 999999999)}"


def _random_email(name=None):
    if name:
        parts = name.lower().split()
        user = f"{parts[0]}.{parts[-1]}"
    else:
        user = "".join(random.choices(string.ascii_lowercase, k=6))
    uid = random.randint(100, 999)
    domains = ["testmail.com", "company.com", "corp.in", "enterprise.in"]
    return f"{user}{uid}@{random.choice(domains)}"


def _random_address():
    return f"{random.randint(1,999)}, Updated Test Street, {random.choice(['Pune', 'Mumbai', 'Bangalore', 'Hyderabad', 'Delhi'])}"


def _random_pin():
    return str(random.randint(110000, 899999))


def generate_update_data():
    """Generate random update data for all 5 steps. Returns dict per step."""
    name = _random_name()

    step1 = {
        "contact_name": name,
        "email": _random_email(name),
        "mobile_number": _random_mobile(),
    }

    step2 = {
        "promoter_name": _random_name(),
        "promoter_remark": f"Updated remark {random.randint(100,999)}",
    }

    step3 = {
        "address": _random_address(),
        "pin_code": _random_pin(),
    }

    step4 = {
        "business_model": f"Updated Business Model {random.randint(100,999)}",
        "market_linkages": f"Updated Market Linkages {random.randint(100,999)}",
    }

    step5 = {
        "infra_location": f"Updated Infra Location {random.randint(100,999)}",
    }

    all_updates = {1: step1, 2: step2, 3: step3, 4: step4, 5: step5}

    return step1, step2, step3, step4, step5, all_updates


# Generate on import - fresh random data every run
STEP1_UPDATES, STEP2_UPDATES, STEP3_UPDATES, STEP4_UPDATES, STEP5_UPDATES, ALL_UPDATES = generate_update_data()