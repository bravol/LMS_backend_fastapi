from uuid import uuid4
import base64

def generateUniqueId(length=20):
    return base64.urlsafe_b64encode(uuid4().bytes).rstrip(b'=').decode('ascii')[:length]