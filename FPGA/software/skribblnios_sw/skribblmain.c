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
#include "sys/alt_alarm.h"
#include "sys/times.h"
#include "alt_types.h"

//Accelerometer setup and filters
#define FILTER_TAP_NUM 2500
#define SAMPLING_TIME 3
#define DEMEAN_DEPTH 8
alt_32 x_read; //Usually not needed
alt_32 y_read; //Pitch
alt_32 z_read; //Yaw
alt_up_accelerometer_spi_dev * acc_dev;
#define PI 3.14159

//Convert letters - will be upside down
alt_u8 convertDisplay(char digit) {
	switch (digit) {
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
	case 'h':
		return 0b10001001;
	case 'e':
		return 0b10110000;
	case 'l':
		return 0b11111000;
	default:
		return 0b11111111;
	}
}
//Write to hex
void writeScore(char* scoreStr) {
	IOWR_ALTERA_AVALON_PIO_DATA(HEX0_BASE, convertDisplay(scoreStr[0]));
	IOWR_ALTERA_AVALON_PIO_DATA(HEX1_BASE, convertDisplay(scoreStr[1]));
	switch (strlen(scoreStr)) {
	case 3:
		IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, convertDisplay(scoreStr[2]));
		break;
	case 4:
		IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, convertDisplay(scoreStr[2]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, convertDisplay(scoreStr[3]));
		break;
	case 5:
		IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, convertDisplay('.'));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, convertDisplay(scoreStr[2]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, convertDisplay(scoreStr[3]));
		IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, convertDisplay(scoreStr[4]));
		break;
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

void waitForCommand(FILE* fp, char mode, char mode2, char *command, int *arg1,
		int *arg2) {
	while ((*command != mode) && (*command != mode2)) {
		fscanf(fp, "%c %d %d", command, arg1, arg2);
	}
}

