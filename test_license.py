#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования модуля license.py в режиме разработки
"""

import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))


def test_demo_mode():
    """Тестирует демо-режим"""
    print("=" * 60)
    print("Testing DEMO mode")
    print("=" * 60)
    
    # Временно модифицируем license.py для демо-режима
    license_path = 'package/modules/license.py'
    
    with open(license_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем плейсхолдеры для демо-режима
    import hashlib
    import hmac
    
    secret_key = 'DEMO_BUILD_KEY_2026_XJF8P2QK9M7N3R5T'
    
    demo_hmac = hmac.new(
        secret_key.encode(),
        "DEMO_MODE_ACTIVE".encode(),
        hashlib.sha256
    ).hexdigest()
    
    x = sum(ord(c) for c in secret_key)
    y = len(secret_key) * 7919
    demo_value = (x ^ y) % 256
    
    test_content = content.replace('{{BUILD_SECRET_KEY}}', secret_key)
    test_content = test_content.replace('{{DEMO_TOKEN}}', demo_hmac)
    test_content = test_content.replace('{{FULL_TOKEN}}', '')
    test_content = test_content.replace('{{DEMO_HASH_VALUE}}', str(demo_value))
    test_content = test_content.replace('{{FULL_HASH_VALUE}}', '0')
    
    # Сохраняем для теста
    with open(license_path, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("\n[OK] License module configured for DEMO mode")
    print(f"  Secret Key: {secret_key[:20]}...")
    print(f"  Demo Token: {demo_hmac[:20]}...")
    print(f"  Demo Hash Value: {demo_value}")
    
    # Импортируем и тестируем
    try:
        # Удаляем модуль из кеша если он уже загружен
        if 'package.modules.license' in sys.modules:
            del sys.modules['package.modules.license']
        
        import package.modules.license as license
        
        print("\n" + "-" * 60)
        print("Running tests:")
        print("-" * 60)
        
        is_demo = license.is_demo_mode()
        is_full = license.is_full_mode()
        mode_str = license.get_mode_string()
        
        print(f"\nOK is_demo_mode(): {is_demo}")
        print(f"OK is_full_mode(): {is_full}")
        print(f"OK get_mode_string(): {mode_str}")
        
        if is_demo and not is_full and mode_str == "demo":
            print("\nOKOKOK DEMO MODE TEST PASSED OKOKOK")
            return True
        else:
            print("\nFAILFAILFAIL DEMO MODE TEST FAILED FAILFAILFAIL")
            return False
            
    except Exception as e:
        print(f"\nFAIL Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_mode():
    """Тестирует полный режим"""
    print("\n\n" + "=" * 60)
    print("Testing FULL mode")
    print("=" * 60)
    
    # Временно модифицируем license.py для полного режима
    license_path = 'package/modules/license.py'
    
    with open(license_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем плейсхолдеры для полного режима
    import hashlib
    import hmac
    
    secret_key = 'FULL_BUILD_KEY_2026_K8W9Q2M5P7X3C6V4'
    
    full_hmac = hmac.new(
        secret_key.encode(),
        "FULL_MODE_ACTIVE".encode(),
        hashlib.sha256
    ).hexdigest()
    
    x = sum(ord(c) for c in secret_key)
    y = len(secret_key) * 7919
    full_value = (x ^ y) % 256
    
    test_content = content.replace('{{BUILD_SECRET_KEY}}', secret_key)
    test_content = test_content.replace('{{DEMO_TOKEN}}', '')
    test_content = test_content.replace('{{FULL_TOKEN}}', full_hmac)
    test_content = test_content.replace('{{DEMO_HASH_VALUE}}', '0')
    test_content = test_content.replace('{{FULL_HASH_VALUE}}', str(full_value))
    
    # Сохраняем для теста
    with open(license_path, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("\nOK License module configured for FULL mode")
    print(f"  Secret Key: {secret_key[:20]}...")
    print(f"  Full Token: {full_hmac[:20]}...")
    print(f"  Full Hash Value: {full_value}")
    
    # Импортируем и тестируем
    try:
        # Удаляем модуль из кеша если он уже загружен
        if 'package.modules.license' in sys.modules:
            del sys.modules['package.modules.license']
        
        import package.modules.license as license
        
        print("\n" + "-" * 60)
        print("Running tests:")
        print("-" * 60)
        
        is_demo = license.is_demo_mode()
        is_full = license.is_full_mode()
        mode_str = license.get_mode_string()
        
        print(f"\nOK is_demo_mode(): {is_demo}")
        print(f"OK is_full_mode(): {is_full}")
        print(f"OK get_mode_string(): {mode_str}")
        
        if not is_demo and is_full and mode_str == "full":
            print("\nOKOKOK FULL MODE TEST PASSED OKOKOK")
            return True
        else:
            print("\nFAILFAILFAIL FULL MODE TEST FAILED FAILFAILFAIL")
            return False
            
    except Exception as e:
        print(f"\nFAIL Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def restore_template():
    """Восстанавливает шаблон license.py"""
    print("\n" + "=" * 60)
    print("Restoring template")
    print("=" * 60)
    
    license_path = 'package/modules/license.py'
    
    with open(license_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Восстанавливаем плейсхолдеры
    import re
    
    # Заменяем любые ключи/токены обратно на плейсхолдеры
    patterns = [
        (r'SECRET_KEY = "[^"]*"', 'SECRET_KEY = "{{BUILD_SECRET_KEY}}"'),
        (r'actual = "[0-9a-f]{64}"  # Токен встраивается', 'actual = "{{DEMO_TOKEN}}"'),
        (r'actual = "[0-9a-f]*"  # Токен', 'actual = "{{FULL_TOKEN}}"'),
        (r'demo_value = \d+', 'demo_value = {{DEMO_HASH_VALUE}}'),
        (r'full_value = \d+', 'full_value = {{FULL_HASH_VALUE}}'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    with open(license_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("OK Template restored")


def main():
    print("\n" + "=" * 60)
    print("LICENSE MODULE TESTING")
    print("=" * 60)
    
    demo_passed = test_demo_mode()
    full_passed = test_full_mode()
    
    restore_template()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    print(f"\nDemo mode test: {'OK PASSED' if demo_passed else 'FAIL FAILED'}")
    print(f"Full mode test: {'OK PASSED' if full_passed else 'FAIL FAILED'}")
    
    if demo_passed and full_passed:
        print("\nOKOKOK ALL TESTS PASSED OKOKOK")
        print("\nYou can now build with:")
        print("  python build_demo.py")
        print("  python build_full.py")
        return 0
    else:
        print("\nFAILFAILFAIL SOME TESTS FAILED FAILFAILFAIL")
        return 1


if __name__ == '__main__':
    sys.exit(main())
