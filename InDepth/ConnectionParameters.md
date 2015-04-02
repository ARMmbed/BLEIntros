#Connection Parameters

There are several parameters that affect the connection between the central and peripheral devices. These in turn affect the device's power consumption - the more radio activity on the device, the greater the consumption. 

###setAdvertisingInterval()

When the peripheral device is in advertising mode it sends advertising packets at a fixed interval as short as 20 milliseconds or as long as 10.28 seconds. A short interval allows the central device to find the peripheral quickly, but because it requires frequent radio work the power consumption is quite high. 

The interval is set using ``setAdvertisingInterval``: a function in the BLE_API's ``BLEDevice`` class that accepts a value in milliseconds. Note that if you set 0, advertising will be disabled, and if you set a value lower than the minimum (20), the minimum will be used automatically.

	 ble.setAdvertisingInterval(1000); // one second

The advertising interval should be set to 0 (that is, disabled) when the connection mode is ADV_CONNECTABLE_DIRECTED (meaning that only connections from a pre-defined central device will be accepted).

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Tip:** The advertising interval is completely under the peripheral device's control, as opposed to the other connection parameters, as you'll see below, which are a suggestion that the central device can ignore.
</span>

###Connection Interval

The connection interval suggests to the central device how often to check whether the connection to the peripheral is alive, and whether there is any new data. Note that the central device can reject the suggestion and set its own interval; the peripheral cannot enforce the suggestion, because that might overload the central device's communication infrastructure.

The connection interval has two parameters: *MIN_CONN_INTERVAL* (for the shortest interval) and *MAX_CONN_INTERVAL* (for the longest interval). The two together define the range of intervals. Note that the value they receive is in milliseconds. For example, the following code means that the shortest interval time is 250 milliseconds, and the longest is 350 millisecond:

```c

	#define MIN_CONN_INTERVAL 250
	#define MAX_CONN_INTERVAL 350
```

The connection interval cannot be shorter than 7.5 milliseconds or longer than four seconds.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** the central device can choose to ignore the values of MIN_CONN_INTERVAL and MAX_CONN_INTERVAL. </span>


###Connection Supervision Timeout

Sometimes, devices move out of each other's transmission range, or lose the connection for some other reason. The devices don't know if the connection was lost, but they can assume it was if enough time has gone by without receiving any information from the other side. This is called timeout. The Connection Supervision Timeout parameter defines the time to wait for a data transfer before assuming that the connection was lost.

In our samples, this parameter is called CONN_SUP_TIMEOUT, and receives a value in milliseconds. For example, the following code means that the timeout is six seconds:

```c

	#define CONN_SUP_TIMEOUT 6000
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** the maximum value of CONN_SUP_TIMEOUT depends on the stack you're using. Check your vendor's specifications.
<br />**Note:** the central device can choose to ignore the value of CONN_SUP_TIMEOUT </span>

###Slave Latency

We said earlier that the client (the phone) asks the server (the BLE device) for information. But, sometimes the client may ask the server for new information when the server doesn't have any new information to send. For example, the client may ask for a new temperature reading, but the temperature sensor may not have provided any new readings for the BLE device to send, or the reading may not have changed in a while.

Ideally, when a BLE device (particularly a peripheral) is inactive, it would like to sleep - not process information or respond to connection events - to save its battery. The client, which is often less energy constrained on account of being a phone or a tablet, may want to connect to the peripheral frequently to keep latency low. If a peripheral answers every connection event from the client, it will be forced to expend a lot more energy than necessary. 

A peripheral may therefore choose to ignore a specified number of consecutive connection requests while it has no new data to send. This means that the device can continue sleeping, despite the client's attempt to ask for information - though it must still respond to the client periodically in order to prove that the connection is still alive.

The number of requests to ignore is specified in a parameter called SLAVE_LATENCY. For example, the following code means that the device can ignore four consecutive connection events, but must then respond to the fifth:

```c

	#define SLAVE_LATENCY 4
```

The difference between SLAVE_LATENCY and MIN_CONN_INTERVAL is that  MIN_CONN_INTERVAL is used even when there is new data to send, while SLAVE_LATENCY is used only when the BLE device has no data.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** the maximum value of SLAVE_LATENCY depends on the stack you're using. Check your vendor's specifications.<br />
**Note:** the central device can choose to ignore the value of SLAVE_LATENCY.</span>

##Maximising Battery Life

Although the central device can ignore the peripheral’s suggestions for connection parameters, these parameters have an impact on energy consumption and we, as application developers programming the peripheral, should always put some thought into them. For example, if our temperature sensor takes a reading every second, the connection interval shouldn't be much smaller than that, as it will not get new information on most requests; we should offer a connection interval that matches the rate at which we expect to generate new data. For applications where data updates occur non-periodically (such as mouse movements), the connection interval may determine the delay experienced by a client in receiving the updates; we'll use shorter connection intervals when latency is worth more than energy.

In terms of battery life - the less we use the radio, the better. All of our parameters together mean that we can use the radio quite infrequently:

1. In *advertising* mode, we can use the radio once every 10.28 seconds.

2. In *connected* mode, we can set a max interval of four seconds, but while we're not generating new data we can have an interval that is [(max interval) * (slave latency)]. However, do note that we're limited by the supervision timeout; if our intervals are too great, the central device will assume a disconnect (remember that we cannot force the central device to accept our setting of supervision timeout, so there may be a mismatch).

