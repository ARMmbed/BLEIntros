#BLE for Designers

BLE is an exciting technology that has a natural appeal for designers who are looking to create art or solve problems. If you're a designer, and you've never programmed anything, we're here to help you get your idea prototyped using BLE on mbed boards.

##BLE

BLE stands for Bluetooth Low Energy (or Bluetooth Smart). It is a short-range wireless communication technology - it is how your car, clothes and home can talk to your phone and each other. The difference between BLE and the classic Bluetooth standard is that BLE is specifically designed to reduce power consumption; your BLE device may run for months or years on a coin-cell battery. 

You've probably met BLE in a fitness tracker or a smart TV, but the beauty of BLE is that it's simply a method of transferring small amounts of data - any data. If you have a sensor, button or any other input method, your BLE device can receive input from them and transfer it to a phone, tablet or PC (and with the advent of BLIP - Bluetooth IP Support - directly to the internet). You can then use it with any application you can think of to store or analyse the information, and even send commands back to the device.

This two-way communication means that a single device can be used both to send information and to perform actions based on that information. You could [water your garden](http://www.hosepipeban.org.uk/hosepipe-ban-current-situation/) when the ground is dry, put a beacon with your details on your dog's collar, or flash a light when a car comes too close to your bicycle. You can do anything, so long as you have the right sensor with an appropriate BLE-enabled platform - like mbed.

##mbed

[mbed](http://developer.mbed.org) gives you three things: a platform, APIs for that platform, and a programming environment (compiler). 

The platforms are little boards with a processor, which have various capabilities like receiving input, generating output and storing small bits of information. Some boards require an external BLE component, and [some](http://developer.mbed.org/platforms/mbed-HRM1017/) [have it](http://developer.mbed.org/platforms/RedBearLab-BLE-Nano/) [built-in](http://developer.mbed.org/platforms/Nordic-nRF51-Dongle/).

Because platforms are standard pieces of hardware, it’s up to you to tell them what to do. mbed has created APIs - Application Program Interface - that let you order off the menu. For example, if you want to send something over Bluetooth, you don't need to know the exact commands and sequence of events; you just need to tell the API that you want to send something - we've made sure the API knows how to do it. This is called *abstraction*, and you'll run into that word quite often on our website. BLE has its own API, called BLE_API.

To tell the API what to do, you need a programming environment. BLE, like all other mbed capabilities, can be programmed using the [mbed Compiler](https://developer.mbed.org/compiler/). 

##The mbed Compiler

The compiler fulfils two main purposes: it gives you a programming environment (a place in which to write your code), and it can turn (compile) that code into something that can be executed on the mbed platforms. The compiler can take the same code and compile it for different mbed platforms, meaning you can try out your project on different boards and pick the one that suits you best, without having to re-write your program. 

Programming for mbed is done in *C++*. Don’t let C++ put you off; you can get quite a lot done with BLE without learning C++ in great detail, as many of its advanced features are not normally required.
We'll walk you through using the compiler as we get started on our [coding samples](#samplesintro).