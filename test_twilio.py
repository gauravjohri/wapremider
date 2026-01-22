from twilio.rest import Client

client = Client("ACea1c765b4a73e294779d651f1b5c4386", "90f00acaf0174ec51db9bc36e00983a4")

client.messages.create(
    from_="whatsapp:+14155238886",
    to="whatsapp:+918289074378",
    body="Twilio auth test"
)

print("SUCCESS")
