import random
from datetime import datetime


def random_entity_group_data():
    """Generate random data for Entity Group screen."""
    timestamp = datetime.now().strftime("%H%M%S")
    number = random.randint(10, 99)
    prefixes = ["Admin", "Manager", "Super", "Test", "Demo", "Audit", "Ops"]
    suffixes = ["Role", "Group", "Team", "Access", "Level", "Unit"]
    group_name = f"{random.choice(prefixes)} {random.choice(suffixes)} {timestamp}{number}"
    level = str(random.randint(1, 10))
    return {"group_name": group_name, "level": level}



ENTITY_TYPES = ["BRANCH", "DCB", "PACS"]
def random_role_creation_data():
    """Generate random data for Role Creation screen."""
    timestamp = datetime.now().strftime("%H%M%S")
    number = random.randint(10, 99)
    prefixes = ["Admin", "Manager", "Super", "Test", "Ops"]
    suffixes = ["Role", "Position", "Designation"]
    role_name = f"{random.choice(prefixes)} {random.choice(suffixes)} {timestamp}{number}"
    entity_group = random.choice(ENTITY_TYPES)
    return {"role_name": role_name, "entity_group": entity_group}


USER_TYPES = ["Maker", "Checker", "Approver", "Maker-Checker", "Checker-Approver"]
ROLE_ENTITY_MAP = {
    "DCB": ["dcb1"],
    "PACS": [
        "Anand Shetkari Vividh Karyakari Sahakari Sanstha Maryadit",
        "Maha Seva Society",
        "Songaon Primary Agricultural Cooperative Credit Society.",
        "The Naraina PACS Ltd. Naraina",
        "Mumbai Vikas Society",
        "Sonagro Agriculture Society",
        "Mandave Vikas Seva Society",
        "DHULDEV Vikas Society Ltd Wakshewadi Functional",
        "Malegao PACS",
        "Shivapur Agriculture Society",
        "PunePACS",
        "Shirpur pacs",
        "Khandesh Co Operative Society",
        "Pac One",
        "Sandip Foundation PACS",
        "Chandadevi PACS",
        "Kanosa PACS",
        "RC PACS",
        "IDBI PACS",
        "SAII PACS",
        "MI PACS",
        "OM PACS",
    ],
}


def random_user_creation_data():
    """Generate random data for User Creation screen.

    Role and Entity are paired — DCB only works with dcb1,
    PACS only works with PACS entities.
    """
    timestamp = datetime.now().strftime("%H%M%S")
    number = random.randint(10, 99)
    username = f"testuser{timestamp}{number}"
    email = f"{username}@mail.com"
    first_name = f"Test{number}"
    last_name = f"User{number}"
    password = "Test@1234567"
    user_types = random.sample(USER_TYPES, 2)

    # Pick role, then pick a valid entity for that role
    role = random.choice(list(ROLE_ENTITY_MAP.keys()))
    entity = random.choice(ROLE_ENTITY_MAP[role])

    return {
        "username": username, "email": email,
        "first_name": first_name, "last_name": last_name,
        "password": password, "user_types": user_types,
        "role": role, "entity": entity
    }



entity_group_data = random_entity_group_data()
role_creation_data = random_role_creation_data()
user_creation_data = random_user_creation_data()