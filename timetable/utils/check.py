def check_admin(payload, role):
    if role == "admin" and payload.get("role") == "Roles.admin":
        return True
    if role == "trener" and payload.get("role") == "Roles.trener":
        return True
    else:
        return False

