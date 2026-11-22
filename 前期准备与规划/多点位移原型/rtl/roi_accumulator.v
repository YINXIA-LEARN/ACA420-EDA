// Board-independent pixel-stream sums for one ROI.
// frame_start and pixel_valid are synchronous to pixel_clk.
// Coordinates are integer pixels; division/quality checking are downstream.
module roi_accumulator #(
    parameter integer XW = 12,
    parameter integer YW = 12,
    parameter integer SW = 32
)(
    input wire pixel_clk,
    input wire rst_n,
    input wire frame_start,
    input wire pixel_valid,
    input wire [XW-1:0] pixel_x,
    input wire [YW-1:0] pixel_y,
    input wire [7:0] gray,
    input wire [7:0] threshold,
    input wire [XW-1:0] roi_x0,
    input wire [XW-1:0] roi_x1,
    input wire [YW-1:0] roi_y0,
    input wire [YW-1:0] roi_y1,
    output reg result_valid,
    output reg [SW-1:0] count,
    output reg [SW-1:0] sum_x,
    output reg [SW-1:0] sum_y
);
    reg [SW-1:0] count_acc, x_acc, y_acc;
    wire hit = pixel_valid && gray >= threshold &&
               pixel_x >= roi_x0 && pixel_x <= roi_x1 &&
               pixel_y >= roi_y0 && pixel_y <= roi_y1;
    always @(posedge pixel_clk or negedge rst_n) begin
        if (!rst_n) begin
            count_acc <= 0; x_acc <= 0; y_acc <= 0;
            count <= 0; sum_x <= 0; sum_y <= 0;
            result_valid <= 0;
        end else begin
            result_valid <= 0;
            if (frame_start) begin
                count <= count_acc;
                sum_x <= x_acc;
                sum_y <= y_acc;
                result_valid <= 1;
                count_acc <= 0;
                x_acc <= 0;
                y_acc <= 0;
            end else if (hit) begin
                count_acc <= count_acc + 1'b1;
                x_acc <= x_acc + pixel_x;
                y_acc <= y_acc + pixel_y;
            end
        end
    end
endmodule
