from twilio.rest import Client

class Notify:
    def __init__(self, account_sid, auth_token, from_number):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send_sms(self, to_number, message):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return {"status": "sent", "sid": message.sid}
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return {"status": "failed", "error": str(e)}
