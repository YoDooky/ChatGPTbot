def validate_data(string_data: str) -> bool:
    if "www.youtube.com/" or "youtu.be" in string_data:
        return True
    return False
