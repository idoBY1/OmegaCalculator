
def delete_whitespace(expression: str) -> str:
    return "".join(expression.split())

def organize_whitespace(expression: str) -> str:
    return " ".join(expression.split())

def is_float_str(value: str) -> bool:
    # Handling the case for one decimal point
    value = delete_whitespace(value)
    cleaned_value = value.replace(".", "", 1)

    # Check if the cleaned string consists only of digits
    return cleaned_value.isdigit()