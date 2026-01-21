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



if __name__ == "__main__":
    # Test cases
    # test_cnics = [
    #     "35202-1234567-1",
    #     "3520212345671",
    #     "",
    #     None,
    #     "35202-1234567-A",  # Invalid
    #     "35202123456",      # Invalid
    # ]

    # for cnic in test_cnics:
    #     try:
    #         formatted_cnic = validate_cnic(cnic)
    #         print(f"Input CNIC: {cnic} → Formatted: {formatted_cnic}")
    #     except ValueError as e:
    #         print(f"Input CNIC: {cnic} → Error: {e}")

    test_mobiles = [
        "0300-1234567",
        "03001234567",
        "",
        None,
        "0300-123456",   # Invalid
        "04001234567",   # Invalid
    ]

    for mobile in test_mobiles:
        try:
            formatted_mobile = validate_phone_number(mobile)
            print(f"Input Mobile: {mobile} → Formatted: {formatted_mobile}")
        except ValueError as e:
            print(f"Input Mobile: {mobile} → Error: {e}")