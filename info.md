<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The design is an 8-bit synchronous counter with enable, up/down direction and parallel load.
On every rising clock edge, in this priority order:

1. If `rst_n` is low, the counter is cleared to 0.
2. Else if `LOAD` (`ui[2]`) is high, the counter takes the value on `uio[7:0]`.
3. Else if `ENABLE` (`ui[0]`) is high, the counter adds 1 (`DOWN` low) or subtracts 1 (`DOWN` high), wrapping at 0 and 255.
4. Otherwise the counter holds its value.

The counter value is always visible on `uo[7:0]`. The `uio` pins are inputs only (they carry the load value).

## How to test

1. Pulse `rst_n` low, then high: `uo` reads 0.
2. Set `ENABLE` = 1: `uo` counts up once per clock.
3. Set `DOWN` = 1 as well: `uo` counts down.
4. Put a value on `uio[7:0]` and pulse `LOAD`: `uo` jumps to that value.

The cocotb tests in `test/test.py` cover reset, counting up, counting down with wrap, load priority and reset while counting. Run them with `cd test && make`.

## External hardware

None. Eight LEDs on `uo[7:0]` show the count, and three switches on `ui[2:0]` control it.
