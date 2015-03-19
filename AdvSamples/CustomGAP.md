#Custom GAP Advertising Packet

The GAP advertising packet is modifiable, allowing us to send information to any BLE scanner without waiting for it to establish a connection. We're going to modify advertising data step by step, then receive the result with a custom-built Evothings app.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
Get the code [here](http://developer.mbed.org/users/mbedAustin/code/BLE_EvothingsExample_GAP/).
</span>

##Prerequisites

You'll need:

1. A BLE-enabled mbed board.

2. Install the [Evothings Workbench for your PC and the Evothings app for your phone](http://evothings.com/download/).

3. Install the mbed Evothings [custom GAP app](https://github.com/BlackstoneEngineering/evothings-examples/tree/development/experiments/mbed-Evothings-CustomGAP) on your phone:
	* Downloading the [code](https://github.com/BlackstoneEngineering/evothings-examples/tree/development/experiments/mbed-Evothings-CustomGAP).
	* Drag-and-dropping the index.html file into the Evothings Workbench on your computer.
	* Clicking RUN on the workbench.
	* The code will run on your phone's Evothings client.

3. The [LightBlue iOS](https://itunes.apple.com/us/app/lightblue-bluetooth-low-energy/id557428110?mt=8) app or the [nRF Master Control Panel Android](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en) app to view the results.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
For more information about Evothings, see their [Quick Start Guide](http://evothings.com/getting-started-with-evothings-studio-in-90-seconds/), [tutorials](http://evothings.com/doc/studio/tutorials.html) and [BLE API reference](http://evothings.com/doc/plugins/com.evothings.ble/com.evothings.module_ble.html).
</span>

##GAP Data Review

The general GAP broadcast's data breakdown is illustrated in this diagram:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/GAP/GeneralStruct.png)
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">*The BLE stack eats part of our package's 47B, until only 26 bytes are available for our data*</span>

Every BLE package can contain a maximum of 47 bytes (which isn't much), but:

1. Right off the bat, the BLE stack require 8 for its own purposes.

1. The advertising packet data unit (PDU) therefore has at maximum 39 bytes. But the BLE stack once again requires some overhead, taking up 8 bytes.

2. The PDFU's advertising data field has 31 bytes left, divided into advertising data (AD) structures. Then:

	* The GAP broadcast must contain flags that tell the device about the type of advertisement we're sending. The flag structure takes up three bytes in total (one for data length, one for data type and one for the data itself). The reason we use up these two bytes - the data length and type indications - is to help the parser work correctly with our information. We're down to 28 bytes.

	* Now we're finally sending our data - but it, too, requires an indication of length and type (two bytes in total), so we're down to 26 bytes.

All of which means that we have only 26B to use for the data we want to send over GAP.

And here's what the bottom two layers of structure look like for our particular example - sending manufacturer data:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/GAP/ExampleStruct.png)
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">*The example we use here only requires two data structures, one of 3B, one of 28B - of which two are used for data length and type indications*</span>

##Using the mbed BLE API

First, we need to include a couple of headers: for mbed and for BLE:

```c

	#include "mbed.h"
	#include "BLEDevice.h"
```

Then, we declare the BLE object:

```c

	BLEDevice ble;
```

Now we provide the name of the device:

```c
	
	// change the device's name
	const static char DEVICE_NAME[] = "ChangeMe!!"; 
```

We have up to 26 bytes of data to customise (less is fine - but you can't exceed 26 bytes!):

```c

	// example of hex data
	const static uint8_t AdvData[] = {0x01,0x02,0x03,0x04,0x05};   
```

We can use character data instead of hex:

```c

	// example of character data
	const static uint8_t AdvData[] = {"ChangeThisData"};         
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** most BLE scanner programs will only display the hex representation, so you may see the characters displayed as the numbers that represent them.
</span>

All of that was just setup. Now we need to do something with it. We start by calling the initialiser for the BLE base layer:

```c

	int main(void)
	{
		ble.init();
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** the ``ble.init()`` should always be performed before any other BLE set up.
</span>

Next, we set up the advertising flags:

```c

	    ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | 
			GapAdvertisingData::LE_GENERAL_DISCOVERABLE );
    	ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
```

The second half of the first line puts the advertisement in the *general discoverable* mode, and the last flag sets the type of advertisement to be a *connectable undirected advertisement*. These are the flags that will cost us a total of three out of the 31 bytes. 

It is worth noting that the ``ADV_CONNECTABLE_UNDIRECTED`` flag could just as easily be ``ADV_NON_CONNECTABLE_UNDIRECTED`` if no connection is needed. We have chosen to use the connectable flag as some BLE apps will not display advertising data until a connection is established.

We can then set up the payload. The header ``MANUFACTURER_SPECIFIC_DATA`` is the point where we lose another two bytes of data. Once the header has announced the data we plug in the array we created earlier:

```c

	    ble.accumulateAdvertisingPayload(GapAdvertisingData::MANUFACTURER_SPECIFIC_DATA, 
			AdvData, sizeof(AdvData));
```

Notice that the ``AdvData`` variable is added to the BLE device at this point.

Now we set the advertising interval and start advertising:

```c

    ble.setAdvertisingInterval(160); // 100ms; in multiples of 0.625ms.
    ble.startAdvertising();
```

This will take care of the GAP advertising on the mbed side.

##Seeing Our Data

###Generic Apps

Compile your program and install it on your board (drag and drop it to the board).

On your phone, start the BLE application ([nRF Master Control Panel](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en) for Android and [LightBlue](https://itunes.apple.com/us/app/lightblue-bluetooth-low-energy/id557428110?mt=8) for iOS). It will scan for BLE devices, and should show us ours:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/GAP/SeeingAdvData.png)
</span>

We can see the name we set, the appropriate flags and the data we pushed into the manufacturer data field.

###Evothings Custom-Made App

We're created a [custom-made app for Evothings](https://github.com/BlackstoneEngineering/evothings-examples/tree/development/experiments/mbed-Evothings-CustomGAP) to go with our advertising:


To run the app:

1. Make sure you've installed the Evothings Workbench on your computer and the Evothings client on your phone.

2. Drag-and-drop the **index.html** file into the Evothings Workbench on your computer.

3. Click **RUN** on the workbench.

4. The code will run on your phone's Evothings client.

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/GAP/EvothingsBench.png)
</span>

The code for the application is in the **app.js** file. It is written in JavaScript and can be modified in real time. Try making a modification, save the changes, and watch them load to the Evothings client on your phone.

This demo is very simple but provides a starting point for more advanced programming. 

