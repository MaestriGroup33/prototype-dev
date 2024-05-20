import requests
from django.apps import AppConfig


class WhatsappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.tools.whatsapp"
    verbose_name = "WhatsApp - Integração com API do WhatsApp para envio de mensagens."


def send_whatsapp_message(phone_number: str):
    access_token = ""
    api_url = ""
    message = ""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message,
        },
    }
    response = requests.post(f"{api_url}/messages", headers=headers, json=data)
    return response.json()
