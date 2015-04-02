#Connection Parameters

There are several parameters that affect the connection between the central and peripheral devices. These in turn affect the device's power consumption - the more radio activity on the device, the greater the consumption. 

##setAdvertisingInterval()

When the peripheral device is in advertising mode it sends advertising packets at a fixed interval as short as 20 milliseconds or as long as 10.28 seconds. A short interval allows the central device to find the peripheral quickly, but because it requires frequent radio work the power consumption is higher. 

The interval is set using ``setAdvertisingInterval``: a function in the BLE_API's ``BLEDevice`` class that accepts a value in milliseconds. The advertising interval is completely under the peripheral device's control (as opposed to the other connection parameters, as you'll see below, which are suggestions that the central device can ignore).

```c

	 ble.setAdvertisingInterval(1000); // one second
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:**
<br />1. If you set 0, advertising will be disabled.
<br />2. It should be set to 0 (that is, disabled) when the connection mode is ``ADV_CONNECTABLE_DIRECTED`` (meaning that only connections from a pre-defined central device will be accepted).
<br />3. If you set a value lower than the minimum (20), the minimum will be used automatically.
</span>

##Connection Interval and Slave Latency

When a connection between the peripheral and central devices is established (connected mode), the central decides how often to synchronise with the peripheral. This decision is one sided: the peripheral cannot force anything on the central, but it can make suggestions that the central may choose to honour. The suggestions are made using three parameters: ``MIN_CONN_INTERVAL`` (for the shortest interval) and ``MAX_CONN_INTERVAL`` (for the longest interval), which together describe the interval range; and SLAVE_LATENCY, which defines the number of times a peripheral can ignore a connection event.

###Connection Intervals

The interval parameters  receive values in milliseconds. For example, the following code means that the shortest interval time is 250 milliseconds, and the longest is 350 millisecond:

```c

	#define MIN_CONN_INTERVAL 250 //250 milliseconds
	#define MAX_CONN_INTERVAL 350 //350 milliseconds
```

The connection interval cannot be shorter than 7.5 milliseconds or longer than four seconds. The central will pick a value between the min and max suggested by the peripheral, or enforce its own value. It's important to understand that while the peripheral can suggest a range (two values), in the end only one value can be used. The synchronisation itself must always happen at a fixed interval, not a random point on a range. The two parameters are used only when the peripheral is suggesting a range to the central; when the central picks a value, it's stored in a new variable and the connection refers only to that variable.

Connection interval is a misleading name; it is not the case that a new connection is re-attempted at each connection event. Rather, within the context of an ongoing connection, a connection event allows the two sides to synchronize with one another and send and receive basic communication. Specifically, the server (BLE device) has the opportunity to send notifications to the client if there is any new state-change to report. 

###Slave Latency

Ideally, when a BLE device (particularly a peripheral) is inactive, it would like to sleep - not process information or respond to connection events - to save its battery. The client, which is often less energy constrained on account of being a rechargeable phone or a tablet, may want to synchronize with the peripheral frequently to stay up to date. In this situation, where a peripheral answers every connection event from the client despite having no new information, it will be forced to expend a lot more energy than necessary. 

One way this situation is mitigated is by the central allowing a peripheral to ignore a specified number of consecutive connection events while it has no new data to send. This means that the peripheral can continue sleeping, despite the client's attempt to synchronize - though it must still respond to the client periodically in order to prove that the connection is still alive.

The number of connection events that the peripheral can ignore is specified in a parameter called ``SLAVE_LATENCY``. This parameter (much like the interval parameters) is set by the central device, but the peripheral can make a suggestion based on what the peripheral knows about its own operations.

The slave latency parameter accepts an integer specifying the number of connection events that may be ignored. For example, the following code means that the device can ignore four consecutive connection events, but must then respond to the fifth:

```c

	#define SLAVE_LATENCY 4 // four events can be ignored, the fifth must be met
```

The difference between SLAVE_LATENCY and MIN_CONN_INTERVAL is that  MIN_CONN_INTERVAL is used even when there is new data to send, while SLAVE_LATENCY is used only when the peripheral device has no data. In other words, MIN_CONN_INTERVAL is state-independent. The combination of these parameters allows us conditional control of our radio usage: we’ll communicate very rapidly when there is new information, but very rarely when there is no information. A good example is a BLE mouse: we don’t want to use the radio too much when the user isn’t moving the mouse, but we don’t want slow communication when the user is using it, because that makes its use harder (it lags behind the user’s actions); we’ll therefore set a high latency but low minimum connection interval.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** the maximum value of SLAVE_LATENCY depends on the stack you're using. Check your vendor's specifications.</span>

##Putting it Together

Here's a diagram describing an interaction between a peripheral and a central. Note that in this case, we've named the variable holding the connection interval ``connectionInterval``, but this is not a universal name:

<span style="text-align:center; display:block;">
![](/InDepth/Images/Connection_parameters.png)
</span>

##Connection Supervision Timeout

Sometimes, devices move out of each other's transmission range, or lose the connection for some other reason. The devices don't know if the connection was lost, but they can assume it was if enough time has gone by without receiving any information from the other side. This is called timeout. The Connection Supervision Timeout parameter defines the time to wait for a data transfer before assuming that the connection was lost.

In our samples, this parameter is called CONN_SUP_TIMEOUT, and receives a value in milliseconds. For example, the following code means that the timeout is six seconds:

```c

	#define CONN_SUP_TIMEOUT 6000 // six seconds
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">**Note:** The connection supervision timeout is a suggestion that the central device is free to ignore. This means that we can’t rely on our own value too much, which in turn limits our usage of the other parameters: if we use them to create a long gap between data transfers, and the central accepts these parameters but then rejects our supervision timeout, it might set a shorter timeout and assume we disconnected.
<br />
**Note:** the maximum value of CONN_SUP_TIMEOUT depends on the stack you're using. Check your vendor's specifications.
</span>

##Maximising Battery Life

The central device can ignore the peripheral’s suggestions for connection parameters, but since these parameters have an impact on energy consumption we, as application developers programming the peripheral, should always put some thought into them and hope that the central honours our suggestions. For example, if our temperature sensor takes a reading every second, the connection interval shouldn't be much smaller than that, as it will not get new information on most requests; we should offer a connection interval that matches the rate at which we expect to generate new data. For applications where data updates occur non-periodically (such as mouse movements), the connection interval may determine the delay experienced by a client in receiving the updates; we'll use shorter connection intervals when user experience is worth more than energy. We could complement the short connection interval in this case with a high slave latency so that the mouse peripheral can keep sleeping for longer when there is no motion.

In terms of battery life - the less we use the radio, the better. All of our parameters together mean that we can use the radio quite infrequently:

1. In *advertising* mode, we can use the radio once every 10.28 seconds.

2. In *connected* mode, we can set a max connection interval of four seconds, but while we're not generating new data the longest duration without radio activity could be as long as [(max interval) * (slave latency)]. However, do remember that we're limited by the supervision timeout; if our intervals are too large, the central device may assume a disconnect (remember that we cannot force the central device to accept our setting of supervision timeout, so there may be a mismatch).


