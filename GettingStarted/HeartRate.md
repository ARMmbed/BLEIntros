#Tutorial 2: Heart Rate Monitor (BLE Services)

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Note:** To complete tutorials, you'll need an account on 
[mbed.org](https://developer.mbed.org/account/signup/?next=%2F). 
</span>

The heart rate service gathers the heart rate reading from a monitor and sends it to an app capable of working with the heart rate profile. That means that if you want to work with a heart rate monitor, you don't have to write your own code just to get the input from the device to your phone.

This tutorial covers a lot, and you may need to read it more than once:

1. If you just want to get the heart rate monitor up and running, go to the [quick guide](#quickguide).

2. If you want a deeper understanding of the code, go to [Understanding the Heart Rate Service](#understanding). It covers [objects](#objects), [loops](#loops), [parameters](#parameters), [conditions](#conditions) and [events](#eventdriven).

##What You'll Need

If you don't already know how to import your board and a program into the compiler, please see the [URI Beacon](/GettingStarted/URIBeacon/) sample.

To see the heart rate information on your phone, download PanoBike for [iOS](https://itunes.apple.com/gb/app/panobike/id567403997?mt=8) or [Android](https://play.google.com/store/apps/details?id=com.topeak.panobike&hl=en).

<a name="quickguide">
##Quick Guide
</a>

If you're familiar with mbed and our compiler, you can get the heart rate monitor working in just a few minutes:

1. Open the compiler and select or add your board.

2. Import the [``heart rate service``](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_HeartRate/).

3. In ``main.cpp``, find the line ``const static char DEVICE_NAME[] = "Nordic_HRM";`` and change the beacon's name from Nordic_HRM. 

4. Compile the code. It will be downloaded to your Downloads folder (on some browsers you may need to specify a download location).

5. Drag and drop the compiled file to your board.

6. Restart the board.

6. On the PanoBike application, watch the heart rate. It should go from 100 to 175 in increments of one, then reset.
____

<a name="understanding">
##Understanding the Heart Rate Service
</a>

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**If you don't want to get too deeply into the code - skip [ahead](#renamebeacon).**
</span>

The Heart Rate Service forms part of the Heart Rate Profile (together with the Device Information Service). It connects a heart rate monitor to an app that requires its input, for example a fitness app.

The service has [three characteristics](https://developer.bluetooth.org/TechnologyOverview/Pages/HRS.aspx):

* **Heart Rate Measurement** - sends the heart rate to the app.

* **Body Sensor Location** - describes where on the body to put the sensor.

* **Heart Rate Control Point** - receives a value from the user when the user wants to reset the *Energy Expanded* measurement.

It is important to understand that this demo synthesizes a heart rate value; it does not interact with a physical heart rate sensor to fetch real data. To work with a real heart rate application, we would have had to create a very specific example, which would have been harder to learn from. You should be able to modify the general demo to fit any app that you want to work with if you have a real heart rate sensor. Please check [mbed.org](developer.mbed.org) before you start working - there may already be code available for your heart rate sensor.

##Understanding the Code

The code we generated for this sample may seem long and complex, but when we break it down to components, it becomes clear that the heart rate portion is quite simple.

<a name=”objects”>
###Setting Up the Service (Creating an Instance of the Object)
</a>

We start with setting up the service:

```c

	 // Setup primary service.
	uint8_t hrmCounter = 100;
	HeartRateService hrService(ble, 
		hrmCounter, HeartRateService::LOCATION_FINGER);
```

The first line is only a comment, telling us the general purpose of this section. 

The second line sets up a fake heart rate for the purpose of this sample:

```c

	uint8_t hrmCounter = 100;
```

It's a parameter that we call ``hrmCounter``, and we give it an initial value of 100 (in the context we'll be using it, it means 100 heart beats per minute). Because we're programming in C++, we used ``uint8_t`` to indicate to the compiler that the parameter ``hrmCounter`` is of a type called **unsigned integer**, and its length is 8 bits. We won't get into what that means now, but there's plenty of information on line if you're interested in parameter types.

The third line of code is more interesting, as in it we set up the full service. Let's take a closer look at it:

```c

	HeartRateService hrService(ble, 
		hrmCounter, HeartRateService::LOCATION_FINGER);
```

In our [URI Beacon](/GettingStarted/URIBeacon/) sample we talked about objects and their instances. To get the heart rate measurement we want, we need to create an instance of a type called ``HeartRateService``. This is an object that's defined as part of ``BLE_API``, so you can find its ``.h`` file in your compiler by going to **BLE_HeartRate > BLE_API > services > HeartRateService.h**.

When we create the instance of a type, we first give it a name (in this case ``hrService``), and then provide it with information it requires to be set up correctly:

1. ``ble`` - this is a reference to the fact that we're using a BLE device. 

2. ``hrmCounter`` - the initial value of the counter; we defined this as 100 in the previous line. It could just as easily have been another value, and if we had a sensor it would have been the initial measurement from that sensor.. 

3. ``HeartRateService::LOCATION_FINGER`` - where on the body to attach the sensor. The ``HeartRateService.h`` has a list of locations, and we've selected the finger.

**Tip:** The information an object requires to be initialised correctly is part of the overall definition of the object, and in this case can be found in the ``HeartRateService.h`` file.

<a name=”loops”>
###Using the Service (While and If loops)
</a>

####Objects and Functions

Once we create an instance of a type by giving it a name and its initial parameters, we can start using it. Objects have functions that are defined along with them (they're part of the type's blueprint), and can be accessed from every instance of an object. In this case, the functions are all in the ``HeartRateService.h`` file that we used to create the object.

This is what we do with the ``hrService`` object:

```c

	while (true) {
		if (triggerSensorPolling && ble.getGapState().connected) {
			triggerSensorPolling = false;

			/* Do blocking calls or whatever is necessary for sensor polling. */
			/* In our case, we simply update the dummy HRM measurement. */

			hrmCounter++;
			if (hrmCounter == 175) {
				hrmCounter = 100;
			}

			hrService.updateHeartRate(hrmCounter);
		} else {
			ble.waitForEvent();
		}
```

Let's break that down.

####While

Before saying what the program should do (the function), we tell it when to do it. We've created a WHILE loop that will keep going so long as the condition it's checking returns the value TRUE. For the function to stop running, then, the condition it's checking will have to become false.

The condition we're checking for this loop has two parts:

```c

	if (triggerSensorPolling && ble.getGapState().connected)
```

1. ``triggerSensorPolling``: checks whether we need to read a new value from heart-rate sensor. This condition is set to TRUE periodically (see [below](#eventdriven)). 

2. ``ble.getGapState().connected``: checks whether a GAP connection exists between our peripheral device and a central device. The intention here is to avoid polling for sensor data unless there is a connection that allows a client to fetch values - in the absence of a connection, polling for new sensor data would be futile.
``ble.getGapState()`` by itself returns a collection of status information about the GAP connection, out of which we’re only interested in the boolean status of the connection (where connected is TRUE and disconnected is FALSE). This member is extracted from the collection by the expression ble.getGapState()``.connected``, and the value is then used to evaluate the condition for the if statement.
 
Both parts of the condition - trigger to read a new value and connection status - must be true for the condition as a whole to be considered true. In other words, the loop will not run if it’s not time to read information from the sensor, or if the GAP status is not "connected".

<a name=”parameters”>
####Manipulating Parameters - Increments
</a>

While the loop is running, it updates the heart rate reading it sends our fitness app. Since we're faking a sensor, our code supplies fake values:

```c

	hrmCounter++;
```

C++ has several shorthands it uses for common mathematical actions. When we see ``hrmCounter++``, it means that ``hrmCounter's`` value grows by 1. It's the same as saying ``hrmCounter = hrmCounter + 1``. This is called an *increment operator*.

In our code, every time the loop runs we take the current value of ``hrmCounter`` (it starts at 100, because that's the value we gave it when we set up our service earlier), and add 1. So our app will show 100, 101, 102, 103...

<a name=”conditions”>
####If
</a>

But we don't want the heart rate to grow indefinitely, so we created a condition:

```c

	if (hrmCounter == 175) {
		hrmCounter = 100;
	}
	hrService.updateHeartRate(hrmCounter);
```

This condition is checked every time the loop runs: every time we're done adding 1 to our heart rate, we check its new value. When it reaches 175, we change it to 100 and start counting to 175 again. 

Note that we use two equal signs (==) to check the condition, not one. This is because we're checking if ``hrmCounter`` equals 175, not giving it the value 175. If we were to write ``hrmCounter = 175``, we'd be assigning the value to the parameter. We did that earlier in the code, when we gave the parameter its initial value of 100, and we do it again in the very next line, when we once again assign 100 as its value.

Note also that the IF is nested in the WHILE loop; it doesn't wait for the WHILE loop to finish running, but rather runs as part of it.

####Updating Objects

When we determine what the heart rate is (our incremented value or back to 100), we set that as the value of the heart rate in the service. We called our instance of the service ``hrService`` earlier, so that's what we call it now. As an object of type ``HeartRateService``, it has a function called ``updateHeartRate`` (defined in the ``HeartRateService.h`` file), and that function can accept as an input our ``hrmCounter``. So, let's say the current value of ``hrmCounter`` is 83. We say:

```c

	hrService.updateHeartRate(hrmCounter);
```

Which means, in plain English, "tell the object *hrService* to use its function *updateHeartRate*; that function will update the object's heart rate value to *hrmCounter's* value".

<a name="eventdriven">
####Event-Driven Programming
</a>

mbed programming is event-driven. Unlike normal programming, where logic is expressed in small functions that get executed sequentially, event-driven programming involves writing event handlers that get invoked by the operating system (mbed-OS) in response to system interrupts or other events. In the world of electronics, interrupts come from the hardware: they are generated by changes in electrical signals or system activity (such as radio communication). Interrupts often lead to the execution of event handlers by the OS; event-driven programming means writing code to execute in response to interrupts. 

Code in embedded applications is executed in two contexts:

1. A main loop - ``main()`` - that forms the background activity of an application, and sends the application into a deep sleep whenever no action is required.

2. One or more event handlers, which respond to asynchronous system activities (activities whose timing is not predetermined). In the context of BLE, event handlers may be triggered quite regularly, for example if a sensor sends a measurement every x seconds, or they may be triggered intermittently.

Event handlers are often preemptive, meaning they can interrupt the main program’s execution to force their own execution; the main program will resume when the interrupting event is fully handled. In the case of BLE, we expect the main program to be a sleep loop (``waitForEvent``), which means that the device will sleep unless it receives an interrupt - which is why BLE is a low energy technology.

<span style="text-align:center; display:block;">
![events](/GettingStarted/Images/EventHandle.png "An event interrupts the main loop and triggers an event handler. The interrupt is handled, and the event handler then returns control to main()")
</span>

<span style="background-color:lightblue; color:gray; display:block; height:100%; padding:10px;">An event interrupts the main loop and triggers an event handler. The interrupt is handled, and the event handler then returns control to main()</span>


The relationship between ``main()`` and event handlers - and especially the decision which code to move to an event handler and which to leave in ``main()`` - is all about timing. Handler execution time is often determined not by the size of the code but by how many times it must run - for example, how many iterations of a data-processing loop it performs - or by communication with external components such as sensors (also called polling). Communication delays can range from a few microseconds to milliseconds, depending on the sensor involved. Reading an accelerometer can take around a millisecond, and a temperature sensor can take up to a few hundred microseconds. A barometer, on the other hand, can take up to 10 milliseconds to yield a new sensor value. 

If an event, such as a sensor reading, arrives when the program is in ``main()`` (in our case, then, when the device is sleeping), it can be executed. But if it arrives when another event is being executed, it may have to wait for the first event to be handled in full. In this scenario, the first event is blocking the execution of the second event. Because event handlers can block each other, they are supposed to execute quickly and return control to ``main()``, to allow the system to remain responsive. In the world of microcontrollers, anything longer than a few dozen microseconds is too long and a millisecond is an eternity. Long-running activities - anything longer than 100 microseconds, such as data processing and sensor communication - should be left in ``main()`` rather than an event handler. This is because ``main()`` can then be interrupted by event handlers, so that the long-running process doesn’t affect the system’s responsiveness. 

In these cases, the event handler is used not to perform functions but rather to enqueue work for the main loop. In the heart rate demo, the work of polling for heart rate data is communicated to the main loop through the variable ``triggerSensorPolling``, which gets set periodically from an event handler called ``periodicCallback()``.

####Waiting for Events

The last bit of the WHILE loop is the ELSE section. ELSE tells the program what to do if the condition of the WHILE loop isn't met. Remember that our condition was to have a sensor that's providing information and an active GAP connection. If the program sees that we don't have one or the other of these, it will enter the ELSE clause. 

```c

	ble.waitForEvent();
```

When we created our object we said that it's a BLE device, and that gave it the ability to use the function ``waitForEvent`` that belongs to the ``BLE. waitForEvent`` lets the device sleep until something is needed of it, to reduce battery usage. When an event occurs, for example when the heart rate monitor starts sending values (which is a condition of the WHILE loop), the device will wake up and update the value in the service. 

##Recap: the Heart Rate Service

To summarise, this is how we used the Heart Rate service:

1. ``BLE_API`` gives us a .h file called ``HeartRateService``, which holds all the code we need to correctly set up a service object.

2. In our ``main.cpp`` file, we created an object of type ``HeartRateService``, and called it ``hrService``.

3. To correctly initialise the object, we gave it three parameters, one of which is an initial heart rate value. We called the parameter holding that value ``hrmCounter`` and gave it the value 100.

4. We decided that the object will be used periodically, rather than constantly. So we set a condition that it should only be used when it is time to poll the physical sensor for new information, but only if there is a GAP connection between the BLE device and a client.

5. Then we created a heart rate value to give the object. In a normal service, this value will be provided by the heart rate sensor. Because we're not using a sensor, we created a fake value that is a one-step increment from the previous value. We reset the value to 100 every time it reaches 175.

6. When we have our value, we update the service by using the object's built-in update function: ``hrService.updateHeartRate(hrmCounter)``.

7. Lastly, we said that if we can't meet the conditions set up in step #4, we'll let the device sleep until it receives an event, at which point it will check the condition again. 

___

<a name="renamebeacon">
##Renaming Your Beacon
</a>

Your device's name is part of the advertisement information, and you can (and should) change it from a standard name to something you'll easily recognise. 

To rename your beacon, find the following line of code in the ``main.cpp`` file:

```c

	const static char     DEVICE_NAME[]        = "Nordic_HRM";
```

The default name is "Nordic_HRM". You can change it to anything you like (but stay under 18 characters). Don't forget to leave it in quotes. 

```c

	const static char     DEVICE_NAME[]        = "I_Renamed_This";
```

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
**Tip**: iOS "sticks" to the name it first discovers for each beacon, so whatever name you choose now you'll have for a while. This is called *caching*, and is intended to save your phone some time and energy.
</span>
____

##Viewing the Service Details

Panobike and other fitness apps show you the heart rate, but you can use [nRF Master Control Panel](http://www.nordicsemi.com/eng/Products/nRFready-Demo-APPS/nRF-Master-Control-Panel-for-Android-4.3), [LightBlue](https://itunes.apple.com/gb/app/lightblue-bluetooth-low-energy/id557428110?mt=8) and similar products to see more details.

Here is our app, discovered on nRF:

<span style="text-align:center; display:block;">
![Discover](/GettingStarted/Images/HeartRate/Discover.png)
</soan>

By clicking the HRM entry, we can see some more information about it:

<span style="text-align:center; display:block;">
![Information](/GettingStarted/Images/HeartRate/Connect.png)
</span>

We can click **Connect** to see the full details:

<span style="text-align:center; display:block;">
![Full info](/GettingStarted/Images/HeartRate/StartNoti.png)
</span>

If we click the **notifications** button, we'll be asking the service to notify our device of updates. In our case, that will be heart rate values:

<span style="text-align:center; display:block;">
![Heart rate](/GettingStarted/Images/HeartRate/ShowRate1.png)
</span>

The server will notify our phone with each new value:

<span style="text-align:center; display:block;">
![Updated heart rate](/GettingStarted/Images/HeartRate/ShowRate2.png)
</span>



