#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт сборки ДЕМО-версии Net-Constructor
Генерирует токены и встраивает их в модуль license.py перед компиляцией
"""

import hashlib
import hmac
import subprocess
import sys
import shutil
import os

# Конфигурация для демо-сборки
DEMO_CONFIG = {
    'BUILD_SECRET_KEY': 'DEMO_BUILD_KEY_2026_XJF8P2QK9M7N3R5T',
    'BUILD_TYPE': 'demo'
}


def generate_tokens(secret_key):
    """Генерирует токены для встраивания"""
    demo_hmac = hmac.new(
        secret_key.encode(),
        "DEMO_MODE_ACTIVE".encode(),
        hashlib.sha256
    ).hexdigest()
    
    full_hmac = hmac.new(
        secret_key.encode(),
        "FULL_MODE_ACTIVE".encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Вычисляем обфусцированные значения
    x = sum(ord(c) for c in secret_key)
    y = len(secret_key) * 7919
    demo_value = (x ^ y) % 256
    
    return {
        'DEMO_TOKEN': demo_hmac,
        'FULL_TOKEN': '',  # Пустой для демо
        'DEMO_HASH_VALUE': demo_value,
        'FULL_HASH_VALUE': 0
    }


def backup_license_module():
    """Создает резервную копию модуля license.py"""
    source = 'package/modules/license.py'
    backup = 'package/modules/license.py.backup'
    
    if os.path.exists(source):
        shutil.copy2(source, backup)
        print(f"✓ Backup created: {backup}")
        return True
    return False


def restore_license_module():
    """Восстанавливает резервную копию модуля license.py"""
    source = 'package/modules/license.py.backup'
    target = 'package/modules/license.py'
    
    if os.path.exists(source):
        shutil.copy2(source, target)
        os.remove(source)
        print(f"✓ License module restored from backup")
        return True
    return False


def prepare_license_module():
    """Подготавливает модуль license.py с встроенными токенами"""
    # Создаем backup
    if not backup_license_module():
        print("✗ Failed to create backup")
        return False
    
    try:
        # Читаем шаблон
        with open('package/modules/license.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Генерируем токены
        tokens = generate_tokens(DEMO_CONFIG['BUILD_SECRET_KEY'])
        
        # Заменяем плейсхолдеры
        content = content.replace('{{BUILD_SECRET_KEY}}', DEMO_CONFIG['BUILD_SECRET_KEY'])
        content = content.replace('{{DEMO_TOKEN}}', tokens['DEMO_TOKEN'])
        content = content.replace('{{FULL_TOKEN}}', tokens['FULL_TOKEN'])
        content = content.replace('{{DEMO_HASH_VALUE}}', str(tokens['DEMO_HASH_VALUE']))
        content = content.replace('{{FULL_HASH_VALUE}}', str(tokens['FULL_HASH_VALUE']))
        
        # Сохраняем
        with open('package/modules/license.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ License module prepared for {DEMO_CONFIG['BUILD_TYPE']} build")
        print(f"  Secret Key: {DEMO_CONFIG['BUILD_SECRET_KEY'][:20]}...")
        print(f"  Demo Token: {tokens['DEMO_TOKEN'][:20]}...")
        print(f"  Demo Hash Value: {tokens['DEMO_HASH_VALUE']}")
        
        return True
    except Exception as e:
        print(f"✗ Error preparing license module: {e}")
        restore_license_module()
        return False


def build_with_nuitka():
    """Запускает сборку с Nuitka"""
    cmd = [
        'python', '-m', 'nuitka',
        '--standalone',
        '--enable-plugin=pyside6',
        '--windows-company-name=Constant',
        '--windows-product-name=Net-Constructor Demo',
        '--windows-product-version=1.1.0',
        '--output-dir=build_demo',
        '--output-filename=net-constructor-demo.exe',
        'main.pyw'
    ]
    
    # Добавляем иконку если файл существует
    if os.path.exists('resources/app-icon.ico'):
        cmd.insert(4, '--windows-icon-from-ico=resources/app-icon.ico')
    
    print("\nStarting Nuitka build...")
    print(f"Command: {' '.join(cmd)}")
    print("This may take several minutes...\n")
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"\n✓ Demo build completed successfully!")
        return True
    else:
        print(f"\n✗ Build failed with code {result.returncode}")
        return False


def main():
    print("=" * 60)
    print("Building DEMO version of Net-Constructor")
    print("=" * 60)
    print()
    
    # Проверяем наличие Nuitka
    try:
        result = subprocess.run(['python', '-m', 'nuitka', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Nuitka found: {result.stdout.strip()}")
        else:
            print("✗ Nuitka not found. Install it with: pip install nuitka")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error checking Nuitka: {e}")
        sys.exit(1)
    
    print()
    
    # Подготавливаем модуль license
    if not prepare_license_module():
        sys.exit(1)
    
    print()
    
    # Запускаем сборку
    try:
        success = build_with_nuitka()
    finally:
        # Всегда восстанавливаем оригинальный файл
        print("\nRestoring original license.py...")
        restore_license_module()
    
    if success:
        print("\n" + "=" * 60)
        print("✓ Demo build ready in build_demo/")
        print("=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
