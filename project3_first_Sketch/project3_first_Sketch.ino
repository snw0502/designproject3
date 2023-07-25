#include <RGBmatrixPanel.h>

#define CLK  8
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2

RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);

//setup initial image
void setup() {
  matrix.begin();

  draw_outline(); //Draw maze outline
  draw_maze1();
}

void draw_outline() {
  matrix.begin();

  for(uint8_t x=0; x<32; x++) {
    matrix.drawPixel(x, 0, matrix.Color333(7, 7, 7));
    matrix.drawPixel(x, 14, matrix.Color333(7, 7, 7));
    matrix.drawPixel(x, 15, matrix.Color333(7, 7, 7));
  }

  for(uint8_t y=0; y<16; y++) {
    if (y != 5) { //leave room for entrance
      matrix.drawPixel(0, y, matrix.Color333(7, 7, 7));
    }
    if (y != 7) { //leave room for exit
      matrix.drawPixel(30, y, matrix.Color333(7, 7, 7));
      matrix.drawPixel(31, y, matrix.Color333(7, 7, 7));
    }
  }

}

void draw_maze1() {


  //Row 1
  matrix.drawPixel(1, 10, matrix.Color333(7, 7, 7));
  matrix.drawPixel(1, 24, matrix.Color333(7, 7, 7));

  //Row 2
  matrix.drawPixel(2, 2, matrix.Color333(7, 7, 7));
  //matrix.drawLine(2, 4, 2, 6, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 4, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 5, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 6, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 8, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 10, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 11, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 12, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 14, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 16, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 17, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 18, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 20, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 21, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 22, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 24, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 25, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 26, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 28, matrix.Color333(7, 7, 7));
  matrix.drawPixel(2, 29, matrix.Color333(7, 7, 7));

  //Row 3
  matrix.drawPixel(3, 2, matrix.Color333(7, 7, 7));
  matrix.drawPixel(3, 8, matrix.Color333(7, 7, 7));
  matrix.drawPixel(3, 12, matrix.Color333(7, 7, 7));
  matrix.drawPixel(3, 14, matrix.Color333(7, 7, 7));
  matrix.drawPixel(3, 22, matrix.Color333(7, 7, 7));
  matrix.drawPixel(3, 26, matrix.Color333(7, 7, 7));

  //Row 4
  matrix.drawPixel(4, 2, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 3, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 4, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 6, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 8, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 9, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 10, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 12, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 14, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 16, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 17, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 18, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 19, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 20, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 22, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 23, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 24, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 26, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 27, matrix.Color333(7, 7, 7));
  matrix.drawPixel(4, 28, matrix.Color333(7, 7, 7));

  //Row 5
  matrix.drawPixel(5, 6, matrix.Color333(7, 7, 7));
  matrix.drawPixel(5, 10, matrix.Color333(7, 7, 7));
  matrix.drawPixel(5, 18, matrix.Color333(7, 7, 7));
  matrix.drawPixel(5, 24, matrix.Color333(7, 7, 7));

  //Row 6
  matrix.drawPixel(6, 6, matrix.Color333(7, 7, 7));
  matrix.drawPixel(6, 6, matrix.Color333(7, 7, 7));
  matrix.drawPixel(6, 6, matrix.Color333(7, 7, 7));
  


}

void show_breadth_first(){
  //TODO
}

void show_a_star(){
  //TODO
}

void reset_animation(){
  matrix.drawRect(0, 0, 32, 16, matrix.Color333(0, 0, 0));
}

void loop() {
  // Do nothing -- image doesn't change
}
