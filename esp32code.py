import ujson
import utime
import network
import urequests
from machine import UART, Pin


WIFI_SSID = "Robots"
WIFI_PASS = "artofwar3"

API_URL_ALARM =
API_URL_EVENT = 
API_HEADERS = {
    "Content-Type": "application/json"
}

ROBOT = "92605b29faf841e5938e9e782f7d89bb"


uart = UART(2, baudrate=115200, tx=17, rx=16)
def fake_uart_data():

    return ujson.dumps({

        "type": "alarm",

        "situation": "Fire",

        "status": "ACTIVE"

    }) + "\n"
buf = b""

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    utime.sleep(2)

    wlan.active(True)
    utime.sleep(2)

    if not wlan.isconnected():
        print(f"Connecting to {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            utime.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print(f"Wi-Fi OK: {wlan.ifconfig()[0]}")
    else:
        print("Wi-Fi FAILED — работаем без сети")
    return wlan


def ensure_wifi(wlan):
    """Переподключаемся при потере соединения."""
    if not wlan.isconnected():
        print("Wi-Fi lost, reconnecting...")
        wlan.disconnect()
        utime.sleep(1)
        wlan.connect(WIFI_SSID, WIFI_PASS)
        for _ in range(15):
            if wlan.isconnected():
                break
            utime.sleep(1)


def post_to_api(url: str, payload: dict) -> bool:
    """Отправляет POST на API. Возвращает True при успехе."""
    try:
        body = ujson.dumps(payload)
        resp = urequests.post(url, data=body, headers=API_HEADERS, timeout=10)
        ok = resp.status_code in (200, 201, 204)
        resp.close()
        if ok:
            print(f"[API OK] {url} → {resp.status_code}")
        else:
            print(f"[API ERR] {url} → {resp.status_code}")
        return ok
    except Exception as e:
        print(f"[API EXC] {e}")
        return False


def handle_message(raw: str, wlan):
    """Разбирает JSON от Pico и отправляет на нужный эндпоинт."""
    try:
        msg = ujson.loads(raw.strip())
    except Exception:
        print(f"[PARSE ERR] {raw}")
        return

    msg_type = msg.get("type")
    msg.pop("type")
    msg["robot"] = ROBOT
    ensure_wifi(wlan)

    if msg_type == "alarm":
        print(f"[ALARM]")
        post_to_api(API_URL_ALARM, msg)

    elif msg_type == "event":
        print(f"[EVENT]")
        post_to_api(API_URL_EVENT, msg)

    else:
        print(f"[UNKNOWN] {msg}")


def main():
    global buf
    print("ESP32 started")
    wlan = connect_wifi()

    while True:
        if uart.any():
            chunk = uart.read(256)
            if chunk:
                buf += chunk

        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            if line:
                handle_message(line.decode("utf-8", "ignore"), wlan)

        utime.sleep_ms(50)


main()
