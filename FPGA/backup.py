import time
import intel_jtag_uart

try:
    ju = intel_jtag_uart.intel_jtag_uart()

except Exception as e:
    print(e)
    exit(0)

ju.write(b'v')
time.sleep(1)
print("read: ", ju.read())

import concurrent.futures
import intel_jtag_uart

class SkribblNIOS():
    def __init__(self):
        try:
            self.UART = intel_jtag_uart.intel_jtag_uart()
        except Exception as e:
            print(e)
            exit(0)

    def recieve(self):
        with concurrent.futures.ThreadPoolExecutor() as thread:
            self.mainThread = thread.submit(self.UART.read)
            return self.mainThread.result()

    def send(self, outputStr):
        sendStr = bytes(outputStr, 'utf-8')
        with concurrent.futures.ThreadPoolExecutor() as thread:
            self.mainThread = thread.submit(self.UART.write, sendStr)

    def close(self):
        self.UART.close()


FPGA = SkribblNIOS()

while True:
    inputCmd = input("Enter command: ")
    FPGA.send(inputCmd)
    FPGA
