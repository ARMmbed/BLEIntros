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

##Debugging with the mbed Interface Chip

Most mbed platforms come with an interface chip placed between the target microcontroller (in our case, the BLE microcontroller) and the development host (our computer). This interface chip plays a key role in debugging: it is a USB-bridge between the development host and the debugging capabilities available in ARM microcontrollers. This bridge functionality is encapsulated in a standard called [CMSIS-DAP](http://developer.mbed.org/handbook/CMSIS-DAP) that major toolchain vendors have started to support, so we can expect it to grow in popularity and availability over time. 

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** some smaller boards reduce size and cost by not carrying an interface chip. For these, you might like to move on to the next sections.
</span>

By using the interface chip we can debug with:

* ``printf()`` and its associated capabilities.

* ``error()``.

* PyOCD.

<span style="text-align:center; display:block;">
![](/BLEIntros/InDepth/Images/DebugviaUSB.png)
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">*The development host uses a USB connection with the interface chip to debug the microcontroller. Some of the terms in this image will be clarified later in the document.*</span>

###Printf()

The microcontroller's universal asynchronous receiver/transmitter (UART) console peripheral can "feed" the microctronolloer's ``printf()`` output to the interface chip, which then forwards it to the development host. We can then intercept that traffic with a terminal program running on the host. These examples use the CoolTerm serial port application to read the ``printf()`` output, but you can use any terminal program you want and expect similar results.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
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
	#define TRACE_DEBUG(...)      { if (traceLevel >= TRACE_LEVEL_DEBUG)   { printf("-D- " __VA_ARGS__); } }
	#define TRACE_WARNING(...)    { if (traceLevel >= TRACE_LEVEL_WARNING) { printf("-W- " __VA_ARGS__); } }
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

###Fast Circular Log-Buffers Based on printf()



##The UART Service
the universal asynchronous receiver/transmitter (UART)


it is a BLE service wihch provides printf() like facility over Bluetooth Smart
without requiring physical connectivity offered by interface chip
if there is no interface chip, then UARTService could be a way for forwarding printf() to the user


##External Sniffers
