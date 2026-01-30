# license.py
# Модуль защиты демо-режима с многоуровневой верификацией

import hashlib
import hmac
import base64
import sys
import os

# Константы сборки: из _build_config (при сборке exe) или режим разработки по env
try:
    from ._build_config import (
        BUILD_SECRET_KEY,
        BUILD_DEMO_TOKEN,
        BUILD_FULL_TOKEN,
        BUILD_DEMO_HASH_VALUE,
        BUILD_FULL_HASH_VALUE,
    )
    _DEV_MODE = False
    SECRET_KEY = BUILD_SECRET_KEY
    _DEMO_TOKEN = BUILD_DEMO_TOKEN
    _FULL_TOKEN = BUILD_FULL_TOKEN
    _DEMO_HASH_VALUE = BUILD_DEMO_HASH_VALUE
    _FULL_HASH_VALUE = BUILD_FULL_HASH_VALUE
except ImportError:
    _DEV_MODE = True
    SECRET_KEY = ""
    _DEMO_TOKEN = ""
    _FULL_TOKEN = ""
    _DEMO_HASH_VALUE = 0
    _FULL_HASH_VALUE = 0


def _get_runtime_signature():
    """Создает подпись на основе исполняемого файла"""
    try:
        exe_path = sys.executable
        with open(exe_path, 'rb') as f:
            # Читаем первые и последние 4KB для быстрой проверки
            start = f.read(4096)
            f.seek(-4096, 2)
            end = f.read(4096)
        data = start + end + SECRET_KEY.encode()
        return hashlib.sha256(data).hexdigest()
    except Exception:
        # Fallback для разработки
        return hashlib.sha256(SECRET_KEY.encode()).hexdigest() if SECRET_KEY else ""


class _LicenseValidator:
    """Внутренний класс для проверки лицензии"""

    def __init__(self):
        self._cache = {}
        self._validation_count = 0

    def _compute_hmac(self, data):
        """Вычисляет HMAC для данных"""
        return hmac.new(
            SECRET_KEY.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

    def _check_demo_token(self):
        """Проверка токена демо-режима"""
        expected = self._compute_hmac("DEMO_MODE_ACTIVE")
        actual = _DEMO_TOKEN
        return actual == expected

    def _check_full_token(self):
        """Проверка токена полной версии"""
        expected = self._compute_hmac("FULL_MODE_ACTIVE")
        return _FULL_TOKEN == expected


def _obfuscated_check():
    """Обфусцированная проверка режима"""
    x = sum(ord(c) for c in SECRET_KEY)
    y = len(SECRET_KEY) * 7919  # Простое число
    z = (x ^ y) % 256

    demo_value = _DEMO_HASH_VALUE
    full_value = _FULL_HASH_VALUE

    if z == demo_value:
        return True  # Demo mode
    elif z == full_value:
        return False  # Full mode
    return None  # Invalid


def _check_debugger():
    """Проверка на наличие отладчика"""
    if sys.gettrace() is not None:
        return True
    if sys.platform == 'win32':
        try:
            import ctypes
            if ctypes.windll.kernel32.IsDebuggerPresent():
                return True
        except Exception:
            pass
    return False


# Глобальный валидатор
_validator = _LicenseValidator()


def is_demo_mode():
    """
    Проверяет, запущена ли программа в демо-режиме.

    Returns:
        bool: True если демо-режим, False если полная версия
    """
    if _DEV_MODE:
        return os.environ.get("NET_CONSTRUCTOR_MODE", "demo") == "demo"

    _validator._validation_count += 1

    check1 = _validator._check_demo_token()
    check2 = _obfuscated_check()

    result = check1 and check2 is True

    sig = _get_runtime_signature()
    _validator._cache[sig] = result

    return result


def is_full_mode():
    """
    Проверяет, запущена ли программа в полной версии.

    Returns:
        bool: True если полная версия, False если демо
    """
    return not is_demo_mode()


def get_mode_string():
    """
    Возвращает строковое представление режима.

    Returns:
        str: "demo" или "full"
    """
    return base64.b64decode(b'ZGVtbw==').decode() if is_demo_mode() else base64.b64decode(b'ZnVsbA==').decode()
