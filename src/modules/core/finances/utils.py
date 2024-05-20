CommissionClassificationValues = {
    "A": 50,
    "B": 48,
    "C": 47,
    "D": 45,
    "E": 44,
    "F": 42,
    "G": 41,
    "H": 39,
    "I": 37,
    "J": 36,
    "K": 34,
    "L": 33,
    "M": 31,
    "N": 29,
    "O": 28,
    "P": 26,
    "Q": 25,
    "R": 23,
    "S": 22,
    "T": 20,
}


def calculate_commission(classification: str, group: str = "C"):
    if group != "C":
        return 5

    return CommissionClassificationValues[classification.upper()]


# if group == convenant return 5
