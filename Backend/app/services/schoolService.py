# app/services/school_service.py
from app.repositories.school import get_school_by_id


def get_school_details(school_id):
    school = get_school_by_id(school_id)
    if not school:
        return None
    return {
        "id": school.id,
        "name": school.name,
        "address": school.address,
        "contact_name": school.contact_name,
        "primary_contact": school.primary_contact,
        "primary_role": school.primary_role,
    }