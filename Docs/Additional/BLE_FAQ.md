Read through our documentation and didn't find the answer you were looking for? Try our FAQ.

##Q: How can I make my BLE device interactive?

BLE devices become interactive when you:

* Provide a means of input. This can be local, like a button or a touchpad, or remote, like a mobile app or webpage. 
* Write your program so that it reacts to these inputs.

To learn about prototyping interactivity, see [here](../Introduction/Prototyping.md).

##Q: How is a BLE beacon better than a QR code?

QR codes are passive, meaning users have to decide which ones to scan. The main advantage of BLE beacons is that they're actively broadcasting to anyone in the area. The only decision the users need to make is to look at their BLE scanner, which will show them all beacons in range. As BLE beacons come into greater use, we can expect users to leave their BLE scanners working more often.

If you have BLE on an mbed board, you can also have an onboard interface, such as a screen or lights, to drive engagement.

Another advantage of BLE beacons is that they can be hidden from view, unlike QR codes that need to be prominently displayed in an accessible location.

##Q: Can I display the information locally?

If your hardware supports it (that is, has an external display). If you’re working with local display it’s best to show the raw data, because processing the information before showing it will eat through your device’s battery.

Most platforms include LEDs, which are enough if you’re trying to indicate simple states such as connection status. 

##Q: I have a lot of information to send. What do I do?

BLE is short-range and designed for small bits of information. If you have a lot of information to show the user, it's more efficient to use BLE only to redirect the user to a webpage or application.

If you're trying to send your information to a server you should use Ethernet or WiFi. mbed boards offer support for both.

If you still must send a large stream of data over BLE, you might want to shorten the connection interval and use write-without-response commands instead of a simple write. See [here](../Advanced/HighData.md) for more information.

##Q: I have a lot of information to store. What do I do?

If you want a small and power-efficient device, you probably don't want to store too much locally. Instead, send your information to a server (it doesn't have to be a web server; it can be your own computer, if it's set up correctly). See the question above for information about that.

##Q: Can I use BLE beacons for geolocation?

If you're desperate enough. You can calculate how far away a mobile phone is from a beacon if you know how distance affects the signal strength. But there are a lot of other factors that affect signal strength, and you cannot predict or cancel them out. For example, if there is nothing between the phone and the BLE device, you'll get a stronger signal strength than if anything - including the person holding the phone - comes between them. So using one BLE device for geolocation will not give you accurate results.

You can get a far more accurate result by triangulating the phone's location, but this requires having a lot of BLE devices scattered in the same space, all measuring the signal strength of a single phone. But this is probably not an efficient use of BLE devices. For one thing, it requires a computer to do the actual triangulation, which means the BLE devices will need network access and will cost more. They'll also eat through their batteries. 

##Q: Can I use BLE for location-based interactions?

Yes, if by location you mean "when a phone or other BLE-capable device comes within range of my BLE beacon".

##Q: Can a beacon reveal its location?

A beacon can explicitly reveal its location through its advertisement payload. But you may have more fun playing Marco Polo with the beacon: measure its signal strength, and find it by assuming that the stronger the signal - the closer you are to the source.

##Q: What is BLE's range, and can I extend or limit it?

Bluetooth signals have a limited range, with Class 2 devices limited to about ten meters (33 feet); this can be extended with an antenna. 

Concrete and metal can block signals, so a room's walls may be the signal's border, even if the room is small.

##Q: Is there a version limit for BLE?

The Bluetooth Core Specification Version 4.0 arrived in 2010 and is not supported on older mobile devices or tablets. However, since users replace their devices regularly, and almost all new devices do support BLE, we can expect wide support within a year or two.

##Q: Can the BLE device talk to the internet?

At the moment, BLE devices don't have direct internet access. To get internet access, you can do one of two things:

1. You can give your board a secondary communication method, like Ethernet or WiFi. Do note that this can double the price of the board. 

2. The BLE device can get internet over its BLE connection to a mobile phone. That is: there could be phone apps that act as internet gateways for BLE devices. When the phone terminates the BLE connection, the BLE device will lose its internet access. This doesn't require additional hardware, so it doesn't affect the price of the board, but it does mean that for the device to have constant internet access it will need a phone (or BLE-enabled computer) next to it.

In the future, we may find routers that accept BLE connections, in the same way that they currently accept WiFi connections. This is already a part of the latest BLE standard, and should become available through mbed in the near future.

##Q: What's meshing, and does it work?

Mesh is a network topology in which each node relays data for the network, often using broadcasts. Every node takes part in the distribution of data in the network. This makes the network somewhat independent from the need for centralised routing and more resilient to failures. Meshing is an effective way of sending small amounts of information from one BLE device to another, or from one device to a large array of devices. 

At the moment there's no easy way of doing it with BLE, since it requires enabling the scanning for advertisements in BLE peripherals. The mbed team is working on bringing this feature to BLE_API soon.

##Q: How can I use several BLE devices at once?

As we said, meshing isn't a workable option yet. But BLE devices on their own can all lead to a single place, like a web server. That single place can aggregate all their information for storage, processing or interactivity. From there, you can control each one on its own, or several at once.

##Q: What's FOTA, and does it work?

FOTA stands for Firmware Over the Air, and is a method of updating the BLE device's programming remotely, rather than by physically connecting it to the computer. 

FOTA works (on the Nordic nRF51822 board), but at the moment it doesn’t come with security features to authenticate or verify new firmware. We’ll bring security into mbed FOTA during 2015.

_____

Still have questions? Ask [our community](https://developer.mbed.org/teams/Bluetooth-Low-Energy/community/).

______
Copyright © 2015 ARM Ltd. All rights reserved.
