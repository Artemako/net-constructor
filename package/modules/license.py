# license.py
# Модуль защиты демо-режима с многоуровневой верификацией

import hashlib
import hmac
import base64
import sys
import os

# Секретный ключ встраивается на этапе компиляции
# Для демо: SECRET_KEY = "{{BUILD_SECRET_KEY}}"
# Для полной: SECRET_KEY = "{{BUILD_SECRET_KEY}}"
SECRET_KEY = "{{BUILD_SECRET_KEY}}"


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
    except:
        # Fallback для разработки
        return hashlib.sha256(SECRET_KEY.encode()).hexdigest()


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
        # Токен встраивается на этапе компиляции
        actual = "90a5cd5e89bcb54f8a6ed2e7ab812d6be99264e01ea83b3fae58471c9d46536d"
        return actual == expected
    
    def _check_full_token(self):
        """Проверка токена полной версии"""
        expected = self._compute_hmac("FULL_MODE_ACTIVE")
        actual = ""
        return actual == expected


def _obfuscated_check():
    """Обфусцированная проверка режима"""
    # Множественные вычисления для усложнения анализа
    x = sum(ord(c) for c in SECRET_KEY)
    y = len(SECRET_KEY) * 7919  # Простое число
    z = (x ^ y) % 256
    
    # Встроенные значения на этапе компиляции
    demo_value = {{DEMO_HASH_VALUE}}
    full_value = {{FULL_HASH_VALUE}}
    
    if z == demo_value:
        return True  # Demo mode
    elif z == full_value:
        return False  # Full mode
    return None  # Invalid


def _check_debugger():
    """Проверка на наличие отладчика"""
    import sys
    import ctypes
    
    if sys.gettrace() is not None:
        # Отладчик обнаружен
        return True
    
    # Проверка для Windows
    if sys.platform == 'win32':
        try:
            if ctypes.windll.kernel32.IsDebuggerPresent():
                return True
        except:
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
    _validator._validation_count += 1
    
    # Множественные проверки
    check1 = _validator._check_demo_token()
    check2 = _obfuscated_check()
    
    # Все проверки должны совпадать
    result = check1 and check2 is True
    
    # Кешируем результат с подписью
    sig = _get_runtime_signature()
    _validator._cache[sig] = result
    
    # Проверка на отладчик (опционально)
    # if _check_debugger():
    #     return True  # В демо-режиме при отладке
    
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
