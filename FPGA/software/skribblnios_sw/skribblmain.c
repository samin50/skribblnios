//NIOS Imports
#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"

//Standard Imports
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>

//Time Import
#include "sys/alt_timestamp.h"


#define SAMPLING_TIME 3
#define INTERVALSECOND 100000000
#define BUFFERSIZE 50

//Accelerometer setup
alt_32 x_read;
alt_32 y_read;
alt_32 z_read;
alt_up_accelerometer_spi_dev * acc_dev;

//Convert letters - will be upside down
alt_u8 convertDisplay(char digit) {
	switch(digit) {
	case '0':
		return 0b11000000;
	case '1':
		return 0b11001111;
	case '2':
		return 0b10100100;
	case '3':
		return 0b10000110;
	case '4':
		return 0b10001011;
	case '5':
		return 0b10010010;
	case '6':
		return 0b10010000;
	case '7':
		return 0b11000111;
	case '8':
		return 0b10000000;
	case '9':
		return 0b10000010;
	case '-':
		return 0b10111111;
	case 's':
		return 0b10010010;
	case 't':
		return 0b10111000;
	case 'a':
		return 0b10000001;
	case 'r':
		return 0b10111101; //0b11110001 Capital
	default:
		return 0b11111111;
	}
}
//Write to hex
void writeScore(char* scoreStr) {
	IOWR_ALTERA_AVALON_PIO_DATA(HEX0_BASE, convertDisplay(scoreStr[0]));
	IOWR_ALTERA_AVALON_PIO_DATA(HEX1_BASE, convertDisplay(scoreStr[1]));
	switch (strlen(scoreStr)){
	case 3:
		IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, convertDisplay(scoreStr[2]));
	case 4:
		IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, convertDisplay(scoreStr[2]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, convertDisplay(scoreStr[3]));
	case 5:
		IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, convertDisplay(scoreStr[2]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, convertDisplay(scoreStr[3]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, convertDisplay(scoreStr[4]));
	case 6:
		IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, convertDisplay(scoreStr[2]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, convertDisplay(scoreStr[3]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, convertDisplay(scoreStr[4]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, convertDisplay(scoreStr[5]));
	}
	return;
}



//Write to leds
void ledWrite(unsigned int led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

//Function that halts till certain data is received
char* waitForData(FILE* fp, char* compare1, char* compare2) {
	char* waitIn[BUFFERSIZE];
	while ((strcmp(waitIn, compare1) != 0) && (strcmp(waitIn, compare2) != 0 )) {
		read(fp, &waitIn, BUFFERSIZE);
	}
	printf("BREAK");
	if ((strcmp(waitIn, compare1)) != 0) {
		return compare1;
	} else {
		return compare2;
	}
}

//Function that runs during a round
void roundLoop(FILE* fp) {
	char* timeRatio[BUFFERSIZE];
	int ratio = 0;
	alt_timestamp_start();
	alt_32 startTime = alt_timestamp();
	alt_32 stopTime;
	//While time is not up
	while (strcmp(timeRatio, "100") != 0) {
		//If received a time ratio
		if(read(fp, &timeRatio, 1) > 0) {
			ratio = atoi(timeRatio);
			if (ratio < 10) {
				ledWrite(0b1);
			} else if (ratio < 20) {
				ledWrite(0b11);
			} else if (ratio < 30) {
				ledWrite(0b111);
			} else if (ratio < 40) {
				ledWrite(0b1111);
			} else if (ratio < 50) {
				ledWrite(0b11111);
			} else if (ratio < 60) {
				ledWrite(0b111111);
			} else if (ratio < 70) {
				ledWrite(0b1111111);
			} else if (ratio < 80) {
				ledWrite(0b11111111);
			} else if (ratio < 90) {
				ledWrite(0b111111111);
			}
		}
		//Send  accelerometer and input values
		//Obtain values at a certain frequency
		/*
		stopTime = alt_timestamp();
		//Frequency of accelerometer is 2^SAMPLING_TIME Hz, with 6, 64Hz
		if ((stopTime-startTime) > (INTERVALSECOND >> SAMPLING_TIME-1)) {
			alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
			alt_up_accelerometer_spi_read_y_axis(acc_dev, & y_read);
			alt_up_accelerometer_spi_read_z_axis(acc_dev, & z_read);
			printf("%d %d %d\n", x_read, y_read, z_read);
			startTime = alt_timestamp();

		}
		*/
	}
}

int main () {
	acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
	if (acc_dev == NULL) {
		// if return 1, check if the spi ip name is "accelerometer_spi"
		return 1;
	}
	char* dataIn[BUFFERSIZE];
	FILE* fp = open("/dev/jtag_uart", O_RDWR|O_NONBLOCK|O_NOCTTY|O_SYNC);
	writeScore("start");
	ledWrite(0b1111111111);
	//Wait for start
	strcpy(dataIn, waitForData(fp, "STARTGAME", "STARTGAME"));
	writeScore("------");
	//Wait for round start
	strcpy(dataIn, waitForData(fp, "STARTROUND", "STARTROUND"));
	fclose(fp);

	//MAIN LOOP - Terminate loop when game end
	while (strcmp(dataIn, "ENDGAME") != 0) {
		fp = open("/dev/jtag_uart", O_RDWR|O_NONBLOCK|O_NOCTTY|O_SYNC);
		roundLoop(fp);
		strcpy(dataIn, waitForData(fp, "STARTGAME", "ENDGAME"));
		fclose(fp);
	}
	return 0;
}
