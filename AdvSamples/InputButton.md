#Creating an Input Service

With mbed BLE, we offer a growing set of SIG-defined BLE services implemented as C++ headers to ease application development. These can be found under [our services respository](https://github.com/mbedmicro/BLE_API/tree/master/services).

If, for instance, you needed to develop a heart-rate application for an mbed platform, you could get started with the [BLE heart rate demo](/GettingStarted/HeartRate/). This demo instantiates the [heart rate service](https://github.com/mbedmicro/BLE_API/blob/master/services/HeartRateService.h), which takes care of the majority of the BLE plumbing and offers high-level APIs to work with service configuration and sensor values. You'd need to add custom code to your application to poll sensor data periodically (from some safe, non-interrupt context if polling takes a while), and the HeartRateService takes care of the rest..

But, we don’t expect you to settle for what’s already been done; we expect you to develop applications for custom sensors and actuators, often outside the scope of the standard Bluetooth services or the service templates offered by mbed BLE. In this case, you could use the ``BLE_API``. You may also find that you benefit from modeling your custom services as C++ classes for ease of use (and reuse). Here, we'd like to capture the process of creating a BLE service.

#Button Service

Let's work our way towards creating a service for a trivial sensor: a button. We'll assume a use-case where a phone-app would like to connect to this mbed application and poll for button state; notifications could also be set up for asynchronous updates. In the non-connected state, the application simply advertises its capability of providing the button service.

<span style="background-color:lightgray; color:purple; display:block; height:100%; padding:10px">
Get the code [here](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_Button/).
</span>

##The Basic Template - Advertising and Connecting

Here's a basic template code to get you off the ground. We've thrown in a blinking LED to indicate program stability. This code doesn't create any custom service; it advertises Button as the device name through the advertisement payload. The application is discoverable (``LE_GENERAL_DISCOVERABLE``) and connectable (``ADV_CONNECTABLE_UNDIRECTED``), and offers only the standard GAP and GATT services. The function ``disconnectionCallback`` re-starts advertisements if connection is lost.


	#include "mbed.h"
	#include "BLEDevice.h"
	
	BLEDevice   ble;        /* Instantiation of a BLEDevice in 
							* global scope allows us to refer to
							* it anywhere in the program. */
	DigitalOut led1(LED1);
	
	const static char DEVICE_NAME[] = "Button"; 	/* setting up a device name helps with identifying
													* your device; this is often very useful when
													* there are several other BLE devices in the
													* neighborhood. */

	void disconnectionCallback(Gap::Handle_t handle, Gap::DisconnectionReason_t reason)
	{
		ble.startAdvertising();  /* One needs to explicitly re-enable
								* advertisements after a connection
								* teardown. */
	}

	void periodicCallback(void)
	{
		led1 = !led1; /* Do blinky on LED1 to indicate system aliveness. */
	}
	
	int main(void)
	{
		led1 = 1;                        		/* aliveness LED starts out with being off; doesn't really */
												/* matter too much because we only toggle it. */
		Ticker ticker;                   		/* A mechanism for periodic callbacks. */
		ticker.attach(periodicCallback, 1); 	/* Setting up a callback to go at an interval of 1s. */

		ble.init();                      		/*  initialize the BLE stack and controller. */
		ble.onDisconnection(disconnectionCallback);

		/* setup advertising */

		/* BREDR_NOT_SUPPORTED means classic bluetooth not supported;
 		* LE_GENERAL_DISCOVERABLE means that this peripheral can be
 		* discovered by any BLE scanner--i.e. any phone. */
		ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);

		/* This is where we're collecting the device name into the advertisement payload. */
		ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));

		/* We'd like for this BLE peripheral to be connectable. */
		ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);

		/* set the interval at which advertisements are sent out; this has
 		* an implication power consumption--radio activity being a
 		* biggest draw on average power. The other software controllable
 		* parameter which influences power is the TX power of the radio
 		* level--there is an API to adjust that. */
		
		ble.setAdvertisingInterval(Gap::MSEC_TO_ADVERTISEMENT_DURATION_UNITS(1000)); /* 1000ms. */

		/* we are finally good to go with advertisements. */
		ble.startAdvertising();
	
		while (true) {
		ble.waitForEvent();
		}
	}


