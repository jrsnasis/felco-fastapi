#!/usr/bin/env python3
"""
Secret Key Generator for FastAPI Applications
Generate cryptographically secure secret keys for different environments
"""

import secrets
import string
from datetime import datetime


def generate_secret_key(length: int = 64) -> str:
    """Generate a cryptographically secure secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_jwt_secret() -> str:
    """Generate a URL-safe base64 secret for JWT tokens"""
    return secrets.token_urlsafe(32)


def generate_openssl_style() -> str:
    """Generate OpenSSL-style hex secret"""
    return secrets.token_hex(32)


def main():
    print("=" * 60)
    print("SECRET KEY GENERATOR FOR FASTAPI")
    print("=" * 60)
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print("1. Standard Secret Key (64 chars with special characters):")
    print(f"   {generate_secret_key()}")
    print()

    print("2. JWT-Safe Secret Key (URL-safe base64):")
    print(f"   {generate_jwt_secret()}")
    print()

    print("3. OpenSSL-style Hex Secret (64 hex chars):")
    print(f"   {generate_openssl_style()}")
    print()

    print("ENVIRONMENT-SPECIFIC KEYS:")
    print("-" * 30)

    environments = ["development", "staging", "production"]
    for env in environments:
        print(f"{env.upper()}_SECRET_KEY={generate_secret_key()}")

    print()
    print("SECURITY NOTES:")
    print("- Use different keys for each environment")
    print("- Never commit secret keys to version control")
    print("- Store production keys in secure environment variables")
    print("- Rotate keys regularly in production")
    print("=" * 60)


if __name__ == "__main__":
    main()
