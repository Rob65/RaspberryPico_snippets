# WS2813b example

This example shows a running light of green, red, blue and white on a string with 90 LEDs

The WS2813b is an RGBW LED controller from the same family as the WS2812b.
The WS2813b not only uses 32 bits to control RGB and White LEDs but it also uses a different timing.

Where the WS2812 uses a fixed 1.25 µs period for a 0 or a 1, the WS2813 uses a fixed low period of 800 ns with only the high period changing fron 300 to 800 ns for a 0 or 1.
This results in a variable data-rate, depending on the number of 0's and 1's being sent. It takes up to 51.2 µs for one LED to be addressed.

Note that the datasheet specifies a minimum of 280 µs for a reset period.
The script implements a 500 µs delay. This is needed because the sm.put(ar) command will finish before all data has been sent.
A shorter delay may result in data corruption, which is visible as a wrong pattern being shown.