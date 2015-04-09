#mbed's BLE_API

<span style="float:right; display:block;">
![](/GettingStarted/Images/API/BLEDiagram.png)
</span>

mbed development relies on APIs to do the grunt work of controlling the platforms, freeing developers to focus on their programs. And because the API also takes responsibility for platform compatibility, developers can reuse their code on any supported platform.

While the mbed OS interfaces with the platform itself, mbed’s BLE_API interfaces with the BLE controller on the platform, and is designed to hide the BLE stack’s complexity behind C++ abstractions. BLE_API is compatible with all BLE-enabled mbed platforms, and together with mbed OS lets developers implicitly benefit from all the low-power optimisations offered by the hardware: the clocks, timers and other hardware peripherals are automatically configured to their lowest power consumption, and all the programmer has to do is remember to yield to  the ``waitForEvent()`` function of the BLE_API anytime the system needs to idle (for more information about ``waitForEvent()``, see our [event-driven programming section](/InDepth/Events/).

##BLE_API, Bridges and Stacks

A BLE application is composed of mbed OS (which currently takes the form of the mbed SDK), BLE_API, and a controller-specific Bluetooth stack together with some bridge software to adapt it to BLE_API:

* BLE_API as described above. The API is developed on [Github](https://github.com/mbedmicro/BLE_API/) and mirrored on [mbed.org](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_API/).

* The bridge software is specific to each vendor’s platform. It provides the instantiations for the interfaces offered by BLE_API, and helps drive the underlying controller and Bluetooth stack.

* The Bluetooth stack implements the Bluetooth protocol, and is specific to the controller, so a vendor using different controllers may provide different stacks.

##Inside BLE_API

<span style="text-align:center; display:block; padding: 10px;">
![](/GettingStarted/Images/API/Inside_API.png)
</span>

BLE_API offers building blocks to help construct applications. These fall into three broad categories: 

1. Interfaces under **'public/'** to express BLE constructs such as GAP, GATT, services and characteristics.

2. Code under **'common/'** encapsulates headers that need to be shared between the public interfaces and underlying bridge code.

3. Classes under **'services/'** to offer reference implementations for many of the commonly used GATT profiles. The code under 'services/' isn't essential, but it’s a useful starting point for prototyping. We continue to implement the standard GATT profiles, so these classes are updated from time to time.

##The BLEDevice Class and Header

The heart of mbed's BLE_API is the`` BLEDevice`` class, accessible in the IDE via the header ``BLEDevice.h``. This class allows us to create a BLE object that includes the basic attributes of a spec-compatible BLE device and can work with any BLE radio:

```c

	#include "BLEDevice.h"

	BLEDevice mydevicename;

```

The class's member functions can be divided by purpose:

1.  Basic BLE operations such as initializing the controller.

2. GAP related methods: radio transmission power levels, advertisements, and parameters affecting connection establishment.

3. GATT related methods: to set up and control the GATT database describing services together with the characteristics and attributes composing them.

4. Event-driven programming controls, such as methods to set up various callbacks to be invoked in response to system events. 

##Sample mbed BLE Apps

We have examples of the [BLE apps, along with documentation](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/).

##Full BLE_API Documentation

The current BLE_API documentation is on the [developer site](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_API/).
