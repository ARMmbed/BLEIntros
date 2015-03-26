#Debugging on mbed BLE

This is a review of some debugging techniques that you can use when writing applications that use the BLE_API on mbed boards. 

We'll look at using the interface chip, LEDs and third-party sniffers to debug our applications.

##The Quick Method: LEDs

Most boards come with at least one LED. Turning the LED on or off, or flashing it, is a quick method of knowing that you've reached a certain state. For example, you can have an LED flash if your code has reached an error handler, or turn it on at the start of ``main()`` and then turn it off whenever an interrupt handler preempts ``main()``; if you never get your LED back on, it means that ``main()`` never got back control and you have a problem.

LEDs require almost no coding and processing, giving them near-zero overhead.

```c


	#include <mbed.h>

	DigitalOut led(LED1);

	... somewhere later ...
		/* writing 1 to an LED usually turns it on; but your world could be topsy turvy. */
		led = 1; 

	... or perhaps in some other file ...

		extern DigitalOut led;
		led = 0;

```

###The LED Error() Utility

Runtime errors are caused by:

* Code trying to perform an invalid operation.

* Hardware that cannot be accessed because it is malfunctioning. 

The mbed SDK includes a nice utility called ``error(). It takes in printf()-style parameters, but its output is an LED pattern that is easily identified as an alert. This gives visual error indication without need to write with ``prinft()`` (as we do below).

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
For more information about ``error()``, see the [handbook](http://developer.mbed.org/handbook/Debugging#runtime-errors).
</span>

You can use ``assert()`` to improve error reporting:

```c

	#define ASSERT(condition, ...)	{
		if (!(condition))	{
			error("Assert: " __VA_ARGS__);

		}
	}

```

##Debugging with the mbed Interface Chip

Most mbed platforms come with an interface chip placed between the target microcontroller (in our case, the BLE microcontroller) and the development host (our computer). This interface chip plays a key role in debugging: it is a USB-bridge between the development host and the debugging capabilities available in ARM microcontrollers. This bridge functionality is encapsulated in a standard called [CMSIS-DAP](http://developer.mbed.org/handbook/CMSIS-DAP) that major toolchain vendors have started to support, so we can expect it to grow in popularity and availability over time. 

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** some smaller boards reduce size and cost by not carrying an interface chip. For these, you might like to move on to the next sections.
</span>

By using the interface chip we can debug with:

* ``printf()`` and its associated capabilities.

* pyOCD.

<span style="text-align:center; display:block;">
![](/BLEIntros/InDepth/Images/DebugviaUSB.png)
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">*The development host uses a USB connection with the interface chip to debug the microcontroller. Some of the terms in this image will be clarified later in the document.*</span>

###Printf()

The microcontroller's universal asynchronous receiver/transmitter (UART) console peripheral can "feed" the microctronolloer's ``printf()`` output to the interface chip, which then forwards it to the development host. We can then intercept that traffic with a terminal program running on the host. These examples use the CoolTerm serial port application to read the ``printf()`` output, but you can use any terminal program you want and expect similar results.

<span style="background-color:#D8F6CE; color:#886A08; display:block; height:100%; padding:10px">
**Tip:** The UART protocol requires that the sender and receiver each maintain their own clocks and know the baud rate. mbed interface chips use the 9,600 baud rate and your terminal program should be set to that baud rate to intercept the communication.
</span>

The costs of ``printf()``:

* An additional 5-10K of flash memory use. This makes a good case for not using it unnecessarily. Do note, however, that this is the cost of the first use of ``printf()`` in a program; additional uses cost almost no additional memory.

* Each call to ``printf()`` takes a significant time for processing and executing: about 10 milliseconds and 100,000 instructions. This is only a baseline; if your ``printf()`` allows for formatting its costs will be higher still. If your clock runs slowly (as most microcontrollers' clocks do) and your computational power is lower, ``printf()`` can sometimes be used as a delay.

These two points show the problems of using ``printf()``: there is limited space on the board, and we expect interrupt handlers to terminate within a few microseconds. ``printf()`` doesn't match these requirements. Calling ``printf()``, especially from an event handler, should be done judiciously.

Using ``printf()`` on mbed requires including the ``stdio`` header:

```c

	#include <stdio.h>

	... some code ...

		printf("debug value %x\r\n", value);
```

Here's a very basic example. In the [URI Beacon program](/GettingStarted/URIBeacon/), we've added ``printf()`` in three places (this is excessive):

* After setting ``DEVICE_NAME``, we've added ``printf("Device name is %s\r\n", DEVICE_NAME);``

* After ``startAdvertisingUriBeaconConfig();`` we've added ``printf("started advertising \r\n")``;.

* After ``ble.waitForEvent();`` we've added ``printf("waiting \r\n");``.

This is the terminal output. Note that "waiting" is printed every time ``waitForEvent`` is triggered:

<span style="text-align:center; display:block;">
![](/BLEIntros/InDepth/Images/TerminalOutput.png)
</span>

###Printf() Macros

There are some nifty tricks you can do with pre-processor macros using printf()s:

```c
	
	-- within some header file named like trace.h --
	enum {
		TRACE_LEVEL_DEBUG,
		TRACE_LEVEL_WARNING
	};

	extern unsigned traceLevel;

	...

	// Trace output depends on traceLevel value
	#define TRACE_DEBUG(...)      
		{ if (traceLevel >= TRACE_LEVEL_DEBUG)   { printf("-D- " __VA_ARGS__); } }
	#define TRACE_WARNING(...)    
		{ if (traceLevel >= TRACE_LEVEL_WARNING) { printf("-W- " __VA_ARGS__); } }
```

Here's a contribution from a user:

```c



	#define LOG(x, ...)  
		{ printf("\x1b[34m%12.12s: \x1b[39m"x"\x1b[39;49m\r\n", 
		MODULE_NAME, ##__VA_ARGS__); fflush(stdout); }
	#define WARN(x, ...) 
		{ printf("\x1b[34m%12.12s: \x1b[33m"x"\x1b[39;49m\r\n", 
		MODULE_NAME, ##__VA_ARGS__); fflush(stdout); }

```

Set ``#define MODULE_NAME "<YourModuleName>"`` before #including the above code, and enjoy colourised, formatted printf tagged with the module name that generated it.

###Fast Circular Log Buffers Based on Printf()

When trying to capture logs from events that occur in very rapid succession, using a ``printf()`` may introduce unacceptable run-time latencies that might alter the system's behaviour or destabilise it. But the biggest cause of delay with ``printf()`` is pushing the logs to the UART; just generating the message is significantly less expensive. So the obvious solution is not to push the logs to the UART while the operation we're debugging is running.

Instead, we use ``sprintf()`` to write the log messages into a ring buffer (buffers that append to the tail and wrap around as needed), which waits until the system is idle to go through UART (we can transmit it from ``main()`` while waiting for events). 

Here is an example of such an implementation. Because sprintf() assumes an arbitrarily long
string, we must be careful not to overflow the actual space. This example appends to the tail of a ring buffer as long as it doesn't exceed the half-way mark (an arbitrarily selected point); when the half-way mark is reached the buffer is wrapped around.

```c


	#define BUFFER_SIZE 512 /* You need to choose a suitable value here. */
	#define HALF_BUFFER_SIZE (BUFFER_SIZE >> 1)

	char ringBuffer[BUFFER_SIZE]; /* This is just one way of allocating the ring buffer. */
	char *ringBufferStart = ringBuffer;
	char *ringBufferTail  = ringBuffer;

	void xprintf(const char *format, ...)
	{
		va_list args;
		va_start(args, format);
		size_t largestWritePossible = BUFFER_SIZE - (ringBufferTail - ringBufferStart);
		int    written = vsnprintf(ringBufferTail, largestWritePossible, format, args);
		va_end(args);

		if (written < 0) {
			/* do some error handling */
			return;
		}

		/*
		* vsnprintf() doesn't write more than 'largestWritePossible' bytes to the
		* ring buffer (including the terminating null byte '\0'). If the output is
		* truncated due to this limit, then the return value ('written') is the
		* number of characters (excluding the terminating null byte) which would
		* have been written to the final string if enough space had been available.
		*/

		if (written > largestWritePossible) {
			/* There are no easy solutions to tackle this. It may be easiest to enlarge
			* your BUFFER_SIZE to avoid this. */
			return; /* this is a poor short-cut; you may want to do something about it.*/
		}

		ringBufferTail += written;

		/* Is it time to wrap around? */
		if (ringBufferTail > (ringBufferStart + HALF_BUFFER_SIZE)) {
			size_t overflow = ringBufferTail - (ringBufferStart + HALF_BUFFER_SIZE);
			memmove(ringBufferStart, ringBufferStart + HALF_BUFFER_SIZE, overflow);
			ringBufferTail = ringBufferStart + overflow;
		}
	}


```

With this implementation, debug messages accumulated using xprintf() can be read out circularly starting from ``ringBufferTail`` and wrapping around (``ringBufferTail`` + ``HALF_BUFFER_SIZE``). The first message would most likely be garbled because of an overwrite by the most recently appended message.

###pyOCD-Based Debugging (GDB Server)

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** using GDB (or any other debugger) to connect to the GDB server is useful only if we have access to the program symbols and their addresses. This is currently *not* exported when building ``.hex`` files using the mbed online IDE; we need to export our project to an offline toolchain to be able to generate either an ``.elf`` file which holds symbols alongside the program, or a ``.map`` file for symbols. In the following section, we're assuming  an ``.elf`` file.
</span>

So far, we've seen the UART connection between the interface chip and the target microcontroller. But there is another connection between the two: serial wire debug (SWD). This protocol offers debugging capabilities for stack trace analysis, register dumps and inspection of program execution (breakpoints, watchpoints etc). When combined with a source-level debugger on the development host, such as the GNU Project Debugger (GDB), SWD offers a very rich debugging experience - much more powerful than ``printf()``. 

<span style="background-color:#D8F6CE; color:#886A08; display:block; height:100%; padding:10px">
**Tip:** GDB is often "too rich" - don't forget the fast efficiency of ``printf()`` and the LEDs.
</span>

The interface chip implements CMSIS-DAP. On the mbed boards, you'll need the [pyOCD Python library](https://github.com/mbedmicro/pyOCD) to drive the CMSIS-DAP interface chip over USB.

<span style="text-align:center; display:block;">
![](/BLEIntros/InDepth/Images/PyOCD.png)
</span>


<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
To install pyOCD, follow the [instructions](https://github.com/mbedmicro/pyOCD/blob/master/README.md#installation) to get the external USB libraries pyOCD relies on.
<br /><br />
**Notes:**
<br />
* You'll need to run ``setup.py`` for both the USB libraries and pyOCD. 
<br />
* You can follow [HOW_TO_BUILD.md](https://github.com/mbedmicro/pyOCD/blob/master/HOW_TO_BUILD.md) to see how to build pyOCD into a single executable GDB server program.
<br />
* A series of tests in the [test sub-folder](https://github.com/mbedmicro/pyOCD/tree/master/test) offers scripts that you may find useful as a foundation for developing custom interaction with the targets over CMSIS-DAP.

The GDB server can be launched by running ``gdb_server.py``. This script should be able to detect any connected mbed board. Here is an example of executing the script from the terminal while a Nordic mKIT is connected:

```

	$ sudo python test/gdb_server.py
	Welcome to the PyOCD GDB Server Beta Version
	INFO:root:new board id detected: 107002001FE6E019E2190F91
	id => usbinfo | boardname
	0 =>   (0xd28, 0x204) [nrf51822]
	INFO:root:DAP SWD MODE initialised
	INFO:root:IDCODE: 0xBB11477
	INFO:root:4 hardware breakpoints, 0 literal comparators
	INFO:root:CPU core is Cortex-M0
	INFO:root:2 hardware watchpoints
	INFO:root:GDB server started at port:3333

```

At this point, the target microcontroller is waiting for interaction from a GDB server. This server is running at port 3333 on the development host, and may be connected to from a debugger such as GDB.
Here is an example of launching the GDB client:

```

	~/play/demo-apps/BLE_Beacon/Build$ arm-none-eabi-gdb BLE_BEACON.elf
	GNU gdb (GNU Tools for ARM Embedded Processors) 7.6.0.20140731-cvs
	Copyright (C) 2013 Free Software Foundation, Inc.
	License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
	This is free software: you are free to change and redistribute it.
	There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
	and "show warranty" for details.
	This GDB was configured as "--host=x86_64-unknown-linux-gnu --target=arm-none-eabi".
	For bug reporting instructions, please see:
	<http://www.gnu.org/software/gdb/bugs/>...
	Reading symbols from /home/rgrover/play/demo-apps/BLE_Beacon/Build/BLE_BEACON.elf...
	warning: Loadable section "RW_IRAM1" outside of ELF segments
	(gdb)


```

Notice that we pass in the .``elf`` file as an argument. We could also have used the ``file`` command within GDB to load symbols from this ``.elf`` file after starting GDB. The command set offered by GDB to help with symbol management and debugging is outside the scope of this document, but you can find it in [GDB's documentation](https://www.gnu.org/software/gdb/documentation/).


Now, we connect to the GDB server (for ease of reading, we've added line breaks in the path);

````

	(gdb) target remote localhost:3333
	Remote debugging using localhost:3333
	warning: Loadable section "RW_IRAM1" outside of ELF segments
	HardFault_Handler ()
    	at 	/home/rgrover/play/mbed-src/libraries
			/mbed/targets/cmsis/TARGET_NORDIC/TARGET_MCU_NRF51822
			/TOOLCHAIN_ARM_STD/TARGET_MCU_NORDIC_16K
			//startup_nRF51822.s:115
	115                 B       .
	(gdb)


```

Now we can perform normal debugging using the GDB command console (or a GUI, if our heart desires).



##The UART Service

BLE has a UART service that allows debugging over the BLE connection (by forwarding the output over BLE), rather than through the interface chip.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** you'll need an app that can receive the service's output (the logs). There are many of these; you could try [Nordic's nRF UART](http://www.nordicsemi.com/eng/Products/nRFready-Demo-Apps/nRF-UART-App).
</span>

This is what the app needs to be able to use the UART service:

```c

	uart = new UARTService(ble);

	... and somewhat later ...

	uart->write("some updated\r\n", strlen("some update\r\n"));

```

Note that:

* We use ``write()``, not ``prinft()``.

* We have to prepare the output message.

* We have to pass a length argument to ``write()``.

* Currently you can only have one BLE connection to the device at any one time, and the UART app used for debugging takes up that connection. For example, if you're monitoring a heart rate device and receiving output over the nRF UART app, you cannot simultaneously connect to the heart rate device with a standard heart rate app to view the heart rate.


##Sniffers


