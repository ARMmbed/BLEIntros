#BLE for Developers

This document is written for experienced BLE developers who are switching to mbed platforms. If you feel that you need more information than this document provides, please refer to our [extended documentation](/GettingStarted/DesignersIntro/).

##BLE on mbed

[mbed](http://developer.mbed.org) gives you three things: a well defined hardware platform, APIs to abstract this platform (including some specifically for BLE) and an online compiler integrated with these tools:

1. Some platforms require an external [BLE component](http://developer.mbed.org/components/cat/bluetooth/), and [some](http://developer.mbed.org/platforms/mbed-HRM1017/) [have it](http://developer.mbed.org/platforms/RedBearLab-BLE-Nano/) [built-in](http://developer.mbed.org/platforms/Nordic-nRF51-Dongle/).

2. mbed has a BLE-specific API ([BLE_API](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_API/file/1956023d42fb/README.md)), a high level abstraction for using BLE on multiple platforms.
	
3. The mbed BLE tools are written in C++ and can be used from the online [mbed compiler](https://developer.mbed.org/compiler/).

BLE requires an intermediary to be really useful: a website or app on your mobile or tablet. See the next section for options.

![Connecting](/GettingStarted/Images/ConnectDiagram.png "A BLE device requires an app or website running on a phone")

>><span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">A BLE device requires an app or website running on a phone</span>

___


##Fast Prototyping

mbed comes from a heritage of fast prototyping, but implementing BLE brings with it a complication: the need to prototype interactivity. If you’re trying to showcase your project, you want to avoid the compatibility issues you may have with mobile apps and minimise the time you spend on polishing an app that may never be used.

So if you're in the prototyping phase, there are a number of quick ways to get a phone/client app going:

1. Hardware inputs directly to the BLE device, for example a [touchscreen](http://developer.mbed.org/components/cat/touchscreen/).

2. Websites that provide a standard user interface and send commands back to the device. They require programming, but they usually work well on all phones and tablets.

3. [Evothings Studio](http://evothings.com/getting-started-with-evothings-studio-in-90-seconds/) lets you create simple apps that are run from the Evothings App on your phone, so Evothings does the compatibility work for you. It requires some learning of its own, but it may well be worth your time.

Once your prototype is approved, you can invest some more time in your user input. At this point, apps may become worthwhile. But, if you want to be part of the Physical Web, stick to a website - and use the BLE device just to advertise the site's URL.

___

##BLE in Depth

If you want more information about how BLE works, see our [BLE in Depth document](/InDepth/BLEInDepth/). 

___

##Quick Samples

**Tip:** The quick samples are written for experienced BLE developers with an understanding of the mbed IDE; if you want more information about the IDE, see the [tutorials](/GettingStarted/IntroSamples/), which offer extended versions of the same samples. 

The samples cover:

1. A [URI Beacon](#uribeaconsample).
	
2. A [heart rate monitor](#hearratesample).
	
3. [Service creation](/AdvSamples/Overview/): for a read-only characteristic and for a read/write characteristic.

____

<a name="uribeaconsample">
###Quick Sample One: URI Beacon
</a>

**Tip:** If you don’t know how to register your board, or how to work with the mbed compiler, please see the [extended URI Beacon tutorial](/GettingStarted/URIBeacon/). 

To get this sample working, you'll need:

+ To see BLE devices and their advertisement or beacon information, get *one* of the following installed on your phone: 

	-  The physical web app. You can get that app for [iOS](https://itunes.apple.com/us/app/physical-web/id927653608?mt=8) and for 
[Android](https://play.google.com/store/apps/details?id=physical_web.org.physicalweb).

	- For Android, you can get [nRF Master Control Panel](https://play.google.com/store/apps/detailsid=no.nordicsemi.android.mcp&hl=en).

	- For iPhone, you can get [LightBlue](https://itunes.apple.com/gb/app/lightblue-bluetooth-low-energy/id557428110?mt=8).

+ A BLE-enabled mbed board.

+ A user on [developer.mbed.org](developer.mbed.org) to see the compiler.

If you’re familiar with mbed and our compiler, you can get the beacon working in just a few minutes:

1. Open the compiler and select or add your board.

2. Import the [``BLE_URIBeacon``](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_URIBeacon/) program.

3. In ``main.cpp``, find the line ``nrfURIBeaconConfigService uriBeaconConfig(ble, "http://www.mbed.org");`` and edit the URL. Note that it's limited to 18 characters, with “http://www.” (or “http://”, if there’s no “www” ) counting as one, and the suffix “.org” (or “.com”) counting as another.

5. Compile the code. It will be downloaded to your Downloads folder (on some browsers you may need to specify a download location).

6. Drag and drop the compiled file to your board.

7. On the app you installed on your phone, discover your beacon and check that the URL is correct.

____

<a name="hearratesample">
###Quick Sample Two: Heart Rate
</a>

**Tip:** If you don’t know how to register your board, or how to work with the mbed compiler, please see the [extended URI Beacon tutorial](/GettingStarted/URIBeacon/). 

To see the heart rate information on your phone, download PanoBike for [iOS](https://itunes.apple.com/gb/app/panobike/id567403997?mt=8) or [Android](https://play.google.com/store/apps/details?id=com.topeak.panobike&hl=en). Then:

1. Open the compiler and select or add your board.

2. Import the [``heart rate service``](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_HeartRate/).

3. In ``main.cpp``, find the line ``const static char DEVICE_NAME[] = "Nordic_HRM";`` and change the beacon's name from Nordic_HRM. 

4. Compile the code. It will be downloaded to your Downloads folder (on some browsers you may need to specify a download location).

5. Drag and drop the compiled file to your board.

6. On the PanoBike application, watch the heart rate. It should go from 100 to 175 in increments of one, then reset.

____

For service creation, see our [advanced samples](/AdvSamples/Overview/).
