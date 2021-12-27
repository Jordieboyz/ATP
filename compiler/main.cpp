#include "hwlib.hpp"

extern "C" void put_char( char c ){ hwlib::cout << int(c) << hwlib::endl; };
extern "C" int start();


int main( void ){	
   hwlib::wait_ms( 1000 );
   hwlib::cout << start();
}