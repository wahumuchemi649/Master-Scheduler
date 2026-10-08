from app.models.data import School, Term
from app.extensions import db
from sqlalchemy import text
def get_school_by_id(school_id):
    return School.query.get(school_id)

def get_current_term(school_id):
    return (
        Term.query.filter_by(schoolId=school_id)
        .order_by(Term.academic_year.desc(), Term.term_name.desc())
        .first()
    )

def get_school_by_email(email):
    return School.query.filter_by(email=email).first()


def add_school(school_id, name, address, contact_name, primary_contact, primary_role, email, password_hash):
    new_school = School(
        id=school_id,
        name=name,
        address=address,
        contact_name=contact_name,
        primary_contact=primary_contact,
        primary_role=primary_role,
        email=email,
        password_hash=password_hash,
    )
    db.session.add(new_school)
    db.session.commit()
    return new_school
def health():
    db.session.execute(text("SELECT COUNT(*) FROM schools"))
    return {"status": "ok"}, 200