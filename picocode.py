import ujson
import utime
from machine import UART, Pin, ADC

# --- Конфигурация ---
UART_ID = 0
TX_PIN = 0        # GP0
RX_PIN = 1        # GP1
BAUD_RATE = 115200

# Интервалы
EVENT_INTERVAL_MS = 60_000      # 1 минута
SENSOR_POLL_MS = 1_000          # опрос каждую секунду

# --- Пороги аларма с гистерезисом ---
# Алам срабатывает при ПРЕВЫШЕНИИ alarm_high
# Сбрасывается только при падении ниже alarm_low (гистерезис)
ALARM_THRESHOLDS = {
    "Flame": {"alarm_high": 30000.0, "alarm_low": 50000, "situation": "Fire"},
    "Gas":    {"alarm_high": 40000.0, "alarm_low": 30000.0, "situation": "Leakage"},
    "Sound":    {"alarm_high": 5000.0, "alarm_low": 10000.0, "situation": "Explosion"},
}

sound = ADC(Pin(26))

smoke = ADC(Pin(27))

flame = ADC(Pin(28))

uart = UART(UART_ID, baudrate=BAUD_RATE, tx=Pin(TX_PIN), rx=Pin(RX_PIN))

# --- Состояние аларма для каждого сенсора ---
# True = сейчас в состоянии аларма (повторно не отправляем)
alarm_active = {k: False for k in ALARM_THRESHOLDS}


def read_sensors():
    return [
        {
          "sensor": "Flame",
          "value": flame.read_u16()
        },
        {
          "sensor": "Sound",
          "value": sound.read_u16()
        },
        {
          "sensor": "Gas",
          "value": smoke.read_u16()
        }
    ]


def send_to_esp32(payload: dict):
    """Отправляет JSON строку по UART с разделителем \n."""
    line = ujson.dumps(payload) + "\n"
    uart.write(line.encode())


def check_alarms(sensor_data: list):
    for item in sensor_data:
        name  = item["sensor"]   # "Flame" / "Gas" / "Sound"
        value = item["value"]

        if name not in ALARM_THRESHOLDS:
            continue

        thresh    = ALARM_THRESHOLDS[name]
        high      = thresh["alarm_high"]
        low       = thresh["alarm_low"]
        situation = thresh["situation"]

        if not alarm_active[name] and ((name == "Gas" and value > high) or (name != "Gas" and value < high)):
            alarm_active[name] = True
            payload = {
                    "type":      "alarm",
                    "situation": situation,
                    "status": "ACTIVE"
            }
            send_to_esp32(payload)
            print("[ALARM] {}={} > {}".format(name, value, high))

        elif alarm_active[name] and ((name != "Gas" and value > low) or (name == "Gas" and value < low)):
            alarm_active[name] = False
            payload = {
                "type":      "alarm",
                "situation": situation,
                "status": "RTN"
            }
            send_to_esp32(payload)
            print("[OK] {} recovered ({}  < {})".format(name, value, low))

def main():
    print("Pico started")
    last_event_ms = utime.ticks_ms() - EVENT_INTERVAL_MS  # сразу отправить первый event

    while True:
        now = utime.ticks_ms()
        sensor_data = read_sensors()

        # --- Проверка аларма (каждый цикл) ---
        check_alarms(sensor_data)

        # --- Отправка Event (раз в минуту) ---
        if utime.ticks_diff(now, last_event_ms) >= EVENT_INTERVAL_MS:
          for sensor in sensor_data:
            payload = {
                "type": "event",
                "sensor": sensor["sensor"],
                "value": sensor["value"]
            }
            send_to_esp32(payload)
            print(f"[EVENT] sent: {sensor_data}")
          last_event_ms = now

        utime.sleep_ms(SENSOR_POLL_MS)


main()
