def validate_data(string_data: str) -> bool:
    if "https://www.youtube.com/" in string_data:
        return True
    return False
