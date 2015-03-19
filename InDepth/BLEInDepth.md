#BLE Modes and Profiles

This document explores how BLE works, especially how you can use the two BLE modes - connected and advertising - for different purposes. 

##Peripheral and Central Devices v Servers and Clients

When we connect devices over BLE, we think of them as being either a peripheral (slave) device or a central (master) device. The Bluetooth standard established this division to match the resources available on the devices: 

**Master/central**
:	will typically have more computing resources and available energy - a computer or a tablet, for example.

**Slave/peripheral**
:	an mbed device - will be constrained in both computing resources and energy. 

Currently, mbed's BLE_API supports the creation of peripheral devices. We plan to extend this to central devices soon

BLE uses two additional terms to describe the connecting entities - server and client:

**Server**
: 	the device that has information it wishes to share, and in BLE that 	is typically the peripheral (the mbed board).

**Client**
: 	the device that wants information and services, and in BLE that is 	typically the central device - the phone.

The terms *server* and *client* are used when discussing the exchange of information, whereas *central* and *peripheral* are used to denote the origin and target of a BLE connection. It is not uncommon for the central to be connecting as a client, and the peripheral to be acting as a server. 

<span style="text-align:center; display:block;">
![Server and client](/GettingStarted/Images/clientserver.png "The mbed board is the server or peripheral; the phones are the clients and central devices")
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">The mbed board is the server or peripheral; the phones are the clients and central devices</span>


##Initiating Connections

The central initiates and controls the connection, in the sense that the peripheral (the BLE device) cannot force the central to scan for BLE devices, view their information, connect or maintain a connection with them and so on. The central is free to establish or terminate a connection and decides for itself how often to ask the peripheral for information. However, the peripheral can recommend some things to the central, and you'll see [later](connection_parameters) how that's done. It is worth mentioning that these decisions can significantly affect power consumption (and, therefore, battery life).

##Advertising and Connected Mode

The two modes BLE uses are: 

**Advertising mode**
:	the peripheral sends out a bit of information that any device in the area can pick up; this is how central devices know that there are peripherals around. 

**Connected mode**
:	the peripheral and a central device establish a one-to-one conversation. This is how they can exchange complex information. 

A central device must know that a peripheral device exists to be able to connect with it. A peripheral will therefore advertise its presence using the BLE ***advertising mode***. In this mode, the device uses the *Generic Access Profile*, or GAP, to send out a bit of information (an advertisement) at a steady rate. This advertisement is what other devices, like your phone, pick up. It tells them about the presence of a BLE device in the neighbourhood, and whether that device is willing to talk to them.

![Connected and advertising](/InDepth/Images/adv_conn_modes.png)

Advertisements are limited to a maximum of about 31 bytes. For many applications, a peripheral may only want to periodically broadcast a small amount of information that can fit in an advertisement, and as long as it is fine for this data to be available to any central device within range, regardless of authentication, then you don't need to do anything beyond setting up advertisements. But sometimes you'll want to provide more information or more complex interactions than one-way data transfer, and for that you'll need to set up a "conversation" between your BLE device and a user's phone, tablet or computer. The thing that enables this conversation is what's known as ***connected mode***, and it describes a relationship between two devices: the peripheral BLE device and the central device.

For now, advertising and connected modes cannot co-exist; a BLE peripheral device (like a heart rate monitor) can only be connected to one central device at a time (such as your mobile phone). The moment a connection is established, the BLE peripheral will stop advertising, and no other central device will be able to connect to it (since they can't discover that the device is there if it's not advertising). New connections can be established only after the first connection is terminated and the BLE peripheral starts advertising again. Please note that the latest Bluetooth standard allows advertisements to continue in parallel with connections, and this will become a part of mbed's BLE_API before the end of 2015. 

##Services and Profiles (GATT)

In order to make the conversation described above low power, the BLE specification imposes a specific structure on the way data is exchanged in connected mode. A BLE peripheral is able to maintain a database of state variables, such as battery level, temperature and time, that can be accessed by clients. State variables can be grouped into services based on functionality. The Heart Rate Service, for instance, is a collection of state variables including *heart rate measurement* and *body sensor location*. The technical term for these state variables is “Characteristics”. For the sake of interoperability, each characteristic also holds a description of the value’s type. This  allows clients to interpret the value even if they’ve not been specifically programmed to recognise it. 

<span style="text-align:center; display:block;">
![breakdown](/InDepth/Images/Service.png "A single service can contain several characteristics")
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">A single service can contain several characteristics</span>

Services and characteristics (and their supporting attributes) are the fundamental entities that allow arbitrary BLE devices to communicate in connected mode. Services use the Generic Attribute Profile (GATT) to structure the information according to characteristics, and they're bundled together in various profiles. We'll explore characteristics in more detail below. 

*Profile* may sound like a big concept, but it's simply a way of ensuring that services are combined correctly, as sometimes more than one service is needed to get a device working. For example, the Heart Rate *Profile* includes two services: the Heart Rate Service and the Device Information Service. The Blood Pressure Profile similarly includes the Blood Pressure and Device Information services.

