# mbed BLE

Welcome. We're here to help you build something awesome with an mbed-enabled BLE platform.

If you're totally new check out our [starters documentation](Introduction/BeginnersIntro.md), which will walk you through everything you need to know. If you have some BLE experience, check out the [short version](Introduction/DevIntro.md) and get your first project up and running. 

## mbed OS 3.0

<span class="notes">**Note:** This version of the documentation covers mbed OS 3.0. If you're working with version 2.0 or 5.0, please [go here](https://docs.mbed.com/docs/ble-intros/en/mbed_OS_2_and_5/).</span>

mbed currently supports two generations of the mbed operating system: mbed Classic and mbed OS. Both generations rely on APIs: mbed Classic has ``BLE_API``, and mbed OS has renamed it, simply, ``ble``.

Despite the name changes, and despite the significant differences between mbed Classic and mbed OS, most of the information presented in this guide is valid for both generations. BLE is still BLE, and the concept of abstracting the hardware through the use of an API has not changed, either. 

However, to prevent confusion, we have divided the guide into sections:

1. [Introduction to BLE](Introduction/Overview.md): Explores BLE as a technology and as a protocol. While this section might occasionally refer to either mbed Classic or mbed OS, it is almost entirely valid for both.

1. [BLE on mbed OS](mbed_OS/Overview.md): Helps the transition from mbed Classic to mbed OS, with a focus on BLE. For a more general introduction to mbed OS, please see our [mbed OS User Guide](https://docs.mbed.com/docs/getting-started-mbed-os/).

1. [BLE on mbed Classic](mbed_Classic/Overview.md): Details sample applications written for mbed Classic. This section includes general BLE information and basic C++ concepts, so you might find it useful even if you are working with mbed OS.

1. [Advanced samples and features](Advanced/Overview.md): Reviews more advanced BLE features. These focus on mbed Classic, but serve as good demonstrations of using the API, so mbed OS users might find them interesting, too.

1. [Additional resources](Additional/Overview.md): Provides links to other sources, answers to frequently asked questions and a list of abbreviations.
 
## BLE documentation 

If you're looking for the API documentation, please see:

 *  [For mbed Classic](http://developer.mbed.org/teams/Bluetooth-Low-Energy/code/BLE_API/).
 *  [For mbed OS](https://docs.mbed.com/docs/ble-api/en/master/api/index.html).

