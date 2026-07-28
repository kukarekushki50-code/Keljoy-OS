import calendar
import datetime
import os
import sys
import time
import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
from PIL import Image, ImageTk
import psutil
import requests

# Функция для корректного поиска встроенных файлов в .exe сборке
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class KeljoyPhoneOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Keljoy Techs OS")
        
        # Динамический полноэкранный режим под любой монитор / экран
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.attributes('-fullscreen', True)
        
        self.bg_image = None
        self.show_splash()

    def show_splash(self):
        """Экран заставки"""
        self.splash_frame = tk.Frame(self.root, bg="#0d0d0d")
        self.splash_frame.pack(fill="both", expand=True)
        
        tk.Label(
            self.splash_frame, 
            text="Keljoy Techs", 
            font=("Helvetica", 52, "bold"), 
            fg="#00FF66", 
            bg="#0d0d0d"
        ).pack(expand=True)
        
        # Показ заставки 3 секунды, затем переход на рабочий стол
        self.root.after(3000, self.load_desktop)

    def load_desktop(self):
        """Рабочий стол"""
        self.splash_frame.destroy()
        
        self.desktop_frame = tk.Frame(self.root)
        self.desktop_frame.pack(fill="both", expand=True)

        # Обои
        try:
            img_path = resource_path("i (2).png")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                bg_label = tk.Label(self.desktop_frame, image=self.bg_image)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                tk.Label(self.desktop_frame, text="Обои i (2).png не найдены", bg="#1a1a2e", fg="white").place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            tk.Label(self.desktop_frame, text="Ошибка загрузки обоев", bg="#1a1a2e", fg="white").place(x=0, y=0, relwidth=1, relheight=1)

        # Верхняя панель состояния (Статус-бар)
        self.status_bar = tk.Frame(self.desktop_frame, bg="#111111", height=40)
        self.status_bar.pack(side="top", fill="x")

        # Индикатор батареи
        self.battery_label = tk.Label(self.status_bar, font=("Helvetica", 11, "bold"), fg="#00FF66", bg="#111111")
        self.battery_label.pack(side="left", padx=15)
        
        # Настоящее время
        self.time_label = tk.Label(self.status_bar, font=("Helvetica", 13, "bold"), fg="white", bg="#111111")
        self.time_label.pack(side="left", expand=True)
        
        # Кнопка выключения в верхнем углу
        self.power_btn = tk.Button(
            self.status_bar, 
            text=" ✖ ", 
            font=("Helvetica", 12, "bold"), 
            fg="white", 
            bg="#FF3333", 
            activebackground="#CC0000",
            activeforeground="white",
            bd=0, 
            command=self.root.destroy
        )
        self.power_btn.pack(side="right", padx=10, pady=5)

        self.update_status_bar()
        self.create_apps()

    def update_status_bar(self):
        """Обновление времени и заряда"""
        current_time = time.strftime('%H:%M:%S')
        self.time_label.config(text=current_time)
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.battery_label.config(text=f"⚡ {battery.percent}%")
            else:
                self.battery_label.config(text="🔌 Сеть")
        except Exception:
            self.battery_label.config(text="🔌 Сеть")
            
        self.root.after(1000, self.update_status_bar)

    def create_apps(self):
        """Сетка приложений"""
        apps_frame = tk.Frame(self.desktop_frame, bg="")
        apps_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_style = {
            "font": ("Helvetica", 13, "bold"), 
            "width": 16, 
            "height": 2, 
            "bg": "#ffffff", 
            "fg": "#222222", 
            "activebackground": "#00FF66",
            "bd": 0, 
            "cursor": "hand2"
        }

        tk.Button(apps_frame, text="⚙️ Настройки", command=self.app_settings, **btn_style).grid(row=0, column=0, padx=15, pady=15)
        tk.Button(apps_frame, text="🎨 Paint", command=self.app_paint, **btn_style).grid(row=0, column=1, padx=15, pady=15)
        tk.Button(apps_frame, text="🎬 Видео Проект", command=self.app_video_player, **btn_style).grid(row=1, column=0, padx=15, pady=15)
        tk.Button(apps_frame, text="🌤️ Погода", command=self.app_weather, **btn_style).grid(row=1, column=1, padx=15, pady=15)
        tk.Button(apps_frame, text="📅 Календарь", command=self.app_calendar, **btn_style).grid(row=2, column=0, columnspan=2, padx=15, pady=15)

    # --- Приложения ---

    def app_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Настройки")
        win.geometry("350x250")
        win.resizable(False, False)
        tk.Label(win, text="Keljoy Techs OS", font=("Helvetica", 16, "bold")).pack(pady=20)
        tk.Label(win, text=f"Разрешение экрана: {self.screen_width}x{self.screen_height}", font=("Helvetica", 11)).pack(pady=5)
        tk.Label(win, text="Статус системы: Работает штатно", font=("Helvetica", 10), fg="green").pack(pady=10)

    def app_paint(self):
        win = tk.Toplevel(self.root)
        win.title("Paint")
        win.geometry("650x450")
        
        canvas = tk.Canvas(win, bg="white")
        canvas.pack(fill="both", expand=True)
        
        def draw(event):
            x1, y1 = (event.x - 3), (event.y - 3)
            x2, y2 = (event.x + 3), (event.y + 3)
            canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
            
        canvas.bind("<B1-Motion>", draw)
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Очистить", command=lambda: canvas.delete("all")).pack(pady=5)

    def app_video_player(self):
        """Просмотр видео из проекта"""
        win = tk.Toplevel(self.root)
        win.title("Видео из проекта")
        win.geometry("450x250")
        win.resizable(False, False)
        
        tk.Label(win, text="Введите номер видео (от 1 до 10):", font=("Helvetica", 11, "bold")).pack(pady=15)
        
        entry = tk.Entry(win, font=("Helvetica", 12), width=10, justify="center")
        entry.pack(pady=5)
        
        status_label = tk.Label(win, text="", font=("Helvetica", 10), wraplength=400)
        status_label.pack(pady=10)

        def play_video():
            num = entry.get().strip()
            if not num.isdigit() or not (1 <= int(num) <= 10):
                status_label.config(text="Ошибка: Введите число от 1 до 10", fg="red")
                return
            
            filename = f"video_file_kel{num}.mp4"
            # Ищем сначала во встроенных ресурсах EXE, затем в рабочей папке
            file_path = resource_path(filename)
            if not os.path.exists(file_path):
                file_path = os.path.abspath(filename)
            
            if os.path.exists(file_path):
                status_label.config(text=f"Запуск {filename}...", fg="green")
                try:
                    if sys.platform.startswith('win'):
                        os.startfile(file_path)
                    elif sys.platform.startswith('darwin'):
                        subprocess.call(["open", file_path])
                    else:
                        subprocess.call(["xdg-open", file_path])
                except Exception as e:
                    status_label.config(text=f"Ошибка воспроизведения: {e}", fg="red")
            else:
                status_label.config(text=f"Файл {filename} не найден в проекте!\nПоложите его в папку со скриптом.", fg="red")

        tk.Button(win, text="Запустить видео", font=("Helvetica", 11, "bold"), bg="#00FF66", command=play_video).pack(pady=10)

    def app_weather(self):
        win = tk.Toplevel(self.root)
        win.title("Погода")
        win.geometry("320x220")
        win.resizable(False, False)
        
        info_label = tk.Label(win, text="Получение данных...", font=("Helvetica", 12))
        info_label.pack(pady=60)
        
        def fetch_weather():
            try:
                # Бесплатный гео-API без токенов
                res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=55.75&longitude=37.61&current_weather=true", timeout=5).json()
                temp = res['current_weather']['temperature']
                wind = res['current_weather']['windspeed']
                info_label.config(text=f"Температура: {temp}°C\nСкорость ветра: {wind} км/ч")
            except Exception:
                info_label.config(text="Не удалось получить погоду\n(Проверьте интернет)")
                
        threading.Thread(target=fetch_weather, daemon=True).start()

    def app_calendar(self):
        win = tk.Toplevel(self.root)
        win.title("Календарь")
        win.geometry("320x300")
        win.resizable(False, False)
        
        now = datetime.datetime.now()
        cal_text = calendar.month(now.year, now.month)
        tk.Label(win, text=cal_text, font=("Courier", 11, "bold"), justify="left").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeljoyPhoneOS(root)
    root.mainloop()