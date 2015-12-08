#Advanced Samples Overview

Our advanced samples are designed to help you get serious projects into the prototyping stage.

##Service Templates

With mbed BLE, we offer a growing set of SIG-defined BLE services implemented as C++ headers to ease application development. These can be found under [the API's services folder](https://github.com/mbedmicro/BLE_API/tree/master/services).

But, we don’t expect you to settle for what’s already been done; we expect you to develop applications for custom sensors and actuators,. These will often fall outside the scope of the standard Bluetooth services or the service templates offered by mbed BLE. In this case, you could use the ``BLE_API``. You may also find that you benefit from modelling your custom services as C++ classes for ease of use (and reuse). Here, we'd like to capture the process of creating a BLE service.

Creating a BLE service may sound scary, but we've created two templates that you can easily adapt to your needs:

* The *input service* template demonstrates the use of a simple input (boolean values) from a read-only characteristic. You can get the code [here](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_Button/) or read the full explanation [here](../Advanced/InputButton.md).

* The *actuator service* template demonstrates the use of a read-write characteristic to control an LED through a phone app. You can get the code [here](https://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_LED/) or read the full explanation [here](../Advanced/LEDReadWrite.md).

* We have two more service samples that include the use of Evothings custom apps. The first reviews [customising a GAP advertising packet](../Advanced/CustomGAP.md), and the second creates a [GATT service for control of a LED](../Advanced/GATTEvo.md).

##Advanced Features

Reviewing advanced features of standard implementations:

* The [URI Beacon](../Advanced/URIBeaconAdv.md): dynamic configuration of the URIBeacon on start up and configuration persistence. 

* Creating an app for [high data rate, low latency transfers](../Advanced/HighData.md), if you need to transfer large amounts of data.

______
Copyright © 2015 ARM Ltd. All rights reserved.