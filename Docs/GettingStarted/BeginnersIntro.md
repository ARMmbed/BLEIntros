#mbed BLE for Beginners

BLE is an exciting technology that has a natural appeal for beginners who are looking to create art or solve problems. If you're a beginner - meaning you've never programmed anything - we're here to help you get your idea prototyped using BLE on mbed boards.

##BLE

BLE stands for Bluetooth Low Energy (or Bluetooth Smart). It is a short-range wireless communication technology - it is how your car, clothes and home can talk to your phone and each other. The difference between BLE and the classic Bluetooth standard is that BLE is specifically designed to reduce power consumption; your BLE device may run for months or years on a coin-cell battery. 

You've probably met BLE in a fitness tracker or a smart TV, but the beauty of BLE is that it's simply a method of transferring small amounts of data - any data. If you have a sensor, button or any other input method, your BLE device can receive input from them and transfer it to a phone, tablet or PC (and with the advent of BLIP - Bluetooth IP Support - directly to the internet). You can then use it with any application you can think of to store or analyse the information, and even send commands back to the device.

This two-way communication means that a single device can be used both to send information and to perform actions based on that information. You could [water your garden](http://www.hosepipeban.org.uk/hosepipe-ban-current-situation/) when the ground is dry, put a beacon with your details on your dog's collar, or flash a light when a car comes too close to your bicycle. You can do anything, so long as you have the right sensor with an appropriate BLE-enabled platform - like mbed.

<span style="text-align:center; display:block;">
![BLE layout](/GettingStarted/Images/BLEsample.png "A BLE setup requires a board with BLE support and a way to control it - for example a phone app or a local touchscreen")
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">A BLE setup requires a board with BLE support and a way to control it - for example a phone app or a local touchscreen</span>

##mbed

[mbed](http://developer.mbed.org) gives you three things: a platform, APIs for that platform, and a programming environment (compiler). 

The platforms are little boards with a processor, which have various capabilities like receiving input, generating output and storing small bits of information. Some boards require an external [BLE component](http://developer.mbed.org/components/cat/bluetooth/), and [some](http://developer.mbed.org/platforms/mbed-HRM1017/) [have it](http://developer.mbed.org/platforms/RedBearLab-BLE-Nano/) [built-in](http://developer.mbed.org/platforms/Nordic-nRF51-Dongle/).

Because platforms are standard pieces of hardware, it’s up to you to tell them what to do. mbed has created APIs - Application Program Interface - that let you order off the menu. For example, if you want to send something over Bluetooth, you don't need to know the exact commands and sequence of events; you just need to tell the API that you want to send something - we've made sure the API knows how to do it. This is called *abstraction*, and you'll run into that word quite often on our website. BLE has its own API, called BLE_API.

To tell the API what to do, you need a programming environment. BLE, like all other mbed capabilities, can be programmed using the [mbed Compiler](https://developer.mbed.org/compiler/). 

<span style="text-align:center; display:block;">
![BLE layout](/GettingStarted/Images/fullmbedprocess.png "The standard process is to get a board (and maybe a few extending components), write a bit of code and import it to the board. Simple.")
</span>
<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">The standard process is to get a board (and maybe a few extending components), write a bit of code and import it to the board. Simple.</span>

##The mbed Compiler

The compiler fulfils two main purposes: it gives you a programming environment (a place in which to write your code), and it can turn (compile) that code into something that can be executed on the mbed platforms. The compiler can take the same code and compile it for different mbed platforms, meaning you can try out your project on different boards and pick the one that suits you best, without having to re-write your program. 

Programming for mbed is done in *C++*. Don’t let C++ put you off; you can get quite a lot done with BLE without learning C++ in great detail, as many of its advanced features are not normally required.
We'll walk you through using the compiler as we get started on our [coding samples](/GettingStarted/IntroSamples/).

#What Does it all Do?

The combination of an mbed board, extra components and BLE capabilities give you lots of possibilities for prototyping and production. Let's look at a few of those now (we'll discuss the limitations [later](/InDepth/Limitations/)).

##Rapid Prototyping

mbed comes from a heritage of rapid prototyping, and allows you to test code and ideas on BLE devices very easily. 

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
For information about rapid prototyping with mbed BLE, see [here](/InDepth/Prototyping/).
</span>

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

BLE is intended for low power, battery-operated devices, so typical applications will never perform complex processing on the device - processing burns through batteries. Applications will instead export the data, and wait for a response. 

##Sending or Storing Information

If you want a small and power-efficient device, you probably don't want to store too much locally; send your information to a server instead (it doesn't have to be a web server; it can be your own computer, if it's set up correctly).

Because of restrictions on energy use in radio operation, BLE is a short-range method, meaning you'll be able to send information over BLE only if your device and your destination are quite close - a range of a few dozen meters. If they're further away, you'll need to use Ethernet (regular cable connection), WiFi or radio.

##Working With Apps or Websites

So if you can't store or process too much information with a BLE device, what is it good for?

The simplest way to use BLE is to advertise a small bit of information to any device in the area, without becoming interactive. For example, you could notify every user entering your shop that you'll be open till late this evening. There is no need for any response from the users - it's similar to putting a notice on your door. Users will only need a phone app to see these advertisements as notifications. The key thing is that this app will not need to be specific to your project - the same notification app can work with any BLE device; there are several [generic apps](http://www.nordicsemi.com/eng/Products/nRFready-Demo-APPS) that can do this.

If an advertisement-only solution isn’t enough, you can have a transactional interaction (the fancy way of saying “conversation”) between a client and a device over a BLE connection. This usually requires a custom mobile or web-based app, although some generic apps may be enough to get you off the ground. In addition to handling  the data, the app may provide users with an interface through which they can send commands to the BLE device.  A very common example is mobile fitness apps that get your heart rate information from a BLE-based heart rate monitor. The heart rate monitor doesn't store or process information - it just gets your heart rate and sends it to the app, which displays it and gives you some control of the BLE device.

##URI Beacons and the Physical Web

Physical Web brings devices to the internet via websites (rather than device-specific applications), by using BLE as a business card that includes a link to the website; interactions with the device are performed via the website. Using websites rather than apps means that users don't have to install a new app for every device they want to interact with; the interaction is easier and more immediate.

The method used to provide the link is called [URI Beacon](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_URIBeacon/), and it will be the first example we'll [show you]() when we get to programming our BLE devices. A URI Beacon can be attached to anything that you might want to provide information about, or that you can provide any sort of interface for.

For example, the beacon can be attached to a vending machine that you might then control via the web interface the beacon sent you to. The web interface can let you make a large purchase (providing sodas for several people in one transaction) by letting you select several options and pay for them all at once.

##How a BLE Device Gets Internet Access

At the moment, BLE devices don't have independent internet access. To get internet access, you can do one of two things:

1. You can give your board a secondary communication method, like Ethernet or WiFi. This can easily double the price of the board, however. 

2. The BLE device can get internet over its BLE connection to a mobile phone. When the phone terminates the BLE connection, the BLE device will lose its internet access. This doesn't require additional hardware, so it doesn't affect the price of the board, but it does mean that for the device to have constant internet access it will need a phone (or BLE-enabled computer) next to it.

In the future, we may find routers that accept BLE connections, in the same way that they currently accept WiFi connections.
