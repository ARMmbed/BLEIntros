#What Does it all Do?

The combination of an mbed board, extra components and BLE capabilities give you lots of possibilities for prototyping and production. Let's look at a few of those now (we'll discuss the limitations [later](/InDepth/Limitations/)).

##Gathering Information

Any mbed device, with or without BLE capabilities, can gather information. It can do that with [sensors](http://developer.mbed.org/components/) for anything from [light](http://developer.mbed.org/components/cat/light/) to [touch](http://developer.mbed.org/components/cat/capacitive-touch/), or it can receive information from a computer. 

You could also get information directly from users by providing them some input mechanism, such as a mobile app or button. We'll talk about that later.

##Displaying Information

The first thing you can do with a BLE device is simply display information. You can do that with lights or a [display](http://developer.mbed.org/components/cat/display/), or you can send the information to a nearby Bluetooth-enabled device like a mobile phone.

The information can be sensor input - for example, you could display the speed as provided by an [accelerometer](http://developer.mbed.org/components/cat/sensors-motion/) - or static information that you've programmed onto the device, like your own details. 

##Processing Information 

The two most common sources of information that you might want to process are sensors and user input. In either case, there are two main paradigms for processing:

1. *Local processing* means the device itself processes the data and determines what to do. The simplest example is a thermostat, which knows to turn the heat on or off according to a room temperature input, and doesn't require further instructions from anywhere.

2. *Remote processing* means that you send data to a different device to be handled there, and either wait for instructions from the remote device or simply go on gathering and sending data. For example, if you're trying to predict tomorrow's weather, the device will send data (temperature, barometric pressure etc) to a computer that can analyse it - the local device will simply not have the processing power to run a weather program. 

BLE is intended for low power, battery-operated devices, and so typical applications will never perform complex processing on the device - processing burns through batteries. Applications will instead export the data, and wait for a response. 

##Sending or Storing Information

If you want a small and power-efficient device, you probably don't want to store too much locally; send your information to a server instead (it doesn't have to be a web server; it can be your own computer, if it's set up correctly).

Because of restrictions on energy use in radio operation, BLE is a short-range method, meaning you'll be able to send information over BLE only if your device and your destination are quite close - a range of a few dozen meters tens of meters. If they're further away, you'll need to use Ethernet (regular cable connection), WiFi or radio.

##Working With Apps or Websites

So if you can't store or process too much information with a BLE device, what is it good for?

The simplest way to use BLE is to advertise a small bit of information to any device in the area, without becoming interactive. For example, you could notify every user entering your shop that you'll be open till late this evening. There is no need for any response from the users - it's similar to putting a notice on your door. Users will only need a phone app to see these advertisements as notifications. The key thing is that this app will not need to be specific to your project - the same notification app can work with any BLE device; there are several [generic apps](http://www.nordicsemi.com/eng/Products/nRFready-Demo-APPS) that can do this.

If an advertisement-only solution isn’t enough, you can have a transactional interaction (the fancy way of saying “conversation”) between a client and a device over a BLE connection. This usually requires a custom mobile or web-based app, although some generic apps may be enough to get you off the ground. In addition to handling  the data, the app may provide users with an interface through which they can send commands to the BLE device.  A very common example is mobile fitness apps that get your heart rate information from a BLE-based heart rate monitor. The heart rate monitor doesn't store or process information - it just gets your heart rate and sends it to the app, which displays it and gives you some control of the BLE device.

##URI Beacons and the Physical Web

Physical Web brings devices to the internet via websites (rather than device-specific applications), by using BLE as a business card that includes a link to the website; interactions with the device are performed via the website. Using websites rather than apps means that users don't have to install a new app for every device they want to interact with; the interaction is easier and more immediate.

The method used to provide the link is called [URI Beacon](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_URIBeacon/), and it will be the first example we'll [show you]() when we get to programming our BLE devices. A URI Beacon can be attached to anything that you might want to provide information about, or that you can provide any sort of interface for.

For example, the beacon can be attached to a vending machine that you might then control via the web interface the beacon sent you to. The web interface can let you make a large purchase (providing sodas for several people in one transaction) by letting you select several options and pay for them all at once.

##What's Meshing, and Does it Work?

Meshing means sending information from one BLE device to another, and at the moment there's no easy way of doing it with BLE. 

##What's FOTA, and Does it Work?

FOTA stands for Firmware Over the Air, and is a method of updating the BLE device's programming (reprogramming it) remotely, rather than by physically connecting it to the computer. 

FOTA works (on the Nordic nRF51822 board), but at the moment we recommend that you don't use it unless you know how to make it secure.

##What are pucks?

[Pucks](/InDepth/Pucks/) are small BLE devices that trigger events on your phone, display information or mimic infrared remote controls. For example, you can teach your kids' phones to text you when they enter the house, display the weather on a puck next to the umbrella stand or turn on the AC or the telly when you rotate the puck.