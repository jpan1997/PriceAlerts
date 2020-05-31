import twilio.rest

TWILIO_ACCOUNT_SID = 'ACb8bd2991033e5b7a826985740dc4637f'
TWILIO_AUTH_TOKEN = 'b83ee4815bbec4bcc42ce2eb212d4204'
SEND_NUMBER = '+12029529787'
RECV_NUMBER = '+13018321609'

client = twilio.rest.Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_alert(msg):
    send("PRICE ALERT - " + msg)


def send(msg):
    print("Text Message Sent:", msg)
    # message = client.messages.create(body=msg,
    #                                  from_=SEND_NUMBER,
    #                                  to=RECV_NUMBER)
