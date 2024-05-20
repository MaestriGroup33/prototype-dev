from decimal import Decimal

from src.modules.core.finances.models import Indicators


def calculate_tuition(classification: str, base_price: float | Decimal):
    """
    Calculates the tuition price based on classification and the base_price

    Special cases:
    X: -> minimum wage
    Z: -> 50% of base_price
    """

    special_prices = {
        "X": Indicators.get_minimun_wage(),  # Preço definido como salário mínimo
        "Z": Decimal(base_price) * Decimal(0.5),
        # 50% do preço base para programas sociais
    }

    # Verifica se a classificação é uma das especiais e retorna o preço correspondente
    if classification in special_prices:
        return special_prices[classification]

    # Calcula o preço baseado na classificação regular de 'A' a 'G' e 'G' a 'T'
    if classification == "G":
        return base_price
    elif classification == "T":
        return 99.99  # Preço fixo para a classificação 'T'
    elif classification >= "A" and classification <= "G":
        # Aumento progressivo de 'G' (preço base) até 'A'
        divider = ord("G") - ord("A")
        index = divider - (ord("G") - ord(classification))
        multiplier = 2 - index * (1 / divider)
        return Decimal(base_price) * Decimal(multiplier)
    elif "G" < classification < "T":
        print("G < class < T")
        # Diminuição progressiva de 'G' a 'T' com um limite mínimo de 99.99
        index = ord(classification) - ord("G")
        multiplier = 1 - index * (0.9 / (ord("T") - ord("G") - 1))
        return max(Decimal(base_price) * Decimal(multiplier), 99.99)
    else:
        # Se a classificação não for reconhecida, lança um erro
        raise ValueError("Classificação desconhecida")


def calculate_commission(classification: str, group: str):
    if classification == "S":
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


print(calculate_tuition("Q", 1000))
