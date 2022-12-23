# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "ACc1d1e66d2119592c553e93929ed53042"
auth_token = "060144533dcb5c09c6e6712c96992c59"
client = Client(account_sid, auth_token)

validation_request = client.validation_requests \
                           .create(
                                friendly_name='ihsan',
                                phone_number='+905510453344'
                            )

print(validation_request.friendly_name)