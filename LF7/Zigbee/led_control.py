import RPi.GPIO as GPIO
import time

# GPIO setup
LED_PIN = 18  # Wähle den GPIO-Pin, an dem die LED angeschlossen ist
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Flag, um den Zustand der LED zu steuern
led_flag = False

def set_led(state):
    global led_flag
    led_flag = state
    if led_flag:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

try:
    while True:
        # Beispiel: Schaltet die LED ein, wenn die Flagge True ist, und aus, wenn sie False ist
        # Hier kannst du die Logik einfügen, die die Flagge ändert
        set_led(True)  # LED einschalten
        time.sleep(5)  # LED bleibt 5 Sekunden an
        set_led(False)  # LED ausschalten
        time.sleep(5)  # LED bleibt 5 Sekunden aus

except KeyboardInterrupt:
    print("Beende Programm...")

finally:
    GPIO.cleanup()
