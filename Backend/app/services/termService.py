
from app.repositories.term import  add_term


def create_term(school_id, academic_year, term_name):
    if not academic_year or not term_name:
        raise ValueError("academic_year and term_name are required")
    return add_term(school_id, academic_year, term_name.strip())