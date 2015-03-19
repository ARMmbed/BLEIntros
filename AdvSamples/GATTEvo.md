#Custom GATT Service with Evothings

We're going to create a custom GATT service to blink the LED on an mbed board, and demonstrate using Evothing to create a custom app that communicates with our GATT service.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
Get the code [here](http://developer.mbed.org/users/mbedAustin/code/BLE_EvothingsExample_GATT/).
</span>

##Prerequisites

You'll need:

1. A BLE-enabled mbed board.

2. Install the [Evothings Workbench for your PC and the Evothings app for your phone](http://evothings.com/download/).

3. Install the mbed Evothings [custom GATT app](https://github.com/BlackstoneEngineering/evothings-examples/tree/development/experiments/mbed-Evothings-CustomGATT) on your phone:
	* Downloading the [code](https://github.com/BlackstoneEngineering/evothings-examples/tree/development/experiments/mbed-Evothings-CustomGATT).
	* Drag-and-dropping the index.html file into the Evothings Workbench on your computer.
	* Clicking RUN on the workbench.
	* The code will run on your phone's Evothings client.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
For more information about Evothings, see their [Quick Start Guide](http://evothings.com/getting-started-with-evothings-studio-in-90-seconds/), [tutorials](http://evothings.com/doc/studio/tutorials.html) and [BLE API reference](http://evothings.com/doc/plugins/com.evothings.ble/com.evothings.module_ble.html).
</span>

##Intro

Unlike GAP, which operates on broadcasting one-to-many, GATT uses a one-to-one connection between the board and the phone. GATT does not send all the data at connection; it sends only a description of available services, and then - if requested - it will provide details about a service, like the characteristics each service has and the values of these characteristics. All information must be explicitly requested from the server by the client. 

To demonstrate this we will create a service with two characteristics and assign custom UUIDs to both the service and the characteristics. 

##Review of Services

<span style="display:block; float:right;">
![](/InDepth/Images/BLE_Profile_Breakdown.png)
</span>

A GATT server can have multiple services. Each service contains one or more characteristics, each with its own properties such as whether it can be read, written into or send a notification. Each characteristic has a single value of 512 bytes (although it's not mandatory to use them all) and can have zero or more descriptors.

We are going to create a custom GATT service by providing two characteristics, one for reading and one for writing, detailing their properties accordingly, and then putting both into the one service.

##Using the mbed BLE API

To get us started, we'll need to include a couple of headers:

```c

	#include "mbed.h"
	#include "BLEDevice.h"
```

Next, we'll need a few declarations: a BLE object, the LED we'll be toggling, the UUID for our custom service and a UUID for each of our characteristics (READ and WRITE). The UUIDs provide the name of the device that the application will be looking for, and the custom UUID for development. 

```c

	BLEDevice ble;
	DigitalOut led(LED1); 
	uint16_t customServiceUUID  = 0xA000; // service UUID
	uint16_t readCharUUID       = 0xA001; // read characteristic UUID
	uint16_t writeCharUUID      = 0xA002; // write characteristic UUID

	const static char     DEVICE_NAME[]  = "ChangeMe!!"; // change this
	//Custom UUID, FFFF is reserved for development
	static const uint16_t uuid16_list[] = {0xFFFF}; 
	
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** If you change the name here you will also need to change it in the subsequent Evothings application app.js (which will be covered [later]()).
</span>

Now that we have the UUIDs, we can set up the characteristics:

1. We start off by declaring the array variable for the read value ``uint8_t readValue[10]``. 

2. Next, we declare the read only characteristic ``ReadOnlyArrayGattCharacteristic``.

3. We provide the initialiser describing the type of the array and the number of elements in the array ``<uint8_t, sizeof(readValue)>``.  

4. The characteristic will be called ``readChar`` and initialised with the UUID variable for the read characteristic ``readCharUUID``, and the pointer to the array that was just created (``readValue``) . 

5. The same is done for the write characteristic, ``writeValue``.

This is what it looks like:

```c

	// Set Up custom Characteristics
	static uint8_t readValue[10] = {0};
	ReadOnlyArrayGattCharacteristic<uint8_t, 
		sizeof(readValue)> readChar(readCharUUID, readValue);
	
	static uint8_t writeValue[10] = {0};
	WriteOnlyArrayGattCharacteristic<uint8_t, 
		sizeof(writeValue)> writeChar(writeCharUUID, writeValue);
```

Now we can set up the custom service:

1. We initialise a GATT service by filling the characteristics array with references to the read and write characteristics. 

2. Then, we declare the GATT service.

3. The declaration includes the UUID, the characteristics array and the number of characteristics included.

```c


	// Set up custom service
	GattCharacteristic *characteristics[] = {&readChar, &writeChar};
	GattService        	customService(customServiceUUID, 
						characteristics, 
						sizeof(characteristics) / sizeof(GattCharacteristic *));
``` 

We've established the service; we can now create other functions.

First, since GATT is connection-based, we need a disconnection callback function. This functions restarts advertising after a disconnect occurs, so a device can find and reconnect to a lost board. If we don't include this function, we'll have to restart the board to be able to reconnect to it:

```c

	void disconnectionCallback(Gap::Handle_t handle, Gap::DisconnectionReason_t reason)
	{
 	   ble.startAdvertising(); 
	}
```

Next, we need to create the write callback function so it can be called when the BLE board is written to. This callback makes sure the write operation trigger the callback (``params ->charHandle``) is a write operation to the write characteristic (``writeChar.getValueHandle()``). This isn't necessary when you have only one write characteristic, but is absolutely necessary when you have multiple ones on a device. The remainder of the code will print out the data written to the write characteristic:

```c


	/* 
	 *  handle writes to writeCharacteristic
	*/
	void writeCharCallback(const GattCharacteristicWriteCBParams *params)
	{
 	   // check to see what characteristic was written, by handle
  	  if(params->charHandle == writeChar.getValueHandle()) {
   	     // toggle LED if only 1 byte is written
   	     if(params->len == 1) {
    	        led = params->data[0];
     	       (params->data[0] == 0x00) ? printf("\n\rled on ") : 
					printf("\n\rled off "); // print led toggle
    	    }
    	    // print the data if more than 1 byte is written
    	    else {
    	        printf("\n\r Data received: length = %d, data = 0x",params->len); 
    	        for(int x=0; x < params->len; x++) {
    	            printf("%x",params->data[x]);
    	        }
   	     }
   	     // update the readChar with the value of writeChar
   	     ble.updateCharacteristicValue(readChar.getValueHandle(),
										params->data,params->len);
  	  }
	}

```

Now, we start the main loop and initialise the BLE base layer:

```c

	/*
 	*  main loop
	*/ 
	int main(void)
	{
    	/* initialize stuff */
    	printf("\n\r********* Starting Main Loop *********\n\r");
    	ble.init();
```

When that's done, we set up the disconnection callback (to be used if we're disconnected) and the write character callback (to be used when data is written):

```c


    ble.onDisconnection(disconnectionCallback);
    ble.onDataWritten(writeCharCallback);
```

Now we set up the advertising parameters:

1. First, we set the flag saying that this advertising message is BLE only. 

2. You then set the advertising type as connectable and undirected. 

3. The payload can now be given the device name you have chosen and the service's UUID list.

4. Last, we establish the advertising interval, in multiples of 0.625ms (which is the standard interval size).


```c

    /* setup advertising */
	// BLE only, no classic BT
    ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED 
		| GapAdvertisingData::LE_GENERAL_DISCOVERABLE); 
	// advertising type
    ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED); 
    // add name
	ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, 
		(uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME)); 
	// UUID's broadcast in advertising packet
    ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, 
		(uint8_t *)uuid16_list, sizeof(uuid16_list)); 
	// 100ms; in multiples of 0.625ms.
    ble.setAdvertisingInterval(160); 
```

We add our custom service:

```c

	ble.addService(customService);
```

And now that everything is set up, we can start advertising the connection:

```c

 	   // start advertising
    	ble.startAdvertising(); 
   	 
    	// infinite loop waiting for BLE interrupt events
    	while (true) {
     	   ble.waitForEvent(); //Save power
    	}
	}
```

Compile your program and install it on your board (drag and drop it to the board).

##Interacting with the GATT Service - Evothings

The service we created and put on our board is interactive: we can read the LED's status and change it. We do that using a [custom-built app](https://github.com/BlackstoneEngineering/evothings-examples/tree/development/experiments/mbed-Evothings-CustomGATT) designed to work on the Evothings client you installed earlier.

To run the app:

1. Make sure you've installed the Evothings Workbench on your computer and the Evothings client on your phone.

2. 	Drag-and-drop the **index.html** file into the Evothings Workbench on your computer.

3. Click **RUN** on the workbench.

4. The code will run on your phone's Evothings client.

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/Evothings/EvothingsRun.png)
</span>

You need to change the variable ``MyDeviceName`` (in the ``app.js`` file you downloaded from GitHub) to match the device name you gave to your mbed board:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/Evothings/EvothingsChangeName.png)
</span>

You should review the app's code to verify you understand the flow:

1. On start up, the application searches for the device with the name you set earlier. This may take a moment

2. When it finds the devices and connects to it, the message changes from *connecting* to *connected* and the toggle button changes to green.

3. If you click that button, it will change to red and LED1 on the board will light up. 

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/Evothings/EvothingsToggleButton.png)
</span>

<span style="text-align:center; display:block; padding:20px;">
![](/AdvSamples/Images/Evothings/EvothingsLEDOn.png)
</span>

This is the code snippet controlling the toggle function:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/Evothings/EvothingsToggleCode.png)
</span>