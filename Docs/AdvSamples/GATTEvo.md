#Custom GATT Service with Evothings

We're going to create a custom [generic attribute profile (GATT) service](/InDepth/BLEInDepth/#services-and-profiles-gatt) to blink the LED on an mbed board, and demonstrate using Evothing to create a custom app that communicates with our GATT service.

<span style="background-color:#E6E6E6; border:1px solid #000;display:block; height:100%; padding:10px">
Get the code [here](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_GATT_Example/).
</span>

##Prerequisites

You'll need:

1. A BLE-enabled mbed board. [Any of these will work](https://developer.mbed.org/platforms/?connectivity=3).

2. A BLE-capable smartphone or tablet.

2. Install the [Evothings Workbench on your PC](http://evothings.com/download/) and the app on your phone. See here for [Android](https://play.google.com/store/apps/details?id=com.evothings.evothingsclient) or [iOS](https://itunes.apple.com/nz/app/evothings-client/id848974292?mt=8).

<span style="background-color:#E6E6E6; border:1px solid #000;display:block; height:100%; padding:10px">
For more information about Evothings, see their [Quick Start Guide](http://evothings.com/getting-started-with-evothings-studio-in-90-seconds/), [tutorials](http://evothings.com/doc/studio/tutorials.html) and [BLE API reference](http://evothings.com/doc/plugins/com.evothings.ble/com.evothings.module_ble.html).
</span>

##Intro

Unlike GAP, which broadcasts one-to-many, GATT uses a one-to-one connection between the board (server) and the phone (client). When the server connects with GATT it doesn't send all the data it has. Instead, it sends only a description of available services. Then, if the client requests details about a service, like the characteristics the service has and their values, GATT sends those details. In other words, all information must be explicitly requested from the server by the client. 

To demonstrate this we will create a service with two characteristics and assign custom UUIDs to both the service and the characteristics. 

<span style="background-color:#E6E6E6; border:1px solid #000;display:block; height:100%; padding:10px">
You can see an example of setting up an input service on our [YouTube channel](https://www.youtube.com/watch?v=YaLG-6pDFrw).
</span>

##Review of Services

<span style="display:block; float:right;">
![](/InDepth/Images/BLE_Profile_Breakdown.png)
</span>

A GATT server can have multiple services. Each service contains one or more characteristics. Each characteristic has its own properties such as whether it can be read, send a notification or be written in to. Each characteristic has a single value of 512 bytes (although it's not mandatory to use them all) and can have zero or more descriptors.

We are going to create a custom GATT service by providing two characteristics: one for reading and one for writing. We'll detail their properties to match read and write abilities, and then put both characteristics into a single service.

##Using the mbed BLE API

To get us started, we'll need to include a couple of headers:

```c

	#include "mbed.h"
	#include "BLEDevice.h"
```

Next, we'll need a few declarations: 

* A BLE object.
* The LED we'll be toggling.
* The UUID for our custom service.
* A UUID for each of our characteristics (READ and WRITE). The UUIDs provide the name of the device that the application will be looking for and the custom UUID for development. 

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

<span style="background-color:#E6E6E6; border:1px solid #000;display:block; height:100%; padding:10px">
**Note:** If you change ``DEVICE_NAME`` here you will also need to change it in the subsequent Evothings application **app.js** (which will be covered [later](/AdvSamples/GATTEvo/#interacting-with-the-gatt-service-evothings)).
</span>

Now that we have the UUIDs, we can set up the characteristics:

1. We start off by declaring the array variable for the read value ``uint8_t readValue[10]``. 

2. Next, we declare the read only characteristic ``ReadOnlyArrayGattCharacteristic``.

3. We provide the initialiser describing the type of the array and the number of elements in the array ``<uint8_t, sizeof(readValue)>``.  

4. The characteristic will be called ``readChar`` and initialised with:
	* The UUID variable for the read characteristic ``readCharUUID``.
	* The pointer to the array that was just created (``readValue``) . 

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

2. We declare the GATT service. The declaration includes the UUID, the characteristics array and the number of characteristics included.

```c
	// Set up custom service
	GattCharacteristic *characteristics[] = {&readChar, &writeChar};
	GattService        	customService(customServiceUUID, 
						characteristics, 
						sizeof(characteristics) / sizeof(GattCharacteristic *));
``` 

We've established the service; we can now create other functions.

First, since GATT is connection-based, we need a disconnection callback function. This functions restarts advertising after a disconnect occurs, so a phone can find and reconnect to a lost board. If we don't include this function, we'll have to restart the board to be able to reconnect to it:

```c
	void disconnectionCallback(Gap::Handle_t handle, Gap::DisconnectionReason_t reason)
	{
 	   ble.startAdvertising(); 
	}
```

Next, we need to create the write callback function so it can be called when the BLE board is written to. This callback makes sure the write operation triggering the callback (``params ->charHandle``) is a write operation to the correct write characteristic (``writeChar.getValueHandle()``). This isn't necessary when you have only one write characteristic, but is absolutely necessary when you have multiple ones on a device. The remainder of the code will print out the data written to the write characteristic:

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

2. We then set the advertising type as connectable and undirected. 

3. The payload can now be given the device name we've chosen and the service's UUID list.

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
    ble.accumulateAdvertisingPayload(GapAdvertisingData::
		COMPLETE_LIST_16BIT_SERVICE_IDS, 
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

Compile your program and [install it on your board](/GettingStarted/URIBeacon/#compiling-and-installing-your-program) (drag and drop it to the board).

##Interacting with the GATT Service - Evothings

The service we created and put on our board is interactive: we can read the LED's status and change it. We do that using the "mbed Evothings GATT" example code. This example comes pre-packaged with the Evothings Workbench.

To run the app:

1. Make sure you've installed the Evothings Workbench on your computer and the Evothings client on your phone.

2. Download [the application](https://github.com/BlackstoneEngineering/evothings-examples/tree/development/experiments/mbed-Evothings-CustomGATT).

2. Connect the workbench on your computer to the client on your smartphone (it will ask for your computer's IP address).

3. Click **RUN** on the "mbed Evothings GATT" program on the workbench.

4. The code will run on your phone's Evothings client.

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/Evothings/EvothingsRun.png)
</span>

You need to change the variable ``MyDeviceName`` (in the ``app.js`` file you downloaded from GitHub) to match the [device name you gave to your mbed board](/AdvSamples/GATTEvo/#using-the-mbed-ble-api):

```javascript
// JavaScript code for the mbed ble scan app

// Short name for EasyBLE library.
var easyble = evothings.easyble;

// Name of device to connect to, 
// Change this name in the mbed code and the evothings code to match.
var MyDeviceName = "ChangeMe!!" 
```

You should review the app's code to verify you understand the flow:

1. On start up, the application searches for the device with the name you set earlier. This may take a moment.

2. When it finds the device and connects to it, the message changes from *connecting* to *connected* and the toggle button changes to green.

3. If you click that button, it will change to red and LED1 on the board will light up. See the .gif below for an example of the LED blinking when the toggle button is pressed.

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/Evothings/EvothingsToggleButton.png)
</span>

<span style="text-align:center; display:block; padding:20px;">
![](/AdvSamples/Images/Evothings/EvothingsLEDOn.png)
</span>

This is the Evothings code snippet that is run on the smartphone to  control the toggle function:

```javascript
app.toggle = function()
{    
    // console.log(GDevice.__services[2].__characteristics[0]['uuid'])
    GDevice.readCharacteristic( 
        "0000a001-0000-1000-8000-00805f9b34fb",
        function(win){
            var view = new Uint8Array(win)
            var led = new Uint8Array(1)
            if(view[0] == ledON){
                $('#toggle').removeClass('green')
                $('#toggle').addClass('red')
                led[0] = ledOFF;
            }
            else if (view[0] == ledOFF){
                $('#toggle').removeClass('red')
                $('#toggle').addClass('green')
                led[0] = ledON;
            }
            GDevice.writeCharacteristic(
                '0000a002-0000-1000-8000-00805f9b34fb',
                led,
                function(win){console.log("led toggled successfully!")},
                function(fail){console.log("led toggle failed: "+fail)})
            
        },
        function(fail){
            console.log("read char fail: "+fail);
            }
        );
}
```

______
Copyright © 2015 ARM Ltd. All rights reserved.