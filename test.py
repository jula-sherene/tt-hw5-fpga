# SPDX-FileCopyrightText: © 2026 Jula Sherene Mervin
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

EN, DOWN, LOAD = 0x01, 0x02, 0x04


async def tick(dut, n=1):
    """Wait n clock edges, then let the registered outputs settle."""
    await ClockCycles(dut.clk, n)
    await Timer(1, unit="us")


async def start(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)


@cocotb.test()
async def test_reset(dut):
    await start(dut)
    assert dut.uo_out.value == 0
    assert dut.uio_oe.value == 0
    assert dut.uio_out.value == 0


@cocotb.test()
async def test_count_up(dut):
    await start(dut)
    dut.ui_in.value = EN
    await tick(dut, 5)
    assert dut.uo_out.value == 5
    # hold: enable low
    dut.ui_in.value = 0
    await tick(dut, 3)
    assert dut.uo_out.value == 5


@cocotb.test()
async def test_count_down_and_wrap(dut):
    await start(dut)
    dut.ui_in.value = EN | DOWN
    await tick(dut, 1)
    assert dut.uo_out.value == 255  # 0 - 1 wraps
    await tick(dut, 2)
    assert dut.uo_out.value == 253


@cocotb.test()
async def test_load(dut):
    await start(dut)
    dut.uio_in.value = 0xA5
    dut.ui_in.value = LOAD
    await tick(dut, 1)
    assert dut.uo_out.value == 0xA5
    # load has priority over enable
    dut.uio_in.value = 0x10
    dut.ui_in.value = LOAD | EN
    await tick(dut, 1)
    assert dut.uo_out.value == 0x10
    # resume counting from the loaded value
    dut.ui_in.value = EN
    await tick(dut, 3)
    assert dut.uo_out.value == 0x13


@cocotb.test()
async def test_reset_while_counting(dut):
    await start(dut)
    dut.ui_in.value = EN
    await tick(dut, 7)
    assert dut.uo_out.value == 7
    dut.rst_n.value = 0
    await tick(dut, 2)
    assert dut.uo_out.value == 0