This is what the app looks like (on the nRF Master Control Panel):

<span style="text-align:center; display:block;">
![App discovery](/AdvSamples/Images/Button/ButtonDiscovery.png)
</span>

##Assigning UUIDs

Now, let's get down to the business of creating a BLE service for a button. This service will have a single read-only characteristic holding a boolean value for the button’s state.

Bluetooth Smart requires the use of UUIDs to identify types for all involved entities. We'll need two UUIDs - one each - for the button service and the encapsulated characteristic. If we had been creating one of the standard SIG-defined services, we'd have followed the standard [UUID definitions](https://developer.bluetooth.org/gatt/services/Pages/ServicesHome.aspx).

We've chosen a custom UUID space for our button service: 0xA000 for the service, and 0xA001 for the contained characteristic. This avoids collision with the standard UUIDs.



	#define BUTTON_SERVICE_UUID              0xA000
	#define BUTTON_STATE_CHARACTERISTIC_UUID 0xA001
	 
	...
	 
	static const uint16_t uuid16_list[] = {BUTTON_SERVICE_UUID};
	 
	...
 	
	ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t *)uuid16_list, sizeof(uuid16_list));


Adding the button service UUID to the advertising payload is purely optional. Having it is good practice, however, since it gives an early and cheap indication to interested client apps regarding the capabilities of the mbed application. 

**Note:** interpreting non-standard service UUIDs has limited use, and may only work with custom phone apps.

##The Button State Characteristic

``BLE_API`` offers C++ abstractions for entities involved in the definition of services. A ``GattService`` class is composed of one or more ``GattCharacteristics`` (representing state variables exposed by the service). Every ``GattCharacteristic``, in turn, implicitly contains at least a ``GattAttribute`` to hold the value; it may be embellished with further ``GattAttributes`` if needed, but that is uncommon.

The application, therefore, needs to set up one or more ``GattCharacteristics`` and compose them into a ``GattService``. There could be more than one services.

In C++, class objects are instantiated when variables are defined in some scope, or when they’re allocated dynamically using ``new()``. We usually avoid dynamic allocation, but in all cases one needs to take care of scope and aliveness of variables.

The button state characteristic can be defined wherever memory allocations remain persistent throughout the application’s lifetime, for example the ``main()`` function. 

The code only looks complicated; it is essentially a simple use of C++ templates to instantiate a read-only characteristic encapsulating a boolean state. The constructor for ``buttonState`` takes in the UUID and a pointer to the initial value of the characteristic:



	bool buttonPressed = false; //button initial state
	ReadOnlyGattCharacteristic<bool> buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressed);//read-only characteristic of type boolean, accepting the buttonState’s UUID and initial value


**Tip:** there are several variants of ``GattCharacterisitc`` available to ease instantiation. Refer to template declarations at the bottom of [``GattCharacteristic.h``](https://github.com/mbedmicro/BLE_API/blob/master/public/GattCharacteristic.h).

##Adding Notifications

The above definition for the buttonState characteristic may be enhanced to allow notifications, using the optional parameters to specify additional properties.


	
	    ReadOnlyGattCharacteristic<bool> buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressed, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY);



Notifications are a good way to establish asynchronous updates, so that the app doesn’t have to keep checking the BLE device; the device will let the app know if there’s anything new. This helps the BLE device keep its energy usage down.

##Constructing the Button Service

The ``buttonState`` characteristic can be used to construct a ``GattService`` called ``buttonService``. We use a bit of C/C++ syntax to create a one-element array, using an initializer list of pointers to ``GattCharacteristics``. 

This service can then be added to the BLE stack using ``BLEDevice::addService()``.


	GattCharacteristic *charTable[] = {&buttonState};//the service’s characteristic will be the button’s state
	GattService         buttonService(BUTTON_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));//the service is given the UUID we set for it earlier, as well as the charTable we just built from the buttonState variable
	ble.addService(buttonService);//the BLE object’s addService function now builds the buttonService


