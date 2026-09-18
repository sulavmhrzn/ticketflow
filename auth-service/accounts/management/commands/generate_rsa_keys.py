from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates an RSA keypair for signing JWTs (RS256)."

    def handle(self, *args, **kwargs):
        keys_dir = Path(settings.BASE_DIR / "keys")
        keys_dir.mkdir(exist_ok=True)

        private_path = keys_dir / "private.pem"
        public_path = keys_dir / "public.pem"

        if private_path.exists() or public_path.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Key files already exist - refusing to overwrite. Delete them manually."
                )
            )
            return

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_path.write_bytes(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

        public_path.write_bytes(
            private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

        self.stdout.write(self.style.SUCCESS(f"Keys written to {keys_dir}/"))
