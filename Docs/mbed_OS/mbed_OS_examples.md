# Review of mbed OS BLE examples

We have an [ever growing collection](https://github.com/ARMmbed/ble-examples) of BLE application examples for mbed OS. 



## Prerequisites

1. A supported hardware combination, for example:

 * A device with a radio on board, such as a Nordic nRF51-based board.

 * A supported target, such as the frdm-64f-gcc with a shield or external BLE peripheral (like an ST shield).

1. Please [install yotta](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/installation/) to build the applications.

1. For most examples, you'll want to get a BLE app for your phone:

 * For Android, you can get [nRF Master Control Panel](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp).

 * For iPhone, you can get [LightBlue](https://itunes.apple.com/gb/app/lightblue-bluetooth-low-energy/id557428110?mt=8).

	You can use the app to connect to your BLE device and see the example in action.

## Supported yotta targets

yotta can build your code for different targets: different boards and operating systems. It can also use different compilers. This means you don’t have to re-write code every time you want to test or deploy on a new kind of board. It also means you need to explicitly identify your target to yotta. Identifying a target means naming both the hardware and build toolchain you're using. This is equivalent to selecting the platform that you’re building for in the online IDE (at developer.mbed.org).

The BLE examples have been tested on the following targets:

Nordic (using the nrf51822-ble module):

* nrf51dk-armcc.
* nrf51dk-gcc.
* mkit-gcc.
* mkit-armcc.
* bbc-microbit-gcc.
* bbc-microbit-armcc.


ST (using the st-ble module):

* frdm-k64f-st-ble-gcc (an FRDM-k64f with an ST BLE shield).

### Working with the nRF51 SoftDevice

If you are building the application for nRF51-based 16K targets you should use SoftDevice S110, as otherwise some of these examples will run out of memory. 

To select the version of SoftDevice: before you build the software open the ``config.json`` and change the “softdevice” to “S110”.

It is possible to use S130 on 16K devices, but pay very careful attention to memory consumption.

## Running the examples

__To build an example:__

1. Clone the repository containing the collection of examples:

	```
	$ git clone https://github.com/ARMmbed/ble-examples.git
	```


	**Tip:** If you don't have git installed, you can [download a zip file](https://github.com/ARMmbed/ble-examples/archive/master.zip) of the repository.

1. Using a command-line tool, navigate to any of the example directories, like BLE_Beacon:

	```
	$ cd ble-examples
	$ cd BLE_Beacon
	```

1. Set a yotta target. For example, if you have the BBC micro:bit and the GCC toolchain:

	```
	yotta target bbc-microbit-gcc
	```



1. Run the build:

	```yotta build```

__To run the application on your board:__

1. Connect your mbed board to your computer over USB. It appears as removable storage.

1. When you run the ``yotta build`` command, as you did above, yotta creates [a BIN or a combined HEX file](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/Full_Guide/app_on_yotta/#building-the-module) in a ```build/<target-name>/source``` directory under the example's directory. Drag and drop the file to the removable storage.

  For example, if you’re using the bbc-microbit-gcc target, you should copy the file:
  ``build/bbc-microbit-gcc/source/BLE_Beacon-combined.hex`` to the MICROBIT drive ```cp build/bbc-microbit-gcc/source/BLE_Beacon-combined.hex /path/to/MICROBIT/```
