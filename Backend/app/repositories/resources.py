from app.extensions import db
from app.models.data import Resource

def get_resource_by_id(resource_id):
    return Resource.query.get(resource_id)


def get_all_resources(school_id):
    return Resource.query.filter_by(schoolId=school_id).all()


def add_resource(school_id, name, capacity):
    new_resource = Resource(schoolId=school_id, name=name, capacity=capacity)
    db.session.add(new_resource)
    db.session.commit()
    return new_resource


def update_resource(resource_id, **fields):
    resource = Resource.query.get(resource_id)
    if not resource:
        return None
    for key, value in fields.items():
        setattr(resource, key, value)
    db.session.commit()
    return resource

def delete_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        return False
    db.session.delete(resource)
    db.session.commit()
    return True