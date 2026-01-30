#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт варианта сборки: генерирует package/modules/_build_config.py
для демо или полной версии. Запускать перед Nuitka:
  python build_variant.py --demo
  python build_variant.py --full
"""

import argparse
import hashlib
import hmac
import os
import secrets
import string

# Длина секрета (символы)
SECRET_LENGTH = 48
# Алфавит для секрета
SECRET_ALPHABET = string.ascii_letters + string.digits


def _compute_z(secret: str) -> int:
    """z = (x ^ y) % 256, как в license._obfuscated_check"""
    x = sum(ord(c) for c in secret)
    y = len(secret) * 7919
    return (x ^ y) % 256


def _compute_hmac_token(secret: str, message: str) -> str:
    """HMAC-SHA256(secret, message) в hex"""
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()


def generate_secret() -> str:
    """Генерирует случайный секрет для сборки"""
    return "".join(secrets.choice(SECRET_ALPHABET) for _ in range(SECRET_LENGTH))


def build_demo_config() -> str:
    """Генерирует конфиг для демо-сборки: is_demo_mode() == True"""
    secret = generate_secret()
    demo_token = _compute_hmac_token(secret, "DEMO_MODE_ACTIVE")
    z = _compute_z(secret)
    demo_hash_value = z
    full_hash_value = (z + 1) % 256  # чтобы z != full_value
    return _render_config(
        secret=secret,
        demo_token=demo_token,
        full_token="",  # не используется для результата в demo
        demo_hash_value=demo_hash_value,
        full_hash_value=full_hash_value,
    )


def build_full_config() -> str:
    """Генерирует конфиг для полной сборки: is_demo_mode() == False"""
    secret = generate_secret()
    full_token = _compute_hmac_token(secret, "FULL_MODE_ACTIVE")
    z = _compute_z(secret)
    full_hash_value = z
    demo_hash_value = (z + 1) % 256  # чтобы z != demo_value
    return _render_config(
        secret=secret,
        demo_token="",  # не совпадает с expected -> _check_demo_token False
        full_token=full_token,
        demo_hash_value=demo_hash_value,
        full_hash_value=full_hash_value,
    )


def _render_config(
    secret: str,
    demo_token: str,
    full_token: str,
    demo_hash_value: int,
    full_hash_value: int,
) -> str:
    """Формирует содержимое _build_config.py"""
    return f'''# _build_config.py — сгенерирован build_variant.py, не редактировать вручную

BUILD_SECRET_KEY = {repr(secret)}
BUILD_DEMO_TOKEN = {repr(demo_token)}
BUILD_FULL_TOKEN = {repr(full_token)}
BUILD_DEMO_HASH_VALUE = {demo_hash_value}
BUILD_FULL_HASH_VALUE = {full_hash_value}
'''


def main():
    parser = argparse.ArgumentParser(description="Generate _build_config.py for demo or full build")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--demo", action="store_true", help="Demo build")
    group.add_argument("--full", action="store_true", help="Full build")
    args = parser.parse_args()

    if args.demo:
        content = build_demo_config()
        variant = "demo"
    else:
        content = build_full_config()
        variant = "full"

    # Путь к package/modules/_build_config.py относительно корня проекта
    root = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(root, "package", "modules", "_build_config.py")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Written {out_path} ({variant} variant)")


if __name__ == "__main__":
    main()