//Filtering/accelerometer converter functions
//Moving average filter
void movingAverage(alt_32 x_read, alt_32 y_read, alt_32 z_read, alt_32* xNew,
		alt_32* yNew, alt_32* zNew, alt_32* filterMemX, alt_32* filterMemY,
		alt_32* filterMemZ, int* nTapPtr, alt_32* xTotal, alt_32* yTotal, alt_32* zTotal) {
	//Running totals
	*xTotal += x_read;
	*yTotal += y_read;
	*zTotal += z_read;
	if (filterMemX[*nTapPtr] != 0) {
		*xTotal -= filterMemX[*nTapPtr];
		*yTotal -= filterMemY[*nTapPtr];
		*zTotal -= filterMemZ[*nTapPtr];
	}
	//Append new values
	filterMemX[*nTapPtr] = x_read;
	filterMemY[*nTapPtr] = y_read;
	filterMemZ[*nTapPtr] = z_read;
	(*nTapPtr)++;
	if(*nTapPtr == FILTER_TAP_NUM-1) {
			*nTapPtr = 0;
		}
	//Divide by appropriate amount
	if ((filterMemX[FILTER_TAP_NUM-1] != 0) && (filterMemY[FILTER_TAP_NUM-1] != 0) && (filterMemZ[FILTER_TAP_NUM-1] != 0)) {
		*xNew = *xTotal/FILTER_TAP_NUM;
		*yNew = *yTotal/FILTER_TAP_NUM;
		*zNew = *zTotal/FILTER_TAP_NUM;
	} else {
		*xNew = *xTotal/ *nTapPtr+1;
		*yNew = *yTotal/ *nTapPtr+1;
		*zNew = *zTotal/ *nTapPtr+1;
	}
}
/*N tap filter
int sign(long x) { //Determine sign of a number
    return (x > 0) - (x < 0);
}

void nTapFilter(alt_32 x_read, alt_32 y_read, alt_32 z_read, alt_32* xNew,
		alt_32* yNew, alt_32* zNew, alt_32* filterMemX, alt_32* filterMemY,
		alt_32* filterMemZ, int* nTapPtr) {
	if(* nTapPtr == 0) {
		* nTapPtr = FILTER_TAP_NUM;
	}
	(* nTapPtr)--;
	filterMemX[* nTapPtr] = x_read;
	filterMemY[* nTapPtr] = y_read;
	filterMemY[* nTapPtr] = z_read;
	int i;
	//64 bit numbers
	long long runningSumX = 0;
	long long runningSumY = 0;
	long long runningSumZ = 0;
	//Filtering
	int placeholderPointer = *nTapPtr;
	for(i = 0; i < FILTER_TAP_NUM; i++) { //Calculate running sum
		runningSumX += filterMemX[placeholderPointer - i] * filter_taps[i];
		runningSumY += filterMemY[placeholderPointer - i] * filter_taps[i];
		runningSumZ += filterMemZ[placeholderPointer - i] * filter_taps[i];
		if((placeholderPointer-i) == 0) { //Wrap back around
			placeholderPointer = FILTER_TAP_NUM+i-1;
		}
	}
	*xNew = (abs(runningSumX) >> SHIFT_AMOUNT) * sign(runningSumX);
	*yNew = (abs(runningSumY) >> SHIFT_AMOUNT) * sign(runningSumY);
	*zNew = (abs(runningSumZ) >> SHIFT_AMOUNT) * sign(runningSumZ);
}
*/
//works by removing the mean of previous samples from the current sample to acheive filtering effects
void demeanValues(alt_32 y_read, alt_32 z_read, alt_32* yNew, alt_32* zNew,
		int* sampleArrayY, int* sampleArrayZ, int* arrPointer) {
	int runningSumY = 0;
	int runningSumZ = 0;
	int i;
	//Overwrite previous values
	sampleArrayY[*arrPointer] = y_read;
	sampleArrayZ[*arrPointer] = z_read;
	//Array pointer
	(*arrPointer)++;
	if (*arrPointer == DEMEAN_DEPTH) {
		*arrPointer = 0;
	}
	//Calculate running sum
	for (i = 0; i < DEMEAN_DEPTH; i++) {
		if (sampleArrayY[i] == 0) {
			break;
		}
		runningSumY += sampleArrayY[i];
		runningSumZ += sampleArrayZ[i];
	}
	*yNew = y_read - (runningSumY / (i));
	*zNew = z_read - (runningSumZ / (i));
}
//Calculates Euler angles (rotation control)
void eulerAngles(double x_read, double y_read, double z_read, alt_32* xNew,
		alt_32* yNew, alt_32* zNew) {
	//Convert to degrees
	double x2 = x_read * x_read;
	double y2 = y_read * y_read;
	double z2 = z_read * z_read;
	*xNew = (180 * atan(y_read / sqrt(x2 + z2))) / PI; //Roll
	*yNew = (180 * atan(x_read / sqrt(y2 + z2))) / PI; //Pitch
	*zNew = z_read;
}

