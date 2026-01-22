from twilio.rest import Client

client = Client("ACea1c765b4a73e294779d651f1b5c4386", "c725762bb41419a98ad761e718322946")

client.messages.create(
    from_="whatsapp:+14155238886",
    to="whatsapp:+918289074378",
    body="Twilio auth test"
)

print("SUCCESS")
