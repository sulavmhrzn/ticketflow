import time

import requests
from cryptography.hazmat.primitives import serialization
from jwt.algorithms import RSAAlgorithm


def fetch_verifying_key(
    jwks_url: str, max_retries: int = 5, backoff_seconds: float = 2.0
) -> str:
    last_error = None
    for attemt in range(1, max_retries + 1):
        try:
            response = requests.get(jwks_url, timeout=5)
            response.raise_for_status()

            jwks = response.json()
            first_key = jwks["keys"][0]

            public_key = RSAAlgorithm.from_jwk(first_key)

            return public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as exc:
            last_error = exc
            if attemt < max_retries:
                time.sleep(backoff_seconds * attemt)

    raise RuntimeError(
        f"Could not fetch JWKS from {jwks_url} after {max_retries} attempts."
        f"Is the auth service reachable? Last error: {last_error}"
    )
