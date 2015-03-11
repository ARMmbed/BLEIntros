#Tutorial 1: URI Beacon (and an Intro to the mbed Compiler)

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">**Note:** To complete tutorials, you'll need an account on [mbed.org](https://developer.mbed.org/account/signup/?next=%2F).</span>

We're starting with the URI Beacon because it's a quick, simple way to get a BLE device going. URI Beacons advertise a bit of information (usually a URL) to any nearby device.  They're really easy to set up, because the code is fully available on the mbed website, so all you'll need to do is tell the beacon what to broadcast. 

This tutorial covers:

1. The mbed [compiler](#compiler) and [importing code](#import).

2. Understanding [the code](#understanding), including [comments](#comments), [including other files](#include), an introduction to [objects](#objects), [editing the beacon](#edituribeacon) and [compiling and installing your program](#installing).

##What You'll Need

To get this going, you'll need:

+ To see BLE devices and their advertisement or beacon information, get *one* of the following installed on your phone: 

	-  The physical web app. You can get that app for [iOS](https://itunes.apple.com/us/app/physical-web/id927653608?mt=8) and for 
[Android](https://play.google.com/store/apps/details?id=physical_web.org.physicalweb).

	- For Android, you can get [nRF Master Control Panel](https://play.google.com/store/apps/detailsid=no.nordicsemi.android.mcp&hl=en).

	- For iPhone, you can get [LightBlue](https://itunes.apple.com/gb/app/lightblue-bluetooth-low-energy/id557428110?mt=8).

+ A BLE-enabled mbed board, but don't worry if you don't have one yet - we'll show you how it would have worked.

+ A user account on [developer.mbed.org](developer.mbed.org) to see the compiler. We recommend you get access to the compiler even if you don't have a board yet, so that you can play along with the example.

##Quick Guide

If you’re familiar with mbed and our compiler, you can get the beacon working in just a few minutes:

1. Open the compiler and select or add your board.

2. Import the [``BLE_URIBeacon``](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_URIBeacon/) program.

3. In ``main.cpp``, find the line ``uriBeaconConfig = new URIBeaconConfigService(ble, params, "http://uribeacon.org", defaultAdvPowerLevels);`` and edit the URL. Note that it's limited to 18 characters, with “http://www.” (or “http://”, if there’s no “www” ) counting as one, and the suffix “.org” (or “.com”) counting as another.

5. Compile the code. It will be downloaded to your Downloads folder (on some browsers you may need to specify a download location).

6. Drag and drop the compiled file to your board.

7. On the app you installed on your phone, discover your beacon and check that the URL is correct.

<a name=”compiler”>
##Getting Started With the Compiler
</a>

The mbed compiler can take the same program and compile it to match any mbed board that supports BLE. This means you're not constrained in your board selection, but it also means that you need to tell the compiler which board you're working with at any given time.

To select a board for the program: 

1. Log in to mbed [site](https://developer.mbed.org) with your mbed account.

2. Plug your board into your computer's USB port. The board will be displayed in your file browser as a removable storage (similar to plugging in your phone or a USB stick).

![Adding board](/GettingStarted/Images/URIBeacon/DeviceOnMac.png)

3. In your file browser, double-click the board to see its files. By default, every board has an HTML file. 

4. Double click the board's .HTML file to navigate to its page on the mbed site. 

5. On the board's page, click *Add to your mbed Compiler*.

![Adding board](/GettingStarted/Images/URIBeacon/Adding_Platform.png)

6. The compiler will open with your board. You're ready to program. 

![Adding board](/GettingStarted/Images/URIBeacon/IDE_Empty.png)

<a name=”import”>
##Getting a URI Beacon Program
</a>

URI Beacons have a basic structure that's fully available on the mbed website. All you need to do is import it to the compiler and replace the default information with your own. To do that:

1. Go to the [BLE_URIBeacon](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_URIBeacon/) page.

2. On the right-hand side of the page, click *Import this program*.

![Importing program](/GettingStarted/Images/URIBeacon/Import_URIBeacon.png)

3. The compiler will open with an import dialog box. You can give your program a name, or use the default (BLE_URIBeacon).

![Importing dialog](/GettingStarted/Images/URIBeacon/IDE_Import_Dialog.png)

4. Click *Import*. The program will be imported for the board you selected in the previous section. 

![Program imported](/GettingStarted/Images/URIBeacon/IDE_New_URIBeacon.png)

You can now edit the beacon. We'll show you below how to do it, but first we'd like to explain the program a little. You can skip [ahead](#edituribeacon) if you feel like you're not quite ready for C++ yet.

___

<a name=”understanding”>
##Understanding the Code
</a>

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**If you don't want to get too deep into the code - skip [ahead](#edituribeacon).**
</span>

The URI Beacon program is a very small and simple one. The only part of it that you need to look at is the ``main.cpp`` file, which is - as the name suggests - the program's main file. The other files you can ignore for now - they're there to help the compiler do its job.

Click ``main.cpp`` to see its code.

<a name=”comments”>
###Comments
</a>

The first thing you'll see is a bunch of green text, sitting between /* a  * /. This text is comment text, meaning the compiler doesn't read it - it's intended for humans. Any text you see between /* and */ is always comment, and some might help you understand the code.

<a name=”include”>
###Including Other Files
</a>

	#include "mbed.h"
	#include "BLEDevice.h"
	#include "URIBeaconConfigService.h"
	#include "DFUService.h"
	#include "DeviceInformationService.h"
	#include "ConfigParamsPersistence.h"

The next bit of the program is the inclusions list. This tells the compiler which files other than the ``main.cpp`` file it needs to include when it compiles your program. You can see that the ``URI Beacon`` program has six files it includes. These all focus on different capabilities, such as working with the mbed board (``mbed.h``) or the BLE itself (``BLEDevice.h``).

<a name=”objects”>
###Objects
</a>

You may have heard the phrase "object oriented programming". It's a big concept, but it's easy to understand (in a simplified way) using an analogy. If you think of houses as an object type, it's easy to understand that *your* house is an instance, or occurrence, of that type of object. Your house has a blueprint that was used to construct it, and a set of characteristics such as number of rooms and colour of window frames. You can use the same blueprint to create many houses, and they'll all be separate instances of the same object type. 

Once you've created instances you can use each one independently of the others. So you could, for example, create a hundred houses and then re-paint the window frames on just one of them. Manipulating the object or using the object to affect others is done using functions. It's important to understand that if you have the definition of an object, but don't have an instance of the object (in other words, if you only have a blueprint, but haven't actually built the house) you can't get anything done with your house; you cannot hang up pictures before you've built the walls.

In our program, we have an object type called ``BLEDevice``. This is a blueprint that includes instructions for communicating with the ``BLE API`` (remember that the ``BLE API`` is a way of telling the BLE chip what to do without need to know how it does it). The first line of our program builds an instance of the object - builds an actual house - and gives it a name. We do this by first saying what we want to build, and then what to call it. So the line

	BLEDevice ble;

Says "give me an instance of the object type BLEDevice, and call it ble", so now we have an object that knows how to talk to the ``BLE API``.

There's a lot more code in the program, but we'll ignore it for now. You'll learn about it in later samples. Let's just see how to set up the beacon to advertise what we want it to.

___

<a name="edituribeacon">
##Editing the URI Beacon
</a>

URI Beacons are used to send a URL (a website's address). The line of code in our program that does that is:

	uriBeaconConfig = new URIBeaconConfigService(ble, params, !fetchedFromPersistentStorage, "http://uribeacon.org", defaultAdvPowerLevels);

You can very easily spot the interesting bit - it's "http://www.mbed.org". You can replace that URL with a URL of your choosing (but make sure to leave the quotes and the *http://www.* bit).

The URI Beacon isn't limitless in size. It can only accept 18 characters, with “HTTP://www” counting as one, and the suffix “.org” (or “.com”) counting as another. If your URL is very long, you'll have to use services like [bit.ly](https://bitly.com) and [tinyurl.com](http://tinyurl.com) to get a short version.

<a name=”installing”>
##Compiling and Installing Your Program
</a>

For your code to work on a board, it needs to be compiled: the compiler takes all of the files it needs and turns them into a single file, in our case HEX. That file can then be installed on your board. 

To compile and install your program:

1. In the compiler, click *Compile*.

2. The compiled code is automatically sent to your *Downloads* folder as a single file of type HEX (on some browsers you may need to specify a download location).

3. If you've unplugged your board from the USB port, please re-plug it now.

4. Drag and drop the HEX file to the board's entry in the file browser.

5. As part of the installation process, the board is disconnected and reconnected. 

6. Your board is now working as a URI beacon with the URL you gave it. If it has a battery, you can unplug it from the computer and walk around with it.

##Finding Your URI Beacon

Using one of the applications you installed on your phone during our *What You'll Need* section, discover your beacon and check that the URL is correct.

Discovering the beacon:

![Program imported](/GettingStarted/Images/URIBeacon/Discover.png)

Viewing its details:

![Program imported](/GettingStarted/Images/URIBeacon/Details.png)

Congratulations! You've created your first BLE device.

##Recap: the URI Beacon

To get a URI Beacon:

1. You gave your phone the ability to discover BLE devices using a BLE application. 

2. You imported your board to the mbed Compiler, so that the compiler knows which board to prepare your code for.

3. You imported the ``URI Beacon`` program from mbed.org to your compiler.

4. You edited the program to include your own URL. 

5. You compiled and installed the program on your board, so that the board's BLE chip broadcast your beacon.

6. You used your phone to find the beacon broadcast by your board.

7. You had a nice cup of tea to celebrate. 

Along the way, you also learned a little about object oriented programming and the general principle of importing, compiling and installing programs. 

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Tip:** You don't have to send a URL with the beacon. You could send a very simple text (remember that it can't exceed 18 characters, and don't forget to put it in quotes). For example, you could replace the URL with "Open Sundays!", just to let your shoppers know about your new hours.
</span>
_____

