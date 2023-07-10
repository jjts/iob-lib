`timescale 1ns / 1ps

module iob_modcnt #(
   parameter DATA_W  = 21,
   parameter RST_VAL = {DATA_W{1'b0}},
   parameter CLKEDGE = "posedge"
) (

   `include "iob_clk_en_rst_port.vs"

   input rst_i,
   input en_i,

   input  [DATA_W-1:0] mod_i,
   output [DATA_W-1:0] data_o
);

   wire ld_count = (data_o == mod_i);
   wire                               [DATA_W-1:0] ld_val = {DATA_W{1'b0}};

   iob_counter_ld #(
      .DATA_W (DATA_W),
      .RST_VAL(RST_VAL),
      .CLKEDGE(CLKEDGE)
   ) cnt0 (
      `include "iob_clk_en_rst_portmap.vs"
      .rst_i   (rst_i),
      .en_i    (en_i),
      .ld_i    (ld_count),
      .ld_val_i(ld_val),
      .data_o  (data_o)
   );

endmodule
