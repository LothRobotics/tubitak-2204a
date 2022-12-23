# Download the helper library from https://www.twilio.com/docs/python/install
import os, random
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "ACc1d1e66d2119592c553e93929ed53042"
auth_token = "060144533dcb5c09c6e6712c96992c59"
client = Client(account_sid, auth_token)

num = str(random.randint(100000, 1000000))

message = client.messages.create(
  body="Furkan bu senin mesajin = "+ str(num),
  from_="+18655357482",
  media_url= 'https://p4.wallpaperbetter.com/wallpaper/833/966/492/4k-anime-girl-hatsune-miku-polygons-wallpaper-preview.jpg',
  to="+905465952986"
)

print(message.sid)