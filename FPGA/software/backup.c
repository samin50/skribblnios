//NIOS Imports
#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"

//Standard Imports
#include <stdlib.h>
#include <stdio.h>

//Threading Import
#include <pthread.h>

//Time Import
#include "sys/alt_timestamp.h"
#define SAMPLING_TIME 1
#define INTERVALSECOND 100000000

alt_u8 led;
int level;

void led_write(alt_u8 led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

int main() {
	//Timer
	alt_u32 startTime, stopTime;
	//Accelerometer
    alt_32 x_read;
    alt_32 y_read;
    alt_32 z_read;
    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) {
    	// if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }
    //JTAG
    FILE* fp;
    fp = fopen("/dev/jtag_uart", "r+");

    //Begin
    alt_timestamp_start();
    startTime = alt_timestamp();
    while (1) {
    	//Obtain values at a certain frequency
    	stopTime = alt_timestamp();
    	//Frequency of accelerometer is 2^SAMPLING_TIME Hz, with 6, 64Hz
    	if ((stopTime-startTime) > (INTERVALSECOND >> SAMPLING_TIME-1)) {
    		alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
    		alt_up_accelerometer_spi_read_y_axis(acc_dev, & y_read);
    		alt_up_accelerometer_spi_read_z_axis(acc_dev, & z_read);
    		alt_printf("%ld %ld %ld %c\n", x_read, y_read, z_read, 0x4);
    		startTime = alt_timestamp();
    	}

    }
    return 0;
}
