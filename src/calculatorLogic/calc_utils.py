
def is_float_str(value: str) -> bool:
    # Handling the case for one decimal point
    cleaned_value = value.replace(".", "", 1)

    # Check if the cleaned string consists only of digits
    return cleaned_value.isdigit()