def convert_temperature(celsius_value: float, target_unit: str) -> float:
    """
    Converts a temperature from Celsius to the target unit.
    Accepted units: 'C' (Celsius), 'F' (Fahrenheit), 'K' (Kelvin).
    """
    unit = target_unit.upper()
    
    if unit == "F":
        return round((celsius_value * 9/5) + 32, 2)
    elif unit == "K":
        return round(celsius_value + 273.15, 2)
    
    # Returns Celsius by default (or if the unit is invalid)
    return round(celsius_value, 2)
