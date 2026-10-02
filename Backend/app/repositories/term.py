from app.extensions import db
from app.models.data import Term

def add_term(school_id, academic_year, term_name):
    new_term = Term(schoolId=school_id, academic_year=academic_year, term_name=term_name)
    db.session.add(new_term)
    db.session.commit()
    return new_term