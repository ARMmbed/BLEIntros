#Custom GAP Advertising Packet

The GAP advertising packet is modifiable, allowing us to send information to any BLE scanner without waiting for it to establish a connection. 

##GAP Data Review

The general GAP connection's data breakdown is illustrated in this diagram:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/GAP/GeneralStruct.png)
</span>

Every package sent by BLE contains 47 bytes (which isn't much), but:

1. Right off the bat, the BLE stack require 8 for its own purposes.

1. The advertising data therefore has 39 bytes. But the BLE stack once again requires some overhead, taking up 8 bytes.

2. Our advertisement data has 31 bytes left, divided into advertising data (AD) structures. Then:

	* The advertisement data must contain flags that tell the device about the type of advertisement we're sending, and those take up three bytes in total (one for data length, one for data type and one for the data itself). The reason we use up these two bytes - the data length and type indications - is to help the parser work correctly with our information. We're done to 28 bytes.

	* Now we're finally sending our data - but it, too, requires an indication of length and type (two bytes in total), so we're done to 26 bytes.

All of which means that we have only 26B to use for the data we want to send over GAP.

And here's what the bottom two layers of structure look like for our particular example - sending manufacturer data:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/GAP/ExampleStruct.png)
</span>





