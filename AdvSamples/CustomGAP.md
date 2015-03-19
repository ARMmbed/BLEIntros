#Custom GAP Advertising Packet

The GAP advertising packet is modifiable, allowing us to send information to any BLE scanner without waiting for it to establish a connection. We're going to modify advertising data step by step, then use a custom-built Evothings app to view it.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
Get the code [here](http://developer.mbed.org/users/mbedAustin/code/BLE_EvothingsExample_GAP/).
</span>
##Prerequisites

You'll need:

1. A BLE-enabled mbed board.

2. Install the [Evothings Workbench for your PC and the Evothings app for your phone](http://evothings.com/download/).

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




