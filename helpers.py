def required_fields(data, fields):
    """
    data is the payload from the user
    fields is a list of required fields
    """
    for field in fields:
        if data[field] == "":
            return "All fields required."
    return None
