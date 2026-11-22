`timescale 1ns/1ps
module tb_roi_accumulator;
    reg clk=0, rst_n=0, frame_start=0, pixel_valid=0;
    reg [11:0] pixel_x=0, pixel_y=0;
    reg [7:0] gray=0;
    wire result_valid;
    wire [31:0] count, sum_x, sum_y;
    always #5 clk=~clk;
    roi_accumulator dut(
        .pixel_clk(clk), .rst_n(rst_n), .frame_start(frame_start),
        .pixel_valid(pixel_valid), .pixel_x(pixel_x), .pixel_y(pixel_y),
        .gray(gray), .threshold(8'd150),
        .roi_x0(12'd10), .roi_x1(12'd20),
        .roi_y0(12'd30), .roi_y1(12'd40),
        .result_valid(result_valid), .count(count), .sum_x(sum_x), .sum_y(sum_y));
    task send_pixel(input [11:0] x, input [11:0] y, input [7:0] g);
        begin
            @(negedge clk); pixel_valid=1; pixel_x=x; pixel_y=y; gray=g;
            @(negedge clk); pixel_valid=0;
        end
    endtask
    initial begin
        repeat(2) @(negedge clk); rst_n=1;
        send_pixel(12,32,200);
        send_pixel(18,38,255);
        send_pixel(19,39,100); // below threshold
        send_pixel(40,50,255); // outside ROI
        @(negedge clk); frame_start=1;
        @(posedge clk); #1;
        if (!result_valid || count!==32'd2 || sum_x!==32'd30 || sum_y!==32'd70)
            $fatal(1,"ROI accumulator mismatch");
        @(negedge clk); frame_start=0;
        $display("PASS roi_accumulator");
        $finish;
    end
endmodule
