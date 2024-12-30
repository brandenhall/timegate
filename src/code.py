import adafruit_ntp
import board
import neopixel
import rtc
import socketpool
import time
import wifi

from settings import settings, LocalTimeZone

# This maps pixels to time positions on the clock, so 12/0 = pixel 5
PIXEL_MAP = [5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7, 6]

pixels = neopixel.NeoPixel(board.D11, 12, brightness=1, auto_write=False)

# last time we synced network time
last_time_sync = None

# keep track of local time
localtime = None


# Connect ot WiFi and sync time with an NTP server
def sync_network_time():
    try:
        if not wifi.radio.connected:
            wifi.radio.connect(settings["WIFI_SSID"], settings["WIFI_PASSWORD"])
        pool = socketpool.SocketPool(wifi.radio)
        ntp = adafruit_ntp.NTP(
            pool, tz_offset=0, server=settings["NTP_SERVER"], socket_timeout=30
        )
        rtc.RTC().datetime = ntp.datetime
    except Exception:
        pass


# Make a "boot up" pattern of 3 white lines
pixels[PIXEL_MAP[0]] = (255, 255, 255)
pixels[PIXEL_MAP[4]] = (255, 255, 255)
pixels[PIXEL_MAP[8]] = (255, 255, 255)
pixels.show()

while True:
    # update the time
    utc_now = time.time()

    # sync time if needed (on boot or at 2am after running for ~1 day)
    if last_time_sync is None or (
        utc_now - last_time_sync > 86000
        and localtime.tm_hour == 2
        and localtime.tm_min == 0
    ):
        # show special pattern when syncing
        sync_network_time()
        utc_now = time.time()
        last_time_sync = utc_now

    localtime = LocalTimeZone.localtime(utc_now)

    # figure out lights to display for the clock
    hour = localtime.tm_hour % 12
    minute = localtime.tm_min // 5
    second = localtime.tm_sec // 5

    # color per LED
    colors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # colors are powers of 2 so they add together for combos, h+m, h+s, s+m, h+m+s etc.
    colors[hour] += 1
    colors[minute] += 2
    colors[second] += 4

    for i in range(12):
        if colors[i] == 0:
            pixels[PIXEL_MAP[i]] = (0, 0, 0)
        else:
            pixels[PIXEL_MAP[i]] = settings["HOUR_PALETTES"][localtime.tm_hour][
                colors[i] - 1
            ]
    pixels.show()
