import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import telebot
from telebot import types
import pyautogui
import socket
import platform
import ctypes
import webbrowser

# --- 📝 НАСТРОЙКИ ---
AUTHOR_NAME = "EdvardCode"      # Твое имя
AUTHOR_LINK = "https://t.me/edvardcode"  # Твоя ссылка
APP_VERSION = "v1.0"       
CONFIG_FILE = "config.json"
ICON_NAME = "app.ico"               # Имя файла иконки

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Функция для поиска ресурсов внутри EXE (для иконки)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === ЧАСТЬ 1: GUI (НАСТРОЙКА) ===
class SetupApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PC Remote Setup")
        self.geometry("500x450")
        self.resizable(False, False)
        
        # Установка иконки приложения
        try:
            self.iconbitmap(resource_path(ICON_NAME))
        except: pass

        self.create_context_menu()

        # Заголовки
        ctk.CTkLabel(self, text="⚙️ Настройка Remote Bot", font=("Roboto", 24, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self, text=f"{APP_VERSION}", font=("Roboto", 12), text_color="gray").pack(pady=(0, 15))

        # Поле Token
        self.token_entry = ctk.CTkEntry(self, placeholder_text="Bot Token (содержит : )", width=350, height=40)
        self.token_entry.pack(pady=10)
        self.token_entry.bind("<Button-3>", self.show_context_menu)

        # Поле ID
        self.id_entry = ctk.CTkEntry(self, placeholder_text="User ID (только цифры)", width=350, height=40)
        self.id_entry.pack(pady=10)
        self.id_entry.bind("<Button-3>", self.show_context_menu)

        # Кнопка
        self.save_btn = ctk.CTkButton(self, text="💾 Сохранить и Запустить", command=self.save_config, width=250, height=50, font=("Roboto", 16, "bold"), fg_color="#E74C3C", hover_color="#C0392B")
        self.save_btn.pack(pady=30)
        
        ctk.CTkLabel(self, text="ПКМ - вставить текст", text_color="gray", font=("Arial", 10)).pack(side="bottom", pady=5)
        ctk.CTkLabel(self, text=f"Created by {AUTHOR_NAME}", text_color="gray", font=("Arial", 10)).pack(side="bottom", pady=5)

    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Вставить", command=self.paste_text)
        self.menu.add_command(label="Очистить", command=self.clear_text)

    def show_context_menu(self, event):
        self.focused_widget = event.widget
        self.focused_widget.focus()
        try: self.menu.tk_popup(event.x_root, event.y_root)
        finally: self.menu.grab_release()

    def paste_text(self):
        try: self.focused_widget.insert(tk.INSERT, self.clipboard_get())
        except: pass

    def clear_text(self):
        try: self.focused_widget.delete(0, tk.END)
        except: pass

    def save_config(self):
        token = self.token_entry.get().strip()
        user_id = self.id_entry.get().strip()
        
        # --- ВАЛИДАЦИЯ ---
        if not token or not user_id:
            tk.messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        if ":" not in token:
            tk.messagebox.showerror("Ошибка", "Некорректный Токен!\nОн должен содержать двоеточие (:).")
            return
        if not user_id.isdigit():
            tk.messagebox.showerror("Ошибка", "User ID должен состоять только из цифр!")
            return
        
        data = {"BOT_TOKEN": token, "ADMIN_ID": int(user_id)}
        try:
            with open(CONFIG_FILE, "w") as f: json.dump(data, f)
            self.destroy()
        except Exception as e: tk.messagebox.showerror("Error", str(e))

# === ЧАСТЬ 2: ЛОГИКА БОТА ===

# -- МЕНЮ --
def menu_main():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📸 Скриншот", callback_data="screen"),
        types.InlineKeyboardButton("ℹ️ Инфо", callback_data="info")
    )
    markup.add(
        types.InlineKeyboardButton("🎛 Медиа и Звук", callback_data="goto_media"),
        types.InlineKeyboardButton("⚡️ Система", callback_data="goto_system")
    )
    markup.add(
        types.InlineKeyboardButton("💬 Текст на экран", callback_data="input_msg"),
        types.InlineKeyboardButton("🔗 Открыть ссылку", callback_data="input_url")
    )
    markup.add(
        types.InlineKeyboardButton("👨‍💻 Автор", callback_data="goto_author"),
        types.InlineKeyboardButton("🔴 ВЫКЛ БОТА", callback_data="kill_bot_ask")
    )
    return markup

def menu_media():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🔉 -", callback_data="vol_down"),
        types.InlineKeyboardButton("🔇 Mute", callback_data="vol_mute"),
        types.InlineKeyboardButton("🔊 +", callback_data="vol_up")
    )
    markup.add(types.InlineKeyboardButton("⏯ Пауза/Плей", callback_data="media_play"))
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="goto_main"))
    return markup

def menu_system():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔒 Блок экрана", callback_data="sys_lock"),
        types.InlineKeyboardButton("🔽 Свернуть всё", callback_data="sys_min")
    )
    markup.add(types.InlineKeyboardButton("💀 Выключить ПК", callback_data="sys_shutdown_ask"))
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="goto_main"))
    return markup

def menu_author():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌐 Связаться", url=AUTHOR_LINK))
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="goto_main"))
    return markup

