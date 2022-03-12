/*
 * "Small Hello World" example.
 *
 * This example prints 'Hello from Nios II' to the STDOUT stream. It runs on
 * the Nios II 'standard', 'full_featured', 'fast', and 'low_cost' example
 * designs. It requires a STDOUT  device in your system's hardware.
 *
 * The purpose of this example is to demonstrate the smallest possible Hello
 * World application, using the Nios II HAL library.  The memory footprint
 * of this hosted application is ~332 bytes by default using the standard
 * reference design.  For a more fully featured Hello World application
 * example, see the example titled "Hello World".
 *
 * The memory footprint of this example has been reduced by making the
 * following changes to the normal "Hello World" example.
 * Check in the Nios II Software Developers Manual for a more complete
 * description.
 *
 * In the SW Application project (small_hello_world):
 *
 *  - In the C/C++ Build page
 *
 *    - Set the Optimization Level to -Os
 *
 * In System Library project (small_hello_world_syslib):
 *  - In the C/C++ Build page
 *
 *    - Set the Optimization Level to -Os
 *
 *    - Define the preprocessor option ALT_NO_INSTRUCTION_EMULATION
 *      This removes software exception handling, which means that you cannot
 *      run code compiled for Nios II cpu with a hardware multiplier on a core
 *      without a the multiply unit. Check the Nios II Software Developers
 *      Manual for more details.
 *
 *  - In the System Library page:
 *    - Set Periodic system timer and Timestamp timer to none
 *      This prevents the automatic inclusion of the timer driver.
 *
 *    - Set Max file descriptors to 4
 *      This reduces the size of the file handle pool.
 *
 *    - Check Main function does not exit
 *    - Uncheck Clean exit (flush buffers)
 *      This removes the unneeded call to exit when main returns, since it
 *      won't.
 *
 *    - Check Don't use C++
 *      This builds without the C++ support code.
 *
 *    - Check Small C library
 *      This uses a reduced functionality C library, which lacks
 *      support for buffering, file IO, floating point and getch(), etc.
 *      Check the Nios II Software Developers Manual for a complete list.
 *
 *    - Check Reduced device drivers
 *      This uses reduced functionality drivers if they're available. For the
 *      standard design this means you get polled UART and JTAG UART drivers,
 *      no support for the LCD driver and you lose the ability to program
 *      CFI compliant flash devices.
 *
 *    - Check Access device drivers directly
 *      This bypasses the device file system to access device drivers directly.
 *      This eliminates the space required for the device file system services.
 *      It also provides a HAL version of libc services that access the drivers
 *      directly, further reducing space. Only a limited number of libc
 *      functions are available in this configuration.
 *
 *    - Use ALT versions of stdio routines:
 *
 *           Function                  Description
 *        ===============  =====================================
 *        alt_printf       Only supports %s, %x, and %c ( < 1 Kbyte)
 *        alt_putstr       Smaller overhead than puts with direct drivers
 *                         Note this function doesn't add a newline.
 *        alt_putchar      Smaller overhead than putchar with direct drivers
 *        alt_getchar      Smaller overhead than getchar with direct drivers
 *
 */
#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include <stdlib.h>
#include "alt_types.h"
#include "sys/times.h"
#include "sys/alt_timestamp.h"
#include "sys/alt_stdio.h"
#include <stdbool.h>

#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>

#define SHIFT_AMOUNT 22
#define SAMPLING_TIME 8
#define INTERVALSECOND 700000000
#define OFFSET -32
#define PWM_PERIOD 16
#define NTAPFILTER 250
#define MAXSTRLENGTH 256

static int filterCoeff[NTAPFILTER] = {
		  756,
		  744,
		  1066,
		  1439,
		  1847,
		  2273,
		  2688,
		  3060,
		  3349,
		  3513,
		  3506,
		  3286,
		  2812,
		  2050,
		  980,
		  -409,
		  -2107,
		  -4085,
		  -6294,
		  -8660,
		  -11087,
		  -13461,
		  -15644,
		  -17489,
		  -18837,
		  -19527,
		  -19401,
		  -18313,
		  -16138,
		  -12775,
		  -8160,
		  -2267,
		  4885,
		  13230,
		  22654,
		  32996,
		  44050,
		  55572,
		  67288,
		  78900,
		  90099,
		  100575,
		  110030,
		  118188,
		  124806,
		  129683,
		  132670,
		  133676,
		  132670,
		  129683,
		  124806,
		  118188,
		  110030,
		  100575,
		  90099,
		  78900,
		  67288,
		  55572,
		  44050,
		  32996,
		  22654,
		  13230,
		  4885,
		  -2267,
		  -8160,
		  -12775,
		  -16138,
		  -18313,
		  -19401,
		  -19527,
		  -18837,
		  -17489,
		  -15644,
		  -13461,
		  -11087,
		  -8660,
		  -6294,
		  -4085,
		  -2107,
		  -409,
		  980,
		  2050,
		  2812,
		  3286,
		  3506,
		  3513,
		  3349,
		  3060,
		  2688,
		  2273,
		  1847,
		  1439,
		  1066,
		  744,
		  756
		};





alt_8 pwm = 0;
alt_u8 led;
int level;

void led_write(alt_u8 led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

    if (pwm < abs(level)) {

        if (level < 0) {
            led_write(led << 1);
        } else {
            led_write(led >> 1);
        }

    } else {
        led_write(led);
    }

    if (pwm > PWM_PERIOD) {
        pwm = 0;
    } else {
        pwm++;
    }

}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x0900);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);

}

