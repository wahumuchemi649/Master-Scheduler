from app.repositories.resources import (
    get_resource_by_id,
    get_all_resources,
    add_resource,
    update_resource,
    delete_resource,
)


def create_resource(school_id, name, capacity=1):
    if not name or not name.strip():
        raise ValueError("Resource name is required")
    if capacity is None or capacity < 1:
        raise ValueError("Capacity must be at least 1")
    return add_resource(school_id, name.strip(), capacity)


def list_resources(school_id):
    return get_all_resources(school_id)


def edit_resource(resource_id, **fields):
    resource = get_resource_by_id(resource_id)
    if not resource:
        raise ValueError("Resource not found")
    return update_resource(resource_id, **fields)


def remove_resource(resource_id):
    deleted = delete_resource(resource_id)
    if not deleted:
        raise ValueError("Resource not found")
    return True