##Putting it Together

So, now we have the following code which defines a custom button service containing a read-only characteristic:

	#include "mbed.h"
	#include "BLEDevice.h"
	
	BLEDevice  ble;
	DigitalOut led1(LED1);

	#define BUTTON_SERVICE_UUID              0xA000
	#define BUTTON_STATE_CHARACTERISTIC_UUID 0xA001

	const static char     DEVICE_NAME[] = "Button";
	static const uint16_t uuid16_list[] = {BUTTON_SERVICE_UUID}; 
	
	void disconnectionCallback(Gap::Handle_t handle, Gap::DisconnectionReason_t reason)
	{
		ble.startAdvertising();
	} 

	void periodicCallback(void)
	{
		led1 = !led1; /* Do blinky on LED1 to indicate system aliveness. */
	}
	int main(void)
	{
		led1 = 1;
		Ticker ticker;
		ticker.attach(periodicCallback, 1);

		ble.init();
		ble.onDisconnection(disconnectionCallback);

		/*
		* The part which sets up the characteristic and service. Objects
		* are instantiated within the scope of main(), but then this
		* isn't a problem since main() remains alive as long as the
		* application runs.
		*/

		bool buttonPressed = false;
		ReadOnlyGattCharacteristic<bool> buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressed, 		GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY);

		GattCharacteristic *charTable[] = {&buttonState};
		GattService         buttonService(BUTTON_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));
		ble.addService(buttonService);

		/* setup advertising */
		ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
		ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t *)uuid16_list, sizeof(uuid16_list));
		ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));
		ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
		ble.setAdvertisingInterval(Gap::MSEC_TO_ADVERTISEMENT_DURATION_UNITS(1000)); /* 1000ms. */
		ble.startAdvertising();

		while (true) {
			ble.waitForEvent();
		}
	}


When you connect to the service, you can see the characteristic and enable notifications (note that you must manually enable them - the service doesn't force notifications on the client):

<span style="text-align:center; display:block;">
![App notifications](/AdvSamples/Images/Button/Notifications.png)
</span>

##Updating the Button’s State

So far, the buttonState characteristic within the service has been static. We can now add some code to update the characteristic when the button is pressed or released, using the ``BLEDevice::updateCharacteristicValue() API``.

The following code sets up callbacks for when button1 is pressed or released:

	InterruptIn button(BUTTON1);//mbed class for receiving interrupts
	...
	void buttonPressedCallback(void)//reaction to falling edge
	{
		buttonPressed = true;
		ble.updateCharacteristicValue(buttonState.getValueHandle(), (uint8_t *)&buttonPressed, sizeof(bool));//gives the buttonState characteristic the value TRUE
	}

	void buttonReleasedCallback(void)//reaction to rising edge
	{
		buttonPressed = false;
		ble.updateCharacteristicValue(buttonState.getValueHandle(), (uint8_t *)&buttonPressed, sizeof(bool));//gives the buttonState characteristic the value FALSE
	}
	...
	int main(void)
	{
	...
		button.fall(buttonPressedCallback);//falling edge
		button.rise(buttonReleasedCallback);//rising edge

Note that ``updateCharacteristicValue()`` identifies the ``buttonState`` characteristic using a value handle. The ``buttonState`` characteristic needs to be moved into a global context in order for the button callbacks to access it. Here's the full code:

	#include "mbed.h"
	#include "BLEDevice.h"

	BLEDevice   ble;
	DigitalOut  led1(LED1);
	InterruptIn button(BUTTON1);

	#define BUTTON_SERVICE_UUID              0xA000
	#define BUTTON_STATE_CHARACTERISTIC_UUID 0xA001

	const static char     DEVICE_NAME[] = "Button";
	static const uint16_t uuid16_list[] = {BUTTON_SERVICE_UUID};
	
	bool buttonPressed = false;
	ReadOnlyGattCharacteristic<bool> buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressed,
	GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY);//buttonState is accessible to button callbacks

	void buttonPressedCallback(void)
	{
		buttonPressed = true;
		ble.updateCharacteristicValue(buttonState.getValueHandle(), (uint8_t *)&buttonPressed, sizeof(bool));
	}
	
	void buttonReleasedCallback(void)
	{
		buttonPressed = false;
		ble.updateCharacteristicValue(buttonState.getValueHandle(), (uint8_t *)&buttonPressed, sizeof(bool));
	}

	void disconnectionCallback(Gap::Handle_t handle, Gap::DisconnectionReason_t reason)
	{
		ble.startAdvertising();
	}

	void periodicCallback(void)
	{
		led1 = !led1; /* Do blinky on LED1 to indicate system aliveness. */
	}

	int main(void)
	{
		led1 = 1;
		Ticker ticker;
		ticker.attach(periodicCallback, 1);
		button.fall(buttonPressedCallback);
		button.rise(buttonReleasedCallback);

		ble.init();
		ble.onDisconnection(disconnectionCallback);

		GattCharacteristic *charTable[] = {&buttonState};
		GattService         buttonService(BUTTON_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));
		ble.addService(buttonService);

		/* setup advertising */
		ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
		ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t *)uuid16_list, sizeof(uuid16_list));
		ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));
		ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
		ble.setAdvertisingInterval(Gap::MSEC_TO_ADVERTISEMENT_DURATION_UNITS(1000)); /* 1000ms. */
		ble.startAdvertising();

		while (true) {
			ble.waitForEvent();
		}
	}

