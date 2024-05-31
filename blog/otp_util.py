# blog/otp_util.py

import random
from django.core.cache import cache
from django.conf import settings

def generate_otp(user):
    otp = random.randint(100000, 999999)
    cache.set(f'otp_{user.id}', otp, timeout=300)  # OTP valid for 5 minutes
    return otp

def verify_otp(user, otp):
    stored_otp = cache.get(f'otp_{user.id}')
    if stored_otp is not None and str(stored_otp) == str(otp):
        cache.delete(f'otp_{user.id}')
        return True
    return False
