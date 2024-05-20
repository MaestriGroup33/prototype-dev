from django.test import TestCase
from views import send_message

# Create your tests here.


class WhatsappTestCase(TestCase):
    def test_send_message(self):
        chat_id = "554396648750@c.us"
        text = "Hello, world!"
        send_message(chat_id, text)
        self.assertEqual(
            WhatsAppMessage.objects.filter(chat_id=chat_id, text=text).count(),
            1,
        )
        self.assertTrue(WhatsAppMessage.objects.get(chat_id=chat_id, text=text).is_sent)

    send_message("554396648750@c.us", "Hello, world!")
