# app/services/auth_service.py
from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.school import get_school_by_email, add_school
from app.services.id_generator import generate_school_id


def signup_school(name, address, contact_name, primary_contact, primary_role, email, password):
    if get_school_by_email(email):
        raise ValueError("Email already registered")
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not name or not name.strip():
        raise ValueError("School name is required")

    school_id = generate_school_id(name)
    password_hash = generate_password_hash(password)

    return add_school(
        school_id, name, address, contact_name, primary_contact, primary_role, email, password_hash
    )


def login_school(email, password):
    school = get_school_by_email(email)
    if not school or not check_password_hash(school.password_hash, password):
        raise ValueError("Invalid email or password")
    return school