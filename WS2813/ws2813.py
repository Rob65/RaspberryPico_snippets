import array, time
from machine import Pin
import rp2

num_leds   = 90
reset_time = 500

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=32)
def ws2813():
    T1 = 3
    T2 = 5
    T3 = 8
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1] 
    jmp(not_x, "bitloop")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on Pin(4).
sm = rp2.StateMachine(0, ws2813, freq=10_000_000, sideset_base=Pin(4))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

ar = array.array("I", [0 for _ in range(num_leds+1)])
#         GGRRBBWW
while True:	

    for s in [24,16,8,0]: # Repeat this for each color
        for i in range(num_leds+1):
            ar[i] = 0x11 << s
            sm.put(ar)
            time.sleep_us(reset_time) # reset period - don't go any faster or risk data corruption
        
    for i in range(num_leds+1): # clear all LEDs
        ar[i] = 0
        sm.put(ar)
        time.sleep_us(reset_time)