# -- ЗАПУСК --
def run_bot(config):
    # 1. ПРОВЕРКА ТОКЕНА
    try:
        bot = telebot.TeleBot(config["BOT_TOKEN"])
        bot.get_me() # Тестовый запрос
    except Exception as e:
        print(f"Ошибка токена: {e}")
        try: os.remove(CONFIG_FILE) # Удаляем битый конфиг
        except: pass
        
        # Показываем ошибку пользователю
        root = tk.Tk(); root.withdraw()
        messagebox.showerror("Ошибка запуска", "Неверный токен бота!\nКонфиг сброшен. Перезапустите программу.")
        root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv) # Перезапуск
        return

    admin_id = config["ADMIN_ID"]
    print(f"🤖 Бот {APP_VERSION} запущен...")

    # Стартовое сообщение
    try:
        bot.send_message(admin_id, f"🖥 <b>Панель управления {APP_VERSION}</b>\nСистема онлайн.", 
                         parse_mode="HTML", reply_markup=menu_main())
    except: pass

    @bot.message_handler(commands=['start'])
    def start(message):
        if message.from_user.id == admin_id:
            bot.send_message(message.chat.id, "🖥 <b>Главное меню</b>", parse_mode="HTML", reply_markup=menu_main())

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        if call.from_user.id != admin_id: return
        
        # НАВИГАЦИЯ
        if call.data == "goto_main":
            bot.edit_message_text("🖥 <b>Главное меню</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=menu_main())
        elif call.data == "goto_media":
            bot.edit_message_text("🎛 <b>Медиа</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=menu_media())
        elif call.data == "goto_system":
            bot.edit_message_text("⚡️ <b>Система</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=menu_system())
        elif call.data == "goto_author":
            text = f"👨‍💻 <b>Автор:</b> {AUTHOR_NAME}\n📦 <b>Версия:</b> {APP_VERSION}\n🛠 <i>Remote Control Tool</i>"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=menu_author())

        # ФУНКЦИИ
        elif call.data == "vol_up":
            for _ in range(5): pyautogui.press('volumeup')
            bot.answer_callback_query(call.id, "+")
        elif call.data == "vol_down":
            for _ in range(5): pyautogui.press('volumedown')
            bot.answer_callback_query(call.id, "-")
        elif call.data == "vol_mute":
            pyautogui.press('volumemute')
            bot.answer_callback_query(call.id, "Mute")
        elif call.data == "media_play":
            pyautogui.press('playpause')
            bot.answer_callback_query(call.id, "Play/Pause")

        elif call.data == "sys_lock":
            try: ctypes.windll.user32.LockWorkStation()
            except: pass
            bot.answer_callback_query(call.id, "Locked")
        elif call.data == "sys_min":
            pyautogui.hotkey('win', 'd')
            bot.answer_callback_query(call.id, "Desktop")

        elif call.data == "sys_shutdown_ask":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✅ ДА", callback_data="sys_shutdown_confirm"))
            markup.add(types.InlineKeyboardButton("Отмена", callback_data="goto_system"))
            bot.edit_message_text("⚠️ <b>Выключить ПК?</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

        elif call.data == "sys_shutdown_confirm":
            bot.edit_message_text("💀 Bye...", call.message.chat.id, call.message.message_id)
            os.system("shutdown /s /t 5")

        elif call.data == "screen":
            bot.send_chat_action(call.message.chat.id, 'upload_photo')
            scr = "screen.png"
            try:
                pyautogui.screenshot(scr)
                with open(scr, "rb") as f: bot.send_photo(call.message.chat.id, f)
                os.remove(scr)
            except: pass

        elif call.data == "info":
            ip = socket.gethostbyname(socket.gethostname())
            info = f"💻 {platform.node()}\n🌐 IP: {ip}\n💿 {platform.system()}"
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, info)

        elif call.data == "input_msg":
            msg = bot.send_message(call.message.chat.id, "✍️ Введите сообщение:")
            bot.register_next_step_handler(msg, lambda m: [pyautogui.alert(m.text, "Bot"), bot.send_message(m.chat.id, "✅ Показано", reply_markup=menu_main())])

        elif call.data == "input_url":
            msg = bot.send_message(call.message.chat.id, "🔗 Введите ссылку:")
            bot.register_next_step_handler(msg, lambda m: [webbrowser.open(m.text if "http" in m.text else f"https://{m.text}"), bot.send_message(m.chat.id, "✅ Открыто", reply_markup=menu_main())])

        elif call.data == "kill_bot_ask":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🛑 ВЫКЛЮЧИТЬ", callback_data="kill_bot_confirm"))
            markup.add(types.InlineKeyboardButton("Отмена", callback_data="goto_main"))
            bot.edit_message_text("🛑 <b>Убить процесс бота?</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

        elif call.data == "kill_bot_confirm":
            bot.edit_message_text("⛔️ Бот остановлен.", call.message.chat.id, call.message.message_id)
            bot.stop_polling()
            os._exit(0)

    try:
        bot.infinity_polling()
    except: pass

# --- ЗАПУСК ---
if __name__ == "__main__":
    if not os.path.exists(CONFIG_FILE):
        app = SetupApp()
        app.mainloop()
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                config = json.load(f)
                run_bot(config)
            except:
                os.remove(CONFIG_FILE)
                os.execl(sys.executable, sys.executable, *sys.argv)