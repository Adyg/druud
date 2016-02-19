from twilio.rest import TwilioRestClient
from django.conf import settings


def send_sms(phone_number, message):
    client = TwilioRestClient(account=settings.TWILIO_ACCOUNT_SID, token=settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(to=phone_number, from_=settings.TWILIO_PHONE_NUMBER, body=message)

