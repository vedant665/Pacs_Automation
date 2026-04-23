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


entity_group_data = random_entity_group_data()
role_creation_data = random_role_creation_data()