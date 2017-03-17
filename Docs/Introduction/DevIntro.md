# mbed BLE for developers

This document is written for experienced BLE developers who are switching to mbed platforms. If you feel that you need more information than this document provides, please refer to our [extended documentation](../Introduction/BeginnersIntro.md).

## BLE on mbed

[mbed](https://www.mbed.com/) gives you three things: a well defined hardware platform, APIs to abstract this platform (including some specifically for BLE) and an online compiler integrated with these tools:

1. Some platforms require an external [BLE component](http://developer.mbed.org/components/cat/bluetooth/), and [some](http://developer.mbed.org/platforms/mbed-HRM1017/) [have it](http://developer.mbed.org/platforms/RedBearLab-BLE-Nano/) [built-in](http://developer.mbed.org/platforms/Nordic-nRF51-Dongle/).

1. mbed has a BLE-specific API, a high level abstraction for using BLE on multiple platforms. You can [see the Doxygen here](https://docs.mbed.com/docs/mbed-os-api/en/mbed-os-5.4/api/classBLE.html).
	
1. The mbed BLE tools are written in C++ and can be used from the online [mbed compiler](https://developer.mbed.org/compiler/) or offline, for example with [GCC](http://developer.mbed.org/forum/team-63-Bluetooth-Low-Energy-community/topic/5257/).

BLE is most useful when used with a website or app on your mobile or tablet. See the next section for options.

<span class="images">![Connecting](../Introduction/Images/ConnectDiagram.png)<span>A BLE device currently requires an app or website running on a phone
</span></span>

## Rapid prototyping

mbed comes from a heritage of rapid prototyping and allows you to test code and ideas on BLE devices very easily. 

<span class="tips">For information about rapid prototyping with mbed BLE, see [here](../Introduction/Prototyping.md).</span>

## BLE in depth

If you want more information about how BLE works, see our [BLE in Depth document](../Introduction/BLEInDepth.md). 

## Quick samples

<span class="tips">**Tip:** The quick samples are written for experienced BLE developers with an understanding of the mbed IDE. If you want more information about the IDE, see the [tutorials](../mbed_Classic/Overview.md), which offer extended versions of the same samples. </span>

The samples cover:
	
1. A [heart rate monitor](#hearratesample).
	
1. [Service creation](../Advanced/Overview.md): for a read-only characteristic and for a read/write characteristic.

<a name="hearratesample">
### Quick sample: heart rate
</a>

<span class="tips">**Tip:** If you don’t know how to register your board, or how to work with the mbed compiler, please see the [mbed OS handbook](https://docs.mbed.com/docs/mbed-os-handbook/en/latest/getting_started/blinky_compiler/).</span>

To see the heart rate information on your phone, download PanoBike for [iOS](https://itunes.apple.com/gb/app/panobike/id567403997?mt=8) or [Android](https://play.google.com/store/apps/details?id=com.topeak.panobike&hl=en). Then:

1. Open the compiler and select or add your board as the target platform.

2. Import the [``heart rate service``](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_HeartRate/).

3. In ``main.cpp``, find the line ``const static char DEVICE_NAME[] = "HRM1";`` and change the beacon's name from HRM1. 

4. Compile the code. It will be downloaded to your Downloads folder (on some browsers you may need to specify a download location).

5. Drag and drop the compiled file to your board.

6. Restart the board.

6. On the PanoBike application, watch the heart rate. It should go from 100 to 175 in increments of one, then reset.

### Quick sample: service creation

For service creation, see our [advanced samples](../Advanced/Overview.md).
