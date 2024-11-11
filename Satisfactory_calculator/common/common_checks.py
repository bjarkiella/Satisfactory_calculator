# This file contains general checks used throughout the program


def check_overclock(value: float) -> float:
    '''
    Validates the overclock value, ensuring it is within the range 1-250.
    Raises a ValueError if out of range.
    '''
    try:
        if 1.0 <= value <= 250.0:
            return value
        else:
            raise ValueError("Overclock must be within the range 1 to 250.")
    except ValueError as e:
        print(f"{e} Setting overclock to default value of 100.")
        return 100.0