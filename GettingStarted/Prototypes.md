#Prototypes and Getting Information From Users

Prototyping is a lot easier (and faster) if you don't have to build an app for user interaction. Not only are apps lots of work, they also aren't compatible with different operating systems (iOS and Android), or even with different versions of the same operating system.

So if you're in the prototyping phase, there are three easier ways to allow user interaction:

1. Hardware inputs directly to the BLE device, for example a [touchscreen](http://developer.mbed.org/components/cat/touchscreen/).

2. Websites that provide a standard user interface and send commands back to the device. They require programming, but they usually work well on all phones.

3. [Evothings Studio](http://evothings.com/getting-started-with-evothings-studio-in-90-seconds/) lets you create simple apps that are run from the Evothings App on your phone, so Evothings does the compatibility work for you. It requires some learning of its own, but it may well be worth your time.

Once your prototype is approved, you can invest some more time in your user input. At this point, apps may become worthwhile. But, if you want to be part of the Physical Web, stick to a website - and use the BLE device just to advertise the site's URL.

<a name="internetaccess">
##How a BLE Device Gets Internet Access
</a>

At the moment, BLE devices don't have independent internet access. To get internet access, you can do one of three things:

1. You can give your board a secondary communication method, like Ethernet or WiFi. This can easily double the price of the board, however. 

2. The BLE device can get internet over its BLE connection to a mobile phone. When the phone terminates the BLE connection, the BLE device will lose its internet access. This doesn't require additional hardware, so it doesn't affect the price of the board, but it does mean that for the device to have constant internet access it will need a phone (or BLE-enabled computer) next to it.

3. In the future, we may find routers that accept BLE connections, in the same way that they currently accept WiFi connections.

______
