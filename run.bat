@echo off
echo === Запуск Django проекта ===

REM 1. Проверка и создание виртуального окружения
if not exist djangoenv (
    echo Виртуальное окружение не найдено. Создаю...
    python -m venv djangoenv
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось создать виртуальное окружение.
        pause
        exit /b
    )
)

REM 2. Активация виртуального окружения
call djangoenv\Scripts\activate
if errorlevel 1 (
    echo [ОШИБКА] Не удалось активировать виртуальное окружение.
    pause
    exit /b
)
echo Виртуальное окружение активировано.

REM 3. Установка Django (если не установлен)
python -c "import django" 2>NUL
if errorlevel 1 (
    echo Django не найден. Устанавливаю...
    pip install django
) else (
    echo Django уже установлен.
)

REM 4. Установка requests (если не установлен)
python -c "import requests" 2>NUL
if errorlevel 1 (
    echo requests не найден. Устанавливаю...
    pip install requests
) else (
    echo requests уже установлен.
)

REM 4. Применение миграций
echo Применение миграций...
python weatherproject/manage.py migrate

REM 5. Запуск сервера
echo Запуск сервера...
python weatherproject/manage.py runserver

pause
