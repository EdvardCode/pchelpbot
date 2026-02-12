# 🖥 PC Remote Control via Telegram

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge&logo=telegram)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Современный инструмент для полного удаленного управления компьютером через Telegram.**  
*Красивый GUI для настройки, Inline-меню, управление медиа и системой.*

[Возможности](#-возможности) • [Скриншоты](#-скриншоты) • [Установка](#-установка) • [Скачать EXE](#-скачать-exe)

</div>

---

## ✨ Возможности

Бот предоставляет удобную панель управления прямо в чате Telegram (Inline-кнопки):

*   🔊 **Управление звуком:** Громкость `+` / `-`, `Mute`, `Play/Pause`.
*   📸 **Наблюдение:** Моментальный скриншот экрана.
*   ⚡ **Система:**
    *   Безопасное выключение ПК (с подтверждением).
    *   Блокировка экрана (Win+L).
    *   Свернуть все окна (режим "Босс").
*   💬 **Взаимодействие:**
    *   Вывод всплывающих сообщений на экран.
    *   Удаленное открытие ссылок в браузере.
*   ⚙️ **Легкая настройка:** Графическое окно при первом запуске (не нужно лезть в код).

---

## 🖼 Скриншоты

| ⚙️ Окно настройки (GUI) | 📱 Управление в Telegram |
|:-----------------------:|:------------------------:|
| ![Setup Window](https://i.ibb.co/bMQgDDhw/image.png) | ![Bot Interface](https://i.ibb.co/V87gyjx/image.png) |

---

## 🛠 Установка и Запуск (из кода)

Если вы хотите запустить проект через Python:

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/EdvardCode/pchelpbot.git
    cd pchelpbot
    ```

2.  **Установите библиотеки:**
    ```bash
    pip install customtkinter pyTelegramBotAPI pyautogui opencv-python-headless screeninfo
    ```

3.  **Запустите:**
    ```bash
    python main.py
    ```

---

## 📦 Скачать EXE (Готовая сборка)

Вы можете собрать `.exe` файл, чтобы запускать бота на компьютерах без Python.

**Команда для сборки (используется PyInstaller):**
*(Убедитесь, что файл `app.ico` лежит рядом с скриптом)*

```bash
pyinstaller --noconsole --onefile --icon=app.ico --add-data "app.ico;." --collect-all customtkinter --exclude-module PyQt5 main.py
```
📂 Где искать файл?
После завершения процесса готовый файл main.exe появится в папке dist.

## 🚀 Инструкция по запуску
1. Запустите файл main.exe (или скрипт main.py).

2. При первом запуске откроется окно настройки.

3. Введите необходимые данные:
Bot Token — получите у @BotFather.
User ID — узнайте свой ID у @userinfobot.
Нажмите "Сохранить и Запустить".

4. Бот отправит вам приветственное сообщение в Telegram! 🎉
```bash
Примечание: Ваши данные сохраняются локально в файл config.json.
Если захотите сменить токен, просто удалите этот файл, и окно настройки появится снова.
```
🔐 Личный доступ: Бот запрограммирован реагировать только на ваш User ID. Никто посторонний не сможет управлять вашим компьютером, даже если найдет вашего бота.

[Мой сайт](https://edvardcode.rf.gd/)