With notifications active, you can see the button characteristic's value change when you press the button on the board:

<span style="text-align:center; display:block;">
![Side by side - zero and one](/AdvSamples/Images/Button/SideBySide.png)
</span>

##The ButtonService Class

The above application is fully functional, but has grown to be a bit messy. In particular, all the plumbing creating the button service could be encapsulated within a ``ButtonService`` class. In other words, it should be possible to substitute most of the above code with a simple initialization of a ``ButtonService`` class, while retaining the functionality.

Here's something to get you started with the ``ButtonService`` class:

	#ifndef __BLE_BUTTON_SERVICE_H__
	#define __BLE_BUTTON_SERVICE_H__

	class ButtonService {
	public:
		const static uint16_t BUTTON_SERVICE_UUID              = 0xA000;
		const static uint16_t BUTTON_STATE_CHARACTERISTIC_UUID = 0xA000;

	private:
		/* private members to come */
	};

	#endif /* #ifndef __BLE_BUTTON_SERVICE_H__ */

Nearly all ``BLE APIs`` require a reference to ``BLEDevice``, so we must require this in the constructor. The ``buttonState`` characteristic should be encapsulated as well:

	#ifndef __BLE_BUTTON_SERVICE_H__
	#define __BLE_BUTTON_SERVICE_H__

	class ButtonService {
	public:
		const static uint16_t BUTTON_SERVICE_UUID              = 0xA000;
		const static uint16_t BUTTON_STATE_CHARACTERISTIC_UUID = 0xA000;

	/* The constructor. This gets called automatically when we
	* instantiate an LEDService object. It uses an initializer list
	* to initialize the member variables. */

		ButtonService(BLEDevice &_ble, bool buttonPressedInitial) :
			ble(_ble), buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressedInitial, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY)
		{
			/* empty */
		}
	
	private:
		BLEDevice                        &ble;
		ReadOnlyGattCharacteristic<bool>  buttonState;
	};
	
	#endif /* #ifndef __BLE_BUTTON_SERVICE_H__ */

