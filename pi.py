import time
import gpiod
import urllib.request

chip = gpiod.Chip("gpiochip4")

WLED_URL = "http://192.168.2.21/win"
PINS = [14, 15, 18, 23, 24, 25, 8, 7]

lines = [chip.get_line(i) for i in PINS]


def setup():
    for i in range(4):
        lines[i].request(consumer="button", type=gpiod.LINE_REQ_DIR_OUT)
        lines[i].set_value(1)

    for i in range(4, 8):
        lines[i].request(
            consumer="button",
            type=gpiod.LINE_REQ_DIR_IN,
            flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP,
        )


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


def loop():
    for r in range(4):
        lines[r].set_value(0)
        for c in range(4, 8):
            if lines[c].get_value() == 0:
                i = r * 4 + c % 4
                button_pressed(i)
                while lines[c].get_value() == 0:
                    time.sleep(0.01)
        lines[r].set_value(1)


setup()
try:
    while True:
        loop()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
    for line in lines:
        line.release()
