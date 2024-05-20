from decimal import Decimal


def calculate_tuition(
    classification: str,
    base_price: float | Decimal,
    salario_minimo: float | Decimal,
):
    special_prices = {
        "X": salario_minimo,  # Preço definido como salário mínimo
        "Z": Decimal(base_price)
        * Decimal(0.5),  # 50% do preço base para programas sociais
    }

    # Verifica se a classificação é uma das especiais e retorna o preço correspondente
    if classification in special_prices:
        return special_prices[classification]

    # Calcula o preço baseado na classificação regular de 'A' a 'G' e 'G' a 'T'
    if classification == "G":
        return base_price
    if classification == "T":
        return 99.99  # Preço fixo para a classificação 'T'

    if "A" <= classification <= "G":
        index = ord("G") - ord(classification)
        multiplier = 2 - index * (1 / (ord("G") - ord("A")))
        return Decimal(base_price) * Decimal(multiplier)

    if "G" < classification < "T":
        index = ord(classification) - ord("G")
        multiplier = 1 - index * (0.9 / (ord("T") - ord("G") - 1))
        return max(Decimal(base_price) * Decimal(multiplier), 99.99)

    unknown_classification_error = "Classificação desconhecida"
    raise ValueError(unknown_classification_error)


def calculate_commission(classification: str, group: str):
    if classification == "Z":
        return 0
    if group == "C":
        return 5
    if group == "P":
        if classification == "P":
            return 10
        if classification == "T":
            return 20
        if classification == "A":
            return 50
    return None  # Adicionado retorno explícito de None para clareza


def calculate_monthly(classification: str, duration: int):
    if classification == "P":
        return 0
    return duration + 6
