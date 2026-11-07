
import serial
import time

arduino = serial.Serial('COM5', 9600, timeout=2)
time.sleep(2)

print("=== SSMM V1.0 ===")
print("Arduino connected!")
print("Reading sensor...\n")

while True:
    raw_data = arduino.readline()

    if raw_data:
        try:
            data = raw_data.decode('utf-8').strip()

            # Mengambil angka setelah tanda ":"
            adc = int(data.split(":")[-1].strip())

            if 476 <= adc <= 1023:
                status = "DRY"
            elif 340 <= adc <= 475:
                status = "HUMID"
            elif 150 <= adc <= 339:
                status = "WET"
            else:
                status = "OUT OF RANGE"

            print(f"ADC: {adc} | STATUS: {status}")

        except (ValueError, IndexError):
            print("Data tidak valid:", repr(raw_data))
