def bod_validator(bod: str):
    if bod is not None:
        bod_month = bod.split("-")[0]
        bod_day = bod.split("-")[1]
        bod_year = bod.split("-")[2]

        if int(bod_month) < 1 or int(bod_month) > 12:
            raise ValueError("Format must be MM-DD-YYYY")
        if int(bod_day) < 1 or int(bod_day) > 31:
            raise ValueError("Format must be MM-DD-YYYY")
        if int(bod_year) < 1940:
            raise ValueError("Year must be greater than 1940")

        return bod


def validate_password(password: str) -> bool:
    """
    Validate the password to ensure it meets the following criteria:
    - At least 8 characters long
    - Contains at least one lowercase letter
    - Contains at least one uppercase letter
    - Contains at least one digit
    - Contains at least one special character (e.g., @, #, $, etc.)
    """
    if len(password) < 8:
        return False  # Password too short

    has_lowercase = False
    has_uppercase = False
    has_digit = False
    has_special_char = False
    special_chars = "!@#$%^&*(),.?\":{}|<>"

    for char in password:
        if char.islower():
            has_lowercase = True
        elif char.isupper():
            has_uppercase = True
        elif char.isdigit():
            has_digit = True
        elif char in special_chars:
            has_special_char = True

    # Check if all conditions are met
    if has_lowercase and has_uppercase and has_digit and has_special_char:
        return True  # Password meets all criteria

    return False  # One or more criteria not met
