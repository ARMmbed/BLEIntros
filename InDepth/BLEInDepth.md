#BLE Modes and Profiles

This document explores how BLE works, especially how you can use connected and advertising mode for different purposes. 

##Peripheral and Central Devices v Servers and Clients

When we connect devices over BLE, we think of them as being either a peripheral (slave) device or a central (master) device. The Bluetooth standard established this division to match the resources available on the devices: the master will typically have more computing resources and available energy - a computer or a tablet, for example - while the slave - an mbed device - will be constrained in both respects. 

Currently, mbed's BLE_API supports the creation of peripheral devices. We plan to extend this to central devices soon

BLE uses two additional terms to describe the connecting entities - server and client:

**Server**
: 	the device that has information it wishes to share, and in BLE that 	is typically the peripheral (the mbed board).

**Client**
: 	the device that wants information and services, and in BLE that is 	typically the central device - the phone.

The terms *server* and *client* are used when discussing the exchange of information, whereas *central* and *peripheral* are used to denote the origin and target of a BLE connection. It is not uncommon for the central to be connecting as a client, and the peripheral to be acting as a server. 

![Server and client](/GettingStarted/Images/clientserver.png)

##Initiating Connections

The central initiates and controls the connection, in the sense that the peripheral (the BLE device) cannot force the central to scan for BLE devices, view their information, connect or maintain a connection with them and so on. The central is free to establish or terminate a connection and decides for itself how often to ask the peripheral for information. However, the peripheral can recommend some things to the central, and you'll see [later](connection_parameters) how that's done.

##Advertising and Connected Mode

When you set up a BLE device, the first thing it does it advertise its presence (using the Generic Access Profile method, or GAP) - send out a bit of information at a steady rate. This is called *advertisement mode*. The advertisement is what other devices, like your phone, pick up. It tells them about the presence of a BLE device in the neighbourhood, and whether that device is willing to talk to them.

Advertisements are limited to a maximum of about 31 bytes. For many applications, a peripheral may only want to periodically broadcast a small amount of information that can fit in an advertisement, and as long as this data can be shared insecurely you don't need to do anything beyond setting up advertisements. But sometimes you'll want to provide more information or a service, and for that you'll need to set up a "conversation" between your BLE device and a user's phone. This conversation is what's known as *connected mode*, and it describes a relationship between two devices: the peripheral BLE device and the central device.

For now, advertising and connected modes cannot co-exist; a BLE peripheral device (like a heart rate monitor) can only be connected to one central device (such as your mobile phone). The moment a connection is established, the BLE peripheral will stop advertising, and no other central device will be able to connect to it (since they can't discover that the device is there if it's not advertising). New connections can be established only after the original connection is terminated and the BLE peripheral starts advertising again. Please note that the latest Bluetooth standard allows advertisements to continue in parallel with connections, and this will become a part of mbed BLE_API before the end of 2015. 

![Connected and advertising](/GettingStarted/Images/adv_conn_modes.png)

##Services and Profiles (GATT)

In addition to being able to broadcast small amounts of data in advertisements, a BLE peripheral is able to maintain a database of state variables, such as battery level, temperature and time, that can be accessed by clients. State variables can be grouped into services based on functionality. The Heart Rate Service, for instance, is a collection of state variables including *heart rate measurement and *body sensor location*.. The technical term for these state variables is “Characteristics”. For the sake of interoperability, each characteristic also holds a description of the value’s type. This  allows clients to interpret the value even if they’ve not been specifically programmed to recognize it. 

Services and characteristics (and their supporting attributes) are the fundamental entities that allow arbitrary BLE devices to communicate in connected mode. Services use the Generic Attribute Profile (GATT) to structure the information according to characteristics, and they're bundled together in various profiles. We'll explore characteristics in more detail below. 

*Profile* may sound like a big concept, but it's simply a way of ensuring that services are combined correctly, as sometimes more than one service is needed to get a device working. For example, the Heart Rate *Profile* includes two services: the Heart Rate Service and the Device Information Service. The Blood Pressure Profile similarly includes the Blood Pressure and Device Information services.

BLE has been around for a while, so it has some standard services that you can tap into. Going back to our heart rate monitor example, the Heart Rate Service is well established and very easy to use; it can read information from a BLE heart rate monitor and send it to an app. You'll see that in a later [coding sample](/GettingStarted/HeartRate/).

Before you start working on a project, it's worthwhile to see if there's already a service that can do what you need done; it'll save you lots of coding and testing. You can find the list of available profiles and services [here](https://developer.bluetooth.org/TechnologyOverview/Pages/Profiles.aspx).

##Characteristics and Interactions

Services break their data down into *characteristics*. Each characteristic is mapped onto a single data point - it tells you one thing, and one thing only. For example, the [Device Information Service](https://developer.bluetooth.org/TechnologyOverview/Pages/DIS.aspx) has the following characteristics:

* Manufacturer name.

* Model number.

* Serial number.

* Hardware revision.

* Firmware revision.

* Software revision.

* System ID.

* IEEE 11073-20601 regulatory certification data list.

Each of these characteristics should only contain the information its label says it contains. Together, they reveal the device's manufacturer information and make up a full Device Information Service, which as we saw is itself bundled into quite a few profiles.

A characteristic is fully defined by its declaration, value and descriptor:

1. The **declaration** contains data about the characteristic, such as its universally unique identifier (UUID).

2. The **value** is the “interesting” part of the characteristic, in that it’s the value that contains the data you’re viewing and reacting to.

3. The **descriptor** is not mandatory; you can use it to provide more information about a characteristic or to control its behaviour. For example, descriptors are used when working with notifications.

Characteristics can be either static (like your device's manufacturer name) or dynamic: your device can generate a new value for them as required. For example, in the Heart Rate Service, the current heart rate is a characteristic that gets a new value regularly.

Some characteristics are two-way entities: the server (the BLE peripheral) can update them locally, but it can also receive new values for them from the client (the phone/tablet). This two-way traffic is how BLE becomes interactive: the user sends a new value to one or more characteristics and the device responds to these new values. For example, in the Heart Rate Service, the *Heart Rate Control Point* characteristic allow the client to write to it; changing the value of the characteristic tells the device to restart the Energy Expended measurement.

It is up to the service to decide which characteristics can be modified; the service states, for each characteristic, whether or not clients have permission to write to that characteristic. This is done when setting up the GATT server on the peripheral. In our example, the service has stated that the client has permission to write to the Heart Rate Control Point characteristic. If it revoked the permission, the client would not be able to reset the Energy Expended measurement, because the Heart Rate Control Point would never accept a new value.

##UUIDs

Each service and characteris requires a universally unique identifier (UUID). For official BLE entities the UUID is 16-bit, and a full list is available on the BLE site for [services](https://developer.bluetooth.org/gatt/services/Pages/ServicesHome.aspx) and [characteristics](https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicsHome.aspx). For services and characteristics that you create yourself, you’ll need a 128-bit UUID; you can generate those on the [UTI website](http://www.itu.int/en/ITU-T/asn1/Pages/UUID/uuids.aspx).

More information about UUID assignments is available in our [service creation samples](link here).
 
##Profiles, Services and Characteristics - a Summary

The full breakdown for a profile is, therefore: one or more services, each containing zero or more characteristic, with zero or more descriptors for every characteristic:

![breakdown](/InDepth/Images/BLE_Profile_Breakdown.png)