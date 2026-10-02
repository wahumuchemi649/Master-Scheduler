# app/services/id_generator.py
import random
import re
from app.repositories.school import get_school_by_id


def generate_school_id(school_name):
    letters = re.sub(r"[^A-Za-z]", "", school_name).upper()
    prefix = (letters[:4] if len(letters) >= 4 else letters.ljust(4, "X"))

    for _ in range(20):  # retry a reasonable number of times before giving up
        suffix = "".join(str(random.randint(0, 9)) for _ in range(4))
        candidate = prefix + suffix
        if not get_school_by_id(candidate):
            return candidate

    raise RuntimeError("Could not generate a unique school ID — try again")