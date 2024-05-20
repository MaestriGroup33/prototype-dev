def calculate_payment_duration(
    duration_semesters: int,
    classification: str | None,
) -> int:
    """
    Based on the number of Semesters, calculates the number of paying months.

    Besides when the classification is 'X' (promotion), it always returns 0

    >>> calculate_payment_duration(2)
    >>> returns 18
    """
    if classification == "X":
        return 0

    return (duration_semesters * 6) + 6
