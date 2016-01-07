# Creating mbed OS BLE applications

This chapter explains how to use BLE on mbed OS, our [new operating system](www.mbed.com/en/development/software/mbed-os) for mbed-enabled boards.

The BLE libraries in mbed OS work as they did in mbed Classic: the BLE API abstracts the BLE protocol, so that no matter which manufacturer's stack you're using, the API remains the same and you don't need to rewrite your code. By moving to yotta, however, we have gained the ability to switch between API implementations depending on which [target](http://yottadocs.mbed.com/tutorial/targets.html) we select. 

## Instructions for the impatient

If you want to jump straight in - and already have some background with mbed or BLE - this section allows you to get a BLE example running on an existing supported mbed OS board.

1. Install yotta [by following the docs here](http://yottadocs.mbed.com).
1. Clone the ble-examples repository:
    ```git clone https://github.com/ARMmbed/ble-examples.git```
1. Choose your example (here, we use the heart rate example):
   ```cd ble-examples/BLE_Heartrate/```
1. Choose your target:
    ```yt target bbc-microbit-gcc #or any of the other supported targets; see below```
1. Build the example for the target:
    ```yt build```
1. Copy the built file onto your device:
    ```cp build/bbc-microbit-gcc/source/BLE_Beacon-combined.hex /Volumes/MICROBIT/ #Update the path if you’re not on Mac OS X``` 

Verify that the program is running by scanning for a Heart Rate monitor with a BLE scanning app on your computer or phone (see below for more).

## Migrating from mbed Classic and the original mbed IDE

You have to understand a few basic concepts of programming for mbed OS if you want to make the transition from mbed Classic, because the two are very different. You can then either write new applications, or port your mbed Classic applications to mbed OS.

<span style="background-color:#E6E6E6;  border:1px solid #000;display:block; height:100%; padding:10px">**Note:** To learn more about mbed OS, see [the user guide](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/).</span>

## Moving to asynchronous programming

In mbed Classic, all application callbacks execute in handler mode (interrupt context). mbed OS comes with its own scheduler, [MINAR](https://github.com/ARMmbed/minar), which encourages an asynchronous programming style based on thread-mode callbacks (non-interrupt user context). With mbed OS, application code is made up entirely of callback handlers. We don’t even expose `main()` to users; instead; you should use `app_start()`. Please refer to [MINAR's documentation](https://github.com/ARMmbed/minar#impact) to understand its impact.

<span style="background-color:#E6E6E6;  border:1px solid #000;display:block; height:100%; padding:10px">**Tip:** An expended version of the MINAR documentation is avaialble in the [mbed OS user guide](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/Full_Guide/MINAR/).</span>

## Guidelines for application code

If you're porting an mebd Classic application to mbed OS, please:

* Replace `main()` with `void app_start(int argc, char *argv[])`. app_start() receives control after system initialization, but should finish quickly without blocking (like any other callback handler). If application initialization needs to issue blocking calls, app_start() can pend callbacks for later activity.

* Unlike the former main(), app_start() should *not* finish with an infinite wait loop for system events or for entering sleep. mbed OS expects app_start() to return quickly and yield to the scheduler for callback execution. The application should handle events by posting callbacks, and when there are no pending callbacks the system is automatically put to low-power sleep (the scheduler implicitly calls the equivalent of ``BLE::waitForEvent()``). Please remove any equivalent of the following from your app_start():

	```
	while (true) {
		ble.waitForEvent();
	}
	```

* If you expect objects to persist across callbacks, you need to allocate them either from the global static context or [from the free-store](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/Full_Guide/memory/) (that is, using malloc() or new()). This is similar to the situation in mbed Classic - the key difference is that objects allocated in app_start() do not persist over the lifetime of the programme as they would if created in main().

* Migrate your applications to newer system APIs. For instance, with mbed Classic, applications use the Ticker to post time-deferred callbacks. You should now use MINAR's postCallback APIs directly. Refer to [https://github.com/ARMmbed/minar#using-events](https://github.com/ARMmbed/minar#using-events). The replacement code would look something like:

	```
	minar::Scheduler::postCallback(callback).delay(minar::milliseconds(DELAY));
	```
	
	Or, if we are more explicit:
	
	```
	Event e(FunctionPointer0<void>(callback).bind());
	minar::Scheduler::postCallback(e).delay(minar::milliseconds(DELAY));
	```
  
	Using MINAR to schedule callbacks means that the callback handler executes in thread mode (non-interrupt context), which results in a more stable system.

	Again, you might find it useful to study the documentation covering [MINAR](https://github.com/ARMmbed/minar#minar-scheduler).

### Including BLE functionality in an application

To help reduce the size of applications that use only other connectivity methods, mbed OS doesn't include BLE automatically. In fact, BLE functionality is ‘just another module’ to an mbed OS application. To use BLE in your application, you will therefore need to explicitly include the BLE API in both the application code and the project's [``module.json`` file](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/Full_Guide/app_on_yotta/) (as you'll see below).

#### General BLE functionality 

To include BLE functionality, add the following to your application's ``main.cpp` file:

```c++
#include "ble/BLE.h"
```

If you're using one of the standard Bluetooth services that come with BLE API, include its header as well:

```c++
#include "ble/services/iBeacon.h" 
```

You will also need to add these dependencies to your project's ``module.json`` file:


```json
"dependencies": {
	"ble": "^2.0.0" 
}
```

<span style="background-color:#E6E6E6;  border:1px solid #000;display:block; height:100%; padding:10px">**Tip:** ``ble`` has ``mbed-drivers`` as its own dependency, so there is no need to explicitly list ``mbed-drivers`` in ``module.json``.</span>

The version qualification for the BLE dependency (above) indicates that any implementation of `ble` at major API version 2 would suffice. Ideally, new applications should depend on the latest version of BLE, which can be deduced from the ``module.json`` of the master branch of the ble repository on Github: https://github.com/ARMmbed/ble/blob/master/module.json#L3

For more information about versions in ``module.json``, please see the [mbed OS User Guide](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/Full_Guide/app_on_yotta/).

#### BLE profiles and services

The BLE API offers standard BLE [profiles and services](../Introduction/BLEInDepth.md) through headers in the ``ble`` module. These include GATT and GAP functionality and some of the [BLE services](https://github.com/ARMmbed/ble/tree/master/ble/services). 

Here is the [BLE Heart Rate example](https://github.com/ARMmbed/ble-examples/tree/master/BLE_HeartRate) including the headers it requires:

```
#include "mbed.h"
#include "ble/BLE.h"
#include "ble/Gap.h"
#include "ble/services/HeartRateService.h"
```

## Where next

A good way to understand the difference between mbed OS and mbed Classic BLE applications is to compare their [examples](mbed_OS_examples.md).

You might also want to look at the [mbed OS User Guide](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/).
