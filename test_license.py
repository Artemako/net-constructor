#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования модуля license.py в режиме разработки.
Использует переменную окружения NET_CONSTRUCTOR_MODE и/или сгенерированный _build_config.py
(без правки license.py на диске).
"""

import sys
import os
import subprocess
import glob

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))


def _reimport_license(clear_build_config_cache=False):
    """Удаляет license и _build_config из кеша и импортирует license заново.
    Если clear_build_config_cache=True, удаляет __pycache__ для _build_config,
    чтобы подхватить перезаписанный _build_config.py."""
    if clear_build_config_cache:
        root = os.path.dirname(os.path.abspath(__file__))
        pycache = os.path.join(root, "package", "modules", "__pycache__")
        for path in glob.glob(os.path.join(pycache, "_build_config*.pyc")):
            try:
                os.remove(path)
            except OSError:
                pass
    for mod in ("package.modules.license", "package.modules._build_config"):
        if mod in sys.modules:
            del sys.modules[mod]
    import package.modules.license as license_module
    return license_module


def _ensure_no_build_config():
    """Удаляет _build_config.py при наличии, чтобы license использовал env."""
    root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root, "package", "modules", "_build_config.py")
    if os.path.isfile(path):
        os.remove(path)


def test_demo_mode_env():
    """Тестирует демо-режим через переменную окружения (режим разработки)."""
    print("=" * 60)
    print("Testing DEMO mode (via NET_CONSTRUCTOR_MODE=demo)")
    print("=" * 60)

    _ensure_no_build_config()
    os.environ["NET_CONSTRUCTOR_MODE"] = "demo"
    license_module = _reimport_license()

    print("\n" + "-" * 60)
    print("Running tests:")
    print("-" * 60)

    is_demo = license_module.is_demo_mode()
    is_full = license_module.is_full_mode()
    mode_str = license_module.get_mode_string()

    print(f"\nOK is_demo_mode(): {is_demo}")
    print(f"OK is_full_mode(): {is_full}")
    print(f"OK get_mode_string(): {mode_str}")

    if is_demo and not is_full and mode_str == "demo":
        print("\nOKOKOK DEMO MODE TEST PASSED OKOKOK")
        return True
    print("\nFAILFAILFAIL DEMO MODE TEST FAILED FAILFAILFAIL")
    return False


def test_full_mode_env():
    """Тестирует полный режим через переменную окружения (режим разработки)."""
    print("\n\n" + "=" * 60)
    print("Testing FULL mode (via NET_CONSTRUCTOR_MODE=full)")
    print("=" * 60)

    _ensure_no_build_config()
    os.environ["NET_CONSTRUCTOR_MODE"] = "full"
    license_module = _reimport_license()

    print("\n" + "-" * 60)
    print("Running tests:")
    print("-" * 60)

    is_demo = license_module.is_demo_mode()
    is_full = license_module.is_full_mode()
    mode_str = license_module.get_mode_string()

    print(f"\nOK is_demo_mode(): {is_demo}")
    print(f"OK is_full_mode(): {is_full}")
    print(f"OK get_mode_string(): {mode_str}")

    if not is_demo and is_full and mode_str == "full":
        print("\nOKOKOK FULL MODE TEST PASSED OKOKOK")
        return True
    print("\nFAILFAILFAIL FULL MODE TEST FAILED FAILFAILFAIL")
    return False


def test_demo_mode_build_config():
    """Тестирует демо-режим через сгенерированный _build_config.py (как в exe)."""
    print("\n\n" + "=" * 60)
    print("Testing DEMO mode (via _build_config from build_variant.py --demo)")
    print("=" * 60)

    root = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, "build_variant.py", "--demo"], cwd=root, check=True)

    # Убираем env, чтобы license использовал только _build_config
    os.environ.pop("NET_CONSTRUCTOR_MODE", None)
    license_module = _reimport_license(clear_build_config_cache=True)

    print("\n" + "-" * 60)
    print("Running tests:")
    print("-" * 60)

    is_demo = license_module.is_demo_mode()
    is_full = license_module.is_full_mode()
    mode_str = license_module.get_mode_string()

    print(f"\nOK is_demo_mode(): {is_demo}")
    print(f"OK is_full_mode(): {is_full}")
    print(f"OK get_mode_string(): {mode_str}")

    if is_demo and not is_full and mode_str == "demo":
        print("\nOKOKOK DEMO MODE (build_config) TEST PASSED OKOKOK")
        return True
    print("\nFAILFAILFAIL DEMO MODE (build_config) TEST FAILED FAILFAILFAIL")
    return False


def test_full_mode_build_config():
    """Тестирует полный режим через сгенерированный _build_config.py (как в exe)."""
    print("\n\n" + "=" * 60)
    print("Testing FULL mode (via _build_config from build_variant.py --full)")
    print("=" * 60)

    root = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, "build_variant.py", "--full"], cwd=root, check=True)

    os.environ.pop("NET_CONSTRUCTOR_MODE", None)
    license_module = _reimport_license(clear_build_config_cache=True)

    print("\n" + "-" * 60)
    print("Running tests:")
    print("-" * 60)

    is_demo = license_module.is_demo_mode()
    is_full = license_module.is_full_mode()
    mode_str = license_module.get_mode_string()

    print(f"\nOK is_demo_mode(): {is_demo}")
    print(f"OK is_full_mode(): {is_full}")
    print(f"OK get_mode_string(): {mode_str}")

    if not is_demo and is_full and mode_str == "full":
        print("\nOKOKOK FULL MODE (build_config) TEST PASSED OKOKOK")
        return True
    print("\nFAILFAILFAIL FULL MODE (build_config) TEST FAILED FAILFAILFAIL")
    return False


def main():
    print("\n" + "=" * 60)
    print("LICENSE MODULE TESTING")
    print("=" * 60)

    r1 = test_demo_mode_env()
    r2 = test_full_mode_env()
    r3 = test_demo_mode_build_config()
    r4 = test_full_mode_build_config()

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    print(f"\nDemo mode (env):           {'OK PASSED' if r1 else 'FAIL FAILED'}")
    print(f"Full mode (env):          {'OK PASSED' if r2 else 'FAIL FAILED'}")
    print(f"Demo mode (_build_config): {'OK PASSED' if r3 else 'FAIL FAILED'}")
    print(f"Full mode (_build_config): {'OK PASSED' if r4 else 'FAIL FAILED'}")

    if r1 and r2 and r3 and r4:
        print("\nOKOKOK ALL TESTS PASSED OKOKOK")
        print("\nBuild with:")
        print("  python build_variant.py --demo")
        print("  python build_variant.py --full")
        return 0
    print("\nFAILFAILFAIL SOME TESTS FAILED FAILFAILFAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