<span style="text-align:center; display:block;">
![breakdown](/InDepth/Images/heart_rate_profile.png "An example profile with two services")
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">An example profile with two services</span>

BLE has been around for a while, so it has some standard services that you can tap into. Going back to our heart rate monitor example, the Heart Rate Service is well established and very easy to use; it can read information from a BLE heart rate monitor and send it to an app. You'll see that in a later [coding sample](/GettingStarted/HeartRate/).

Before you start working on a project, it's worthwhile to see if there's already a service that can do what you need done; it'll save you lots of coding and testing. You can find the list of available profiles and services [here](https://developer.bluetooth.org/TechnologyOverview/Pages/Profiles.aspx).

##Characteristics and Interactions

Services break their data down into *characteristics*. Each characteristic is mapped onto a single data point - it tells you one thing, and one thing only. For example, the [Device Information Service](https://developer.bluetooth.org/TechnologyOverview/Pages/DIS.aspx) has the following characteristics:

<span style="display:block; float:right;">
![](/InDepth/Images/DeviceInformationService.png)
</span>

* Manufacturer name.

* Model number.

* Serial number.

* Hardware revision.

* Firmware revision.

* Software revision.

* System ID.

* IEEE 11073-20601 regulatory certification data list.

Each of these characteristics should only contain the information its label says it contains. Together, they reveal the device's manufacturer information and make up a full Device Information Service, which as we saw is itself bundled into quite a few profiles.

Creating a characteristic on mbed requires very little effort, because ``BLE_API`` offers C++ abstractions for entities involved in the definition of services. For example, here we create a simple characteristic that notifies the client of the state of a button (pressed/released):

```c


	bool buttonPressed = false; //button initial state
	ReadOnlyGattCharacteristic<bool> buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressed);//read-only characteristic of type boolean, accepting the buttonState’s UUID and initial value
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
For a full walkthrough of characteristic creation on mbed, see our [input service template](AdvSamples/InputButton/#the-button-state-characteristic).
</span>

A characteristic is fully defined by its declaration, value and descriptor:

1. The **declaration** contains data about the characteristic, such as its universally unique identifier (UUID).

2. The **value** is the “interesting” part of the characteristic, in that it’s the value that contains the data you’re viewing and reacting to.

3. The **descriptor** is not mandatory; you can use it to provide more information about a characteristic or to control its behaviour. For example, descriptors are used when working with notifications.

Characteristics can be either static (like your device's manufacturer name) or dynamic: your device can generate a new value for them as required. For example, in the Heart Rate Service, the current heart rate is a characteristic that gets a new value regularly.

Here's an example of creating a read/write characteristic (a characteristic that can receive new values and reveal its current value):

```c

	bool initialValueForLEDCharacteristic = false;
	ReadWriteGattCharacteristic<bool> ledState(LED_STATE_CHARACTERISTIC_UUID, &initialValueForLEDCharacteristic);
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
For information about creating a read/write characteristic on mbed, see our [actuator service template](AdvSamples/LEDReadWrite/#the-led-state-characteristic).
</span>

Some characteristics are two-way entities: the server (the BLE peripheral) can update them locally, but it can also receive new values for them from the client (the phone/tablet). This two-way traffic is how BLE becomes interactive: the user sends a new value to one or more characteristics and the device responds to these new values. For example, when a URI Beacon device is turned on, it goes into a temporary *configuration mode*, allowing the values of its characteristics (containing the data it will later advertise) to be modified. 

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
For information about the configuration mode, see the [URI Beacon Advanced Features page](AdvSamples/URIBeaconAdv/).
</span>

The service definition specifies which characteristics can be modified; the service states, for each characteristic, whether or not clients have permission to write to that characteristic. This is done when setting up the GATT server on the peripheral. In our example, the *configuration mode* states that the advertising information is read/write, and the *advertising mode* states that it is read-only. The same characteristic can, therefore, have two different permissions, depending on the device's mode. 

##UUIDs

Each service and characteristic require a universally unique identifier (UUID), listed as part of their declaration (as we saw above). For official BLE entities the UUID is 16-bit, and a full list is available on the BLE site for [services](https://developer.bluetooth.org/gatt/services/Pages/ServicesHome.aspx) and [characteristics](https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicsHome.aspx). For services and characteristics that you create yourself, you’ll need a 128-bit UUID; you can generate those on the [UTI website](http://www.itu.int/en/ITU-T/asn1/Pages/UUID/uuids.aspx).

More information about UUID assignments is available in our [service creation samples](link here).
 
##Profiles, Services and Characteristics - a Summary

The full breakdown for a profile is, therefore: one or more services, each containing zero or more characteristic, with zero or more descriptors for every characteristic:

<span style="text-align:center; display:block;">
![breakdown](/InDepth/Images/BLE_Profile_Breakdown.png "A single profile can contains several services, and each of the services can contain several characteristics")
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">A single profile can contains several services, and each of the services can contain several characteristics</span>
