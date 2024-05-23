from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Identification:
    number: int
    type: str


@dataclass
class Payer:
    id: int
    email: str
    identification: Identification
    type: str


@dataclass
class Item:
    id: str
    title: str
    description: str
    picture_url: str
    category_id: str
    quantity: int
    unit_price: float


@dataclass
class ReceiverAddress:
    street_name: str
    street_number: int
    zip_code: int
    city_name: str
    state_name: str


@dataclass
class Shipments:
    receiver_address: ReceiverAddress


@dataclass
class AdditionalInfo:
    items: List[Item]
    payer: Dict[str, str]
    shipments: Shipments


@dataclass
class TransactionDetails:
    net_received_amount: float
    total_paid_amount: float
    overpaid_amount: float
    installment_amount: float


@dataclass
class FeeDetail:
    type: str
    amount: float
    fee_payer: str


@dataclass
class Cardholder:
    name: str
    identification: Identification


@dataclass
class Card:
    first_six_digits: int
    last_four_digits: int
    expiration_month: int
    expiration_year: int
    date_created: str
    date_last_updated: str
    cardholder: Cardholder


@dataclass
class ApplicationData:
    name: str
    version: str


@dataclass
class TransactionData:
    qr_code_base64: str
    qr_code: str
    ticket_url: str


@dataclass
class PointOfInteraction:
    type: str
    application_data: ApplicationData
    transaction_data: TransactionData


@dataclass
class PaymentResponseData:
    id: int
    date_created: str
    date_approved: str
    date_last_updated: str
    money_release_date: str
    issuer_id: int
    payment_method_id: str
    payment_type_id: str
    status: str
    status_detail: str
    currency_id: str
    description: str
    # taxes_amount: float
    # shipping_amount: float
    # collector_id: int
    payer: Payer
    metadata: Dict
    # additional_info: AdditionalInfo
    # external_reference: str
    # transaction_amount: float
    # transaction_amount_refunded: float
    # coupon_amount: float
    # transaction_details: TransactionDetails
    # fee_details: List[FeeDetail]
    # statement_descriptor: str
    installments: int
    card: Card
    notification_url: str
    processing_mode: str
    # point_of_interaction: PointOfInteraction

    @staticmethod
    def create_from_json(data: dict) -> "PaymentResponseData":
        return PaymentResponseData(
            id=data["id"],
            date_created=data["date_created"],
            date_approved=data["date_approved"],
            date_last_updated=data["date_last_updated"],
            money_release_date=data["money_release_date"],
            issuer_id=data["issuer_id"],
            payment_method_id=data["payment_method_id"],
            payment_type_id=data["payment_type_id"],
            status=data["status"],
            status_detail=data["status_detail"],
            currency_id=data["currency_id"],
            description=data["description"],
            # taxes_amount=data['taxes_amount'],
            # shipping_amount=data['shipping_amount'],
            # collector_id=data['collector_id'],
            payer=Payer(
                id=data["payer"]["id"],
                email=data["payer"]["email"],
                identification=Identification(
                    number=data["payer"]["identification"]["number"],
                    type=data["payer"]["identification"]["type"],
                ),
                type=data["payer"]["type"],
            ),
            metadata=data["metadata"],
            # additional_info=AdditionalInfo(
            #     items=[Item(**item) for item in data["additional_info"]["items"]],
            #     payer=data["additional_info"]["payer"],
            #     shipments=Shipments(
            #         receiver_address=ReceiverAddress(
            #             **data["additional_info"]["shipments"]["receiver_address"]
            #         )
            #     ),
            # ),
            # external_reference=data['external_reference'],
            # transaction_amount=data['transaction_amount'],
            # transaction_amount_refunded=data['transaction_amount_refunded'],
            # coupon_amount=data['coupon_amount'],
            # transaction_details=TransactionDetails(**data['transaction_details']),
            # fee_details=[FeeDetail(**fee) for fee in data['fee_details']],
            # statement_descriptor=data['statement_descriptor'],
            installments=data["installments"],
            card=Card(
                first_six_digits=data["card"]["first_six_digits"],
                last_four_digits=data["card"]["last_four_digits"],
                expiration_month=data["card"]["expiration_month"],
                expiration_year=data["card"]["expiration_year"],
                date_created=data["card"]["date_created"],
                date_last_updated=data["card"]["date_last_updated"],
                cardholder=Cardholder(
                    name=data["card"]["cardholder"]["name"],
                    identification=Identification(
                        number=data["card"]["cardholder"]["identification"]["number"],
                        type=data["card"]["cardholder"]["identification"]["type"],
                    ),
                ),
            ),
            notification_url=data["notification_url"],
            processing_mode=data["processing_mode"],
            # point_of_interaction=PointOfInteraction(
            #     type=data['point_of_interaction']['type'],
            #     application_data=ApplicationData(**data['point_of_interaction']['application_data']),
            #     transaction_data=TransactionData(**data['point_of_interaction']['transaction_data'])
            # )
        )
