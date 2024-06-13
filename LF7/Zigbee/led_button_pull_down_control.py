import RPi.GPIO as GPIO
import time

# GPIO setup
LED_PIN = 18
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN)  # Kein interner Pull-Up/Down-Widerstand

# Flag, um den Zustand der LED zu steuern
led_flag = False


def set_led(state):
    global led_flag
    led_flag = state
    if led_flag:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)


# Callback-Funktion, die bei einem Tastendruck aufgerufen wird
def button_callback(channel):
    global led_flag
    set_led(not led_flag)  # LED-Zustand umschalten


# Event-Detection für den Button einrichten
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)  # Kurze Verzögerung, um CPU-Last zu reduzieren

except KeyboardInterrupt:
    print("\nBeende Programm...\nFühre GPIO.cleanup durch")

finally:
    GPIO.cleanup()
