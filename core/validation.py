async def validate_data_on_create(obj):
    if obj is None:
        return False
    user = obj.split(', ')
    if not (
            len(user) == 2 and
            isinstance(int(user[0]), int) and
            isinstance(user[1], str)):
        return False
    data = {
        'user_id': int(user[0]),
        'username': user[1],
        'is_admin': True
    }
    return data


async def validate_data_on_delete(obj):
    if obj is None:
        return False
    if not isinstance(int(obj), int):
        return False
    return int(obj)
