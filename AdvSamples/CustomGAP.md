#Custom GAP Advertising Packet

The GAP advertising packet is modifiable, allowing us to send information to any BLE scanner without waiting for it to establish a connection. 

##GAP Data Review

The general GAP connection's data is illustrated in this diagram:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/GAP/GeneralStruct.png)
</span>

And here's what the bottom two layers of structure look like for our particular example - sending manufacturer data:

<span style="text-align:center; display:block;">
![](/AdvSamples/Images/GAP/ExampleStruct.png)
</span>





