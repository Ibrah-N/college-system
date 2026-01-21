import re


def title_case(text: str | None):

    if not text:
        return ""
    return " ".join(word.capitalize() for word in text.split())




def validate_cnic(cnic: str | None) -> str | None:
    """
    Accepts:
    - 00000-0000000-0
    - 13 digit number

    Returns:
    - Formatted CNIC: 00000-0000000-0
    - None if empty

    Raises:
    - ValueError if invalid
    """
    if not cnic:
        return ""

    cnic = cnic.strip()

    # already formatted
    if re.fullmatch(r"\d{5}-\d{7}-\d", cnic):
        return cnic

    # digits only → format it
    if cnic.isdigit() and len(cnic) == 13:
        return f"{cnic[:5]}-{cnic[5:12]}-{cnic[12]}"

    raise ValueError("Invalid CNIC format")




def validate_phone_number(mobile: str) -> str:
    """
    Accepts:
    - 03xx-xxxxxxx
    - 03xxxxxxxxx

    Returns:
    - Formatted mobile: 03xx-xxxxxxx

    Raises:
    - ValueError if invalid
    """
    if not mobile:
        return ""

    mobile = mobile.strip()

    # already formatted
    if re.fullmatch(r"03\d{2}-\d{7}", mobile):
        return mobile

    # digits only → format it
    if mobile.isdigit() and len(mobile) == 11 and mobile.startswith("03"):
        return f"{mobile[:4]}-{mobile[4:]}"

    raise ValueError("Invalid mobile number format")
