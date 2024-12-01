import time
import RPi.GPIO as GPIO
import urllib.request

REPO_URL = "https://github.com/lyr-7D1h/button_matrix"
WLED_URL = "http://192.168.2.21/win"
PINS = [14, 15, 18, 23, 24, 25, 8, 7]

GPIO.setmode(GPIO.BOARD)
for i in range(4):
    GPIO.setup(PINS[i], GPIO.OUT)
    GPIO.output(PINS[i], GPIO.HIGH)

for i in range(4, 8):
    GPIO.setup(PINS[i], GPIO.IN, GPIO.PUD_UP)


def request(url: str):
    return urllib.request.urlopen(url).read()


# https://kno.wled.ge/interfaces/http-api/
class WLED:
    def __init__(self, url) -> None:
        self.url = url
        pass

    def set_brightness(self, brightness: int):
        request(self.url + f"&B={brightness}")

    def toggle_power(self):
        request(self.url + "&T=2")


wled = WLED(WLED_URL)


def button_pressed(i: int):
    print(i, "pressed")
    match i:
        case 0:
            wled.toggle_power()
        case 1:
            wled.set_brightness(64)
        case 2:
            wled.set_brightness(125)
        case 3:
            wled.set_brightness(255)


last_update = time.time()


def loop():
    for r in range(4):
        GPIO.output(PINS[r], GPIO.LOW)
        for c in range(4):
            if GPIO.input(PINS[c]) == GPIO.LOW:
                i = r * 4 + c
                button_pressed(i)
                while GPIO.input(PINS[c]) == GPIO.LOW:
                    time.sleep(0.01)
        GPIO.output(PINS[r], GPIO.LOW)


try:
    while True:
        loop()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
