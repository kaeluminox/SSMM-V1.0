
import tkinter as tk
import serial
import time

# =========================
# SERIAL CONNECTION
# =========================

try:
    arduino = serial.Serial('COM5', 9600, timeout=0.1)
    time.sleep(2)
    connected = True
except serial.SerialException:
    arduino = None
    connected = False


# =========================
# WINDOW
# =========================

window = tk.Tk()
window.title("SSMM V1.0 | Milo Monitor")
window.geometry("520x570")
window.configure(bg="#172B36")
window.resizable(False, False)


# =========================
# COLORS & FONTS
# =========================

BG = "#172B36"
PANEL = "#29434C"
WHITE = "#FFFFFF"
MINT = "#B8D7D5"
YELLOW = "#F4C66A"
GREEN = "#8DD9A5"


# =========================
# HEADER
# =========================

title = tk.Label(
    window,
    text="MILO",
    font=("Arial", 28, "bold"),
    fg=MINT,
    bg=BG
)
title.pack(pady=(20, 0))

subtitle = tk.Label(
    window,
    text="SMART SOIL MOISTURE MONITOR",
    font=("Arial", 10),
    fg=MINT,
    bg=BG
)
subtitle.pack(pady=5)


# =========================
# CONNECTION STATUS
# =========================

connection = tk.Label(
    window,
    text="● ARDUINO CONNECTED" if connected
    else "● ARDUINO DISCONNECTED",
    font=("Arial", 10, "bold"),
    fg=GREEN if connected else "#FF7777",
    bg=BG
)
connection.pack(pady=10)


# =========================
# MILO CHARACTER
# =========================

milo = tk.Label(
    window,
    text="(≽^•⩊•^≼)",
    font=("Arial", 48, "bold"),
    fg=MINT,
    bg=PANEL,
    width=12,
    height=2
)
milo.pack(pady=15)


# =========================
# SENSOR DISPLAY
# =========================

adc_label = tk.Label(
    window,
    text="ADC: ---",
    font=("Arial", 24, "bold"),
    fg=WHITE,
    bg=BG
)
adc_label.pack(pady=10)

status_label = tk.Label(
    window,
    text="WAITING FOR DATA",
    font=("Arial", 20, "bold"),
    fg=YELLOW,
    bg=BG
)
status_label.pack(pady=5)

message = tk.Label(
    window,
    text="Milo is waiting for soil data...",
    font=("Arial", 11),
    fg=MINT,
    bg=BG
)
message.pack(pady=5)


# =========================
# CLASSIFICATION
# =========================

def classify_moisture(adc):

    if 476 <= adc <= 1023:
        return "DRY", "≽^•ꞈ•^≼", YELLOW, "Milo needs water!"

    elif 340 <= adc <= 475:
        return "HUMID", "≽^•⩊•^≼", GREEN, "Milo is happy!"

    elif 150 <= adc <= 339:
        return "WET",  "≽^•o•^≼", "#78C9E8", "Soil is very wet."

    else:
        return "OUT OF RANGE", "≽^•_•^≼", "#FF7777", "Check sensor reading."


# =========================
# LIVE SENSOR UPDATE
# =========================

def update_sensor():

    if connected:
        try:
            if arduino.in_waiting:
                raw_data = arduino.readline().decode(
                    "utf-8", errors="ignore"
                ).strip()

                if raw_data:
                    adc = int(raw_data.split(":")[-1].strip())

                    if 0 <= adc <= 1023:
                        status, face, color, text = classify_moisture(adc)

                        adc_label.config(text=f"ADC: {adc}")
                        status_label.config(
                            text=status,
                            fg=color
                        )
                        milo.config(text=face)
                        message.config(text=text)

        except (ValueError, serial.SerialException):
            connection.config(
                text="● SENSOR DATA ERROR",
                fg="#FF7777"
            )

    window.after(100, update_sensor)


# =========================
# CLOSE APPLICATION
# =========================

def close_app():
    if arduino and arduino.is_open:
        arduino.close()

    window.destroy()


window.protocol("WM_DELETE_WINDOW", close_app)

update_sensor()
window.mainloop()
