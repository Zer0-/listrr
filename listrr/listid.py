from random import SystemRandom
from base64 import urlsafe_b64encode

def urlsafe_bytestring(n):
    randint = lambda: SystemRandom().randint(0, 255)
    bytestring = bytes([randint() for i in range(n)])
    return urlsafe_b64encode(bytestring)

def gen_list_uuid(size):
    return urlsafe_bytestring(3*size)
