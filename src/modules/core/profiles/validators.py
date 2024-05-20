import re

from django.core.exceptions import ValidationError
from django.utils import timezone

PHONE_NUMBER_LENGTH = 11
CPF_LENGTH = 11

INVALID_PHONE_NUMBER_MESSAGE = "O número de telefone deve conter {length} dígitos."
INVALID_PHONE_NUMBER_DDD_MESSAGE = "O DDD do telefone é inválido."
PHONE_NUMBER_START_DIGIT = "O número de telefone deve começar com o dígito 9."

INVALID_CPF_MESSAGE = "CPF inválido."

INVALID_BIRTHDATE_MESSAGE = "A data de nascimento não pode ser maior que a data atual."

CEP_NOT_FOUND_ERROR_MESSAGE = (
    "CEP não encontrado. Por favor, verifique e tente novamente."
)

VALID_DDDS = {
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "21",
    "22",
    "24",
    "27",
    "28",
    "31",
    "32",
    "33",
    "34",
    "35",
    "37",
    "38",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "51",
    "53",
    "54",
    "55",
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
    "68",
    "69",
    "71",
    "73",
    "74",
    "75",
    "77",
    "79",
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "88",
    "89",
    "91",
    "92",
    "93",
    "94",
    "95",
    "96",
    "97",
    "98",
    "99",
}


def validate_phone(value):
    phone_number = re.sub(r"\D", "", value)
    if len(phone_number) != PHONE_NUMBER_LENGTH:
        raise ValidationError(
            INVALID_PHONE_NUMBER_MESSAGE.format(length=PHONE_NUMBER_LENGTH),
            code="invalid_phone_number",
        )

    ddd = phone_number[:2]
    if ddd not in VALID_DDDS:
        raise ValidationError(
            INVALID_PHONE_NUMBER_DDD_MESSAGE,
            code="invalid_phone_number",
        )
    if phone_number[2] != "9":
        raise ValidationError(
            PHONE_NUMBER_START_DIGIT,
            code="invalid_phone_number",
        )

    return f"+55 ({ddd}) {phone_number[2:7]}-{phone_number[7:]}"


def validate_cpf(value):
    cpf = [int(char) for char in value if char.isdigit()]
    if len(cpf) != CPF_LENGTH or len(set(cpf)) == 1:
        raise ValidationError(INVALID_CPF_MESSAGE, code="invalid")

    for i in range(9, 11):
        value = sum(cpf[num] * ((i + 1) - num) for num in range(i))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            raise ValidationError(INVALID_CPF_MESSAGE, code="invalid")

    return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"


def validate_birthdate(value):
    if value > timezone.now().date():
        raise ValidationError(
            INVALID_BIRTHDATE_MESSAGE,
            code="invalid_birth_date",
        )
    return value


class CEPNotFoundError(ValidationError):
    def __init__(self):
        super().__init__(CEP_NOT_FOUND_ERROR_MESSAGE)
