def add_hateoas_links(resource, obj):
    obj["links"] = {
        "self": f"/api/{resource}/{obj['id']}",
        "update": f"/api/{resource}/{obj['id']}", # Typically PUT
        "delete": f"/api/{resource}/{obj['id']}"  # Typically DELETE
    }
    return obj
