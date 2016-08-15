#Creating Services

With mbed BLE, we offer a growing set of SIG-defined BLE services implemented as C++ headers to ease application development. These can be found under [the API's services folder](https://github.com/mbedmicro/BLE_API/tree/master/services).

But, we don’t expect you to settle for what has already been done; we expect you to develop applications for custom sensors and actuators, often outside the scope of the standard Bluetooth services or the service templates offered by mbed BLE. You can do this using the BLE_API. You may also find that you benefit from modelling your custom services as C++ classes for ease of use (and reuse). 

Creating a BLE service may sound daunting, but we've created two templates that you can easily adapt to your needs:

1. The *input service* template demonstrates the use of a simple input (boolean values) from a read-only characteristic. You can get the code [here](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_Button/) or read the full explanation [here](../AdvSamples/InputButton.md).

2. The *actuator service* template demonstrates the use of a read-write characteristic to control an LED through a phone app. You can get the code [here](https://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_LED/) or read the full explanation [here](../AdvSamples/LEDReadWrite.md).
