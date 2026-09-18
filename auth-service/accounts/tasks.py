from celery import shared_task


@shared_task
def send_otp_sms(*, phone_number: str, code: str, purpose: str):
    print(f"[SMS STUB] Sending OTP '{code}' to {phone_number} for {purpose}")
