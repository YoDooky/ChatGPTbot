from __future__ import annotations


def validate_data(string_data: str) -> None | str:
    if "youtube.com" not in string_data and "youtu.be" not in string_data:
        return
    if "youtu.be" in string_data:
        data = string_data.replace('youtu.be/', 'www.youtube.com/watch?v=')
    else:
        data = string_data
    return data