//Function that runs during a round
void roundLoop(FILE* fp, int roundLength) {
	//filter parameters
	int arrPointer = 0;
	int nTapPtr = 0;
	int sampleArrayY[DEMEAN_DEPTH] = { 0 };
	int sampleArrayZ[DEMEAN_DEPTH] = { 0 };
	alt_32 filterMemX[FILTER_TAP_NUM] = { 0 };
	alt_32 filterMemY[FILTER_TAP_NUM] = { 0 };
	alt_32 filterMemZ[FILTER_TAP_NUM] = { 0 };
	alt_32 xNew, yNew, zNew;
	alt_32 xTotal = 0;
	alt_32 yTotal = 0;
	alt_32 zTotal = 0;
	//Setup
	clock_t startRoundTime = alt_nticks();
	clock_t stopTime, t_freq;
	int timeRatio = 0;
	//Inputs on board
	int buttonIn = 3; //Buttons are active low
	int switchIn = 0;
	int tempButtonIn, tempSwitchIn;
	//While time is not up
	while (timeRatio < 100) {
		stopTime = alt_nticks();
		t_freq = alt_ticks_per_second();
		//Calculate ratio of time elapsed
		timeRatio = (((stopTime - startRoundTime) / t_freq) * 100)
				/ roundLength;
		if (timeRatio < 10) {
			ledWrite(0b0);
		} else if (timeRatio < 20) {
			ledWrite(0b1);
		} else if (timeRatio < 30) {
			ledWrite(0b11);
		} else if (timeRatio < 40) {
			ledWrite(0b111);
		} else if (timeRatio < 50) {
			ledWrite(0b1111);
		} else if (timeRatio < 60) {
			ledWrite(0b11111);
		} else if (timeRatio < 70) {
			ledWrite(0b111111);
		} else if (timeRatio < 80) {
			ledWrite(0b1111111);
		} else if (timeRatio < 90) {
			ledWrite(0b11111111);
		} else {
			ledWrite(0b111111111);
		}
		//Send  accelerometer and input values
		alt_up_accelerometer_spi_read_x_axis(acc_dev, &x_read);
		alt_up_accelerometer_spi_read_y_axis(acc_dev, &y_read);
		alt_up_accelerometer_spi_read_z_axis(acc_dev, &z_read);
		//Filter values
		movingAverage(x_read, y_read, z_read, &xNew, &yNew, &zNew, filterMemX, filterMemY, filterMemZ, &nTapPtr, &xTotal, &yTotal, &zTotal);
		//nTapFilter(x_read, y_read, z_read, &xNew, &yNew, &zNew, filterMemX, filterMemY, filterMemZ, &nTapPtr);
		//demeanValues(y_read, z_read, &newY, &newZ, sampleArrayY, sampleArrayZ, &arrPointer); //Demean filter
		x_read = xNew;
		y_read = yNew;
		z_read = zNew;
		eulerAngles(x_read, y_read, z_read, &xNew, &yNew, &zNew); //Get angles of rotation
		printf("C %d %d\n", xNew, yNew); //Roll and pitch -> x and y
		tempButtonIn = IORD_ALTERA_AVALON_PIO_DATA(BUTTON_BASE);
		tempSwitchIn = IORD_ALTERA_AVALON_PIO_DATA(SWITCH_BASE);
		printf("B %d\n", tempButtonIn);
		printf("S %d\n", tempSwitchIn);
	}
}

int main() {
	acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
	if (acc_dev == NULL) {
		// if return 1, check if the spi ip name is "accelerometer_spi"
		return 1;
	}
	//Declare variables for accepting commands/data
	char commandChar = 0;
	int roundLength, arg1, arg2;
	char* scoreStr[6];
	writeScore("......");
	FILE* fp = fopen("/dev/jtag_uart", "r+");
	//Wait for start
	writeScore("hell0.");
	ledWrite(0b0000000000);
	waitForCommand(fp, 'I', 'I', &commandChar, &arg1, &arg2);
	writeScore("start.");
	ledWrite(0b1111111111);
	waitForCommand(fp, 'S', 'S', &commandChar, &arg1, &arg2);
	roundLength = arg1;		//Length of round will be stored into arg1
	writeScore("------");
	//Wait for round start
	waitForCommand(fp, 'R', 'R', &commandChar, &arg1, &arg2);
	fclose(fp);
	//MAIN LOOP - Terminate loop when game end - command E
	while (commandChar != 'E') {
		sprintf(scoreStr, "%d-%d", arg1, arg2); //Build score str
		writeScore(scoreStr);
		fp = fopen("/dev/jtag_uart", "r+");
		roundLoop(fp, roundLength);
		commandChar = 'F';
		ledWrite(0b1111111111);
		waitForCommand(fp, 'R', 'E', &commandChar, &arg1, &arg2);
		fclose(fp);
	}
	ledWrite(0b0);
	return 0;
}
