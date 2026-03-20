# Скрипт аудита ресурсов для Jupyter Notebook
import os
import sys
import psutil
import platform

def audit_resources():
    print("--- ОТЧЁТ УАДИА: ВЫЧИСЛИТЕЛЬНЫЕ РЕСУРСЫ ---")
    # Процессор
    print(f"Процессор: {platform.processor()}")
    print(f"Ядра: {os.cpu_count()}")
    # Память
    mem = psutil.virtual_memory()
    print(f"Всего RAM: {mem.total / (1024 ** 3):.2f} GB")
    print(f"Доступно RAM: {mem.available / (1024 ** 3):.2f} GB")
    # GPU (если есть torch)
    try:
        import torch
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"Память GPU: {torch.cuda.get_device_properties(0).total_memory / 1024**2:.2f} MB")
        else:
            print("GPU: Не обнаружен (CPU mode)")
    except ImportError:
        print("GPU: Библиотека torch не установлена")
    print("--- КОНЕЦ ОТЧЁТА ---")

# audit_resources() # Раскомментировать для запуска
