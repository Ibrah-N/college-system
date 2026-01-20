def title_case(text: str | None):

    if not text:
        return ""
    return " ".join(word.capitalize() for word in text.split())
