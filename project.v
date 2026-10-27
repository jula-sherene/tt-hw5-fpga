/*
 * Copyright (c) 2026 Jula Sherene Mervin
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

// 8-bit up/down counter with enable and parallel load.
//   ui_in[0]  enable    : count only while high
//   ui_in[1]  down      : 0 = count up, 1 = count down
//   ui_in[2]  load      : load uio_in into the counter (has priority)
//   uio_in    load value
//   uo_out    counter value
module tt_um_jula_sherene_counter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  wire enable = ui_in[0];
  wire down   = ui_in[1];
  wire load   = ui_in[2];

  reg [7:0] count;

  always @(posedge clk) begin
    if (!rst_n) begin
      count <= 8'd0;
    end else if (load) begin
      count <= uio_in;
    end else if (enable) begin
      if (down) count <= count - 8'd1;
      else      count <= count + 8'd1;
    end
  end

  assign uo_out  = count;
  assign uio_out = 8'd0;
  assign uio_oe  = 8'd0;  // uio pins are all inputs (load value)

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in[7:3], 1'b0};

endmodule