int sign(long x) { //Determine sign of a number
    return (x > 0) - (x < 0);
}

alt_32 movingAverage(alt_32 * acc_read, short * filterMem, int * filterPointer, int * filterCoeff, bool useCoeff, bool normalisedCoeff) {
	if(* filterPointer == 0) {
		* filterPointer = NTAPFILTER;
	}
	(* filterPointer)--;
	filterMem[* filterPointer] = * acc_read;
	int i;
	long long runningSum = 0; //64 bit number
	float runningDoubleSum = 0;
	if(useCoeff) {
		//If using pre-specified coefficients
		//If normalised
		int placeholderPointer = *filterPointer;
		if (normalisedCoeff) {
			for(i = 0; i < NTAPFILTER; i++) { //Calculate running sum
				runningSum += filterMem[placeholderPointer - i] * filterCoeff[i];
				if((placeholderPointer-i) == 0) { //Wrap back around
					placeholderPointer = NTAPFILTER+i-1;
				}
			}
			//printf("Reg: %d\n, ", (abs(runningSum) >> SHIFT_AMOUNT+1) * sign(runningSum));
			return ((abs(runningSum) >> SHIFT_AMOUNT) * sign(runningSum)); //Final shift and retain sign
		//If not normalised
		} else {
			for(i = 0; i < NTAPFILTER; i++) { //Calculate running sum
				runningDoubleSum += filterMem[placeholderPointer - i] * filterCoeff[i];
				if((placeholderPointer-i) == 0) { //Wrap back around
					placeholderPointer = NTAPFILTER+i-1;
				}
			}
			//printf("Reg: %d\n, ", (int) runningDoubleSum);
			return (int) (runningDoubleSum);
		}
	} else {
		//If doing simple moving average
		for(i = 0; i < NTAPFILTER; i++) { //Calculate running sum
			runningSum += filterMem[i];
		}
		return runningSum/NTAPFILTER;
	}
}

void getText(char *enteredText){ //Function to enter strings into console
	int idx = 0;
	memset(enteredText, 0, MAXSTRLENGTH); //Clear string
	char newChar = alt_getchar();
	while ((newChar != '\n') && (idx < MAXSTRLENGTH)) {
		enteredText[idx] = newChar;
		idx++;
		newChar = alt_getchar();
	}
}


int main() {
	alt_u32 start, stop;
	short filterMem[NTAPFILTER] = { 0 }; //Stores values for moving average
	int filterPointer = NTAPFILTER; //Which element in the array to replace
	int sampleTime = (unsigned int)INTERVALSECOND >> SAMPLING_TIME; //The interval to sample at, currently around 64Hz
	bool normalisedCoeff = true;
	char enteredText[MAXSTRLENGTH]; //String that user can enter into
    alt_32 x_read; //Range is from -256 to 255
    alt_up_accelerometer_spi_dev * acc_dev;
    alt_32 sampleVal;

    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }
    timer_init(sys_timer_isr);

    //Setup function for filter
    bool useFilter = false;
    bool useCoeff = false;
    printf("Number of samples for transmission: %c", 0x4);
    getText(enteredText);
    int sampleNum = atoi(enteredText);
    printf("Filter or no filter? [1/0] Moving Average or Define Coefficients or Predefined Coeff? [m/c/p]: %c", 0x4);
    getText(enteredText);
    if (enteredText[0] == '1') {
       	useFilter = true;
       	if (enteredText[1] == 'c'){
       		printf("Please enter the coefficients separated by an ENTER. %c", 0x4);
			useCoeff = true;
			int i;
			/*
			for(i = 0; i < NTAPFILTER; i++) { //Get coefficients
				getText(enteredText);
				filterCoeff[i] = atoi(enteredText);
			}
			*/
		}
       	if (enteredText[1] == 'p'){
       	   useCoeff = true;
       	}
    }
    int counter = 0;
    int mainCounter = 1;
    bool samplingComplete = false;
    alt_timestamp_start(); //Timestamp disables the leds?
    start = alt_timestamp();
    printf("%c", 0x4);
    while (mainCounter) {
        alt_up_accelerometer_spi_read_z_axis(acc_dev, & x_read); //Changed to z axis for easier reading
        if (useFilter) {
        	alt_32 convertedRead = movingAverage(& x_read, filterMem, & filterPointer, filterCoeff, useCoeff, normalisedCoeff);
        	sampleVal = convertedRead;
        	convert_read(convertedRead, & level, & led);
        } else {
        	sampleVal = x_read;
        	convert_read(x_read, & level, & led);
        }
        if (mainCounter == 10000) {
        	stop = alt_timestamp();
        	printf("Time taken: %x", stop-start);
        }
        //Sampling code
        ///*
        if (samplingComplete == false) {
        	stop = alt_timestamp();
        	//If enough time has passed to sample, sample
        	if ((stop-start) > sampleTime) {
        		start = alt_timestamp();
        		counter++;
        		printf("DATA: %x\n", sampleVal);
        		//Every 15 samples send data
        		if ((counter % 15) == 0) {
        			printf("%c", 0x4);
        		}
        		if (counter > sampleNum) {
        			samplingComplete = true;
        		    printf("Sampling complete. %c", 0x4);
        		}
        	}
        }
        //*/
    }
    return 0;
}
