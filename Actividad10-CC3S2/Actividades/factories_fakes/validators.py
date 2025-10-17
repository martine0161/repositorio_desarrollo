# Actividades/factories_fakes/validators.py
def validate_account(d):
    """Validación estricta de cuenta"""
    if not isinstance(d, dict):
        raise TypeError("account must be dict")
    
    for k in ("id", "email", "role", "active"):
        if k not in d:
            raise ValueError(f"missing {k}")
    
    if not isinstance(d["id"], str) or not d["id"]:
        raise ValueError("id must be non-empty str")
    
    if "@" not in d["email"]:
        raise ValueError("invalid email")
    
    if not isinstance(d["role"], str):
        raise ValueError("role must be str")
    
    if not isinstance(d["active"], bool):
        raise ValueError("active must be bool")
    
    return True