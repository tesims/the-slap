
import machine, neopixel, time

# Initialize the ADC for reading the photoresistor
ldr = machine.ADC(26)

# Number of LEDs to control
num_leds = 8  # Adjust based on your setup

# Setup the pin connected to your LED strip
pin = machine.Pin(15, machine.Pin.OUT)

# Create a NeoPixel object
np = neopixel.NeoPixel(pin, num_leds)

# Initial settings
current_led = 0
timer = 0
all_blink = False
led_states = [(0, 0, 0)] * num_leds  # State of each LED to handle visibility toggling

def update_leds():
    global current_led, timer, all_blink, led_states
    light_value = ldr.read_u16()

    # Update LED states based on the sequence, independent of the photoresistor
    if current_led < num_leds and time.ticks_diff(time.ticks_ms(), timer) >= 10000:  # Changed from 20000 to 10000 ms
        if current_led == 7:  # Special case for the 8th LED
            led_states[current_led] = (255, 0, 0)  # Set to red
            all_blink = True  # Start blinking all after this
        else:
            led_states[current_led] = (255, 255, 255)  # Set to white
        current_led += 1
        timer = time.ticks_ms()

    # Apply LED states based on the light condition
    if light_value < 650:
        for i in range(num_leds):
            np[i] = led_states[i]
    else:
        np.fill((0, 0, 0))  # Turn off all LEDs to conserve battery when dark

    np.write()

def blink_leds():
    global all_blink, led_states
    if all_blink:
        for state_index in range(len(led_states)):
            led_states[state_index] = (0, 0, 0)
        np.fill((0, 0, 0))
        np.write()
        time.sleep(0.5)
        for state_index in range(len(led_states)):
            led_states[state_index] = (255, 0, 0)  # All LEDs red
        np.fill((255, 0, 0))
        np.write()
        time.sleep(0.5)

# Initialize the first LED and start timer
led_states[0] = (255, 255, 255)
np[0] = (255, 255, 255)
np.write()
timer = time.ticks_ms()

while True:
    update_leds()
    blink_leds()
    time.sleep(0.1)  # Check conditions more frequently for smooth operation