We can move more of the service’s setup into the constructor:

	#ifndef __BLE_BUTTON_SERVICE_H__
	#define __BLE_BUTTON_SERVICE_H__
	
	class ButtonService {
	public:
		const static uint16_t BUTTON_SERVICE_UUID              = 0xA000;
		const static uint16_t BUTTON_STATE_CHARACTERISTIC_UUID = 0xA001;

	ButtonService(BLEDevice &_ble, bool buttonPressedInitial) :
	ble(_ble), buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressedInitial, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY)
	{
		GattCharacteristic *charTable[] = {&buttonState};
		GattService         buttonService(ButtonService::BUTTON_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));
		ble.addService(buttonService);
	}

	private:
		BLEDevice                        &ble;
		ReadOnlyGattCharacteristic<bool>  buttonState;
	};

	#endif /* #ifndef __BLE_BUTTON_SERVICE_H__ */

And here's a small extension with a helper API that updates the button’s state:

	#ifndef __BLE_BUTTON_SERVICE_H__
	#define __BLE_BUTTON_SERVICE_H__

	class ButtonService {
	public:
		const static uint16_t BUTTON_SERVICE_UUID              = 0xA000;
		const static uint16_t BUTTON_STATE_CHARACTERISTIC_UUID = 0xA000;
		ButtonService(BLEDevice &_ble, bool buttonPressedInitial) :
		ble(_ble), buttonState(BUTTON_STATE_CHARACTERISTIC_UUID, &buttonPressedInitial, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY)
	{
		GattCharacteristic *charTable[] = {&buttonState};
		GattService         buttonService(ButtonService::BUTTON_SERVICE_UUID, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));
		ble.addService(buttonService);
	}
	
	void updateButtonState(bool newState) {
		ble.updateCharacteristicValue(buttonState.getValueHandle(), (uint8_t *)&newState, sizeof(bool));
	}
	private:
		BLEDevice                        &ble;
		ReadOnlyGattCharacteristic<bool>  buttonState;
	};
	
	#endif /* #ifndef __BLE_BUTTON_SERVICE_H__ */

And now with this encapsulated away in the ``ButtonService``, the main application is more readable:

	#include "mbed.h"
	#include "BLEDevice.h"
	#include "ButtonService.h"
	
	BLEDevice   ble;
	DigitalOut  led1(LED1);
	InterruptIn button(BUTTON1);
	
	const static char     DEVICE_NAME[] = "Button";
	static const uint16_t uuid16_list[] = {ButtonService::BUTTON_SERVICE_UUID};

	ButtonService *buttonServicePtr;

	void buttonPressedCallback(void)
	{
		buttonServicePtr->updateButtonState(true);
	}
	
	void buttonReleasedCallback(void)
	{
		buttonServicePtr->updateButtonState(false);
	}

	void disconnectionCallback(Gap::Handle_t handle, Gap::DisconnectionReason_t reason)
	{
		ble.startAdvertising();
	}

	void periodicCallback(void)
	{

	led1 = !led1; /* Do blinky on LED1 to indicate system aliveness. */
	}

	int main(void)
	{
		led1 = 1;
		Ticker ticker;
		ticker.attach(periodicCallback, 1);
		button.fall(buttonPressedCallback);
		button.rise(buttonReleasedCallback);

		ble.init();
		ble.onDisconnection(disconnectionCallback);

		ButtonService buttonService(ble, false /* initial value for button pressed */);
		buttonServicePtr = &buttonService;

		/* setup advertising */
		ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
		ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t *)uuid16_list, sizeof(uuid16_list));
		ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));
		ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
		ble.setAdvertisingInterval(Gap::MSEC_TO_ADVERTISEMENT_DURATION_UNITS(1000)); /* 1000ms. */
		ble.startAdvertising();

		while (true) {
			ble.waitForEvent();
		}
	}

One final note: notice that we've  set up a ``buttonServicePTR``. This was necessary because ``onDataWritten`` callback needs to refer to the ``buttonService`` object. One reasonable way to achieve this would have been to move the definition of the ``buttonService`` object in the global scope, but constructing a ``buttonService`` object requires the use of ``BLE_API`` calls such as ``ble.addService()``, which can only be safely used after a call to ``ble.init()``. Unfortunately, ``ble.init()`` is called only within ``main()``, delaying the instantiation of ``buttonService``. This leads us to making a reference available to the ``buttonService`` object through a pointer. This is a bit roundabout.