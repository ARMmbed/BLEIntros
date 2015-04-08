#High Data Rate, Low Latency Transfers

As mentioned in the [previous sections](/GettingStarted/DesignersIntro/), BLE is primarily designed for low data rate applications where only a few bytes are transmitted every second. However, you may find yourself in need of transferring a large amount of data, so in this section we'll show you how to build a high data rate, low latency application using mbed’s ``BLE_API`` while still keeping a low power profile.

For low data rate applications, the typical way to interact with characteristics is through the read, write, and indication commands that send a packet of data and subsequently wait for a response. But waiting for a response can add significantly to the latency and increase the delay before sending the next packet, increasing the overall transmission time when sending large amounts of data, so it’s less suitable for low latency applications, or applications that need to exchange a large amount of data as quickly as possible. Worse, the central might decide to terminate the current connection after each read and write command, exacerbating the problem by delaying the next operation to the following connection.

There are two orthogonal approaches to overcome these limitations: [transfer quickly](#fast) - decreasing the time between packets - or [transfer often](#often) - reducing the interval between connection events.

<a name="fast">
##Transfer Quickly
</a>

To decrease the time between successive packets, the BLE standard defines a command and message pair for sending and receiving data between a client and server - without waiting for a response after each message:

1. The **_Write Without Response_** command for sending data from the [client to the server](#write).

2. The **_Handle Value Notification_** message for sending data from the [server to the client](#handle).

<a name="write">
###Client to Server
</a>

For sending data from the client to the server, the _Write Without Response_ property must be enabled in the write characteristic. Using ``BLE_API``, this is done by setting the ``GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY`` property in the property field when instantiating a new ``GattCharacteristic``:

```c
    
	GattCharacteristic writeTo(uuid, valuePtr, initialLen, maxLen,
		GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_WRITE |
		GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_WRITE_WITHOUT_RESPONSE);

```

Where ``uuid`` is the UUID for the write characteristic; ``valuePtr`` and ``initialLen`` hold the initial value for the characteristic and will be copied into the BLE stack; and ``maxLen`` is the maximum size of the attribute. Note that some clients require the ``GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_WRITE`` to be set as well.

Any connected client can now send data with minimal overhead by issuing a _Write Without Response_ to this characteristic. 

<a name="handle">
###Server to Client
</a>

Sending data in the opposite direction, from the server to the client, is slightly different because servers are not supposed to "write" to clients. However, this behaviour can be emulated by repurposing _Handle Value Notifications_.

Usually, _Handle Value Notifications/Indications_ are used by the server to send updated values to a subscribed client or for signalling a client that a subscribed read attribute has been updated. Because _Handle Value Notifications_ can carry the same payload as any other BLE message, is sent at the server’s discretion, and doesn't generate a response from the client, _Handle Value Notifications_ can be repurposed for transmitting low latency data from server to client. 

Using ``BLE_API``, the first step is to set up a read characteristic with the ``GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY`` property enabled:

```c

	GattCharacteristic readFrom(uuid, valuePtr, initialLen, maxLen,
		GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_READ |
		GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY);

```

Where ``uuid``, ``valuePtr``, ``initialLen``, and ``maxLen`` are the same as above. The ``GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_READ`` property is mandatory, since only read characteristics can have value updates.

The second step is to register a callback function to the ``BLEDevice::onDataSent`` method. This method is called whenever the BLE radio has transmitted some data and is ready to transmit again. The callback function is responsible for setting up the data to be transmitted next. This loop will keep the radio busy as long as there is data to be sent. 

The third step is for the client to subscribe to the read characteristic and be ready to receive _Handle Value Notifications_. 

The server can now send a stream of low latency messages to the client by calling the ``BLEDevice::updateCharacteristicValue`` method. If the return value is ``BLE_ERROR_NONE``, the message will be sent without interruption. If the value is not ``BLE_ERROR_NONE``, this indicates that the last call did not succeed (because the buffer is full) and the message will have to be sent again. By calling ``BLEDevice::updateCharacteristicValue`` repeatedly we take advantage of all the available transmit buffers in the radio, and by keeping the radio busy as much as possible we can reduce the inter-packet latency. This is illustrated in the code below:

```c

	BLEDevice ble;

	...

	void onDataSent(unsigned count)
	{
		sendData();
	}

	void sendData()
	{
		ble_error_t didSendValue = BLE_ERROR_NONE;

		while (didSendValue == BLE_ERROR_NONE)
		{
			uint8_t* payload;
			uint16_t payloadSize;

			// Update payload pointer and payload size or break loop
			...

			didSendValue = ble.updateCharacteristicValue(readFrom,payload,payloadSize);
		}

		if (didSendValue != BLE_ERROR_NONE)
		// Last message was not sent. Undo update above.
	}
```

The function ``sendData`` is responsible for keeping track of what data to send and has to be called first to initiate the transfer. Once one or more messages have been sent, the callback function ``onDataSent`` will call ``sendData`` again, thereby ensuring the BLE stack is kept busy as long as there is data to send.

<a name="often">
##Transfer Often
</a>

Another way to reduce latency is to increase the number of potential connections by updating the minimum and maximum connection interval. Note that connections are established completely at the central’s discretion and any connection preferences or connection requests issued by the peripheral are only optional and can be ignored by the central. 

Nevertheless, successfully setting a small connection interval can have a significant impact on the latency. However, care should be taken to ensure that the low power profile is maintained by dynamically switching connection parameters based on the latency requirements.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Tip**: more information about the connection parameters is available [here](/InDepth/ConnectionParameters/).
</span>

The following code example shows how ``BLE_API`` can be used for updating the connection parameters:

```c

	BLEDevice ble;
	Gap::ConnectionParams_t fast;

	...

	void whenConnected(Gap::Handle_t handle, 
							Gap::addr_type_t peerAddrType, 
							const Gap::address_t peerAddr, 
							const Gap::ConnectionParams_t *params)
	{
		// Option 1:
		// update parameters after a connection has been made
		ble.updateConnectionParams(handle, &fast);
	}

	...

	int main()
	{
		...

		// Option 1:
		// set callback for updating connection parameters when connected
		ble.onConnection(whenConnected);

		// Option 2:
		// Set preferred connection parameters before connection is established
		ble.getPreferredConnectionParams(&fast);
		fast.minConnectionInterval = 16; // 20 ms
		fast.maxConnectionInterval = 32; // 40 ms
		fast.slaveLatency = 0;
		ble.setPreferredConnectionParams(&fast);

		...
	}
```

Where ``minConnectionInterval`` and ``maxConnectionInterval`` suggest to the central how often connections should be attempted and ``slaveLatency`` suggests how many of these connection attempts the slave is allowed to miss before the central may consider the peripheral disconnected. 


